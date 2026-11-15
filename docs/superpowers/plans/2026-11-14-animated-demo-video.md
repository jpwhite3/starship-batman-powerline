# 10-Second Animated Showcase Video Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a high-contrast 10-second (300 frames @ 30 fps) 1080p animated video (`assets/demo.mp4`) and optimized animated GIF (`assets/demo.gif`) demonstrating the `starship-batman-powerline` preset in an authentic developer workflow.

**Architecture:** A Python storyboard engine calculates discrete terminal states (prompt segments, typed commands, output logs, cursor blink) for 300 frames. An HTML/SVG template renders each state with exact Dark Deco styling and Powerline chevrons, rendered to PNGs via headless Chrome and assembled into MP4 and GIF assets using FFmpeg.

**Tech Stack:** Python 3 (standard library), Headless Google Chrome, FFmpeg, HTML5/CSS3/SVG, Starship Batman TAS color palette.

**Spec:** [2026-11-14-animated-demo-video-design.md](file:///Users/jpwhite/code/starship-batman-powerline/docs/superpowers/specs/2026-11-14-animated-demo-video-design.md)

## Global Constraints

- Duration: Exactly 10.0 seconds (300 frames at 30 fps).
- Video Output: `assets/demo.mp4` (1920x1080, H.264 / `yuv420p`, 30 fps).
- GIF Output: `assets/demo.gif` (optimized 2-pass palette generation via `palettegen` / `paletteuse`, <10MB).
- Palette hex colors copied verbatim from `starship.toml`:
  - `joker_purple` = `#805ad5`
  - `cape_blue` = `#0f3460`
  - `signal_yellow` = `#ecc94b`
  - `robin_green` = `#2f855a`
  - `alert_crimson` = `#c53030`
  - `gotham_midnight` = `#16213e`
  - `gotham_dark` = `#1a1a2e`
  - `gotham_fog` = `#e2e8f0`
  - `silver_highlight` = `#cbd5e0`
- Zero external runtime network calls or package installations required.

## Review Focus

1. Powerline chevrons (``, ``) must have zero pixel gaps or visible hairline seams between adjacent color segments.
2. Bat-Signal Yellow segment text (`#1a1a2e`) must maintain sharp dark contrast against the `#ecc94b` background.
3. GIF output must be under 10MB to load smoothly in GitHub READMEs.
4. Total video runtime must be exactly 10.0 seconds (300 frames at 30 fps).
5. Headless Chrome screenshot pipeline must cleanly execute within macOS local permissions.

---

### Task 1: Terminal Storyboard Engine

**Files:**
- Create: `scripts/storyboard.py`
- Create: `tests/test_storyboard.py`

**Interfaces:**
- Consumes: None (pure Python standard library).
- Produces: `get_terminal_state(frame_idx: int) -> dict` returning:
  - `segments`: `list[dict]` with keys `text`, `bg`, `fg`, `icon`
  - `command`: `str`
  - `cursor`: `bool`
  - `history`: `list[dict]` previous prompt lines and command outputs

- [ ] **Step 1: Write the failing unit tests for storyboard timeline**

```python
# tests/test_storyboard.py
import unittest
from scripts.storyboard import get_terminal_state, TOTAL_FRAMES, FPS

class TestStoryboard(unittest.TestCase):
    def test_total_frames(self):
        self.assertEqual(TOTAL_FRAMES, 300)
        self.assertEqual(FPS, 30)

    def test_initial_state(self):
        state = get_terminal_state(0)
        self.assertEqual(state["segments"][0]["text"], "jpwhite")
        self.assertEqual(state["segments"][0]["bg"], "#805ad5")
        self.assertEqual(state["segments"][1]["text"], "~")
        self.assertEqual(state["segments"][1]["bg"], "#0f3460")
        self.assertEqual(state["command"], "")

    def test_repo_navigation_state(self):
        state = get_terminal_state(70)
        # Should be inside gotham-app with git and node runtime
        seg_texts = [s["text"] for s in state["segments"]]
        self.assertIn("…/gotham-app", seg_texts)
        self.assertIn("main", seg_texts)

    def test_docker_context_state(self):
        state = get_terminal_state(180)
        # Should show alert_crimson docker segment
        docker_segs = [s for s in state["segments"] if s["bg"] == "#c53030"]
        self.assertEqual(len(docker_segs), 1)
        self.assertIn("batcave", docker_segs[0]["text"])

    def test_final_rest_state(self):
        state = get_terminal_state(299)
        self.assertTrue(len(state["history"]) >= 4)
        self.assertEqual(state["command"], "")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_storyboard.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.storyboard'`

- [ ] **Step 3: Implement `scripts/storyboard.py`**

Define `TOTAL_FRAMES = 300`, `FPS = 30`, palette dictionary, and the `get_terminal_state(frame_idx: int)` timeline calculation spanning the 5 phases defined in the spec.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_storyboard.py`
Expected: PASS with 5 tests passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/storyboard.py tests/test_storyboard.py
git commit -m "feat: add terminal storyboard engine for animated demo"
```

---

### Task 2: HTML/SVG Terminal Stage & Headless Frame Renderer

**Files:**
- Create: `scripts/stage_template.py`
- Create: `scripts/render_frames.py`
- Test: `tests/test_render_frames.py`

**Interfaces:**
- Consumes: `scripts.storyboard.get_terminal_state`
- Produces: `render_html_for_state(state: dict) -> str` and `capture_frames(start_frame: int, end_frame: int, output_dir: str)`

- [ ] **Step 1: Write test for HTML/SVG template generation**

```python
# tests/test_render_frames.py
import unittest
import os
from scripts.storyboard import get_terminal_state
from scripts.stage_template import generate_terminal_html

class TestStageTemplate(unittest.TestCase):
    def test_html_contains_palette_and_structure(self):
        state = get_terminal_state(0)
        html = generate_terminal_html(state)
        self.assertIn("#1a1a2e", html) # Gotham dark
        self.assertIn("#805ad5", html) # Joker purple
        self.assertIn("jpwhite", html)
        self.assertIn("<!DOCTYPE html>", html)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_render_frames.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.stage_template'`

- [ ] **Step 3: Implement `scripts/stage_template.py` and `scripts/render_frames.py`**

Build `generate_terminal_html(state)` producing an exact 1920x1080 HTML page with:
- Centered Dark Deco terminal window matching `preview.svg`.
- Vector chevrons with zero gap between background segments.
- SF Mono / monospace font stacks and crisp inline SVG icons (`branch`, `node`, `docker`, `heart`).
- Implement `render_frames.py` using headless Chrome via CLI (`--headless --screenshot`) to render PNG frames into a target directory.

- [ ] **Step 4: Run tests and verify single-frame capture**

Run: `python3 -m unittest tests/test_render_frames.py`
Expected: PASS
Run: `python3 -c "from scripts.render_frames import capture_single_frame; capture_single_frame(0, 'test_frame_0.png')"`
Verify: `file test_frame_0.png` confirms valid PNG 1920x1080.
Cleanup: `rm -f test_frame_0.png`

- [ ] **Step 5: Commit**

```bash
git add scripts/stage_template.py scripts/render_frames.py tests/test_render_frames.py
git commit -m "feat: add HTML/SVG stage template and headless frame renderer"
```

---

### Task 3: FFmpeg Video & Optimized GIF Compilation Pipeline

**Files:**
- Create: `scripts/compile_video.py`
- Output: `assets/demo.mp4`
- Output: `assets/demo.gif`

**Interfaces:**
- Consumes: `scripts.render_frames.capture_all_frames`, FFmpeg binary
- Produces: `compile_mp4(frame_dir: str, output_path: str)`, `compile_gif(mp4_path: str, output_path: str)`

- [ ] **Step 1: Write test for compiler verification**

```python
# tests/test_compiler.py
import unittest
import shutil
from scripts.compile_video import check_ffmpeg_available

class TestCompiler(unittest.TestCase):
    def test_ffmpeg_available(self):
        self.assertTrue(check_ffmpeg_available())
```

- [ ] **Step 2: Run test to verify it passes / fails**

Run: `python3 -m unittest tests/test_compiler.py`

- [ ] **Step 3: Implement `scripts/compile_video.py`**

- Render all 300 frames (parallelized across CPU cores using a worker pool with headless Chrome).
- Invoke `ffmpeg -y -framerate 30 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 assets/demo.mp4`.
- Invoke 2-pass high-contrast palette GIF compilation:
  `ffmpeg -y -i assets/demo.mp4 -vf "fps=24,scale=1280:-1:flags=lanczos,palettegen" /tmp/palette.png`
  `ffmpeg -y -i assets/demo.mp4 -i /tmp/palette.png -lavfi "fps=24,scale=1280:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=3" assets/demo.gif`

- [ ] **Step 4: Execute compilation pipeline and verify outputs**

Run: `python3 scripts/compile_video.py`
Verify:
1. `ffprobe -i assets/demo.mp4` shows duration 10.0s, 1920x1080 resolution, 30 fps.
2. `ls -lh assets/demo.mp4 assets/demo.gif` shows `assets/demo.gif` < 10MB.

- [ ] **Step 5: Commit**

```bash
git add scripts/compile_video.py tests/test_compiler.py assets/demo.mp4 assets/demo.gif
git commit -m "feat: generate 10-second animated MP4 and GIF demo showcase"
```

---

### Task 4: Documentation & README Showcase

**Files:**
- Modify: `README.md:9-12`

**Interfaces:**
- Consumes: `assets/demo.gif`, `assets/demo.mp4`
- Produces: Updated `README.md` with animated visual preview and video link.

- [ ] **Step 1: Update `README.md`**

Add the animated demo prominently below the title badge section:
```markdown
<p align="center">
  <img src="assets/demo.gif" alt="Starship Batman Powerline Animated Demo" width="100%">
</p>
```
Retain the static SVG palette diagram and preview.

- [ ] **Step 2: Verify markdown links and rendering**

Check markdown syntax and file presence.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add 10-second animated showcase to README"
```
