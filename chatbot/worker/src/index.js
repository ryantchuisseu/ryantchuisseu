// Worker Cloudflare du chatbot JCIA 2027 (couche 2 : IA).
// Routes :
//   GET  /faq    -> la FAQ officielle (utilisée par le widget pour les boutons, sans IA)
//   POST /chat   -> question libre, réponse de Claude Haiku basée sur la FAQ
//   GET  /health -> vérification simple
import Anthropic from "@anthropic-ai/sdk";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";
import { z } from "zod";
import faq from "../../knowledge/faq.json";
import { SYSTEM_PROMPT } from "./prompt.js";

const MODEL = "claude-haiku-5-5";
const MAX_HISTORY = 8;        // messages gardés dans l'historique envoyé à l'IA
const MAX_CHARS = 600;        // longueur maximale d'un message visiteur
const WINDOW_MS = 10 * 60 * 1000;

const Reply = z.object({
  answer: z.string(),
  status: z.enum(["answered", "unknown", "off_topic", "guardrail", "unclear", "thanks"]),
});

const FALLBACK = {
  fr: "Je n’ai pas pu répondre pour le moment. Le secrétariat peut vous aider : contact@jciacm.com ou WhatsApp +237 699 089 937.",
  en: "I couldn’t answer right now. The secretariat can help: contact@jciacm.com or WhatsApp +237 699 089 937.",
};
const LIMITED = {
  fr: "Vous avez posé beaucoup de questions en peu de temps. Réessayez dans quelques minutes, ou écrivez à contact@jciacm.com.",
  en: "You have asked many questions in a short time. Please try again in a few minutes, or write to contact@jciacm.com.",
};

// Limiteur simple par visiteur (mémoire de l'instance du Worker).
// Pour une protection forte, ajouter aussi une règle « Rate limiting » dans le tableau de bord Cloudflare.
const hits = new Map();
function allowed(ip, limit) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  if (list.length >= limit) { hits.set(ip, list); return false; }
  list.push(now); hits.set(ip, list);
  if (hits.size > 5000) hits.clear();
  return true;
}

function corsHeaders(request, env) {
  const origin = request.headers.get("Origin") || "";
  const allowedOrigins = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  const ok = allowedOrigins.includes(origin);
  return {
    ok,
    headers: {
      ...(ok ? { "Access-Control-Allow-Origin": origin } : {}),
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Max-Age": "86400",
      Vary: "Origin",
    },
  };
}

function json(data, status, headers) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...headers },
  });
}

// Nettoie l'historique reçu du navigateur : rôles valides, textes courts,
// commence par un message visiteur et se termine par un message visiteur.
function cleanMessages(raw) {
  if (!Array.isArray(raw)) return null;
  let msgs = raw
    .filter((m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
    .map((m) => ({ role: m.role, content: m.content.trim().slice(0, MAX_CHARS) }))
    .filter((m) => m.content.length > 0)
    .slice(-MAX_HISTORY);
  while (msgs.length && msgs[0].role !== "user") msgs.shift();
  // Fusionne deux messages consécutifs du même rôle.
  const merged = [];
  for (const m of msgs) {
    const last = merged[merged.length - 1];
    if (last && last.role === m.role) last.content += "\n" + m.content;
    else merged.push({ ...m });
  }
  if (!merged.length || merged[merged.length - 1].role !== "user") return null;
  return merged;
}

async function handleChat(request, env, cors) {
  let body;
  try { body = await request.json(); } catch { return json({ error: "JSON invalide" }, 400, cors); }
  const lang = body.lang === "en" ? "en" : "fr";
  const messages = cleanMessages(body.messages);
  if (!messages) return json({ error: "Messages invalides" }, 400, cors);

  const ip = request.headers.get("CF-Connecting-IP") || "inconnu";
  if (!allowed(ip, Number(env.RATE_LIMIT) || 20)) {
    return json({ answer: LIMITED[lang], status: "limited" }, 429, cors);
  }

  // Langue d'interface ajoutée à la fin du dernier message (le prompt système reste identique, donc en cache).
  messages[messages.length - 1].content += `\n\n[${lang}]`;

  const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
  try {
    const response = await client.messages.parse({
      model: MODEL,
      max_tokens: 2000, // la réflexion du modèle compte dans ce plafond
      system: [{ type: "text", text: SYSTEM_PROMPT, cache_control: { type: "ephemeral" } }],
      messages,
      output_config: { effort: "low", format: zodOutputFormat(Reply) },
    });

    // Statistiques anonymes : visibles dans les journaux du Worker (aucune donnée personnelle).
    const out = response.parsed_output;
    console.log(JSON.stringify({
      evt: "chat", lang, status: out?.status ?? response.stop_reason,
      in: response.usage.input_tokens, cached: response.usage.cache_read_input_tokens, out: response.usage.output_tokens,
    }));

    if (response.stop_reason === "refusal" || !out) {
      return json({ answer: FALLBACK[lang], status: "unknown" }, 200, cors);
    }
    return json(out, 200, cors);
  } catch (error) {
    if (error instanceof Anthropic.RateLimitError) console.error("Claude: limite de débit atteinte");
    else if (error instanceof Anthropic.AuthenticationError) console.error("Claude: clé API invalide ou absente");
    else if (error instanceof Anthropic.APIError) console.error(`Claude: erreur ${error.status}`, error.message);
    else console.error("Erreur inattendue", error);
    return json({ answer: FALLBACK[lang], status: "error" }, 200, cors);
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const cors = corsHeaders(request, env);

    if (request.method === "OPTIONS") return new Response(null, { status: cors.ok ? 204 : 403, headers: cors.headers });
    if (url.pathname === "/health") return json({ ok: true, model: MODEL }, 200, cors.headers);
    if (url.pathname === "/faq" && request.method === "GET") {
      return json(faq, 200, { ...cors.headers, "Cache-Control": "public, max-age=300" });
    }
    if (url.pathname === "/chat" && request.method === "POST") {
      if (!cors.ok) return json({ error: "Origine non autorisée" }, 403, cors.headers);
      return handleChat(request, env, cors.headers);
    }
    return json({ error: "Introuvable" }, 404, cors.headers);
  },
};
