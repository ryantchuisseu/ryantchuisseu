/*!
 * Widget « Assistant JCIA » (JCIA 2027).
 * Intégration : une seule ligne dans le site, juste avant </body> :
 *   <script src="https://VOTRE-ADRESSE/jcia-chat.js" data-api="https://jcia-chatbot.VOTRE-COMPTE.workers.dev" defer></script>
 * Options (attributs data-) :
 *   data-api   adresse du Worker Cloudflare (obligatoire pour la FAQ et l'IA)
 *   data-lang  "fr" ou "en" (sinon : langue de la page, puis français)
 *   data-open  "true" pour ouvrir le chat au chargement (sinon : réduit en mascotte)
 * Le widget vit dans un Shadow DOM : son style ne touche pas au site, et inversement.
 */
(function () {
  "use strict";
  if (window.__jciaChat) return;
  window.__jciaChat = true;

  const script = document.currentScript || document.querySelector("script[data-api][src*='jcia-chat']");
  const API = ((script && script.dataset.api) || "").replace(/\/$/, "");
  const START_OPEN = script && script.dataset.open === "true";
  let lang = (script && script.dataset.lang) || ((document.documentElement.lang || "").toLowerCase().startsWith("en") ? "en" : "fr");
  const REDUCED = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- Textes ---------------- */
  const T = {
    fr: {
      name: "Assistant JCIA", online: "En ligne", weOnline: "Nous sommes en ligne", ph: "Écrivez votre message",
      welcome: "Bonjour et bienvenue ! Je suis l’assistant des JCIA 2027. Comment puis-je vous aider ?",
      b: { hello: "Bonjour !", idle: "Posez-moi une question.", listen: "Je vous écoute !", think: "Je réfléchis…", done: "Avec plaisir !", surprise: "Je n’ai pas bien compris.", sad: "Je n’ai pas la réponse.", careful: "Restez prudent.", focus: "Revenons aux JCIA." },
      layer: { faq: "FAQ officielle", ai: "Réponse IA, basée sur la FAQ", human: "Contact officiel" },
      unclear: "Je n’ai pas bien compris votre message. Pouvez-vous reformuler ? Vous pouvez aussi choisir un sujet ci-dessus.",
      thanks: "Avec plaisir ! Autre chose sur les JCIA 2027 ?",
      offline: "Je ne peux pas répondre aux questions libres pour le moment. Le secrétariat peut vous aider :",
      more: "En savoir plus", help: "Besoin d’aide ?", open: "Ouvrir l’assistant JCIA", refresh: "Rafraîchir la conversation",
      minimize: "Réduire le chat", emoji: "Choisir un émoji", send: "Envoyer", input: "Votre message", typing: "L’assistant écrit",
      edition: "3e édition", dates: "27 et 28 avril 2027", venue: "Hilton Hotel, Yaoundé", theme: "« Penser l’intelligence artificielle au Cameroun, pour le Cameroun »",
      contacts: "Contacts officiels", phone: "Téléphone", address: "Adresse",
      enjeux: ["Visibilité", "Financement", "Structuration", "Projection internationale"],
      privacy: "Ne partagez jamais de code PIN ni de mot de passe dans ce chat.",
    },
    en: {
      name: "JCIA Assistant", online: "Online", weOnline: "We are online", ph: "Type your message",
      welcome: "Hello and welcome! I am the JCIA 2027 assistant. How can I help you?",
      b: { hello: "Hello!", idle: "Ask me a question.", listen: "I’m listening!", think: "Thinking…", done: "My pleasure!", surprise: "I didn’t quite get that.", sad: "I don’t have the answer.", careful: "Stay safe.", focus: "Back to JCIA." },
      layer: { faq: "Official FAQ", ai: "AI answer, based on the FAQ", human: "Official contact" },
      unclear: "I didn’t quite understand your message. Could you rephrase? You can also pick a topic above.",
      thanks: "My pleasure! Anything else about JCIA 2027?",
      offline: "I can’t answer free questions right now. The secretariat can help:",
      more: "Learn more", help: "Need help?", open: "Open the JCIA assistant", refresh: "Restart the conversation",
      minimize: "Minimise the chat", emoji: "Pick an emoji", send: "Send", input: "Your message", typing: "The assistant is typing",
      edition: "3rd edition", dates: "27–28 April 2027", venue: "Hilton Hotel, Yaoundé", theme: "“Thinking Artificial Intelligence in Cameroon, for Cameroon”",
      contacts: "Official contacts", phone: "Phone", address: "Address",
      enjeux: ["Visibility", "Funding", "Structuring", "Global reach"],
      privacy: "Never share a PIN or password in this chat.",
    },
  };
  const CONTACT_DEFAULT = { email: "contact@jciacm.com", whatsapp: "+237 699 089 937", phones: ["+237 699 089 937", "+237 677 238 022"], address_fr: "Route de l’aéroport, Rond-point Cami-Toyota, Coron, Immeuble Dangote, 2e étage, Yaoundé", address_en: "Route de l’aéroport, Cami-Toyota roundabout, Coron, Dangote Building, 2nd floor, Yaoundé" };

  /* ---------------- Style (isolé dans le Shadow DOM) ---------------- */
  const CSS = `
:host{all:initial}
*{box-sizing:border-box}
[hidden]{display:none!important}
.root{--nuit:#0E1326;--entete:#0F1427;--carte:#182039;--section:#1A223C;--bord:#2C3147;--orange:#F6A343;--orange2:#E3843D;--turq:#2DB8BD;--terra:#CD6035;--violet:#5D4696;--violet2:#9D87DC;--gris:#B5BAD0;--encre:#19203A;--sable:#F4E6D2;--vert:#3CC36B;
  font-family:Sora,Arial,Helvetica,sans-serif;font-size:14px;line-height:1.5;color:#fff;position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));z-index:2147483000}
button{font-family:inherit;color:inherit}
:focus-visible{outline:2px solid var(--turq);outline-offset:2px}
.panel{width:min(384px,calc(100vw - 32px));height:min(640px,calc(100vh - 32px));height:min(640px,calc(100dvh - 32px));background:var(--nuit);border:1px solid var(--bord);border-radius:22px;box-shadow:0 24px 60px rgba(0,0,0,.45);display:flex;flex-direction:column;overflow:hidden}
.head{background:var(--entete);padding:12px 14px 10px;display:flex;align-items:center;gap:10px}
.av{flex:none;width:36px;height:36px;border-radius:50%;display:grid;place-items:center}
.av.bot{background:var(--sable);border:2px solid var(--turq);overflow:hidden}
.av.bot svg{width:30px;height:30px;margin-top:6px}
.av.lg{width:42px;height:42px}.av.lg svg{width:34px;height:34px}
.av.user{background:var(--violet)}.av.user svg{width:18px;height:18px}
.id{flex:1;min-width:0}
.name{font-weight:700;font-size:15px}
.status{font-size:12px;color:var(--gris);display:flex;align-items:center;gap:6px}
.dot{width:8px;height:8px;border-radius:50%;background:var(--vert);box-shadow:0 0 0 3px rgba(60,195,107,.2)}
.tools{display:flex;align-items:center;gap:4px}
.lang{display:flex;border:1px solid var(--bord);border-radius:999px;padding:2px;margin-right:4px}
.lang button{border:0;background:transparent;font-size:11px;font-weight:700;padding:4px 8px;border-radius:999px;cursor:pointer;color:var(--gris)}
.lang button[aria-pressed="true"]{background:var(--section);color:#fff;box-shadow:inset 0 0 0 1px var(--orange)}
.ib{width:34px;height:34px;border-radius:50%;border:0;background:transparent;display:grid;place-items:center;cursor:pointer;color:var(--gris)}
.ib:hover{background:var(--section);color:#fff}
.ib svg{width:18px;height:18px}
.sub{background:var(--entete);font-size:11px;color:var(--gris);padding:0 14px 8px;display:flex;align-items:center;gap:6px}
.sub .dot{width:6px;height:6px;box-shadow:none}
.toghu{height:8px;flex:none;background:linear-gradient(90deg,var(--orange) 0 25%,var(--turq) 25% 50%,var(--terra) 50% 75%,var(--violet2) 75%);opacity:.85}
.msgs{flex:1;min-height:0;overflow-y:scroll;padding:14px 12px 10px;display:flex;flex-direction:column;gap:12px;scrollbar-width:thin;scrollbar-color:var(--violet2) var(--carte)}
.msgs::-webkit-scrollbar{width:8px}.msgs::-webkit-scrollbar-track{background:var(--carte);border-radius:8px}.msgs::-webkit-scrollbar-thumb{background:var(--violet2);border-radius:8px}
.sep{display:flex;align-items:center;gap:10px;font-size:11px;color:var(--gris)}
.sep::before,.sep::after{content:"";flex:1;height:1px;background:var(--bord)}
.row{display:flex;gap:8px;align-items:flex-end}
.row.user{flex-direction:row-reverse}
.row .av{width:30px;height:30px}.row .av.bot svg{width:25px;height:25px;margin-top:5px}.row .av.user svg{width:15px;height:15px}
.col{display:flex;flex-direction:column;gap:4px;min-width:0;max-width:80%}
.row.user .col{align-items:flex-end}
.bubble{padding:10px 13px;border-radius:16px;font-size:13px;line-height:1.5;overflow-wrap:anywhere}
.row.bot .bubble{background:var(--carte);border:1px solid var(--bord);border-bottom-left-radius:4px}
.row.user .bubble{background:var(--violet);color:#fff;border-bottom-right-radius:4px;white-space:pre-wrap}
.bubble p{margin:0}.bubble>*+*{margin-top:8px}
.bubble a{color:var(--orange);text-underline-offset:2px}
.tag{font-size:10px;color:var(--gris);display:flex;align-items:center;gap:5px;padding-left:2px}
.tag::before{content:"";width:6px;height:6px;border-radius:2px;background:var(--tc,var(--gris))}
.typing{display:inline-flex;gap:4px;padding:4px 2px}
.typing span{width:7px;height:7px;border-radius:50%;background:var(--gris);animation:blink 1.2s infinite}
.typing span:nth-child(2){animation-delay:.2s}.typing span:nth-child(3){animation-delay:.4s}
@keyframes blink{0%,80%,100%{opacity:.25;transform:translateY(0)}40%{opacity:1;transform:translateY(-3px)}}
.qr{display:flex;flex-wrap:wrap;gap:8px;padding-left:38px}
.pill{min-height:36px;border-radius:999px;background:transparent;padding:7px 14px;font-size:12px;font-weight:600;cursor:pointer}
.pill.o{border:1.5px solid var(--orange);color:var(--orange)}.pill.o:hover{background:rgba(246,163,67,.1)}
.sugg{display:flex;justify-content:flex-end}
.pill.v{border:1.5px solid var(--violet2);color:var(--violet2);font-weight:400}.pill.v:hover{background:rgba(157,135,220,.1)}
.card{position:relative;background:var(--section);border:1px solid var(--bord);border-radius:22px;overflow:hidden;padding:16px 14px 12px}
.card::before{content:"";position:absolute;inset:0 0 auto;height:5px;background:var(--c,var(--orange))}
.card .wm{position:absolute;right:8px;top:2px;font-size:58px;font-weight:800;line-height:1;opacity:.14;color:var(--c,var(--orange));pointer-events:none}
.card .k{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--gris)}
.card .t{font-size:17px;font-weight:800;color:var(--orange);margin-top:2px}
.card .r{font-weight:600}
.card .s{font-size:12px;color:var(--gris);margin-top:6px}
.card dl{margin:4px 0 0;display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 10px;font-size:12px}
.card dt{color:var(--gris)}.card dd{margin:0;user-select:all;overflow-wrap:anywhere}
.enjeux{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}
.enjeu{position:relative;overflow:hidden;background:var(--section);border:1px solid var(--bord);border-radius:14px;padding:12px 10px 8px;font-size:12px;font-weight:600}
.enjeu::before{content:"";position:absolute;inset:0 0 auto;height:4px;background:var(--c)}
.enjeu i{position:absolute;right:6px;top:0;font-style:normal;font-size:30px;font-weight:800;opacity:.14;color:var(--c)}
.stage{flex:none;height:76px;display:flex;align-items:flex-end;gap:6px;padding:0 12px;background:var(--nuit)}
.m-wrap{position:relative;width:62px;height:74px;flex:none;cursor:pointer;border:0;background:transparent;padding:0}
.m-move{position:absolute;left:0;right:0;bottom:3px;height:68px;transform-origin:50% 100%}
.m-tilt{width:100%;height:100%;transform-origin:50% 100%;transition:transform .35s ease}
.m-tilt svg{width:100%;height:100%;display:block;overflow:visible}
.shadow{position:absolute;left:50%;bottom:-2px;width:44px;height:7px;margin-left:-22px;border-radius:50%;background:rgba(0,0,0,.55);filter:blur(1.5px)}
.say{margin-bottom:26px;background:var(--sable);color:var(--encre);font-size:12px;font-weight:600;border-radius:14px;padding:6px 11px;position:relative;max-width:220px;transition:opacity .2s,transform .2s;transform-origin:left bottom}
.say::before{content:"";position:absolute;left:-6px;bottom:8px;border:6px solid transparent;border-right-color:var(--sable);border-left:0}
.say.off{opacity:0;transform:scale(.9)}
.mascot .e-arc,.mascot .m-frown,.mascot .m-open,.mascot .dots{opacity:0}
.mascot .e-dot,.mascot .e-arc,.mascot .m-smile,.mascot .m-frown,.mascot .m-open,.mascot .dots{transition:opacity .2s,transform .25s;transform-box:fill-box;transform-origin:center}
[data-mood="happy"] .e-dot{opacity:0}[data-mood="happy"] .e-arc{opacity:1}
[data-mood="think"] .e-dot{transform:translate(4px,-2px)}[data-mood="think"] .dots{opacity:1}[data-mood="think"] .m-smile{transform:scaleX(.6)}
[data-mood="surprise"] .m-smile{opacity:0}[data-mood="surprise"] .m-open{opacity:1}[data-mood="surprise"] .e-dot{transform:scale(1.3)}
[data-mood="sad"] .m-smile{opacity:0}[data-mood="sad"] .m-frown{opacity:1}[data-mood="sad"] .e-dot{transform:translateY(1.5px)}
[data-mood="sad"] .m-tilt{transform:rotate(-8deg) translateY(2px)}
[data-mood="think"] .m-tilt{animation:sway 1.6s ease-in-out infinite}
.dots circle{animation:blink 1.2s infinite}.dots circle:nth-child(2){animation-delay:.2s}.dots circle:nth-child(3){animation-delay:.4s}
@keyframes sway{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg)}}
@keyframes jump{0%,100%{transform:translateY(0) scaleY(1)}10%{transform:translateY(0) scaleY(.92)}45%{transform:translateY(-16px) scaleY(1.03)}80%{transform:translateY(0) scaleY(.95)}}
@keyframes hop{0%,100%{transform:translateY(0)}40%{transform:translateY(-7px)}}
@keyframes nod{0%,100%{transform:rotate(0)}50%{transform:rotate(5deg) translateY(1px)}}
@keyframes bounce{0%,100%{transform:scale(1)}25%{transform:scale(1.08,.9)}55%{transform:scale(.95,1.08) translateY(-6px)}}
@keyframes shrink{0%,100%{transform:scale(1);opacity:1}45%{transform:scale(.6);opacity:.5}}
@keyframes shrink2{0%,100%{transform:scale(1)}40%{transform:scale(.8)}}
.a-jump .m-move{animation:jump .55s ease-out}.a-jump .shadow{animation:shrink .55s ease-out}
.a-jump2 .m-move{animation:jump .55s ease-out 2}.a-jump2 .shadow{animation:shrink .55s ease-out 2}
.a-hop .m-move{animation:hop .5s ease-out}.a-hop .shadow{animation:shrink2 .5s ease-out}
.a-nod .m-move{animation:nod .2s ease-out}
.a-bounce .m-move{animation:bounce .6s ease-out}
.composer{flex:none;border-top:2px solid var(--bord);background:var(--entete);padding:10px 10px 8px;position:relative}
.field{display:flex;align-items:center;gap:4px;background:var(--carte);border:1px solid var(--bord);border-radius:999px;padding:4px 4px 4px 6px}
.field:focus-within{border-color:var(--violet2)}
.field input{flex:1;min-width:0;background:transparent;border:0;color:#fff;font:inherit;font-size:16px;padding:8px 4px;outline:none}
.field input::placeholder{color:var(--gris)}
.send{flex:none;width:44px;height:44px;border-radius:999px;border:0;cursor:pointer;display:grid;place-items:center;background:linear-gradient(135deg,var(--orange),var(--orange2));color:var(--encre);box-shadow:0 6px 18px rgba(246,163,67,.35)}
.send svg{width:19px;height:19px}
.send:disabled{opacity:.55;box-shadow:none;cursor:default}
.privacy{font-size:10px;color:var(--gris);text-align:center;margin-top:6px}
.pop{position:absolute;left:10px;bottom:66px;background:var(--section);border:1px solid var(--bord);border-radius:16px;padding:8px;display:grid;grid-template-columns:repeat(6,36px);gap:2px;box-shadow:0 10px 30px rgba(0,0,0,.4)}
.pop button{width:36px;height:36px;border:0;background:transparent;border-radius:10px;font-size:19px;cursor:pointer}
.pop button:hover{background:var(--carte)}
.launcher{display:flex;align-items:flex-end;gap:6px;flex-direction:row-reverse}
.launcher .m-wrap{width:70px;height:82px}.launcher .m-move{height:76px}.launcher .say{margin-bottom:34px;box-shadow:0 6px 18px rgba(0,0,0,.25)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
`;

  /* ---------------- Dessins ---------------- */
  const ROBOT_BODY = `<path d="M50 14C29 14 21 32 21 52v22c0 5-3 7-5 10h68c-2-3-5-5-5-10V52c0-20-8-38-29-38Z" fill="#16193B" stroke="#55609A" stroke-width="2"/><rect x="30" y="31" width="40" height="25" rx="12.5" fill="#fff"/>`;
  const ROBOT_BUTTONS = `<circle cx="40" cy="68" r="3.4" fill="#3CC36B"/><circle cx="50" cy="68" r="3.4" fill="#E5484D"/><circle cx="60" cy="68" r="3.4" fill="#F6A343"/>`;
  const AVATAR = `<svg viewBox="0 0 100 100" aria-hidden="true">${ROBOT_BODY}<circle cx="42" cy="42" r="3.4" fill="#16193B"/><circle cx="58" cy="42" r="3.4" fill="#16193B"/><path d="M44 49q6 5 12 0" fill="none" stroke="#16193B" stroke-width="2.4" stroke-linecap="round"/>${ROBOT_BUTTONS}</svg>`;
  const MASCOT = `<div class="m-move"><div class="m-tilt"><svg class="mascot" viewBox="0 0 100 100" aria-hidden="true">
<g class="dots" fill="#2DB8BD"><circle cx="38" cy="4" r="3.6"/><circle cx="50" cy="1" r="3.6"/><circle cx="62" cy="4" r="3.6"/></g>${ROBOT_BODY}
<circle class="e-dot" cx="42" cy="42" r="3.4" fill="#16193B"/><circle class="e-dot" cx="58" cy="42" r="3.4" fill="#16193B"/>
<path class="e-arc" d="M38.5 43.5q3.5-5 7 0M54.5 43.5q3.5-5 7 0" fill="none" stroke="#16193B" stroke-width="2.4" stroke-linecap="round"/>
<path class="m-smile" d="M44 49q6 5 12 0" fill="none" stroke="#16193B" stroke-width="2.4" stroke-linecap="round"/>
<path class="m-frown" d="M44 52.5q6-4.5 12 0" fill="none" stroke="#16193B" stroke-width="2.4" stroke-linecap="round"/>
<ellipse class="m-open" cx="50" cy="50.5" rx="3" ry="3.4" fill="#16193B"/>${ROBOT_BUTTONS}
<ellipse cx="38" cy="90" rx="9" ry="5.5" fill="#16193B" stroke="#55609A" stroke-width="2"/><ellipse cx="62" cy="90" rx="9" ry="5.5" fill="#16193B" stroke="#55609A" stroke-width="2"/>
</svg></div></div><div class="shadow"></div>`;
  const PERSON = `<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4" fill="#fff"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7" fill="#fff"/></svg>`;
  const I = {
    refresh: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 15.5-6.2L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15.5 6.2L3 16"/><path d="M3 21v-5h5"/></svg>`,
    min: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M5 12h14"/></svg>`,
    emoji: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M8.5 14.5s1.2 2 3.5 2 3.5-2 3.5-2"/><circle cx="9" cy="10" r=".6" fill="currentColor"/><circle cx="15" cy="10" r=".6" fill="currentColor"/></svg>`,
    send: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7Z"/></svg>`,
  };

  /* ---------------- Construction ---------------- */
  const host = document.createElement("div");
  host.id = "jcia-chat";
  const shadow = host.attachShadow({ mode: "open" });
  shadow.innerHTML = `<style>${CSS}</style>
<div class="root">
  <div class="launcher" data-el="launcher">
    <button class="m-wrap" data-el="mini" data-mood="neutral"></button>
    <div class="say" data-el="sayMini"></div>
  </div>
  <section class="panel" data-el="panel" role="dialog" hidden>
    <div class="head">
      <div class="av bot lg">${AVATAR}</div>
      <div class="id"><div class="name" data-el="name"></div><div class="status"><span class="dot"></span><span data-el="online"></span></div></div>
      <div class="tools">
        <div class="lang" role="group" aria-label="Langue / Language"><button data-lang="fr">FR</button><button data-lang="en">EN</button></div>
        <button class="ib" data-el="refresh">${I.refresh}</button>
        <button class="ib" data-el="min">${I.min}</button>
      </div>
    </div>
    <div class="sub"><span class="dot"></span><span data-el="weOnline"></span></div>
    <div class="toghu" aria-hidden="true"></div>
    <div class="msgs" data-el="msgs" aria-live="polite"></div>
    <div class="stage">
      <button class="m-wrap" data-el="mascot" data-mood="happy" aria-hidden="true" tabindex="-1"></button>
      <div class="say" data-el="say" role="status"></div>
    </div>
    <div class="composer">
      <div class="field">
        <button class="ib" data-el="emojiBtn">${I.emoji}</button>
        <input data-el="inp" type="text" autocomplete="off" maxlength="600">
        <button class="send" data-el="send" disabled>${I.send}</button>
      </div>
      <div class="pop" data-el="pop" hidden></div>
      <div class="privacy" data-el="privacy"></div>
    </div>
  </section>
</div>`;
  const $ = (n) => shadow.querySelector(`[data-el="${n}"]`);
  const panel = $("panel"), launcher = $("launcher"), msgs = $("msgs"), inp = $("inp"), sendBtn = $("send"), mascot = $("mascot"), say = $("say"), mini = $("mini");
  mascot.innerHTML = MASCOT; mini.innerHTML = MASCOT;

  /* ---------------- État ---------------- */
  let faq = null, busy = false, open = false, history = [];
  let idleT = null, hopT = null, backT = null;
  const t = () => T[lang];
  const byId = (id) => faq && faq.items.find((x) => x.id === id);
  const contacts = () => (faq && faq.contacts) || CONTACT_DEFAULT;

  /* ---------------- Mascotte ---------------- */
  function anim(el, cls) {
    if (REDUCED) return;
    el.classList.remove("a-jump", "a-jump2", "a-hop", "a-nod", "a-bounce");
    void el.offsetWidth; el.classList.add(cls);
  }
  function setMood(m, bub, motion) {
    mascot.dataset.mood = m === "idle" || m === "neutral" ? "neutral" : m;
    if (bub) { say.textContent = t().b[bub]; say.classList.remove("off"); } else say.classList.add("off");
    if (motion) anim(mascot, motion);
  }
  function clearTimers() { clearTimeout(idleT); clearInterval(hopT); clearTimeout(backT); }
  function scheduleIdle() { clearTimeout(idleT); clearInterval(hopT); if (open) idleT = setTimeout(goIdle, 6000); }
  function goIdle() {
    if (busy || !open) return;
    setMood("idle", "idle", "a-hop");
    clearInterval(hopT); if (!REDUCED) hopT = setInterval(() => anim(mascot, "a-hop"), 3000);
  }
  function backToRest(ms) { clearTimeout(backT); backT = setTimeout(() => { if (!busy) { setMood("neutral", null); scheduleIdle(); } }, ms); }
  mascot.addEventListener("click", () => { if (busy) return; clearTimers(); setMood("happy", "hello", "a-jump"); backToRest(2500); });

  /* ---------------- Rendu ---------------- */
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const linkify = (s) => esc(s).replace(/https?:\/\/[^\s<]+[^\s<.,;:!?)»]/g, (u) => `<a href="${u}" target="_blank" rel="noopener">${u}</a>`);
  const para = (s) => s.split(/\n{2,}/).map((p) => `<p>${linkify(p)}</p>`).join("");
  const LCOL = { faq: "#F6A343", ai: "#2DB8BD", human: "#9D87DC" };

  function card(kind) {
    const c = contacts(), L = t();
    if (kind === "dates") return `<div class="card"><span class="wm">03</span><div class="k">${L.edition}</div><div class="t">${L.dates}</div><div class="r">${L.venue}</div><div class="s">${L.theme}</div></div>`;
    if (kind === "enjeux") {
      const col = ["#F6A343", "#2DB8BD", "#CD6035", "#9D87DC"];
      return `<div class="enjeux">${L.enjeux.map((x, i) => `<div class="enjeu" style="--c:${col[i]}"><i>0${i + 1}</i>${esc(x)}</div>`).join("")}</div>`;
    }
    if (kind === "contact") return `<div class="card" style="--c:#2DB8BD"><div class="k">${L.contacts}</div><dl><dt>E-mail</dt><dd>${esc(c.email)}</dd><dt>WhatsApp</dt><dd>${esc(c.whatsapp)}</dd><dt>${L.phone}</dt><dd>${c.phones.map(esc).join("<br>")}</dd><dt>${L.address}</dt><dd>${esc(lang === "en" ? c.address_en : c.address_fr)}</dd></dl></div>`;
    return "";
  }
  function scroll() { msgs.scrollTop = msgs.scrollHeight; }
  function addBot(html, layer) {
    const d = document.createElement("div"); d.className = "row bot";
    d.innerHTML = `<div class="av bot">${AVATAR}</div><div class="col"><div class="bubble">${html}</div>${layer ? `<div class="tag" style="--tc:${LCOL[layer]}">${t().layer[layer]}</div>` : ""}</div>`;
    msgs.appendChild(d); scroll(); return d;
  }
  function addUser(text) {
    const d = document.createElement("div"); d.className = "row user";
    d.innerHTML = `<div class="av user">${PERSON}</div><div class="col"><div class="bubble">${esc(text)}</div></div>`;
    msgs.appendChild(d); scroll();
  }
  function addTyping() { return addBot(`<span class="typing" aria-label="${t().typing}"><span></span><span></span><span></span></span>`); }

  function applyTexts() {
    const L = t();
    $("name").textContent = L.name; $("online").textContent = L.online; $("weOnline").textContent = L.weOnline;
    inp.placeholder = L.ph; inp.setAttribute("aria-label", L.input);
    panel.setAttribute("aria-label", L.name);
    $("refresh").setAttribute("aria-label", L.refresh); $("refresh").title = L.refresh;
    $("min").setAttribute("aria-label", L.minimize); $("min").title = L.minimize;
    $("emojiBtn").setAttribute("aria-label", L.emoji); $("emojiBtn").title = L.emoji;
    sendBtn.setAttribute("aria-label", L.send);
    mini.setAttribute("aria-label", L.open); $("sayMini").textContent = L.help;
    $("privacy").textContent = L.privacy;
    shadow.querySelectorAll(".lang button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === lang)));
  }

  function welcome() {
    msgs.innerHTML = ""; history = []; busy = false;
    const dt = new Date().toLocaleDateString(lang === "fr" ? "fr-FR" : "en-GB", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
    msgs.insertAdjacentHTML("beforeend", `<div class="sep"><span>${esc(dt)}</span></div>`);
    addBot(`<p>${esc(t().welcome)}</p>`);
    if (faq) {
      const qr = document.createElement("div"); qr.className = "qr";
      faq.quick.map(byId).filter(Boolean).forEach((it) => {
        const b = document.createElement("button"); b.className = "pill o"; b.textContent = it[lang].label || it[lang].q;
        b.onclick = () => askFaq(it); qr.appendChild(b);
      });
      msgs.appendChild(qr);
      const s = byId(faq.suggestions[0]);
      if (s) {
        const sg = document.createElement("div"); sg.className = "sugg";
        const b = document.createElement("button"); b.className = "pill v"; b.textContent = s[lang].label || s[lang].q;
        b.onclick = () => askFaq(s); sg.appendChild(b); msgs.appendChild(sg);
      }
    }
    clearTimers(); setMood("happy", "hello", "a-jump"); backToRest(2500);
  }

  /* ---------------- Couche 1 : FAQ et règles (sans IA) ---------------- */
  function faqHtml(it) {
    let html = para(it[lang].a);
    if (it.card) html += card(it.card);
    if (it.link) html += `<p><a href="${esc(it.link)}" target="_blank" rel="noopener">${t().more}</a></p>`;
    return html;
  }
  function reply(html, layer, mood, bub, plain) {
    const motion = mood === "happy" ? (bub === "done" ? "a-jump2" : "a-jump") : mood === "surprise" ? "a-bounce" : null;
    addBot(html, layer); busy = false;
    setMood(mood, bub, motion);
    backToRest(mood === "surprise" || mood === "sad" ? 3500 : 2500);
    if (plain) history.push({ role: "assistant", content: plain });
  }
  function askFaq(it) {
    if (busy) return;
    const label = it[lang].label || it[lang].q;
    addUser(label); history.push({ role: "user", content: it[lang].q });
    busy = true; clearTimers(); setMood("think", "think");
    const typing = addTyping();
    setTimeout(() => { typing.remove(); reply(faqHtml(it), "faq", "happy", "done", it[lang].a); }, REDUCED ? 200 : 700);
  }
  function isGibberish(text) {
    const n = text.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
    const words = n.replace(/[^a-z\s]/g, " ").trim().split(/\s+/).filter(Boolean);
    if (!words.length) return !/[\p{Extended_Pictographic}?]/u.test(text);
    if (/(.)\1{3,}/.test(n)) return true;
    if (words.every((w) => !/[aeiouy]/.test(w))) return true;
    return words.length === 1 && words[0].length <= 6 && !/^(merci|thanks?|bonjour|hello|salut|hi|hey|ok|oui|non|yes|no|gala|dates?|lieu|prix|price|billets?|tickets?|contact|caia|awards?|salon|expo|stand|hilton|programme|program|faq)$/.test(words[0]);
  }
  const THANKS = /^(merci( beaucoup| bien)?|thanks?( you)?( so much| a lot)?|super|parfait|top|great|ok merci)[\s!.]*$/i;

  /* ---------------- Couche 2 : IA (via le Worker) ---------------- */
  async function send(text) {
    text = (text || "").trim();
    if (!text || busy) return;
    inp.value = ""; sendBtn.disabled = true; $("pop").hidden = true;
    addUser(text);
    busy = true; clearTimers(); setMood("think", "think");
    const typing = addTyping();
    const done = (fn) => setTimeout(() => { typing.remove(); fn(); }, REDUCED ? 200 : 700);

    if (THANKS.test(text)) { history.push({ role: "user", content: text }); return done(() => reply(`<p>${esc(t().thanks)}</p>`, null, "happy", "done", t().thanks)); }
    if (isGibberish(text)) return done(() => reply(`<p>${esc(t().unclear)}</p>`, null, "surprise", "surprise"));

    history.push({ role: "user", content: text });
    if (!API) return done(offline);
    try {
      const res = await fetch(`${API}/chat`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ lang, messages: history.slice(-8) }) });
      const data = await res.json();
      typing.remove();
      showAi(data);
    } catch (e) {
      typing.remove(); offline();
    }
  }
  function offline() {
    reply(`<p>${esc(t().offline)}</p>${card("contact")}`, "human", "sad", "sad");
  }
  function showAi(data) {
    const answer = (data && data.answer) || "";
    const status = data && data.status;
    if (!answer) return offline();
    const map = {
      answered: ["happy", "done", "ai"], thanks: ["happy", "done", "ai"],
      unknown: ["sad", "sad", "human"], error: ["sad", "sad", "human"], limited: ["sad", "sad", "human"],
      unclear: ["surprise", "surprise", "ai"], off_topic: ["neutral", "focus", "ai"], guardrail: ["neutral", "careful", "ai"],
    };
    const [mood, bub, layer] = map[status] || map.answered;
    const extra = status === "unknown" ? card("contact") : "";
    reply(para(answer) + extra, layer, mood, bub, answer);
  }

  /* ---------------- Événements ---------------- */
  inp.addEventListener("input", () => {
    sendBtn.disabled = !inp.value.trim();
    clearInterval(hopT); clearTimeout(backT);
    if (!busy) { if (inp.value.trim()) setMood("happy", "listen", "a-nod"); else setMood("neutral", null); }
    scheduleIdle();
  });
  inp.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.isComposing) { e.preventDefault(); send(inp.value); } });
  sendBtn.onclick = () => send(inp.value);
  const EM = ["😀", "😊", "🙏", "👍", "👏", "🎉", "🤖", "💡", "📅", "📍", "🤝", "❓"];
  $("pop").innerHTML = EM.map((e) => `<button type="button">${e}</button>`).join("");
  $("pop").addEventListener("click", (e) => { const b = e.target.closest("button"); if (!b) return; inp.value += b.textContent; inp.dispatchEvent(new Event("input")); inp.focus(); });
  $("emojiBtn").onclick = () => { $("pop").hidden = !$("pop").hidden; };
  $("refresh").onclick = welcome;
  $("min").onclick = () => setOpen(false);
  mini.onclick = () => setOpen(true);
  shadow.querySelectorAll(".lang button").forEach((b) => (b.onclick = () => { if (b.dataset.lang !== lang) { lang = b.dataset.lang; applyTexts(); welcome(); } }));
  panel.addEventListener("keydown", (e) => { if (e.key === "Escape") { if (!$("pop").hidden) $("pop").hidden = true; else setOpen(false); } });

  let started = false;
  function setOpen(v) {
    open = v; panel.hidden = !v; launcher.hidden = v; clearTimers();
    if (v) {
      if (!started) { started = true; welcome(); } else { setMood("happy", "hello", "a-jump"); backToRest(2500); }
      inp.focus();
    } else {
      mini.focus();
      if (!REDUCED) { anim(mini, "a-hop"); hopT = setInterval(() => anim(mini, "a-hop"), 6000); }
    }
  }

  /* ---------------- Démarrage ---------------- */
  function init() {
    document.body.appendChild(host);
    applyTexts();
    setOpen(START_OPEN);
    if (API) {
      fetch(`${API}/faq`).then((r) => r.json()).then((data) => {
        faq = data;
        if (started && history.length === 0) welcome(); // affiche les boutons dès que la FAQ arrive
      }).catch(() => {});
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
