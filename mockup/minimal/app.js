/* =====================================================================
   JCIA 2027 — maquette MINIMALISTE (HTML/CSS/JS sans dépendance)
   Deux rendus d'icônes : « 3d » (Fluent Emoji 3D, MIT) ou « flat » (traits).
   Choix : ?icons=3d|flat dans l'URL, ou window.JCIA_ICONS (fichiers autonomes de dist/).
   Contenu : pages publiques de https://jciacm.com/ (relevé du 2026-11-02). Toutes les personnes et
   organisations affichées dans Rencontres sont FICTIVES. Rien n'est envoyé : tout reste dans le navigateur.
   ===================================================================== */
"use strict";
const qs = new URLSearchParams(location.search);
const SKIN = ["leger"].includes(qs.get("skin")) ? qs.get("skin") : (window.JCIA_SKIN || "");   // habillage optionnel « Léger »
if(SKIN) document.documentElement.dataset.skin = SKIN;
const STYLE = ["3d","flat"].includes(qs.get("icons")) ? qs.get("icons") : (window.JCIA_ICONS || (SKIN === "leger" ? "flat" : "3d"));
const IMG = window.JCIA_IMG || {}, ASSET = window.JCIA_ASSET || {};
const asset = n => ASSET[n] || ({ logo:"../assets/logo-jcia.png", logoDay:"../assets/logo-jcia-jour.png", band:"../assets/bande-toghu.png", map:"../assets/carte-cameroun.png" })[n];
const EVENT_START = new Date("2027-04-27T07:00:00Z");

/* ---------- Icônes ---------- */
const HAS3D = new Set("home calendar ticket handshake compass trophy bell map mic star rocket briefcase heart ballot pin phone mail help check sun moon camera warning clock mega bulb robot party sparkles books gear tv chat card mobile brain".split(" "));
const FLAT = {
  home:'<path d="M3.5 11.5 12 4l8.5 7.5"/><path d="M5.5 10v9.5h13V10"/><path d="M10 19.5v-5.5h4v5.5"/>',
  calendar:'<rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M8 3v4M16 3v4M3.5 10h17"/>',
  ticket:'<path d="M4 7.5A1.5 1.5 0 0 1 5.5 6h13A1.5 1.5 0 0 1 20 7.5V10a2 2 0 0 0 0 4v2.5a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 16.5V14a2 2 0 0 0 0-4z"/><path d="M14.5 6.5v11" stroke-dasharray="1.6 2.4"/>',
  handshake:'<circle cx="9" cy="8.5" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9.5" r="2.5"/><path d="M17.5 14.5A5 5 0 0 1 21.5 19"/>',
  compass:'<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
  trophy:'<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5v1.5A3 3 0 0 0 8 10.5M16 6h3v1.5a3 3 0 0 1-3 3M12 13v4M8.5 20h7M10 17h4"/>',
  bell:'<path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 2h-15z"/><path d="M10 21a2.2 2.2 0 0 0 4 0"/>',
  map:'<path d="M9 4 3.5 6v14L9 18l6 2 5.5-2V4L15 6z"/><path d="M9 4v14M15 6v14"/>',
  mic:'<rect x="9" y="3" width="6" height="11.5" rx="3"/><path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3"/>',
  star:'<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.9L12 16.9 6.8 19.7l1-5.9-4.3-4.1 5.9-.8z"/>',
  rocket:'<path d="M12 3c3 2 5 5 5 9l-2 3H9l-2-3c0-4 2-7 5-9z"/><circle cx="12" cy="10" r="1.6"/><path d="M9 15l-3 3 3-.5M15 15l3 3-3-.5M12 17v4"/>',
  briefcase:'<rect x="3.5" y="7.5" width="17" height="12" rx="2.5"/><path d="M9 7.5V6a1.5 1.5 0 0 1 1.5-1.5h3A1.5 1.5 0 0 1 15 6v1.5M3.5 13h17"/>',
  heart:'<path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.2 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10z"/>',
  ballot:'<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/>',
  pin:'<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
  phone:'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1.5 1.5 0 0 1-1.6 1.5C10.7 20 4 13.3 3.5 5.6A1.5 1.5 0 0 1 5 4z"/>',
  mail:'<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="m4 7.5 8 6 8-6"/>',
  help:'<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 .9-1 1.7M12 17h.01"/>',
  check:'<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M18.7 5.3l-1.6 1.6M6.9 17.1l-1.6 1.6"/>',
  moon:'<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5z"/>',
  camera:'<path d="M4 8.5A1.5 1.5 0 0 1 5.5 7H8l1.5-2h5L16 7h2.5A1.5 1.5 0 0 1 20 8.5v9a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 17.5z"/><circle cx="12" cy="13" r="3.3"/>',
  warning:'<path d="M12 4l9 16H3z"/><path d="M12 10v4M12 17.2h.01"/>',
  clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
  mega:'<path d="M4 10v4h3l7 4V6L7 10z"/><path d="M17.5 9a4 4 0 0 1 0 6"/>',
  bulb:'<path d="M9 17h6M10 20h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
  robot:'<rect x="5" y="8" width="14" height="11" rx="3"/><path d="M12 8V5M9.5 13h.01M14.5 13h.01M9.5 16.5h5"/><circle cx="12" cy="4" r="1"/>',
  sparkles:'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
  books:'<path d="M5 5a2 2 0 0 1 2-2h12v14H7a2 2 0 0 0-2 2z"/><path d="M5 19a2 2 0 0 0 2 2h12v-4"/>',
  gear:'<circle cx="12" cy="12" r="3"/><path d="M12 3v2.5M12 18.5V21M3 12h2.5M18.5 12H21M5.6 5.6l1.8 1.8M16.6 16.6l1.8 1.8M18.4 5.6l-1.8 1.8M7.4 16.6l-1.8 1.8"/>',
  tv:'<rect x="3" y="5" width="18" height="12" rx="2.5"/><path d="M8 20.5h8M12 17v3.5"/>',
  chat:'<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v7a2.5 2.5 0 0 1-2.5 2.5H11l-4.5 4v-4H6.5A2.5 2.5 0 0 1 4 13.5z"/>',
  card:'<rect x="3" y="6" width="18" height="12" rx="2.5"/><path d="M3 10h18M7 15h3"/>',
  mobile:'<rect x="7" y="3" width="10" height="18" rx="2.5"/><path d="M11 18h2"/>',
  party:'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
  brain:'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
  search:'<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>', close:'<path d="M6 6l12 12M18 6L6 18"/>',
  back:'<path d="M15 5l-7 7 7 7"/>', chevron:'<path d="M9 5l7 7-7 7"/>', share:'<path d="M12 15V3.5M7.5 8 12 3.5 16.5 8"/><path d="M5 12v6.5A1.5 1.5 0 0 0 6.5 20h11a1.5 1.5 0 0 0 1.5-1.5V12"/>',
  user:'<circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20a7.5 7.5 0 0 1 15 0"/>',
};
function ic(name, size = 24){
  if(STYLE === "3d" && HAS3D.has(name))
    return `<img class="i3" src="${IMG[name] || "assets/3d/" + name + ".png"}" width="${size}" height="${size}" alt="" draggable="false">`;
  return `<svg class="ic" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">${FLAT[name] || FLAT.sparkles}</svg>`;
}
const flat = (name, size = 22) => `<svg class="ic" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">${FLAT[name]}</svg>`;

/* ---------- Données (contenu du site) ---------- */
const TICKETS = [
  { id:"gratuit",  name:"Gratuit",  price:0,     old:0,     sub:"Visite des stands et du Salon" },
  { id:"etudiant", name:"Étudiant", price:3500,  old:5000,  sub:"2 jours · carte étudiante à l'entrée" },
  { id:"standard", name:"Standard", price:7000,  old:10000, sub:"Le pass complet : plénières, forums, rencontres", reco:true },
  { id:"online",   name:"En ligne", price:10500, old:15000, sub:"Tout suivre à distance, replay 30 jours" },
  { id:"vip",      name:"VIP",      price:17500, old:25000, sub:"Standard + déjeuner networking" },
];
const DAY1 = [
  ["08:00 – 09:45","Accueil","Accueil et enregistrement","Visite libre des stands."],
  ["09:45 – 10:00","Accueil","Arrivée des officiels","Gouvernement, corps diplomatique, invités."],
  ["10:00 – 11:00","Cérémonie","Cérémonie officielle d'ouverture","Discours des partenaires et des autorités."],
  ["11:00 – 12:00","Salon","Inauguration du Salon 100 % IA","Visite guidée des stands."],
  ["12:00 – 13:00","Plénière","Souveraineté numérique et modèles d'IA africains","Bâtir des systèmes ancrés dans nos langues et nos données."],
  ["13:00 – 13:45","Plénière","Financer l'excellence","Capital, calcul et talents pour les champions africains de l'IA."],
  ["13:45 – 15:00","Networking","Déjeuner networking","Gouvernement, diplomatie, sponsors."],
  ["15:00 – 18:00","Salon","Démos et rencontres d'affaires","Rendez-vous B2B / B2G et démos des exposants."],
  ["18:00","Clôture","Fin de la journée 1",""],
];
const DAY2 = [
  ["09:00 – 12:00","Masterclass","4 masterclasses en parallèle","Administration · Santé · Agriculture · Cybersécurité."],
  ["11:00","Talk","Boris Landry KOUEKAM","Directeur de CAIPI."],
  ["13:30","Pitch","Startup Pitch Competition","Les startups finalistes face aux investisseurs."],
  ["15:00","Forum","Women in AI Forum","Leadership féminin, inclusion, biais."],
  ["16:15","Forum","Young AI Leaders Forum","Travaux d'étudiants et mentorat."],
  ["Toute la journée","Emploi","AI Career Fair","Entreprises, labos et administrations qui recrutent."],
  ["19:30","Gala","Gala des Cameroon AI Awards","Dix prix, sur invitation."],
];
const parseTime = s => { const m = s.match(/(\d{2}):(\d{2})(?:\s*–\s*(\d{2}):(\d{2}))?/); if(!m) return null; const a = +m[1]*60 + +m[2]; return [a, m[3] ? +m[3]*60 + +m[4] : a + 45]; };
const SESSIONS = [DAY1, DAY2].flatMap((L, d) => L.map((e, i) => { const t = parseTime(e[0]); return { id:`d${d+1}-${i}`, day:d+1, time:e[0], tag:e[1], title:e[2], desc:e[3], start:t && t[0], end:t && t[1] }; }));
const overlap = (a, b) => a.id !== b.id && a.day === b.day && a.start != null && b.start != null && a.start < b.end && b.start < a.end;

const SPEAKERS = [
  ["Boris Landry KOUEKAM","Directeur de CAIPI · IAC","Mer. 28 avril · 11:00"],
  ["Natalie DELATTE","Pictet Asset Management","Mer. 28 avril · 09:00"],
  ["Eddy Damaris NONO DEFO","Chaire UNESCO, Université de Montréal","Mar. 27 avril · 12:00"],
  ["Dr. Axel MAZOLO","Directeur · GAIGI","Mar. 27 avril · 12:00"],
  ["Guillaume SOTO","Shauri & Maitrise AI","Mar. 27 avril · 13:00"],
  ["Destin KOUAM","Entrepreneur · IAC","Mer. 28 avril · 15:00"],
  ["Dr. Volviane Saphir MFOGO","Open AIR","Mar. 27 avril · 12:00"],
  ["David KENFACK","Chercheur en IA","Mer. 28 avril · 09:00"],
  ["Dr. Frederic NGABA","OSIA Technologies","Mar. 27 avril · 13:00"],
  ["Habib IYA","Inlab","Mer. 28 avril · 09:00"],
  ["Armel FAMENI","Analyste géospatial · IAC","Mer. 28 avril · 09:00"],
];
const AWARDS = ["IA & santé","IA, agriculture & sécurité alimentaire","IA, éducation & formation","IA, inclusion financière & fintech","IA & administration publique","IA & cybersécurité","IA, langues nationales, culture & industries créatives","Recherche scientifique en IA","Femme de l'année en IA","Jeune talent / Étudiant chercheur"];
const SHORT = ["Santé","Agriculture","Éducation","Fintech","Administration","Cybersécurité","Langues & culture","Recherche","Femme de l'année","Jeune talent"];
const LETTERS = ["A","B","C","D","E"];
const FAQ = [
  ["Quand et où ?","Mardi 27 et mercredi 28 avril 2027, au Hilton Hotel de Yaoundé. Le gala des Awards a lieu le soir du 28, sur invitation."],
  ["Qui peut venir ?","Tout l'écosystème : décideurs, entreprises, investisseurs, chercheurs, startups, étudiants, diaspora, curieux."],
  ["Quelles langues ?","Français et anglais."],
  ["Comment payer ?","MTN Mobile Money, Orange Money, carte bancaire ou PayPal. Nous ne demandons jamais votre code PIN."],
  ["Puis-je suivre à distance ?","Oui, avec le billet « En ligne » : direct, une masterclass avec certificat, replay 30 jours."],
  ["Comment candidater aux Awards ?","Uniquement via le formulaire en ligne, du 15 novembre 2026 au 28 février 2027 à 23:59. C'est gratuit."],
  ["Comment exposer ?","Écrivez à contact@jciacm.com pour recevoir les offres de stand. Les 50 projets présélectionnés exposent gratuitement."],
];
/* Données FICTIVES (aucune vraie personne ni organisation) */
const MM = [
  { id:"m1", name:"Startup Démo Santé",         kind:"B2B", sector:"Santé",                   seeks:"Investisseurs, hôpitaux partenaires" },
  { id:"m2", name:"Fonds Démo Impact",          kind:"B2B", sector:"Investissement",          seeks:"Startups agritech et fintech" },
  { id:"m3", name:"Ministère Démo — Numérique", kind:"B2G", sector:"Administration publique", seeks:"Solutions de dématérialisation" },
  { id:"m4", name:"Coopérative Démo Agri",      kind:"B2B", sector:"Agriculture",             seeks:"Conseil agronomique par mobile" },
  { id:"m5", name:"Commune Démo",               kind:"B2G", sector:"Collectivité",            seeks:"Outils de service aux citoyens" },
];
const SLOTS = ["15:00","15:20","15:40","16:00","16:20","16:40","17:00","17:20","17:40"];
/* Plan indicatif (le plan officiel du Hilton n'est pas publié) */
const CATS = { expo:{ n:"Exposition", c:"var(--k1)" }, conf:{ n:"Conférences", c:"var(--k2)" }, b2b:{ n:"Rencontres & VIP", c:"var(--k3)" }, master:{ n:"Masterclasses", c:"var(--k4)" }, service:{ n:"Services", c:"var(--muted)" } };
const ZONES = [
  { id:"plen",    cat:"conf",    n:"Salle plénière",              x:16,  y:14,  w:180, h:84,  d:"Cérémonie d'ouverture et plénières, retransmises en direct." },
  { id:"stage",   cat:"expo",    n:"Scène du Salon",              x:204, y:14,  w:140, h:84,  d:"Démos en continu et lightning talks des exposants." },
  { id:"village", cat:"expo",    n:"Innovation Village · Startups",x:16, y:106, w:180, h:100, d:"Stands des startups et solutions Made in Cameroon : 150+ exposants attendus." },
  { id:"b2b",     cat:"b2b",     n:"Espaces B2B / B2G",           x:204, y:106, w:140, h:46,  d:"Rendez-vous planifiés dans l'application.", go:"meet" },
  { id:"career",  cat:"b2b",     n:"AI Career Fair",              x:204, y:160, w:140, h:46,  d:"Mercredi 28 avril : recrutement." },
  { id:"m1",      cat:"master",  n:"Masterclass 1",               x:16,  y:214, w:76,  h:56,  d:"IA générative & administration publique · mer. 28, 09:00–12:00." },
  { id:"m2",      cat:"master",  n:"Masterclass 2",               x:100, y:214, w:76,  h:56,  d:"IA & santé · mer. 28, 09:00–12:00." },
  { id:"m3",      cat:"master",  n:"Masterclass 3",               x:184, y:214, w:76,  h:56,  d:"Agriculture intelligente · mer. 28, 09:00–12:00." },
  { id:"m4",      cat:"master",  n:"Masterclass 4",               x:268, y:214, w:76,  h:56,  d:"Cybersécurité & gouvernance de l'IA · mer. 28, 09:00–12:00." },
  { id:"accueil", cat:"service", n:"Accueil",                     x:16,  y:278, w:120, h:48,  d:"Retrait des badges. Mardi dès 08:00, mercredi dès 08:30." },
  { id:"vip",     cat:"b2b",     n:"Salon VIP & networking",      x:144, y:278, w:200, h:48,  d:"Déjeuners et cocktails networking, selon votre billet." },
];
const NOTIFS_SEED = [
  { id:"n1", ico:"clock",  title:"Plénière 1 dans 30 minutes", body:"Souveraineté numérique · mar. 27 avril, 12:00", when:"Il y a 2 min", go:"program", read:false },
  { id:"n2", ico:"mega",   title:"Nouveau : Women in AI Forum", body:"Mercredi 28 avril à 15:00.", when:"Il y a 1 h", go:"program", read:false },
  { id:"n3", ico:"trophy", title:"Les candidatures aux Awards ouvrent bientôt", body:"Du 15 novembre au 28 février.", when:"Hier", go:"awards", read:true },
];

/* ---------- État persisté (localement) ---------- */
const KEY = "jcia-min-v1";
const defaults = () => ({ onboarded:false, ticket:null, fav:[], req:[], votes:{}, theme:"auto", notifs:NOTIFS_SEED.map(n => ({...n})), remind:true, visual:false, interests:[], profile:null, haptics:true, sound:false, sim:null, prepDone:false });
let D = defaults();
try { const s = JSON.parse(localStorage.getItem(KEY) || "null"); if(s && typeof s === "object") D = Object.assign(defaults(), s); } catch(e) {}
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(D)); } catch(e) {} };
const S = { day:1, onlyFav:false, flow:{ step:1, id:"standard", first:"", last:"", email:"", wa:"", org:"", role:"", pay:"momo", terms:false }, mm:"sugg", plan:{ sel:null, cat:null }, vote:{ cat:0, pending:null }, bought:false };

const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c]));
const fcfa = n => n === 0 ? "Gratuit" : n.toLocaleString("fr-FR") + " FCFA";
const initials = n => n.split(" ").filter(Boolean).slice(0, 2).map(w => w[0]).join("").toUpperCase();

/* ---------- Thème : Auto (réglage du téléphone) / Nuit / Jour ---------- */
const mq = window.matchMedia ? matchMedia("(prefers-color-scheme: dark)") : null;
function applyTheme(){
  const q = qs.get("theme"), p = D.theme || "auto";
  const t = SKIN === "leger" ? "day" : (q === "day" || q === "night") ? q : (p === "auto" ? (mq && mq.matches ? "night" : "day") : p);
  document.documentElement.dataset.theme = t;
}
if(mq && mq.addEventListener) mq.addEventListener("change", applyTheme);
applyTheme();

/* ---------- Navigation ---------- */
const TABS = [["home","home","Accueil"],["program","calendar","Programme"],["ticket","ticket","Billet"],["meet","handshake","Rencontres"],["explore","compass","Explorer"]];
const TAB_OF = { home:0, program:1, ticket:2, pay:2, badge:2, meet:3, explore:4, plan:4, speakers:4, awards:4, vote:4, faq:4, contact:4, notifs:4 };
let current = "home", tabIdx = -1, lastV = null, timers = [];

function buildNav(){
  $("#nav").innerHTML = `<span class="bubble" id="bubble" aria-hidden="true"></span>` + TABS.map((t,i) =>
    `<button class="nb" style="left:${i*20}%" data-go="${t[0]}"><span class="nbi">${ic(t[1], 28)}</span><span>${t[2]}</span></button>`).join("");
}
function setTab(i){
  const nav = $("#nav"), b = $("#bubble");
  nav.querySelectorAll(".nb").forEach((el, k) => el.setAttribute("aria-current", k === i ? "page" : "false"));
  nav.style.setProperty("--i", i);
  if(i !== tabIdx){ b.innerHTML = ic(TABS[i][1], STYLE === "3d" ? 38 : 30); b.classList.remove("pop", "jelly"); void b.offsetWidth; b.classList.add("pop", "jelly"); if(tabIdx >= 0) buzz(6); }
  tabIdx = i;
}
function topbar(v){
  const unread = D.notifs.filter(n => !n.read).length;
  const bell = `<button class="iconbtn" data-go="notifs" aria-label="Notifications${unread ? `, ${unread} non lue${unread > 1 ? "s" : ""}` : ""}">${ic("bell", 24)}${unread ? `<span class="badge" aria-hidden="true">${unread}</span>` : ""}</button>`;
  const search = `<button class="iconbtn" data-search aria-label="Rechercher">${flat("search", 22)}</button>`;
  $("#top").innerHTML = v.home
    ? `<img class="logo n" src="${asset("logo")}" alt="JCIA — Journées Camerounaises de l'Intelligence Artificielle, Hilton Yaoundé, 27 et 28 avril 2027" width="150" height="65"><img class="logo d" src="${asset("logoDay")}" alt="" aria-hidden="true" width="150" height="65"><span class="spacer"></span>${search}${bell}`
    : `${v.back ? `<button class="iconbtn" data-go="${v.back}" aria-label="Retour">${flat("back", 22)}</button>` : ""}<span class="spacer"></span>${search}${bell}`;
}
function render(name, o = {}){
  current = name; timers.forEach(clearTimeout); timers = []; closeSheet(true); unbindTilt(); closeScan(); closeSearch();
  const v = V[name](); lastV = v;
  const main = $("#view"), keep = main.scrollTop;
  topbar(v);
  main.classList.toggle("noanim", o.anim === false);
  main.innerHTML = (v.title ? `<h1 class="title">${v.title}</h1>` : "") + v.html;
  if(o.anim !== false) [...main.children].forEach((el, i) => { el.style.animationDelay = Math.min(i, 8) * 50 + "ms"; });
  main.style.scrollBehavior = "auto"; main.scrollTop = o.keep ? keep : 0; main.style.scrollBehavior = "";
  setTab(TAB_OF[name] ?? 4);
  if(v.after) v.after();
  history.replaceState(null, "", location.pathname + location.search + "#" + name);
  if(!o.keep && o.anim !== false) main.focus({ preventScroll:true });
}
const again = { anim:false, keep:true };

/* ---------- Effets : vibrations, sons, confettis (réglables, coupés si « réduire les animations ») ---------- */
const REDUCED = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
const buzz = (p = 8) => { if(D.haptics && navigator.vibrate) { try { navigator.vibrate(p); } catch(e) {} } };
let actx = null;
function chime(){
  if(!D.sound) return;
  try {
    actx = actx || new (window.AudioContext || window.webkitAudioContext)();
    [523.25, 659.25, 783.99].forEach((f, i) => {
      const o = actx.createOscillator(), g = actx.createGain(), t = actx.currentTime + i * .09;
      o.type = "sine"; o.frequency.value = f; g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(.12, t + .02); g.gain.exponentialRampToValueAtTime(.0001, t + .45);
      o.connect(g); g.connect(actx.destination); o.start(t); o.stop(t + .5);
    });
  } catch(e) {}
}
const FX = { cv:null, g:null, parts:[], raf:0, k:1 };
const CONFETTI = ["#F6A343", "#2DB8BD", "#CD6035", "#9D87DC", "#ffffff"];
function burst({ x = .5, y = .4, n = 90, power = 1, sparkle = false } = {}){
  if(REDUCED) return;
  const app = $("#app"); if(!app) return;
  if(!FX.cv){ FX.cv = document.createElement("canvas"); FX.cv.className = "fx"; app.appendChild(FX.cv); FX.g = FX.cv.getContext("2d"); }
  const r = app.getBoundingClientRect(), k = Math.min(2, window.devicePixelRatio || 1);
  FX.cv.width = r.width * k; FX.cv.height = r.height * k; FX.k = k;
  const px = x <= 1 ? x * r.width : x, py = y <= 1 ? y * r.height : y;
  for(let i = 0; i < n; i++){
    const a = Math.random() * Math.PI * 2, v = (sparkle ? 2 + Math.random() * 4 : 6 + Math.random() * 9) * power;
    FX.parts.push({ x:px, y:py, vx:Math.cos(a) * v, vy:Math.sin(a) * v - (sparkle ? 1 : 5), r:Math.random() * 6, vr:(Math.random() - .5) * .4,
      w:sparkle ? 3 + Math.random() * 3 : 6 + Math.random() * 6, h:sparkle ? 3 + Math.random() * 3 : 4 + Math.random() * 5, c:sparkle ? "#F6A343" : CONFETTI[i % CONFETTI.length], life:1, round:sparkle });
  }
  if(!FX.raf) FX.raf = requestAnimationFrame(tickFx);
}
function tickFx(){
  const g = FX.g, k = FX.k; if(!g || !FX.cv){ FX.raf = 0; return; }
  g.clearRect(0, 0, FX.cv.width, FX.cv.height);
  FX.parts = FX.parts.filter(p => p.life > 0 && p.y < FX.cv.height / k + 40);
  FX.parts.forEach(p => {
    p.vy += .35; p.vx *= .99; p.x += p.vx; p.y += p.vy; p.r += p.vr; p.life -= .012;
    g.save(); g.globalAlpha = Math.max(0, p.life); g.translate(p.x * k, p.y * k); g.rotate(p.r); g.fillStyle = p.c;
    if(p.round){ g.beginPath(); g.arc(0, 0, p.w * k / 2, 0, 7); g.fill(); } else g.fillRect(-p.w * k / 2, -p.h * k / 2, p.w * k, p.h * k);
    g.restore();
  });
  if(FX.parts.length) FX.raf = requestAnimationFrame(tickFx); else { FX.raf = 0; FX.cv.remove(); FX.cv = null; }
}
function burstAt(el, o = {}){
  const r = el.getBoundingClientRect(), a = $("#app").getBoundingClientRect();
  burst(Object.assign({ x:r.left - a.left + r.width / 2, y:r.top - a.top + r.height / 2, n:16, sparkle:true, power:.8 }, o));
}
const celebrate = (msg, ico = "party", o) => { buzz([14, 40, 22]); chime(); burst(o); toast(msg, ico); };

/* ---------- Mode « En direct » : session en cours, prochaine session, accès au plan ---------- */
const SIM = { d1:{ day:1, min:12*60 + 10 }, d2:{ day:2, min:15*60 + 5 } };      // simulations pour la démonstration
function clock(){
  if(D.sim && SIM[D.sim]) return SIM[D.sim];
  const t = new Date(Date.now() + 3600e3), ymd = t.toISOString().slice(0, 10);   // Yaoundé = UTC+1
  const day = ymd === "2027-04-27" ? 1 : ymd === "2027-04-28" ? 2 : 0;
  return day ? { day, min:t.getUTCHours() * 60 + t.getUTCMinutes() } : null;
}
function liveInfo(){
  const c = clock(); if(!c) return null;
  const L = SESSIONS.filter(s => s.day === c.day && s.start != null);
  return { c, cur:L.filter(s => s.start <= c.min && c.min < s.end), next:L.find(s => s.start > c.min) };
}
const ZONE_OF_TAG = { Accueil:"accueil", Cérémonie:"plen", Salon:"village", Plénière:"plen", Networking:"vip", Clôture:"accueil", Masterclass:"m1", Talk:"plen", Pitch:"stage", Forum:"plen", Emploi:"career", Gala:"vip" };

/* ---------- Personnalisation (locale) : thèmes et profil → sessions « Pour vous » ---------- */
const INTERESTS = ["Santé","Agriculture","Éducation","Fintech","Administration","Cybersécurité","Langues & culture","Recherche"];
const PROFILES = ["Étudiant","Startup","Entreprise","Chercheur","Institution"];
const TOPICS = { "d1-4":["Langues & culture","Administration"], "d1-5":["Fintech"], "d2-0":["Administration","Santé","Agriculture","Cybersécurité"], "d2-2":["Fintech"], "d2-3":["Éducation","Recherche"], "d2-4":["Éducation","Recherche"] };
const PROFILE_PICKS = { "Étudiant":["d2-4","d2-5"], "Startup":["d2-2","d1-7"], "Entreprise":["d1-7","d2-5"], "Chercheur":["d1-4","d2-3"], "Institution":["d1-2","d1-4"] };
const forYou = s => (TOPICS[s.id] || []).some(t => D.interests.includes(t)) || (PROFILE_PICKS[D.profile] || []).includes(s.id);
const MM_TOPIC = { m1:"Santé", m2:"Fintech", m3:"Administration", m4:"Agriculture", m5:"Administration" };

/* ---------- Préparation : une checklist FINIE (elle se termine et se tait) ---------- */
function prep(){
  const steps = [
    { id:"ticket", done:!!D.ticket,           label:"Réserver mon billet",              go:"ticket",  ico:"ticket" },
    { id:"visual", done:!!D.visual,           label:"Créer mon visuel « Je serai là »", go:"badge",   ico:"camera" },
    { id:"fav",    done:D.fav.length >= 3,    label:"Choisir 3 sessions",               go:"program", ico:"star", extra:`${Math.min(3, D.fav.length)}/3` },
    { id:"meet",   done:D.req.length >= 1,    label:"Demander un rendez-vous",          go:"meet",    ico:"handshake" },
  ];
  const n = steps.filter(s => s.done).length;
  return { steps, n, total:steps.length, pct:Math.round(n / steps.length * 100) };
}
function checkPrep(){
  const p = prep();
  if(p.n === p.total && !D.prepDone){ D.prepDone = true; save(); setTimeout(() => celebrate("Vous êtes prêt pour les JCIA !", "rocket", { y:.45, n:130 }), 350); }
}

/* ---------- Calendrier (.ics) : vrai fichier, fuseau Yaoundé (UTC+1) ---------- */
function download(blob, name){
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
}
function exportICS(list, file){
  const z = n => String(n).padStart(2, "0"), dayOf = d => d === 1 ? "20270427" : "20270428";
  const utc = (d, m) => { const t = m - 60; return `${dayOf(d)}T${z(Math.floor(t / 60))}${z(t % 60)}00Z`; };
  const esc = s => String(s).replace(/[,;\\]/g, "\\$&").replace(/\n/g, "\\n");
  const ev = list.map(s => ["BEGIN:VEVENT", `UID:jcia-${s.id}@jciacm.com`, "DTSTAMP:20261102T000000Z", `DTSTART:${utc(s.day, s.start ?? 480)}`, `DTEND:${utc(s.day, s.end ?? 1080)}`,
    `SUMMARY:${esc("JCIA 2027 · " + s.title)}`, `DESCRIPTION:${esc(s.desc || s.tag)}`, "LOCATION:Hilton Hotel\\, Yaoundé", "END:VEVENT"].join("\r\n"));
  download(new Blob([["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//IAC-CAIPI//JCIA 2027//FR", "CALSCALE:GREGORIAN", ...ev, "END:VCALENDAR"].join("\r\n")], { type:"text/calendar" }), file);
}
const EVENT_DAYS = [
  { id:"event-d1", day:1, start:480, end:1080, title:"Journée 1", desc:"Ouverture officielle, plénières, Salon 100 % IA", tag:"Événement" },
  { id:"event-d2", day:2, start:510, end:1080, title:"Journée 2", desc:"Masterclasses, forums, Startup Pitch, gala", tag:"Événement" },
];

/* ---------- Billet 3D : inclinaison au doigt / au téléphone + reflet ---------- */
let tiltRaf = 0, tiltHandler = null;
function bindTilt(el){
  if(!el) return; let touched = false;
  const set = (px, py) => {
    el.style.setProperty("--ry", ((px - .5) * 20).toFixed(1) + "deg"); el.style.setProperty("--rx", ((.5 - py) * 16).toFixed(1) + "deg");
    el.style.setProperty("--mx", (px * 100).toFixed(0) + "%"); el.style.setProperty("--my", (py * 100).toFixed(0) + "%"); el.style.setProperty("--sh", (px * 100).toFixed(0));
  };
  const clamp = v => Math.min(1, Math.max(0, v));
  const move = e => { touched = true; el.classList.remove("idle"); const r = el.getBoundingClientRect(); set(clamp((e.clientX - r.left) / r.width), clamp((e.clientY - r.top) / r.height)); };
  el.addEventListener("pointermove", move); el.addEventListener("pointerdown", move);
  el.addEventListener("pointerleave", () => { touched = false; el.classList.add("idle"); });
  el.addEventListener("click", () => { if(typeof DeviceOrientationEvent !== "undefined" && DeviceOrientationEvent.requestPermission) DeviceOrientationEvent.requestPermission().catch(() => {}); }, { once:true });
  tiltHandler = e => { if(e.gamma == null || e.beta == null) return; touched = true; set(.5 + Math.max(-30, Math.min(30, e.gamma)) / 60, .5 + (Math.max(20, Math.min(80, e.beta)) - 50) / 60); };
  window.addEventListener("deviceorientation", tiltHandler);
  set(.5, .4); if(REDUCED) return;
  const loop = t => { if(!touched) set(.5 + .32 * Math.sin(t / 1300), .42 + .18 * Math.cos(t / 1700)); tiltRaf = requestAnimationFrame(loop); };
  tiltRaf = requestAnimationFrame(loop);
}
function unbindTilt(){ cancelAnimationFrame(tiltRaf); tiltRaf = 0; if(tiltHandler){ window.removeEventListener("deviceorientation", tiltHandler); tiltHandler = null; } }

/* ---------- Mode scan (QR plein écran, écran maintenu allumé) ---------- */
let scanLock = null;
function openScan(){
  if($("#scan")) return;
  const t = D.ticket, tk = TICKETS.find(x => x.id === t.id), el = document.createElement("div");
  el.className = "scan"; el.id = "scan"; el.setAttribute("role", "dialog"); el.setAttribute("aria-label", "Mode scan");
  el.innerHTML = `<button class="iconbtn" data-scanclose aria-label="Fermer">${flat("close", 22)}</button><div class="qr" role="img" aria-label="QR code fictif"></div>
    <h2>${esc((t.first + " " + t.last).trim())}</h2><p><b>${tk.name}</b> · JCIA 2027</p><p class="muted">Présentez ce code à l'entrée. Luminosité maximale conseillée.</p>`;
  $("#app").appendChild(el); buzz(10);
  try { if(navigator.wakeLock) navigator.wakeLock.request("screen").then(l => { scanLock = l; }).catch(() => {}); } catch(e) {}
}
function closeScan(){ const el = $("#scan"); if(el) el.remove(); if(scanLock){ scanLock.release().catch(() => {}); scanLock = null; } }

/* ---------- Recherche globale ---------- */
function openSearch(){
  if($("#search")) return;
  const el = document.createElement("div"); el.className = "search"; el.id = "search"; el.setAttribute("role", "dialog"); el.setAttribute("aria-label", "Recherche");
  el.innerHTML = `<div class="sbar">${flat("search", 22)}<input id="sq" type="search" placeholder="Session, intervenant, question…" aria-label="Rechercher"><button class="link" data-searchclose>Fermer</button></div><div id="sres" class="sres"></div>`;
  $("#app").appendChild(el);
  const inp = $("#sq"); inp.focus();
  const idx = [
    ...SESSIONS.map(s => ({ t:s.title, d:`${s.day === 1 ? "Mar. 27" : "Mer. 28"} · ${s.time} · ${s.tag}`, text:(s.title + s.desc + s.tag).toLowerCase(), go:"program", arg:s.day, ico:"calendar" })),
    ...SPEAKERS.map(s => ({ t:s[0], d:s[1] + " · " + s[2], text:(s[0] + s[1]).toLowerCase(), go:"speakers", arg:s[0], ico:"mic" })),
    ...FAQ.map(f => ({ t:f[0], d:f[1], text:(f[0] + f[1]).toLowerCase(), go:"faq", arg:null, ico:"help" })),
  ];
  el._idx = idx;
  const draw = () => {
    const q = inp.value.trim().toLowerCase(), r = q ? idx.filter(x => x.text.includes(q)).slice(0, 12) : [];
    $("#sres").innerHTML = !q ? `<p class="note">Cherchez une session, un intervenant ou une question.</p>`
      : r.map(x => `<button class="item" data-sres="${idx.indexOf(x)}">${ic(x.ico, 36)}<span class="grow"><b>${esc(x.t)}</b><span class="muted">${esc(x.d)}</span></span></button>`).join("") || `<p class="note">Aucun résultat pour « ${esc(inp.value.trim())} ».</p>`;
  };
  inp.addEventListener("input", draw); draw();
}
const closeSearch = () => { const el = $("#search"); if(el) el.remove(); };

/* ---------- Visuel « Je serai là » (canvas 1080×1350, photo locale uniquement) ---------- */
const BIMG = {};
const loadImg = (k, src) => BIMG[k] ? Promise.resolve(BIMG[k]) : new Promise(res => { const i = new Image(); i.onload = () => { BIMG[k] = i; res(i); }; i.onerror = () => res(null); i.src = src; });
const TCOL = { gratuit:"#2DB8BD", etudiant:"#9D87DC", standard:"#F6A343", online:"#2DB8BD", vip:"#CD6035" };
async function drawBadge(){
  const cv = $("#bcv"); if(!cv) return;
  const g = cv.getContext("2d"), W = 1080, H = 1350;
  const [logo, band] = await Promise.all([loadImg("logo", asset("logo")), loadImg("band", asset("band"))]);
  try { await document.fonts.load("800 90px Sora"); } catch(e) {}
  if(!$("#bcv")) return;
  const t = D.ticket, tk = TICKETS.find(x => x.id === (t ? t.id : "standard")), col = TCOL[tk.id];
  const name = t ? (t.first + " " + t.last).trim() : "Votre nom", sub = t ? [t.role, t.org].filter(Boolean).join(" · ") : "Votre rôle · votre organisation";
  const bg = g.createLinearGradient(0, 0, W, H); bg.addColorStop(0, "#0E1326"); bg.addColorStop(1, "#232c52"); g.fillStyle = bg; g.fillRect(0, 0, W, H);
  g.globalAlpha = .13; g.fillStyle = col; g.beginPath(); g.arc(W * .86, 230, 360, 0, 7); g.fill(); g.beginPath(); g.arc(W * .08, H * .8, 300, 0, 7); g.fill(); g.globalAlpha = 1;
  if(band) g.drawImage(band, 0, 0, W, 64);
  if(logo){ const lw = 400, lh = lw * logo.height / logo.width; g.drawImage(logo, (W - lw) / 2, 112, lw, lh); }
  const cx = W / 2, cy = 640, r = 230;
  g.fillStyle = col; g.beginPath(); g.arc(cx, cy, r + 22, 0, 7); g.fill();
  g.save(); g.beginPath(); g.arc(cx, cy, r, 0, 7); g.clip();
  if(S.photo){
    const im = S.photo.img, s = Math.max(2 * r / im.width, 2 * r / im.height) * S.photo.zoom, w = im.width * s, h = im.height * s;
    g.drawImage(im, cx - w / 2 + S.photo.ox, cy - h / 2 + S.photo.oy, w, h);
  } else {
    const pg = g.createLinearGradient(cx - r, cy - r, cx + r, cy + r); pg.addColorStop(0, "#5D4696"); pg.addColorStop(1, "#2b2f63"); g.fillStyle = pg; g.fillRect(cx - r, cy - r, 2 * r, 2 * r);
    g.fillStyle = "#fff"; g.font = "800 190px Sora, Arial, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(initials(name) || "?", cx, cy + 10);
  }
  g.restore();
  g.textBaseline = "alphabetic"; g.textAlign = "left";
  g.font = "800 104px Sora, Arial, sans-serif"; const t1 = "JE SERAI LÀ", tw = g.measureText(t1 + " !").width, x0 = cx - tw / 2;
  g.fillStyle = "#fff"; g.fillText(t1, x0, 1002); g.fillStyle = col; g.fillText(" !", x0 + g.measureText(t1).width, 1002);
  g.textAlign = "center";
  let fs = 66; g.font = `700 ${fs}px Sora, Arial, sans-serif`; while(g.measureText(name).width > 900 && fs > 34){ fs -= 2; g.font = `700 ${fs}px Sora, Arial, sans-serif`; }
  g.fillStyle = "#fff"; g.fillText(name, cx, 1090);
  fs = 40; g.font = `400 ${fs}px Sora, Arial, sans-serif`; while(g.measureText(sub).width > 900 && fs > 24){ fs -= 2; g.font = `400 ${fs}px Sora, Arial, sans-serif`; }
  g.fillStyle = "#B5BAD0"; g.fillText(sub, cx, 1150);
  const label = "27 & 28 AVRIL 2027 · HILTON YAOUNDÉ"; g.font = "700 32px Sora, Arial, sans-serif"; const lw2 = g.measureText(label).width + 70;
  g.fillStyle = col; g.beginPath(); g.roundRect ? g.roundRect(cx - lw2 / 2, 1188, lw2, 62, 31) : g.rect(cx - lw2 / 2, 1188, lw2, 62); g.fill();
  g.fillStyle = "#19203A"; g.fillText(label, cx, 1230);
  g.fillStyle = "#fff"; g.font = "700 36px Sora, Arial, sans-serif"; g.fillText("#JCIA2027", cx, 1305);
  if(band) g.drawImage(band, 0, H - 40, W, 40);
}
const badgeBlob = () => new Promise((res, rej) => { try { $("#bcv").toBlob(b => b ? res(b) : rej(new Error("vide")), "image/png"); } catch(e) { rej(e); } });
async function exportBadge(share){
  try {
    const blob = await badgeBlob(), file = new File([blob], "jcia-2027-je-serai-la.png", { type:"image/png" });
    if(share && navigator.canShare && navigator.canShare({ files:[file] })) await navigator.share({ files:[file], title:"JCIA 2027", text:"Je serai aux JCIA 2027 ! #JCIA2027" });
    else download(blob, "jcia-2027-je-serai-la.png");
    D.visual = true; save(); celebrate("Visuel prêt !", "camera"); checkPrep();
  } catch(e) {
    if(e && e.name === "AbortError") return;
    toast("Export impossible en ouverture locale : utilisez le fichier de dist/ ou un serveur.", "warning");
  }
}

/* ---------- Écrans ---------- */
const V = {};

V.home = () => {
  const t = D.ticket, li = liveInfo(), p = prep();
  const days = Math.max(0, Math.ceil((EVENT_START - Date.now()) / 864e5));
  const band = `<img class="band" src="${asset("band")}" alt="" aria-hidden="true">`;
  let hero;
  if(li){
    const cur = li.cur[0], nx = li.next;
    const pct = cur ? Math.round((li.c.min - cur.start) / (cur.end - cur.start) * 100) : 0;
    const zone = ZONE_OF_TAG[(cur || nx || {}).tag];
    hero = `<section class="hero live"><span class="livechip"><i></i>En direct · ${li.c.day === 1 ? "mardi 27" : "mercredi 28"} avril</span>
      ${cur ? `<p class="eyebrow">En ce moment</p><h2 class="nowt">${cur.title}</h2>
        <div class="bar" role="progressbar" aria-label="Avancement de la session" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}"><i style="width:${pct}%"></i></div>
        <p class="when">${cur.tag} · fin dans ${cur.end - li.c.min} min</p>` : `<p class="eyebrow">Pause</p>`}
      <p class="next">${nx ? `Ensuite · <b>${nx.time.split(" – ")[0]}</b> ${nx.title}` : "C'est la fin de la journée. Merci d'être venu !"}</p>
      ${zone ? `<button class="btn" data-where="${zone}">${flat("pin", 20)} M'y emmener</button>` : ""}${band}</section>`;
  } else {
    hero = `<section class="hero">
      <img class="map" src="${asset("map")}" alt="" width="68" height="98">
      <p class="eyebrow">Avant l'ouverture</p>
      <p class="big grad">${days}<span style="font-size:22px;font-weight:700"> jours</span></p>
      <p class="when">27 &amp; 28 avril 2027 · Hilton Hotel, Yaoundé</p>
      <button class="btn" data-go="ticket">${t ? "Voir mon billet" : "Réserver ma place"}</button>${band}</section>`;
  }
  const prepCard = p.n === p.total
    ? (D.prepDone ? `<div class="hi">${ic("rocket", 36)}<b>Vous êtes prêt pour les JCIA !</b></div>` : "")
    : `<button class="card prepc" data-prep><span class="ring" style="--p:${p.pct}"><b>${p.n}/${p.total}</b></span>
        <span class="grow"><b>Votre préparation</b><br><span class="muted">Encore ${p.total - p.n} étape${p.total - p.n > 1 ? "s" : ""} pour être prêt</span></span>${flat("chevron", 20)}</button>`;
  const fy = SESSIONS.filter(s => forYou(s) && !D.fav.includes(s.id)).slice(0, 4);
  const foryou = (D.interests.length || D.profile)
    ? (fy.length ? `<h2>Pour vous</h2><div class="chips">${fy.map(s => `<div class="fycard"><span class="stag">${s.day === 1 ? "Mar. 27" : "Mer. 28"} · ${s.time.split(" – ")[0]}</span><b>${s.title}</b>
        <button class="chipbtn" data-fav="${s.id}" aria-pressed="false" aria-label="Ajouter aux favoris : ${esc(s.title)}">${ic("star", 20)} Ajouter</button></div>`).join("")}</div>` : "")
    : `<button class="card feature" data-prefs>${ic("sparkles", 46)}<span class="grow"><b>Personnalisez votre programme</b><p>Choisissez vos thèmes : nous vous suggérons les bonnes sessions.</p></span>${flat("chevron", 20)}</button>`;
  return { home:true, html:`
    ${t ? `<p class="hello">Bonjour <span class="grad">${esc(t.first)}</span>,<br><span class="muted">bienvenue aux JCIA 2027.</span></p>` : ""}
    ${hero}
    ${prepCard}
    <h2>Accès rapide</h2>
    <div class="tiles">
      <button class="tile" data-go="program">${ic("calendar", 48)}<span><b>Programme</b><br><span class="muted">${D.fav.length ? D.fav.length + " favori" + (D.fav.length > 1 ? "s" : "") : "Deux jours de sessions"}</span></span></button>
      <button class="tile" data-go="meet">${ic("handshake", 48)}<span><b>Rencontres</b><br><span class="muted">B2B et B2G</span></span></button>
      <button class="tile" data-go="plan">${ic("map", 48)}<span><b>Plan du Salon</b><br><span class="muted">Où aller ?</span></span></button>
      <button class="tile" data-go="awards">${ic("trophy", 48)}<span><b>Awards</b><br><span class="muted">Candidater, voter</span></span></button>
    </div>
    ${foryou}
    ${li ? "" : `<h2>À la une</h2>
    <button class="card feature" data-go="awards">${ic("mega", 50)}<span class="grow"><b>Cameroon AI Awards 2027</b><p>Candidatures ouvertes du 15 novembre au 28 février. Gratuit.</p></span>${flat("chevron", 20)}</button>`}` };
};

V.program = () => {
  const mine = SESSIONS.filter(s => D.fav.includes(s.id)), li = liveInfo();
  const L = SESSIONS.filter(s => s.day === S.day && (!S.onlyFav || D.fav.includes(s.id)));
  const rows = L.map(s => {
    const on = D.fav.includes(s.id), [a, b] = s.time.split(" – "), clash = on ? mine.filter(o => overlap(s, o)) : [];
    const now = li && li.c.day === s.day && li.cur.includes(s);
    return `<div class="srow ${now ? "now" : ""}"><div class="stime">${b ? a : s.time.startsWith("Toute") ? "Jour" : a}${b ? `<small>${b}</small>` : ""}</div>
      <div class="sbody"><span class="stag">${s.tag}</span>${now ? `<span class="pill live">En cours</span>` : ""}${forYou(s) ? `<span class="pill fy">Pour vous</span>` : ""}<b>${s.title}</b>${s.desc ? `<p>${s.desc}</p>` : ""}
      ${clash.length ? `<p class="warn">${flat("warning", 16)}<span>Chevauche : ${clash.map(c => esc(c.title)).join(" ; ")}</span></p>` : ""}</div>
      <button class="fav" data-fav="${s.id}" aria-pressed="${on}" aria-label="${on ? "Retirer des" : "Ajouter aux"} favoris : ${esc(s.title)}">${ic("star", 28)}</button></div>`;
  }).join("");
  return { title:"Programme", html:`
    <div class="seg" role="group" aria-label="Jour"><button data-day="1" aria-pressed="${S.day === 1}">Mardi 27</button><button data-day="2" aria-pressed="${S.day === 2}">Mercredi 28</button></div>
    <button class="chipbtn" data-onlyfav aria-pressed="${S.onlyFav}">${ic("star", 20)} Mes favoris${mine.length ? ` (${mine.length})` : ""}</button>
    <div style="margin-top:8px">${rows || `<div class="card empty">${ic("star", 56)}<h3>Aucun favori ce jour-là</h3><p>Touchez l'étoile d'une session pour la retrouver ici.</p><button class="btn alt" data-onlyfav-off>Voir tout le programme</button></div>`}</div>
    ${mine.length ? `<button class="card switch" role="switch" aria-checked="${D.remind}" data-switch="remind" style="margin-top:14px"><span class="trk"></span><span class="grow"><b>Me prévenir 15 min avant</b><br><span class="muted">Pour vos sessions favorites</span></span></button>
      <button class="btn alt" data-ics>${flat("calendar", 20)} Ajouter mes favoris à mon calendrier</button>` : ""}`,
    after(){ const n = $(".srow.now"); if(n) n.scrollIntoView({ block:"center" }); } };
};

/* Billet : choix → informations → paiement → billet */
V.ticket = () => D.ticket ? passView() : flowView();
function flowView(){
  const f = S.flow, t = TICKETS.find(x => x.id === f.id), n = f.step;
  const bar = `<div class="steps" aria-hidden="true">${[1,2,3].map(i => `<i class="${i <= n ? "on" : ""}"></i>`).join("")}</div><p class="stepl">Étape ${n} sur 3</p>`;
  let body = "", title = "", cta = "";
  if(n === 1){
    title = "Choisissez votre billet";
    body = `<p class="note">Offre de lancement −30 % jusqu'au 31 décembre 2026</p>` + TICKETS.map(x => `
      <button class="opt" data-pick="${x.id}" aria-pressed="${x.id === f.id}"><span class="radio">${flat("check", 14)}</span>
        <span class="grow"><b>${x.name}</b>${x.reco ? `<span class="reco">Recommandé</span>` : ""}<br><span class="muted">${x.sub}</span></span>
        <span class="price">${x.old ? `<s>${x.old.toLocaleString("fr-FR")}</s>` : ""}${x.price ? x.price.toLocaleString("fr-FR") + " F" : "Gratuit"}</span></button>`).join("");
    cta = `<button class="btn" data-step="1">Continuer</button>`;
  } else if(n === 2){
    title = "Vos informations";
    const fld = (id, lab, type, val, ac) => `<label for="${id}">${lab}</label><input id="${id}" type="${type}" value="${esc(val)}" autocomplete="${ac}">`;
    body = `<p class="muted" style="margin-top:-8px">Elles figurent sur votre billet.</p>` + fld("f1","Prénom","text",f.first,"given-name") + fld("f2","Nom","text",f.last,"family-name") + fld("f3","E-mail","email",f.email,"email")
      + fld("f4","WhatsApp (6XX XX XX XX ou +44…)","tel",f.wa,"tel") + fld("f5","Organisation","text",f.org,"organization") + fld("f6","Rôle","text",f.role,"organization-title");
    cta = `<button class="btn" data-step="1">Continuer</button><button class="btn alt" data-step="-1">Retour</button>`;
  } else {
    title = t.price ? "Paiement" : "Confirmation";
    body = `<div class="card row">${ic("ticket", 44)}<span class="grow"><b>Billet ${t.name}</b><br><span class="muted">${esc(f.first)} ${esc(f.last)}</span></span><b>${fcfa(t.price)}</b></div>
      ${t.price ? `<h2 style="margin-top:6px">Moyen de paiement</h2>
        <button class="opt" data-pay="momo" aria-pressed="${f.pay === "momo"}"><span class="radio">${flat("check", 14)}</span>${ic("mobile", 34)}<span class="grow"><b>Mobile Money</b><br><span class="muted">MTN ou Orange · approbation sur votre téléphone</span></span></button>
        <button class="opt" data-pay="card" aria-pressed="${f.pay === "card"}"><span class="radio">${flat("check", 14)}</span>${ic("card", 34)}<span class="grow"><b>Carte ou PayPal</b><br><span class="muted">Page de paiement sécurisée</span></span></button>` : ""}
      <label class="check"><input type="checkbox" id="c1" ${f.terms ? "checked" : ""}><span>J'accepte les conditions d'utilisation et la politique de confidentialité.</span></label>`;
    cta = `<button class="btn" id="go" data-step="1" ${f.terms ? "" : "disabled"}>${t.price ? "Payer " + fcfa(t.price) : "Confirmer"}</button><button class="btn alt" data-step="-1">Retour</button>`;
  }
  return { title, html: bar + body + `<div class="cta">${cta}</div>`, after(){ bindFlow(); } };
}
function bindFlow(){
  const f = S.flow, map = { f1:"first", f2:"last", f3:"email", f4:"wa", f5:"org", f6:"role" };
  Object.entries(map).forEach(([id, k]) => { const el = $("#" + id); if(el) el.oninput = () => f[k] = el.value; });
  const c = $("#c1"); if(c) c.onchange = () => { f.terms = c.checked; $("#go").disabled = !f.terms; };
}
function passView(){
  const t = D.ticket, tk = TICKETS.find(x => x.id === t.id);
  return { title:"Mon billet", html:`
    ${S.bought ? `<div class="hi pop">${ic("party", 40)}<b>Billet confirmé. À bientôt à Yaoundé !</b></div>` : ""}
    <div class="pass3d"><div class="pass" id="pass"><div class="head">${ic("ticket", 44)}<span><b>JCIA 2027 · ${tk.name}</b><small>27 &amp; 28 avril · Hilton Yaoundé</small></span></div>
      <div class="cut"></div>
      <div class="body"><div class="qr" role="img" aria-label="QR code fictif"></div><h3>${esc((t.first + " " + t.last).trim() || "Participant Exemple")}</h3><p class="muted">${esc(t.role || "")}${t.role && t.org ? " · " : ""}${esc(t.org || "")}</p></div></div></div>
    <p class="note">Inclinez votre téléphone ou glissez le doigt sur le billet.</p>
    <button class="btn" data-go="badge">${flat("camera", 20)} Créer mon visuel « Je serai là »</button>
    <div class="stack" style="margin-top:12px">
      <button class="btn alt" data-scan>${flat("ticket", 20)} Mode scan (QR en grand)</button>
      <button class="btn alt" data-ics-event>${flat("calendar", 20)} Ajouter à mon calendrier</button></div>
    <p class="note" style="margin-top:16px">Maquette : billet fictif, aucun paiement ni e-mail.</p>`,
    after(){ bindTilt($("#pass")); } };
}

V.badge = () => ({ title:"Mon visuel", back:"ticket", html:`
  <p class="sub">Annoncez votre venue sur vos réseaux. Votre photo reste sur votre téléphone : elle n'est ni envoyée ni enregistrée.</p>
  ${D.ticket ? "" : `<div class="notice">Aperçu : réservez votre billet pour y afficher votre nom.</div>`}
  <canvas id="bcv" class="bcv" width="1080" height="1350" role="img" aria-label="Aperçu de votre visuel « Je serai là »"></canvas>
  <label class="btn alt filebtn" for="bfile">${flat("camera", 20)} <span>${S.photo ? "Changer ma photo" : "Ajouter ma photo"}</span></label>
  <input id="bfile" type="file" accept="image/*" class="sr">
  <div id="zoomrow" ${S.photo ? "" : "hidden"}><label for="bzoom">Zoom (glissez la photo pour la recadrer)</label><input id="bzoom" type="range" min="1" max="3" step="0.05" value="${S.photo ? S.photo.zoom : 1}"></div>
  <div class="cta"><button class="btn" data-bshare>${flat("share", 20)} Partager</button><button class="btn alt" data-bdl>Télécharger l'image</button></div>`,
  after(){
    drawBadge();
    $("#bfile").addEventListener("change", e => {
      const f = e.target.files && e.target.files[0]; if(!f) return;
      const rd = new FileReader();
      rd.onload = () => { const im = new Image(); im.onload = () => { S.photo = { img:im, zoom:1, ox:0, oy:0 }; $("#zoomrow").hidden = false; $("#bzoom").value = 1; drawBadge(); buzz(); }; im.src = rd.result; };
      rd.readAsDataURL(f);
    });
    $("#bzoom").addEventListener("input", e => { if(S.photo){ S.photo.zoom = +e.target.value; drawBadge(); } });
    const cv = $("#bcv"); let drag = null;
    cv.addEventListener("pointerdown", e => { if(!S.photo) return; drag = { x:e.clientX, y:e.clientY, ox:S.photo.ox, oy:S.photo.oy }; cv.setPointerCapture(e.pointerId); });
    cv.addEventListener("pointermove", e => { if(!drag) return; const k = 1080 / cv.getBoundingClientRect().width; S.photo.ox = drag.ox + (e.clientX - drag.x) * k; S.photo.oy = drag.oy + (e.clientY - drag.y) * k; drawBadge(); });
    cv.addEventListener("pointerup", () => { drag = null; });
  } });

V.pay = () => {
  const f = S.flow, t = TICKETS.find(x => x.id === f.id);
  return { title:"Paiement", html:`<div class="card empty"><div class="spinner" role="progressbar" aria-label="Paiement en cours"></div>
    <h3>En attente de votre validation</h3><p>${f.pay === "momo" ? `Une demande de ${fcfa(t.price)} a été envoyée sur votre téléphone. Approuvez-la pour confirmer.` : "Redirection vers la page de paiement sécurisée…"}</p>
    <p class="muted">Simulation : confirmation automatique dans quelques secondes.</p></div><button class="btn alt" data-go="ticket">Annuler</button>`,
    after(){ timers.push(setTimeout(() => { if(current === "pay") createTicket(); }, 2600)); } };
};
function createTicket(){
  const f = S.flow;
  D.ticket = { id:f.id, first:f.first, last:f.last, email:f.email, wa:f.wa, org:f.org, role:f.role };
  D.notifs.unshift({ id:"n" + Date.now(), ico:"ticket", title:"Votre billet est confirmé", body:"Présentez votre QR code à l'entrée du Hilton.", when:"À l'instant", go:"ticket", read:false });
  save(); S.bought = true; render("ticket"); S.bought = false; celebrate("Billet confirmé !", "party", { y:.35, n:120 }); checkPrep();
}

V.meet = () => {
  const reqs = [...D.req].sort((a, b) => a.slot.localeCompare(b.slot));
  const match = p => D.interests.includes(MM_TOPIC[p.id]) ? 1 : 0;
  const seg = `<div class="seg" role="group" aria-label="Rencontres"><button data-mm="sugg" aria-pressed="${S.mm === "sugg"}">Suggestions</button><button data-mm="mine" aria-pressed="${S.mm === "mine"}">Mes rendez-vous${reqs.length ? ` (${reqs.length})` : ""}</button></div>`;
  let body;
  if(S.mm === "sugg"){
    body = `<p class="sub">Proposez un rendez-vous de 20 minutes. ${D.interests.length ? "Les profils proches de vos thèmes apparaissent en premier." : ""} Exemples fictifs.</p>`
      + [...MM].sort((a, b) => match(b) - match(a)).map(p => { const done = D.req.some(r => r.pid === p.id); return `
      <div class="card"><div class="row"><div class="avatar">${initials(p.name)}</div><div class="grow"><h3>${p.name}</h3><p class="muted">${p.sector}</p></div><span class="pill ${p.kind === "B2G" ? "v" : "o"}">${p.kind}</span></div>
        ${match(p) ? `<p class="stag" style="margin-top:10px">${flat("sparkles", 14)} Correspond à votre thème « ${MM_TOPIC[p.id]} »</p>` : ""}
        <p class="muted" style="margin:10px 0 14px">Recherche : ${p.seeks}</p>
        <button class="btn alt" data-req="${p.id}" ${done ? "disabled" : ""}>${done ? "Demande envoyée" : "Proposer un rendez-vous"}</button></div>`; }).join("");
  } else if(!reqs.length){
    body = `<div class="card empty">${ic("handshake", 64)}<h3>Aucun rendez-vous</h3><p>Choisissez un profil et un créneau.</p><button class="btn alt" data-mm="sugg">Voir les suggestions</button></div>`;
  } else {
    body = reqs.map(r => { const p = MM.find(x => x.id === r.pid), ok = r.status === "ok"; return `
      <div class="card"><div class="row"><div class="avatar">${initials(p.name)}</div><div class="grow"><h3>${p.name}</h3><p class="muted">Mar. 27 avril · ${r.slot} · Espace B2B / B2G</p></div>
        <span class="pill ${ok ? "o" : ""}">${ok ? "Confirmé" : "En attente"}</span></div>
        <div class="row" style="margin-top:6px"><button class="link" data-where="b2b">${flat("pin", 16)} Où ?</button><span class="grow"></span><button class="link" data-cancel="${r.id}">Annuler</button></div></div>`; }).join("");
  }
  return { title:"Rencontres", html: seg + body };
};

function scheduleConfirm(r){
  setTimeout(() => {
    const x = D.req.find(q => q.id === r.id); if(!x || x.status !== "wait") return;
    x.status = "ok"; const p = MM.find(q => q.id === x.pid);
    D.notifs.unshift({ id:"n" + Date.now(), ico:"handshake", title:"Rendez-vous confirmé", body:`${p.name} · mar. 27 avril, ${x.slot}`, when:"À l'instant", go:"meet", read:false });
    save(); if(current === "meet") render("meet", again); else topbar(lastV); celebrate("Rendez-vous confirmé", "handshake", { y:.4, n:60 });
  }, 3500);
}
D.req.filter(r => r.status === "wait").forEach(scheduleConfirm);

V.explore = () => {
  const unread = D.notifs.filter(n => !n.read).length, voted = Object.keys(D.votes).length;
  const it = (go, ico, label, sub) => `<button class="item" data-go="${go}">${ic(ico, 44)}<span class="grow"><b>${label}</b><span class="muted">${sub}</span></span>${flat("chevron", 18)}</button>`;
  const sw = (k, label, sub) => `<button class="switch" role="switch" aria-checked="${!!D[k]}" data-switch="${k}"><span class="trk"></span><span class="grow"><b>${label}</b><br><span class="muted">${sub}</span></span></button>`;
  return { title:"Explorer", html:`
    <div class="list">
      ${it("plan","map","Plan du Salon","Stands, salles, accueil")}
      ${it("speakers","mic","Intervenants","40+ voix de haut niveau")}
      ${it("awards","trophy","Awards","Candidater · voter (" + voted + "/10)")}
      ${it("faq","help","Questions fréquentes","Billets, paiement, accès")}
      ${it("contact","phone","Contact","Le secrétariat")}
      ${it("notifs","bell","Notifications", unread ? unread + " non lue" + (unread > 1 ? "s" : "") : "Tout est lu")}
    </div>
    <h2>Pour vous</h2>
    <div class="card stack">
      <button class="item" data-prefs style="box-shadow:none;padding:4px 0;min-height:56px">${ic("sparkles", 40)}<span class="grow"><b>Mes thèmes</b><span class="muted">${D.interests.length ? D.interests.join(", ") : "Aucun thème choisi"}${D.profile ? " · " + D.profile : ""}</span></span>${flat("chevron", 18)}</button>
      ${sw("haptics", "Vibrations", "Un léger retour au toucher")}
      ${sw("sound", "Sons", "Un petit carillon lors des réussites")}
    </div>
    ${SKIN === "leger" ? "" : `<h2>Apparence</h2>
    <div class="seg" role="group" aria-label="Apparence">${[["auto","Auto"],["night","Nuit"],["day","Jour"]].map(x => `<button data-th="${x[0]}" aria-pressed="${D.theme === x[0]}">${x[0] === "night" ? flat("moon", 18) : x[0] === "day" ? flat("sun", 18) : ""} ${x[1]}</button>`).join("")}</div>`}
    ${window.JCIA_ICONS_FIXED ? "" : `<div class="seg" role="group" aria-label="Style d'icônes"><button data-icons="3d" aria-pressed="${STYLE === "3d"}">Icônes 3D</button><button data-icons="flat" aria-pressed="${STYLE === "flat"}">Icônes plates</button></div>`}
    <h2>Mode démonstration</h2>
    <p class="sub" style="margin-top:-6px">Pour présenter l'app : simulez l'événement en cours.</p>
    <div class="seg" role="group" aria-label="Simulation">${[["none","Aujourd'hui"],["d1","Mar. 12:10"],["d2","Mer. 15:05"]].map(x => `<button data-sim="${x[0]}" aria-pressed="${(D.sim || "none") === x[0]}">${x[1]}</button>`).join("")}</div>
    <button class="link" data-reset>Réinitialiser la démonstration</button>
    <p class="note" style="margin-top:6px">Icônes 3D : Fluent Emoji (Microsoft), licence MIT.</p>` };
};

V.plan = () => {
  const p = S.plan, sel = ZONES.find(z => z.id === p.sel);
  const svg = `<svg class="plan ${p.cat ? "dim" : ""}" viewBox="0 0 360 340" role="group" aria-label="Plan indicatif du Hilton Yaoundé">${ZONES.map(z => `
    <g class="z ${p.cat && z.cat === p.cat ? "on" : ""} ${z.id === p.sel ? "sel" : ""}" data-zone="${z.id}" role="button" tabindex="0" aria-label="${esc(z.n)}" aria-pressed="${z.id === p.sel}" style="--c:${CATS[z.cat].c}">
      <rect x="${z.x}" y="${z.y}" width="${z.w}" height="${z.h}" rx="12" style="fill:var(--c);stroke:var(--c)"/><text x="${z.x + z.w / 2}" y="${z.y + z.h / 2}" text-anchor="middle" dominant-baseline="middle">${esc(z.n)}</text></g>`).join("")}
    <g class="here" aria-hidden="true"><circle class="pulse" cx="28" cy="288" r="5.5"/><circle cx="28" cy="288" r="5.5"/></g></svg>`;
  return { title:"Plan du Salon", back:"explore", html:`
    <div class="notice">Plan <b>indicatif</b> : le plan officiel du Hilton n'est pas encore publié. L'agencement est fictif.</div>
    <div class="chips" role="group" aria-label="Filtrer">${Object.entries(CATS).filter(([k]) => k !== "service").map(([k, v]) => `<button class="chipbtn" data-plancat="${k}" aria-pressed="${p.cat === k}"><i style="width:10px;height:10px;border-radius:3px;background:${v.c};display:inline-block"></i>${v.n}</button>`).join("")}</div>
    ${svg}
    ${sel ? `<div class="card" style="border-top:5px solid ${CATS[sel.cat].c}"><h3>${esc(sel.n)}</h3><p class="muted" style="margin-top:4px">${esc(sel.d)}</p>${sel.go ? `<button class="btn alt" style="margin-top:12px" data-go="${sel.go}">Planifier mes rendez-vous</button>` : ""}</div>` : `<p class="note">Touchez une zone pour voir ce qu'elle accueille.</p>`}` };
};

V.speakers = () => ({ title:"Intervenants", back:"explore", html:`
  <input type="search" id="q" placeholder="Rechercher" aria-label="Rechercher un intervenant" value="${esc(S.q || "")}"><div id="sl" style="margin-top:12px"></div>`,
  after(){
    const draw = () => { const q = $("#q").value.trim().toLowerCase(); const r = SPEAKERS.filter(s => (s[0] + s[1]).toLowerCase().includes(q));
      $("#sl").innerHTML = r.map(s => `<div class="card row"><div class="avatar">${initials(s[0])}</div><div class="grow"><h3>${s[0]}</h3><p class="muted">${s[1]}</p><p class="muted" style="color:var(--acc)">${s[2]}</p></div></div>`).join("") || `<p class="note">Aucun résultat.</p>`; };
    $("#q").addEventListener("input", draw); draw();
  } });

V.awards = () => ({ title:"Awards", back:"explore", html:`
  <div class="card row">${ic("trophy", 64)}<span class="grow"><h3>Cameroon AI Awards 2027</h3><p class="muted">Candidatures du 15 novembre 2026 au 28 février 2027, 23:59. Gratuit.</p></span></div>
  <button class="btn" data-stub="Ouvre le formulaire de candidature">Candidater</button>
  <div class="stack" style="margin-top:12px"><button class="btn alt" data-go="vote">${ic("heart", 24)} Voir le vote du public</button></div>
  <h2>Comment ça marche</h2>
  <div class="card stack"><div class="row">${ic("check", 32)}<span><b>1. Candidature</b><br><span class="muted">Jusqu'au 28 février</span></span></div>
    <div class="row">${ic("star", 32)}<span><b>2. 50 présélectionnés</b><br><span class="muted">Publiés le 15 mars</span></span></div>
    <div class="row">${ic("heart", 32)}<span><b>3. Vote du public (40 %)</b><br><span class="muted">20 mars → 15 avril</span></span></div>
    <div class="row">${ic("trophy", 32)}<span><b>4. Jury (60 %) et gala</b><br><span class="muted">28 avril 2027</span></span></div></div>
  <h2>Dix catégories</h2>
  <div class="card stack">${AWARDS.map((a, i) => `<div class="row"><span class="pill">${String(i + 1).padStart(2, "0")}</span><span>${a}</span></div>`).join("")}</div>` });

V.vote = () => {
  const c = S.vote.cat, done = Object.keys(D.votes).length, chosen = D.votes[c];
  return { title:"Vote du public", back:"awards", html:`
    <div class="notice">Aperçu : <b>finalistes fictifs</b>. Vote officiel du 20 mars au 15 avril 2027. Règles à confirmer.</div>
    <div class="card"><div class="row"><b class="grow">Votre participation</b><b>${done} / 10</b></div><div class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="10" aria-valuenow="${done}"><i style="width:${done * 10}%"></i></div></div>
    <div class="chips" role="group" aria-label="Catégories">${SHORT.map((s, i) => `<button class="chipbtn" data-votecat="${i}" aria-pressed="${i === c}">${D.votes[i] ? flat("check", 16) : ""}${s}</button>`).join("")}</div>
    <h2 style="margin-top:0">${AWARDS[c]}</h2>
    ${LETTERS.map(l => { const id = c + "-" + l, mine = chosen === id; return `<div class="card"><div class="row"><div class="avatar">${l}</div><div class="grow"><h3>Projet exemple ${l}</h3><p class="muted">Description fictive d'un projet finaliste.</p></div></div>
      <button class="btn ${mine ? "" : "alt"}" style="margin-top:14px" data-vote="${id}" ${mine ? "disabled" : ""}>${mine ? "Votre vote" : "Voter"}</button></div>`; }).join("")}` };
};

V.faq = () => ({ title:"Questions", back:"explore", html: FAQ.map(f => `<details><summary>${f[0]}</summary><p>${f[1]}</p></details>`).join("") + `<button class="btn alt" data-go="contact" style="margin-top:6px">Une autre question ?</button>` });

V.contact = () => ({ title:"Contact", back:"explore", html:`
  <div class="list">
    <a class="item" href="tel:+237699089937">${ic("phone", 44)}<span class="grow"><b>+237 699 089 937</b><span class="muted">WhatsApp</span></span></a>
    <a class="item" href="tel:+237677238022">${ic("phone", 44)}<span class="grow"><b>+237 677 238 022</b><span class="muted">Secrétariat</span></span></a>
    <a class="item" href="tel:+237222306079">${ic("phone", 44)}<span class="grow"><b>+237 222 306 079</b><span class="muted">Secrétariat</span></span></a>
    <a class="item" href="mailto:contact@jciacm.com">${ic("mail", 44)}<span class="grow"><b>contact@jciacm.com</b><span class="muted">Écrivez-nous</span></span></a>
    <a class="item" href="https://www.google.com/maps/search/?api=1&query=Hilton+Hotel+Yaound%C3%A9" target="_blank" rel="noopener">${ic("pin", 44)}<span class="grow"><b>Hilton Hotel, Yaoundé</b><span class="muted">Mardi 08:00–18:00 · mercredi 08:30–18:00</span></span></a>
  </div><p class="note" style="margin-top:16px">Rond-point Cami-Toyota, Coron, Immeuble Dangote, 2ᵉ étage, Yaoundé</p>` });

V.notifs = () => {
  const unread = D.notifs.filter(n => !n.read).length;
  return { title:"Notifications", back:"explore", html:`
    ${unread ? `<div class="row" style="margin-bottom:12px"><span class="muted grow">${unread} non lue${unread > 1 ? "s" : ""} · exemples fictifs</span><button class="link" data-readall>Tout marquer comme lu</button></div>` : `<p class="sub">Tout est lu · exemples fictifs</p>`}
    ${D.notifs.map(n => `<button class="notif ${n.read ? "" : "unread"}" data-notif="${n.id}">${ic(n.ico, 40)}<span class="grow"><span class="t">${esc(n.title)}</span><br><span class="muted">${esc(n.body)}</span><br><small class="muted">${esc(n.when)}</small></span>${n.read ? "" : `<span class="dot" aria-hidden="true"></span><span class="sr">Non lue</span>`}</button>`).join("")}
    <h2>Préférences</h2>
    <button class="card switch" role="switch" aria-checked="${D.remind}" data-switch="remind"><span class="trk"></span><span class="grow"><b>Rappels de sessions</b><br><span class="muted">15 minutes avant vos favoris</span></span></button>
    <p class="note">Dans l'app réelle, l'autorisation de notifications push est demandée au premier lancement.</p>` };
};

/* ---------- Feuille du bas, toast ---------- */
let sheetNodes = null, sheetOpener = null;
function openSheet(html){
  closeSheet(true); sheetOpener = document.activeElement;
  const back = document.createElement("div"); back.className = "sheet-back"; back.addEventListener("click", () => closeSheet());
  const sh = document.createElement("div"); sh.className = "sheet"; sh.tabIndex = -1; sh.setAttribute("role", "dialog"); sh.setAttribute("aria-modal", "true");
  sh.innerHTML = `<div class="grab"></div>` + html; $("#app").append(back, sh); sheetNodes = [back, sh]; sh.focus();
}
function closeSheet(silent){
  if(!sheetNodes) return; sheetNodes.forEach(n => n.remove()); sheetNodes = null;
  if(!silent && sheetOpener && sheetOpener.isConnected) { try { sheetOpener.focus(); } catch(e) {} }
}
function toast(msg, ico = "check"){
  let n = $("#toast"); if(!n){ n = document.createElement("div"); n.id = "toast"; n.className = "toast"; n.setAttribute("role", "status"); $("#app").appendChild(n); }
  n.innerHTML = `${ic(ico, 24)}<span>${esc(msg)}</span>`; n.classList.remove("show"); void n.offsetWidth; n.classList.add("show");
  clearTimeout(n._t); n._t = setTimeout(() => n.classList.remove("show"), 2800);
}

/* ---------- Actions ---------- */
document.addEventListener("click", e => {
  const a = e.target.closest("[data-go],[data-day],[data-fav],[data-onlyfav],[data-onlyfav-off],[data-switch],[data-pick],[data-pay],[data-step],[data-mm],[data-req],[data-slot],[data-send],[data-cancel],[data-zone],[data-plancat],[data-votecat],[data-vote],[data-voteok],[data-close],[data-notif],[data-readall],[data-th],[data-icons],[data-reset],[data-stub],[data-ob],[data-search],[data-searchclose],[data-sres],[data-scan],[data-scanclose],[data-prefs],[data-prep],[data-where],[data-sim],[data-ics],[data-ics-event],[data-bshare],[data-bdl],[data-int],[data-prof]");
  if(!a) return; const d = a.dataset;

  if(d.stub){ e.preventDefault(); toast("Maquette — " + d.stub, "bulb"); return; }
  if(d.ob !== undefined) return obAction(d.ob);
  if(d.int){ const L = S.pick.interests, i = L.indexOf(d.int); if(i < 0 && L.length >= 4) return toast("4 thèmes au maximum", "warning"); i < 0 ? L.push(d.int) : L.splice(i, 1); a.setAttribute("aria-pressed", String(i < 0)); return buzz(6); }
  if(d.prof){ S.pick.profile = S.pick.profile === d.prof ? null : d.prof; document.querySelectorAll("[data-prof]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.prof === S.pick.profile))); return buzz(6); }
  if("search" in d) return openSearch();
  if("searchclose" in d) return closeSearch();
  if(d.sres !== undefined){ const it = $("#search")._idx[+d.sres]; closeSearch(); if(it.go === "program"){ S.day = it.arg; S.onlyFav = false; } if(it.go === "speakers") S.q = it.arg; return render(it.go); }
  if("scan" in d) return openScan();
  if("scanclose" in d) return closeScan();
  if("prefs" in d) return showOnboarding(3, true);
  if("prep" in d) return openPrep();
  if(d.where){ S.plan.sel = d.where; S.plan.cat = null; buzz(); return render("plan"); }
  if(d.sim){ D.sim = d.sim === "none" ? null : d.sim; save(); render(current, again); return toast(D.sim ? "Simulation : l'accueil passe en direct" : "Simulation désactivée", "clock"); }
  if("ics" in d){ exportICS(SESSIONS.filter(s => D.fav.includes(s.id)), "jcia-2027-mes-favoris.ics"); return toast("Fichier calendrier téléchargé", "calendar"); }
  if("icsEvent" in d){ exportICS(EVENT_DAYS, "jcia-2027.ics"); return toast("Fichier calendrier téléchargé", "calendar"); }
  if("bshare" in d) return exportBadge(true);
  if("bdl" in d) return exportBadge(false);
  if(d.go){ if(d.go === "ticket") S.bought = false; return render(d.go); }
  if(d.day){ S.day = +d.day; return render("program", again); }
  if("onlyfav" in d){ S.onlyFav = !S.onlyFav; return render("program", again); }
  if("onlyfavOff" in d){ S.onlyFav = false; return render("program", again); }
  if(d.fav){
    const i = D.fav.indexOf(d.fav), add = i < 0; add ? D.fav.push(d.fav) : D.fav.splice(i, 1); save();
    if(add){ burstAt(a); buzz(); }
    toast(add ? "Ajouté à vos favoris" : "Retiré de vos favoris", "star"); render(current, again);
    const b = document.querySelector(`[data-fav="${d.fav}"]`); if(b) b.focus(); return checkPrep();
  }
  if(d.switch){ D[d.switch] = !D[d.switch]; save(); a.setAttribute("aria-checked", String(D[d.switch])); return; }

  const f = S.flow;
  if(d.pick){ f.id = d.pick; return render("ticket", again); }
  if(d.pay){ f.pay = d.pay; return render("ticket", again); }
  if(d.step){
    const dir = +d.step;
    if(dir < 0){ f.step = Math.max(1, f.step - 1); return render("ticket", { anim:false }); }
    if(f.step === 2){
      if(![f.first, f.last, f.email, f.wa, f.org, f.role].every(v => v.trim())) return toast("Merci de remplir tous les champs.", "warning");
      if(!/^\S+@\S+\.\S+$/.test(f.email)) return toast("Adresse e-mail invalide.", "warning");
    }
    if(f.step === 3){ const t = TICKETS.find(x => x.id === f.id); if(t.price) return render("pay"); return createTicket(); }
    f.step++; return render("ticket", { anim:false });
  }

  if(d.mm){ S.mm = d.mm; return render("meet", again); }
  if(d.req){
    const p = MM.find(x => x.id === d.req), taken = D.req.map(r => r.slot); S.mmPid = p.id; S.mmSlot = null;
    return openSheet(`<h3>Rendez-vous avec ${esc(p.name)}</h3><p class="muted" style="margin-top:6px">20 minutes · Espace B2B / B2G, mardi 27 avril. Les créneaux du mercredi seront communiqués ultérieurement.</p>
      <div class="slots">${SLOTS.map(t => `<button class="chipbtn" data-slot="${t}" aria-pressed="false" ${taken.includes(t) ? "disabled" : ""}>${t}</button>`).join("")}</div>
      <div class="stack" style="margin-top:22px"><button class="btn" id="sendbtn" data-send disabled>Envoyer la demande</button><button class="btn alt" data-close>Annuler</button></div>`);
  }
  if(d.slot){ S.mmSlot = d.slot; sheetNodes[1].querySelectorAll("[data-slot]").forEach(b => b.setAttribute("aria-pressed", String(b === a))); $("#sendbtn").disabled = false; return; }
  if("send" in d){
    const r = { id:"r" + Date.now(), pid:S.mmPid, slot:S.mmSlot, status:"wait" }; D.req.push(r); save(); closeSheet(true); scheduleConfirm(r);
    S.mm = "mine"; render("meet", { anim:false }); toast("Demande envoyée", "handshake"); return checkPrep();
  }
  if(d.cancel){ D.req = D.req.filter(r => r.id !== d.cancel); save(); toast("Demande annulée", "check"); return render("meet", again); }

  if(d.zone){ S.plan.sel = S.plan.sel === d.zone ? null : d.zone; render("plan", again); const n = document.querySelector(`[data-zone="${d.zone}"]`); if(n && e.detail === 0) n.focus(); return; }
  if(d.plancat){ S.plan.cat = S.plan.cat === d.plancat ? null : d.plancat; return render("plan", again); }

  if(d.votecat){ S.vote.cat = +d.votecat; return render("vote", again); }
  if(d.vote){
    const [c, l] = d.vote.split("-"); S.vote.pending = d.vote;
    return openSheet(`<h3>Confirmer votre vote ?</h3><p class="muted" style="margin:6px 0 22px">Catégorie « ${esc(SHORT[+c])} » · Projet exemple ${esc(l)}. Modifiable jusqu'à la clôture (règle à confirmer).</p>
      <div class="stack"><button class="btn" data-voteok>Confirmer</button><button class="btn alt" data-close>Annuler</button></div>`);
  }
  if("voteok" in d){ D.votes[+S.vote.pending.split("-")[0]] = S.vote.pending; save(); closeSheet(true); render("vote", again); burst({ y:.5, n:40, power:.7 }); buzz([10, 30, 10]); return toast("Vote enregistré", "heart"); }
  if("close" in d) return closeSheet();

  if(d.notif){ const n = D.notifs.find(x => x.id === d.notif); if(n){ n.read = true; save(); } return render(n && V[n.go] ? n.go : current); }
  if("readall" in d){ D.notifs.forEach(n => n.read = true); save(); return render("notifs", again); }
  if(d.th){ D.theme = d.th; save(); applyTheme(); return render(current, again); }
  if(d.icons){ const u = new URL(location.href); u.searchParams.set("icons", d.icons); u.hash = "#explore"; location.href = u.toString(); return; }
  if("reset" in d){ S.photo = null; D = defaults(); save(); applyTheme(); S.flow = { step:1, id:"standard", first:"", last:"", email:"", wa:"", org:"", role:"", pay:"momo", terms:false }; render(current, again); return toast("Démonstration réinitialisée", "check"); }
});
document.addEventListener("keydown", e => {
  if(e.key === "Escape"){ closeSheet(); closeScan(); closeSearch(); }
  const z = e.target.closest && e.target.closest("[data-zone][role=button]");
  if(z && (e.key === "Enter" || e.key === " ")){ e.preventDefault(); z.dispatchEvent(new MouseEvent("click", { bubbles:true })); }
  if(e.key === "Tab" && sheetNodes){
    const f = [...sheetNodes[1].querySelectorAll("button:not([disabled]),a[href],input,select")]; if(!f.length) return;
    const first = f[0], last = f[f.length - 1], cur = document.activeElement;
    if(e.shiftKey && (cur === first || cur === sheetNodes[1])){ e.preventDefault(); last.focus(); } else if(!e.shiftKey && cur === last){ e.preventDefault(); first.focus(); }
  }
});

/* ---------- Écrans d'accueil (3 étapes + choix des thèmes) ---------- */
const OB = [
  { c:"#F6A343", ico:["rocket","sparkles","robot"],      t:"Bienvenue aux <em>JCIA 2027</em>",         p:"Les Journées camerounaises de l'IA, les 27 et 28 avril au Hilton Yaoundé.", cta:"Continuer" },
  { c:"#2DB8BD", ico:["calendar","star","clock"],        t:"Composez <em>votre</em> programme",        p:"Mettez vos sessions en favori. Nous vous prévenons avant qu'elles commencent.", cta:"Continuer" },
  { c:"#5D4696", ico:["handshake","briefcase","ticket"], t:"Rencontrez les <em>bonnes</em> personnes", p:"Planifiez vos rendez-vous B2B et B2G, et gardez votre billet à portée de main.", cta:"Continuer" },
  { c:"#CD6035", ico:["brain","bulb","sparkles"], prefs:true, t:"Qu'est-ce qui vous <em>intéresse</em> ?", p:"Choisissez jusqu'à 4 thèmes : nous vous suggérerons les bonnes sessions et rencontres.", cta:"Commencer" },
];
let obI = 0, obOnly = false;
function showOnboarding(startAt = 0, only = false){
  if($("#ob")) return;
  obI = startAt; obOnly = only; S.pick = { interests:[...D.interests], profile:D.profile };
  const el = document.createElement("div"); el.className = "ob"; el.id = "ob"; el.setAttribute("role", "dialog"); el.setAttribute("aria-label", only ? "Mes thèmes" : "Bienvenue");
  $("#app").appendChild(el); drawOb();
  let x0 = null; el.addEventListener("pointerdown", e => { x0 = e.clientX; });
  el.addEventListener("pointerup", e => { if(x0 === null || obOnly) return; const dx = e.clientX - x0; x0 = null; if(Math.abs(dx) > 60) obAction(dx < 0 ? "next" : "prev"); });
}
function drawOb(){
  const s = OB[obI], el = $("#ob"), f = STYLE === "flat", pos = ["c", "l", "r"];
  el.style.setProperty("--c", s.c); el.classList.toggle("prefs", !!s.prefs);
  const big = s.prefs ? (f ? 60 : 84) : (f ? 84 : 120);
  const chips = s.prefs ? `<p class="lab">Je suis</p><div class="chipset" role="group" aria-label="Je suis">${PROFILES.map(x => `<button class="chipbtn" data-prof="${x}" aria-pressed="${S.pick.profile === x}">${x}</button>`).join("")}</div>
      <p class="lab">Mes thèmes (4 au maximum)</p><div class="chipset" role="group" aria-label="Mes thèmes">${INTERESTS.map(x => `<button class="chipbtn" data-int="${x}" aria-pressed="${S.pick.interests.includes(x)}">${x}</button>`).join("")}</div>` : "";
  el.innerHTML = `<button class="ob-skip" data-ob="skip">${obOnly ? "Fermer" : "Passer"}</button>
    <div class="ob-top"><span class="blob b2"></span><span class="blob b1"></span>${s.ico.map((n, i) => `<span class="ob-ico ${pos[i]} ${f ? "flat" : ""}" ${s.prefs && i ? 'style="transform:scale(.7)"' : ""}>${ic(n, i === 0 ? big : (f ? 40 : (i === 1 ? 84 : 92)))}</span>`).join("")}</div>
    <div class="ob-sheet">${obOnly ? "" : `<div class="dots" role="img" aria-label="Étape ${obI + 1} sur ${OB.length}">${OB.map((_, i) => `<i class="${i === obI ? "on" : ""}"></i>`).join("")}</div>`}
      <h1>${s.t}</h1><p>${s.p}</p>${chips}<button class="btn" data-ob="next">${obOnly ? "Enregistrer" : s.cta}</button></div>`;
}
function obAction(a){
  if(a === "next"){ if(!obOnly && obI < OB.length - 1){ obI++; buzz(6); return drawOb(); } return endOb(true); }
  if(a === "prev"){ if(obI > 0){ obI--; drawOb(); } return; }
  if(a === "skip") return endOb(false);
}
function endOb(keep){
  if(keep){ D.interests = S.pick.interests; D.profile = S.pick.profile; }
  D.onboarded = true; save(); const el = $("#ob"); if(el) el.remove(); render(current, { anim:true });
  if(keep && (D.interests.length || D.profile)) toast("Vos suggestions sont prêtes", "sparkles");
}
function openPrep(){
  const p = prep();
  openSheet(`<h3>Votre préparation</h3><p class="muted" style="margin:6px 0 8px">${p.n} étape${p.n > 1 ? "s" : ""} sur ${p.total} · tout est facultatif.</p>
    ${p.steps.map(s => `<div class="prow ${s.done ? "done" : ""}"><span class="st">${flat("check", 14)}</span>${ic(s.ico, 30)}<span class="grow"><b>${s.label}</b>${s.extra && !s.done ? `<br><span class="muted">${s.extra}</span>` : ""}</span>
      ${s.done ? `<span class="muted">Fait</span>` : `<button class="link" data-go="${s.go}">Faire</button>`}</div>`).join("")}
    <div class="stack" style="margin-top:16px"><button class="btn alt" data-close>Fermer</button></div>`);
}

/* ---------- Démarrage ---------- */
buildNav();
const start = location.hash.slice(1).split("?")[0];
render(V[start] && !["pay"].includes(start) ? start : "home");
if(!D.onboarded || qs.get("onboarding") === "1") showOnboarding();
