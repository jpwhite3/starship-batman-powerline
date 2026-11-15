"""FFmpeg Video & Optimized GIF Compilation Pipeline.

Orchestrates frame rendering and video/GIF encoding for the starship-batman-powerline
animated developer showcase:
- 10-second 1920x1080 @ 30fps H.264 MP4 (`assets/demo.mp4`)
- High-contrast 1280px @ 24fps 2-pass Bayer-dithered GIF under 10MB (`assets/demo.gif`)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Dict, Optional

# Ensure repository root is on sys.path when invoked directly
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from scripts.render_frames import capture_frames


def check_ffmpeg_available() -> bool:
    """Return True if ffmpeg executable is available in PATH."""
    return shutil.which("ffmpeg") is not None


def check_ffprobe_available() -> bool:
    """Return True if ffprobe executable is available in PATH."""
    return shutil.which("ffprobe") is not None


def get_media_info(file_path: str) -> Dict[str, Any]:
    """Retrieve media information (duration, dimensions, streams) via ffprobe."""
    if not check_ffprobe_available():
        raise RuntimeError("ffprobe is not available in PATH.")

    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration,size,bit_rate:stream=width,height,r_frame_rate,nb_frames,codec_name",
        "-of",
        "json",
        file_path,
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if res.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {file_path}: {res.stderr}")

    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse ffprobe JSON output: {exc}") from exc


def get_media_duration(file_path: str) -> float:
    """Return the duration in seconds of a media file via ffprobe."""
    info = get_media_info(file_path)
    # Check format duration first, then stream duration
    fmt_duration = info.get("format", {}).get("duration")
    if fmt_duration is not None:
        return float(fmt_duration)

    streams = info.get("streams", [])
    if streams and "duration" in streams[0]:
        return float(streams[0]["duration"])

    return 0.0


def compile_mp4(
    frame_dir: str,
    output_path: str,
    fps: int = 30,
    crf: int = 18,
) -> str:
    """Compile PNG frames (frame_%04d.png) into a 1080p MP4 video.

    Uses libx264, yuv420p pixel format, and specified crf (default 18 for visually lossless).
    Returns the absolute path to the generated MP4.
    """
    if not check_ffmpeg_available():
        raise RuntimeError("ffmpeg binary not found in PATH. Please install ffmpeg.")

    abs_frame_dir = os.path.abspath(frame_dir)
    abs_output = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(abs_output), exist_ok=True)

    input_pattern = os.path.join(abs_frame_dir, "frame_%04d.png")

    cmd = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(fps),
        "-i",
        input_pattern,
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-crf",
        str(crf),
        abs_output,
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg MP4 compilation failed (exit {res.returncode}):\n{res.stderr}")

    if not (os.path.exists(abs_output) and os.path.getsize(abs_output) > 0):
        raise RuntimeError(f"Compiled MP4 not found or empty at {abs_output}")

    return abs_output


def compile_gif(
    mp4_path: str,
    output_path: str,
    fps: int = 24,
    width: int = 1280,
    palette_path: Optional[str] = None,
) -> str:
    """Compile MP4 into an optimized GIF using 2-pass palette generation.

    Generates a custom palette for maximum color fidelity across the Batman theme,
    followed by Lanczos scaling and Bayer dithering.
    Returns the absolute path to the generated GIF.
    """
    if not check_ffmpeg_available():
        raise RuntimeError("ffmpeg binary not found in PATH. Please install ffmpeg.")

    abs_mp4 = os.path.abspath(mp4_path)
    abs_output = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(abs_output), exist_ok=True)

    cleanup_palette = False
    if not palette_path:
        palette_file = tempfile.NamedTemporaryFile(prefix="batman_palette_", suffix=".png", dir=tempfile.gettempdir(), delete=False)
        palette_path = palette_file.name
        palette_file.close()
        cleanup_palette = True

    try:
        # Pass 1: Generate optimal palette
        pass1_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            abs_mp4,
            "-vf",
            f"fps={fps},scale={width}:-1:flags=lanczos,palettegen",
            palette_path,
        ]
        res1 = subprocess.run(pass1_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        if res1.returncode != 0:
            raise RuntimeError(f"FFmpeg GIF palette generation failed (exit {res1.returncode}):\n{res1.stderr}")

        # Pass 2: Render GIF using custom palette and Bayer dithering
        pass2_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            abs_mp4,
            "-i",
            palette_path,
            "-lavfi",
            f"fps={fps},scale={width}:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=3",
            abs_output,
        ]
        res2 = subprocess.run(pass2_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        if res2.returncode != 0:
            raise RuntimeError(f"FFmpeg GIF render failed (exit {res2.returncode}):\n{res2.stderr}")

        if not (os.path.exists(abs_output) and os.path.getsize(abs_output) > 0):
            raise RuntimeError(f"Compiled GIF not found or empty at {abs_output}")

        return abs_output

    finally:
        if cleanup_palette and os.path.exists(palette_path):
            try:
                os.remove(palette_path)
            except OSError:
                pass


def verify_outputs(
    mp4_path: str,
    gif_path: str,
    max_gif_bytes: int = 10 * 1024 * 1024,
) -> Dict[str, Any]:
    """Verify video duration (~10.0s) and GIF size (< 10MB)."""
    if not os.path.exists(mp4_path):
        raise FileNotFoundError(f"MP4 output not found: {mp4_path}")
    if not os.path.exists(gif_path):
        raise FileNotFoundError(f"GIF output not found: {gif_path}")

    mp4_size = os.path.getsize(mp4_path)
    gif_size = os.path.getsize(gif_path)

    duration = get_media_duration(mp4_path)

    # Verification checks
    duration_valid = 9.8 <= duration <= 10.2
    gif_size_valid = gif_size <= max_gif_bytes

    return {
        "mp4_path": mp4_path,
        "mp4_size_bytes": mp4_size,
        "mp4_size_mb": mp4_size / (1024 * 1024),
        "duration_seconds": duration,
        "duration_valid": duration_valid,
        "gif_path": gif_path,
        "gif_size_bytes": gif_size,
        "gif_size_mb": gif_size / (1024 * 1024),
        "gif_size_valid": gif_size_valid,
    }


def build_demo(
    output_dir: str = "assets",
    workers: int = 8,
    clean_frames: bool = True,
    fps_mp4: int = 30,
    fps_gif: int = 24,
    gif_width: int = 1280,
) -> Dict[str, Any]:
    """Execute end-to-end rendering and compilation of demo MP4 and GIF."""
    if not check_ffmpeg_available():
        raise RuntimeError("ffmpeg binary not found in PATH.")

    start_time = time.time()
    os.makedirs(output_dir, exist_ok=True)
    mp4_path = os.path.join(output_dir, "demo.mp4")
    gif_path = os.path.join(output_dir, "demo.gif")

    temp_frames_dir = tempfile.mkdtemp(prefix="batman_frames_", dir=tempfile.gettempdir())
    print(f"[*] Temporary frame directory: {temp_frames_dir}")

    try:
        print(f"[*] Rendering 300 frames with {workers} workers...")
        frame_start = time.time()
        capture_frames(0, 300, temp_frames_dir, workers=workers)
        frame_time = time.time() - frame_start
        print(f"[+] Rendered 300 frames in {frame_time:.1f}s ({300 / max(frame_time, 0.01):.1f} fps)")

        print(f"[*] Compiling MP4 video to {mp4_path}...")
        mp4_start = time.time()
        compile_mp4(temp_frames_dir, mp4_path, fps=fps_mp4)
        mp4_time = time.time() - mp4_start
        print(f"[+] Compiled MP4 in {mp4_time:.1f}s")

        print(f"[*] Compiling 2-pass optimized GIF to {gif_path}...")
        gif_start = time.time()
        compile_gif(mp4_path, gif_path, fps=fps_gif, width=gif_width)
        gif_time = time.time() - gif_start
        print(f"[+] Compiled GIF in {gif_time:.1f}s")

        verification = verify_outputs(mp4_path, gif_path)
        total_time = time.time() - start_time
        verification["total_time_seconds"] = total_time

        print(f"[+] Verification results:")
        print(f"    - MP4 Duration: {verification['duration_seconds']:.2f}s (valid: {verification['duration_valid']})")
        print(f"    - MP4 Size: {verification['mp4_size_mb']:.2f} MB")
        print(f"    - GIF Size: {verification['gif_size_mb']:.2f} MB (valid: {verification['gif_size_valid']})")
        print(f"    - Total Pipeline Time: {total_time:.1f}s")

        if not verification["duration_valid"]:
            raise ValueError(f"MP4 duration {verification['duration_seconds']}s is outside expected 10.0s window")
        if not verification["gif_size_valid"]:
            raise ValueError(f"GIF size {verification['gif_size_mb']:.2f}MB exceeds 10MB limit")

        return verification

    finally:
        if clean_frames and os.path.exists(temp_frames_dir):
            print(f"[*] Cleaning up temporary frame directory: {temp_frames_dir}")
            shutil.rmtree(temp_frames_dir, ignore_errors=True)


def main() -> None:
    """CLI entrypoint for compile_video.py."""
    parser = argparse.ArgumentParser(description="Compile Starship Batman Powerline Demo Video & GIF")
    parser.add_argument("--workers", type=int, default=8, help="Number of parallel Chrome render workers (default: 8)")
    parser.add_argument("--output-dir", type=str, default="assets", help="Output directory for demo.mp4 and demo.gif")
    parser.add_argument("--keep-frames", action="store_true", help="Keep temporary rendered PNG frames")

    args = parser.parse_args()

    try:
        build_demo(
            output_dir=args.output_dir,
            workers=args.workers,
            clean_frames=not args.keep_frames,
        )
    except Exception as exc:
        print(f"[!] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
