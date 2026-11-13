# Scenario API

`scenario.js` default-exports `function(E){ … return [shot, …]; }`. `E` = the engine. Create characters/sprites **outside** `run`, place them **inside** `run(u)` every frame (`u` = seconds since the shot started).

```js
const {V,pose,hide,makeChar,textSprite,title,line,tally,poof,confettiRain,crowd,crowdLook,easeOutBack,ease,clamp,lerp,CAP}=E;
```

## Shot fields
| Field | Meaning |
|---|---|
| `d` | duration in s (2–3 s typical) |
| `cap` | caption chunks (share `d` equally); `[]` when a voice-over drives captions |
| `cam`, `look` | `[V start, V end]` camera position / target (interpolated, eased) |
| `board` | `[key, draw]` sign-board content; `null` keeps the previous one; **no board defined yet = board hidden**. `key`/`draw` may be functions of `u` for animation |
| `stamp` | `['TEXT', u]` red stamp on the board + shake + thud |
| `chat` | `[[text,u,color?]]` Minecraft-chat-style lines (bottom left) |
| `sfx` | `[[key,u]]`: chime, pop, whoosh, thud, poof, clang, boing |
| `mood` | `happy`/`calm`/`tense`/`epic` (first shot with a mood sets the music) |
| `run(u)` | places characters and effects |

Automatic: fade in/out, whoosh on cuts, caption pops (no voice), vignette, subtle handheld drift.

## Board drawing (canvas 1024×540)
`title(g,'TEXT',y,size,color)`, `line(g,'TEXT',y,size=72,color)`, `tally(g,x,y,n)`; raw 2D canvas `g` also works. Example: `board:['k',g=>{title(g,'RULE #1',110);line(g,'ONE VOTE PER PERSON',300);}]`

## World (default village plaza, y=0 ground)
Stage with characters at `y:.9, z:-4.3`, x∈[-2,2]; sign board centre (0,4.5,-6.4); lamps x=±2.9; crowd spots `E.crowdSpots` (9 villagers, `crowd[0..8]`, `crowdLook(u, opts|fn(i), except[], target)`); houses/trees around. `E.hideWorld()` hides all default decor to build your own with `E.box(w,h,d,E.M.planks,x,y,z)`, `E.house(x,z,rot)`, `E.tree(x,z,h)`, `E.lamp(x,z)`. Materials `E.M`: grass stone planks bricks log leaves cobble glow carpet gold sand water dirt plazaStone glass iron. `E.setSky(bg,fog,hemiTop,hemiBottom,sun)` for night/sunset moods (`E.setSky('#0b1030','#0b1030','#40508f','#101020','#8da2ff')`).

## Characters
`makeChar({skin,hair,eye,shirt,sleeve,longSleeve,pants,shoes,collar,tie,buttons,belt,badge,glasses,beard,cap,brim,helmet,hat,crown,cape,bald,smile,blank})` → 2 units tall; `.scale` for giants.
`pose(c,{x,y,z,ry,t:u,walk:u|-1,wave,armsUp,point,cross,salute,headTilt,talk,lie})` (`lie:1` = lying face-up, head toward -z) — gestures 0..1; `talk:true` opens/closes the mouth in rhythm; `walk` animates legs; `ry` via `E.faceTo(x,z,tx,tz)`. Arm override after `pose`: `c.armR.rotation.set(-1.1,0,.5)`. `hide(c)`.

## Sprites and effects
`textSprite(text,{font,color,bg,scale})` name tags (set `.visible=true` and `.position` in `run`); ready-made `qMarks[0..4]` (?), `exMarks[0..2]` (!), `checkMark`. `poof(V(x,0,z),u-t0,seed)` smoke puff (hide the character right after). `confettiRain(u,t0)`.

## Proven framings
| Shot | cam | look |
|---|---|---|
| Wide stage + crowd from behind | V(0,3.6,9.5)→V(0,3.3,7.2) | V(0,3,-4) |
| Board full frame | V(0,3.7,1.6)→V(0,4,.3) | V(0,4.3,-6.4) |
| Medium on stage speaker | V(1.3,2.5,-1)→V(.8,2.6,-1.7) | V(0,2.7,-4.3) |
| Close-up face | V(.4,2.95,-2)→V(.1,3,-2.7) | V(0,2.98,-4.3) |
| Low angle on speaker | V(1.8,1.3,.6)→V(1.1,1.5,-.6) | V(0,3,-4.6) |

## Easing
`ease(x)`, `easeOutBack(x)` take 0..1: use `(u-start)/duration`.
