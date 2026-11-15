# Design Document: 10-Second Animated Showcase Video for Starship Batman Powerline

## 1. Intent & Context
Create a high-impact, 10-second animated developer terminal video showcasing the `starship-batman-powerline` preset. The video highlights the 1990s *Batman: The Animated Series* Dark Deco color palette, crisp Powerline chevron flow, and dynamic segment activation during real developer workflows.

## 2. Goals, Non-Goals, and Anti-Goals

### Goals
- Produce a polished 10-second video at 1920x1080 (30 fps, 300 frames total).
- Generate two output formats:
  - `assets/demo.mp4`: H.264 encoded, web-optimized, smooth 30 fps playback.
  - `assets/demo.gif`: High-fidelity, optimized 256-color palette (using ffmpeg `palettegen`/`paletteuse`) for GitHub README embedding.
- Simulate an authentic, fast-paced developer terminal session demonstrating:
  1. Initial prompt in home directory (`joker_purple`, `cape_blue`, `gotham_midnight`).
  2. Directory navigation into a Git repository (`…/gotham-app`).
  3. Dynamic git segment updating during branch checkout (`signal_yellow` with ` feature/batmobile`).
  4. Language runtime detection (`robin_green` with Node.js badge).
  5. Container activation via `docker compose up -d` triggering the Docker segment (`alert_crimson` with ` batcave`).
  6. Command test pass (`pnpm test`) and return to a clean, blinking prompt.
- Create an automated, reproducible generator script in the repository.

### Non-Goals
- Recording a live human desktop screen.
- Requiring third-party cloud rendering or proprietary SaaS video services.
- Audio / sound design (silent terminal demo).

### Anti-Goals
- Blurry or low-contrast text and misaligned Powerline chevrons.
- Choppy or inconsistent frame rates.
- Oversized media files that slow down repository cloning or README page loads (>15MB).

## 3. Constraints
- Must run on local macOS tooling using standard binaries: `ffmpeg`, `/Applications/Google Chrome.app`, `python3`.
- No external network downloads required during rendering.

## 4. Approaches Considered

### Approach 1: High-Fidelity SVG/HTML Frame Generator + FFmpeg (Selected)
Build a scripted HTML/SVG terminal renderer styled after `preview.svg` with exact Dark Deco styling, typography, and SVG glyphs. Headless Chrome captures the exact frame sequence, and FFmpeg encodes MP4 and GIF assets.
- **Why chosen**: 100% deterministic millisecond timing, flawless vector glyph rendering, clean looping, and zero desktop interference.

### Approach 2: Live PTY / CLI Recording
Drive an actual PTY session running live starship binary and capture via headless terminal emulator.
- **Why rejected**: Font metrics, terminal line-height discrepancies, and unpredictable execution timings make tight 10-second looping unreliable.

### Approach 3: Native macOS Screen Recording
Automate Terminal / iTerm2 with AppleScript and capture with `screencapture -v`.
- **Why rejected**: Fragile, dependent on screen resolution/scaling, prone to OS notification interruptions.

## 5. Visual Specifications & Palette

The terminal window is styled with the Batman TAS aesthetic:
- **Window frame**: Dark background `#1a1a2e`, title bar `#16213e`, traffic light buttons (`#e53e3e`, `#ecc94b`, `#38a169`), subtle outer glow and drop shadow.
- **Starship Palette Tokens**:
  - `joker_purple` = `#805ad5` (User cap & identity)
  - `cape_blue` = `#0f3460` (Directory & path)
  - `signal_yellow` = `#ecc94b` (Git branch & status)
  - `robin_green` = `#2f855a` (Language runtimes, Node.js)
  - `alert_crimson` = `#c53030` (Docker context)
  - `gotham_midnight` = `#16213e` (Time & end cap)
  - `gotham_dark` = `#1a1a2e` (Terminal background)
  - `gotham_fog` = `#e2e8f0` (Primary text)
  - `silver_highlight` = `#cbd5e0` (Secondary text)

## 6. Storyboard & Frame Timeline (300 Frames @ 30 fps = 10.0s)

| Time | Frames | Action & Visual State |
|---|---|---|
| **0.0s – 1.8s** | 0 – 54 | **Opening & Navigation**: Terminal opens in `~`. Prompt shows: `jpwhite`  `~`  `♥ 15:10`. Typing `cd gotham-app`. |
| **1.8s – 4.2s** | 55 – 126 | **Git & Runtime**: Prompt transitions to: `jpwhite`  `…/gotham-app`  ` main`  `⬢ v22.12.0`  `♥ 15:10`. Typing `git checkout -b feature/batmobile`. Branch switches to ` feature/batmobile`. |
| **4.2s – 6.8s** | 127 – 204 | **Docker Integration**: Typing `docker compose up -d`. Output shows `[+] Running 2/2 ✔ Network batcave_default ✔ Container batcave-api Started`. Prompt updates with Alert Crimson segment: `…`  ` batcave`  `♥ 15:11`. |
| **6.8s – 8.8s** | 205 – 264 | **Testing & Build**: Typing `pnpm test`. Fast output: `PASS test/signal.spec.ts`, `PASS test/turboboost.spec.ts`, `Tests: 12 passed, 12 total`. |
| **8.8s – 10.0s** | 265 – 300 | **Rest State**: Complete Batman Powerline prompt displayed with blinking cursor. Smooth end loop transition. |

## 7. Implementation Pipeline

1. **Renderer Script (`scripts/render_video.py`)**:
   - Creates a self-contained HTML/CSS/SVG stage at 1920x1080 resolution.
   - Defines a discrete timeline function `get_terminal_state(frame_index)` returning prompt segments, cursor position, and terminal scrollback lines.
   - Headless Chrome captures frames to a temporary directory.
2. **Video Assembly (FFmpeg)**:
   - `ffmpeg -framerate 30 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 assets/demo.mp4`
   - Two-pass palette generation for GIF:
     `ffmpeg -i assets/demo.mp4 -vf "fps=30,scale=1280:-1:flags=lanczos,palettegen" palette.png`
     `ffmpeg -i assets/demo.mp4 -i palette.png -lavfi "fps=30,scale=1280:-1:flags=lanczos [x]; [x][1:v] paletteuse" assets/demo.gif`
3. **Repository Updates**:
   - Embed `assets/demo.gif` or link `assets/demo.mp4` in `README.md`.
   - Ensure clean file structure.

## 8. Builder Leeway
The implementer may adjust typing cadence, minor character delays, and exact shadow radius to ensure optimal visual rhythm and readability within the 10-second envelope.
