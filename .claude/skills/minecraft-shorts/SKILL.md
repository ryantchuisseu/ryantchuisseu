---
name: minecraft-shorts
description: Builds short vertical (9:16) videos in a simple Minecraft-style block animation (blocky characters, village set, sign-board infographics, captions, music) entirely locally with Three.js + Playwright + ffmpeg, no external tools. Use whenever the user wants a Minecraft-style / block-world video, TikTok/Shorts/Reels animation, explainer or story in blocks, a "vidéo Minecraft", or wants to turn a script or an English voice-over into a captioned animation. Generic and neutral: not tied to any previous channel's cast, tone or language.
---

# minecraft-shorts — simple Minecraft-style short videos

Pipeline: **Three.js** 3D block scene → **Playwright/Chromium** frame render → **numpy** synthesised music/SFX → **ffmpeg** MP4 (720×1280, 30 fps). One scenario = one file `scenario.js`.
Original assets only: never use official Minecraft textures, skins, logos, fonts, or the word "Minecraft" in an on-screen title. Say "Minecraft-style" to the user.

## What this skill is (and is not)
- Generic engine and neutral cast (diverse villagers, default village plaza + stage + sign board). Language of captions = the scenario's language (English by default for the new channel).
- It does **not** carry any earlier channel identity (no recurring character, tone, or catch-phrases). Style rules live in `references/storytelling.md` and can be changed freely.

## Workflow
1. **Frame**: topic, length (7 s test / 30–120 s), language, voice or not. Default: no voice, captions only. If the user gives an MP3 voice-over → step 6.
2. **Write the script and a storyboard table** (shot, duration, visual, caption) following `references/storytelling.md`. Show it once; don't block on approval unless asked.
3. `bash scripts/new_project.sh <project>` — copies the engine, installs three + fonts, drops `examples/hello.js` as `scenario.js`.
4. Edit `<project>/scenario.js` (API in `references/api.md`).
5. `bash scripts/preview.sh <project> t1 t2 …` → look at `<project>/preview_sheet.jpg` with Read. Fix framing problems, re-run.
6. **Voice-over**: copy the MP3 to `<project>/voix.mp3` and the exact text to `<project>/script_voix.txt`, then `python3 -I scripts/align.py <project>/voix.mp3 <project>/script_voix.txt <project>/words.json` (silence-based alignment, ±0.15 s; no speech model needed). Cut shots on sentence starts, set `cap:[]` per shot (word-by-word captions come from `words.json`), list highlight keywords in `E.HL=[...]`, and make the video ≈ voice + 0.8 s.
7. `bash scripts/make_video.sh <project> <out.mp4> [happy|calm|tense|epic]` — about 1 min per 7 s of video; run with a long timeout.
8. Deliver the MP4 (SendUserFile) and say what is still approximated.

## Rules that avoid the usual failures
- **Never render two projects at once** (they share a port). Use `PORT=8766` if you must.
- **A character in the foreground hides the scene.** Keep the camera at y ≥ 2.4 when the crowd is between camera and target, or hide nearby extras.
- Captions: 1–3 words per chunk, ≤ 22 characters, split by meaning. Put them in the upper area (`E.CAP.y=0.2`) when a face is centered.
- Sign-board text: UPPERCASE, 3–5 lines max (VT323 is narrow and overflows).
- At most 2–3 `stamp`s per video (each shakes the camera + thud).
- No Hugging Face access in the cloud sandbox: no Whisper, no TTS. Never try to install them. Voice = the user's MP3.
- Sensitive topics (politics, religion, history): stay factual, use fictional characters, never caricature a real identifiable person or regime.
- Everything is re-placed in `run(u)` on every frame (the engine hides all characters/sprites each frame) — rendering stays deterministic.

## Files
| File | Role |
|---|---|
| `engine/main.js` | Engine: world, characters (talking mouth), sign board, stamp, chat, poof, confetti, captions, render loop. Edit only to add a reusable capability. |
| `examples/hello.js` | 7 s, 3 shots demo (wave, hand on chest, close-up, talking mouth) |
| `references/api.md` | Scenario API, world map, camera framings, character options |
| `references/storytelling.md` | The Hook → World → Hero → Countdown → Reveal formula and caption style |
| `scripts/*` | `new_project.sh`, `preview.sh`, `make_video.sh`, `render.js`, `audio.py`, `align.py` |
