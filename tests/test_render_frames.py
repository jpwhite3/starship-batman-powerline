import functools
import os
import shutil
import struct
import subprocess
import tempfile
import unittest

from scripts.render_frames import (
    capture_frames,
    capture_single_frame,
    find_chrome_binary,
)
from scripts.stage_template import (
    generate_terminal_html,
    render_html_for_state,
)
from scripts.storyboard import get_terminal_state


def get_png_dimensions(filepath: str) -> tuple[int, int]:
    """Parse PNG width and height from the IHDR chunk without external dependencies."""
    with open(filepath, "rb") as f:
        header = f.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{filepath} is not a valid PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


@functools.lru_cache(maxsize=1)
def can_spawn_chrome() -> bool:
    """Verify if headless Google Chrome can actually execute without process singleton / seatbelt errors."""
    try:
        chrome = find_chrome_binary()
    except Exception:
        return False

    tmp_probe = tempfile.mkdtemp(prefix="chrome_probe_")
    try:
        res = subprocess.run(
            [
                chrome,
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-crash-reporter",
                f"--crash-dumps-dir={tmp_probe}",
                f"--user-data-dir={tmp_probe}",
                "--dump-dom",
                "about:blank",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            check=False,
        )
        return res.returncode == 0
    except Exception:
        return False
    finally:
        shutil.rmtree(tmp_probe, ignore_errors=True)


class TestStageTemplate(unittest.TestCase):
    def test_html_contains_palette_and_structure(self):
        state = get_terminal_state(0)
        html = generate_terminal_html(state)
        self.assertIn("#1a1a2e", html)  # Gotham dark
        self.assertIn("#805ad5", html)  # Joker purple
        self.assertIn("jpwhite", html)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("1920px", html)
        self.assertIn("1080px", html)

    def test_alias_render_html_for_state(self):
        state = get_terminal_state(0)
        self.assertEqual(generate_terminal_html(state), render_html_for_state(state))

    def test_all_phases_render_without_error(self):
        # Sample across all 5 phases: 0, 70, 140, 200, 280
        for f in [0, 70, 140, 200, 280]:
            state = get_terminal_state(f)
            html = generate_terminal_html(state)
            self.assertIn("<!DOCTYPE html>", html)
            self.assertIn("</html>", html)
            self.assertIn("terminal-window", html)

    def test_icons_rendered(self):
        # Frame 0: contains heart icon in time segment
        html_0 = generate_terminal_html(get_terminal_state(0))
        self.assertIn("<path d=\"M8 14.2", html_0)  # Heart icon path

        # Frame 80: contains branch and node icons
        html_80 = generate_terminal_html(get_terminal_state(80))
        self.assertIn("main", html_80)
        self.assertIn("v22.12.0", html_80)
        self.assertIn("<path d=\"M10 3a2 2 0 1 0-3 1.73V7", html_80)  # Branch icon
        self.assertIn("stroke=\"currentColor\"", html_80)  # Node icon hexagon

        # Frame 150: contains switched branch feature/batmobile
        html_150 = generate_terminal_html(get_terminal_state(150))
        self.assertIn("feature/batmobile", html_150)

        # Frame 200: contains docker segment
        html_200 = generate_terminal_html(get_terminal_state(200))
        self.assertIn("batcave", html_200)
        self.assertIn("#c53030", html_200)  # Alert Crimson

    def test_cursor_toggle(self):
        # Frame 0 has cursor True (visible)
        s0 = get_terminal_state(0)
        self.assertTrue(s0["cursor"])
        html0 = generate_terminal_html(s0)
        self.assertIn("visibility: visible;", html0)

        # Frame 15 has cursor False (hidden)
        s15 = get_terminal_state(15)
        self.assertFalse(s15["cursor"])
        html15 = generate_terminal_html(s15)
        self.assertIn("visibility: hidden;", html15)

    def test_history_and_output_rendering(self):
        state = get_terminal_state(280)  # Phase 5: full history
        html = generate_terminal_html(state)
        self.assertIn("gotham-app", html)
        self.assertIn("feature/batmobile", html)
        self.assertIn("compose up -d", html)
        self.assertIn("pnpm", html)
        self.assertIn("badge-pass", html)
        self.assertIn("PASS", html)
        self.assertIn("12 passed", html)


class TestRenderFrames(unittest.TestCase):
    def test_find_chrome_binary(self):
        path = find_chrome_binary()
        self.assertTrue(os.path.exists(path))
        self.assertIn("Chrome", path)

    @unittest.skipUnless(can_spawn_chrome(), "Headless Chrome cannot spawn in current environment")
    def test_capture_single_frame(self):
        tmp_dir = tempfile.mkdtemp(prefix="test_frame_")
        out_png = os.path.join(tmp_dir, "frame_0000.png")
        try:
            result_path = capture_single_frame(0, out_png)
            self.assertEqual(result_path, out_png)
            self.assertTrue(os.path.exists(out_png))
            width, height = get_png_dimensions(out_png)
            self.assertEqual(width, 1920)
            self.assertEqual(height, 1080)
            self.assertGreater(os.path.getsize(out_png), 5000)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    @unittest.skipUnless(can_spawn_chrome(), "Headless Chrome cannot spawn in current environment")
    def test_capture_frames_batch(self):
        tmp_dir = tempfile.mkdtemp(prefix="test_frames_batch_")
        try:
            rendered = capture_frames(start_frame=0, end_frame=2, output_dir=tmp_dir, workers=2)
            self.assertEqual(len(rendered), 2)
            for path in rendered:
                self.assertTrue(os.path.exists(path))
                w, h = get_png_dimensions(path)
                self.assertEqual((w, h), (1920, 1080))
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
