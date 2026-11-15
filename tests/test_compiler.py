"""Tests for FFmpeg video and optimized GIF compiler."""

import os
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts.compile_video import (
    check_ffmpeg_available,
    compile_gif,
    compile_mp4,
    get_media_duration,
)


class TestCompiler(unittest.TestCase):
    def test_ffmpeg_available(self):
        """FFmpeg binary should be detected on PATH."""
        self.assertTrue(check_ffmpeg_available())

    def test_ffmpeg_not_available_mock(self):
        """When ffmpeg is not in PATH, check_ffmpeg_available returns False."""
        with patch("shutil.which", return_value=None):
            self.assertFalse(check_ffmpeg_available())

    def test_compile_mp4_and_gif_short_sequence(self):
        """Verify compiling a 3-frame mini-sequence to MP4 and GIF produces valid files."""
        temp_dir = tempfile.mkdtemp(prefix="test_compile_", dir=tempfile.gettempdir())
        try:
            frames_dir = os.path.join(temp_dir, "frames")
            os.makedirs(frames_dir, exist_ok=True)
            mp4_out = os.path.join(temp_dir, "test.mp4")
            gif_out = os.path.join(temp_dir, "test.gif")

            # Generate 3 synthetic test PNG frames directly via FFmpeg lavfi (no Chrome dependency)
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    "color=c=blue:s=320x240:d=0.1",
                    "-frames:v",
                    "3",
                    "-start_number",
                    "0",
                    os.path.join(frames_dir, "frame_%04d.png"),
                ],
                check=True,
                capture_output=True,
            )
            self.assertTrue(os.path.exists(os.path.join(frames_dir, "frame_0000.png")))
            self.assertTrue(os.path.exists(os.path.join(frames_dir, "frame_0001.png")))
            self.assertTrue(os.path.exists(os.path.join(frames_dir, "frame_0002.png")))

            # Compile MP4
            result_mp4 = compile_mp4(frames_dir, mp4_out, fps=30)
            self.assertEqual(result_mp4, mp4_out)
            self.assertTrue(os.path.exists(mp4_out))
            self.assertGreater(os.path.getsize(mp4_out), 0)

            # Check MP4 duration > 0
            duration = get_media_duration(mp4_out)
            self.assertGreater(duration, 0.0)

            # Compile GIF
            result_gif = compile_gif(mp4_out, gif_out, fps=24, width=640)
            self.assertEqual(result_gif, gif_out)
            self.assertTrue(os.path.exists(gif_out))
            self.assertGreater(os.path.getsize(gif_out), 0)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_compile_missing_ffmpeg_raises(self):
        """If ffmpeg is missing, compile_mp4 raises RuntimeError."""
        with patch("scripts.compile_video.check_ffmpeg_available", return_value=False):
            with self.assertRaises(RuntimeError):
                compile_mp4("/invalid/dir", "/invalid/out.mp4")


if __name__ == "__main__":
    unittest.main()
