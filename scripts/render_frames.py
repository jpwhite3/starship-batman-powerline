"""Headless Frame Renderer using Google Chrome.

Captures pixel-perfect 1920x1080 PNG frames for the starship-batman-powerline
animated showcase video using headless Google Chrome.
"""

import concurrent.futures
import os
import shutil
import subprocess
import sys
import tempfile
from typing import List, Optional

# Ensure repository root is on sys.path when invoked directly
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from scripts.stage_template import generate_terminal_html
from scripts.storyboard import get_terminal_state

# Default Google Chrome binary locations
DEFAULT_CHROME_PATHS = [
    os.environ.get("CHROME_BIN", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome") or "",
    shutil.which("chrome") or "",
    shutil.which("chromium") or "",
]


def find_chrome_binary(custom_path: Optional[str] = None) -> str:
    """Resolve the path to the Google Chrome executable."""
    if custom_path and os.path.exists(custom_path):
        return custom_path

    for path in DEFAULT_CHROME_PATHS:
        if path and os.path.exists(path):
            return path

    raise FileNotFoundError(
        "Google Chrome binary not found. Set CHROME_BIN environment variable or install Chrome."
    )


def capture_single_frame(
    frame_idx: int,
    output_path: str,
    chrome_path: Optional[str] = None,
) -> str:
    """Render a single terminal frame at frame_idx to output_path as a 1920x1080 PNG.

    Returns the absolute path to the generated PNG image.
    """
    chrome = find_chrome_binary(chrome_path)
    abs_output = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(abs_output), exist_ok=True)

    state = get_terminal_state(frame_idx)
    html_content = generate_terminal_html(state)

    user_data_dir = tempfile.mkdtemp(prefix=f"chrome_user_{frame_idx}_", dir="/tmp")
    tmp_html_fd, tmp_html_path = tempfile.mkstemp(
        suffix=f"_{frame_idx}.html", prefix="stage_", dir="/tmp"
    )
    try:
        with open(tmp_html_fd, "w", encoding="utf-8") as f:
            f.write(html_content)

        cmd = [
            chrome,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--disable-crash-reporter",
            f"--crash-dumps-dir={user_data_dir}",
            f"--user-data-dir={user_data_dir}",
            f"--screenshot={abs_output}",
            "--window-size=1920,1080",
            "--default-background-color=00000000",
            f"file://{tmp_html_path}",
        ]

        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        if not (os.path.exists(abs_output) and os.path.getsize(abs_output) > 0):
            err_msg = res.stderr.decode("utf-8", errors="replace")
            raise RuntimeError(
                f"Failed to capture frame {frame_idx} (exit code {res.returncode}): {err_msg}"
            )

        return abs_output

    finally:
        if os.path.exists(tmp_html_path):
            try:
                os.remove(tmp_html_path)
            except OSError:
                pass
        shutil.rmtree(user_data_dir, ignore_errors=True)


def capture_frames(
    start_frame: int,
    end_frame: int,
    output_dir: str,
    workers: int = 4,
    chrome_path: Optional[str] = None,
) -> List[str]:
    """Capture a sequence of frames in parallel using headless Chrome.

    Renders frames [start_frame, end_frame) into output_dir as frame_0000.png, etc.
    If start_frame == end_frame, renders that single frame.
    Returns the sorted list of generated PNG file paths.
    """
    chrome = find_chrome_binary(chrome_path)
    os.makedirs(output_dir, exist_ok=True)

    if start_frame == end_frame:
        frame_indices = [start_frame]
    else:
        frame_indices = list(range(start_frame, end_frame))

    output_paths = {
        idx: os.path.join(output_dir, f"frame_{idx:04d}.png")
        for idx in frame_indices
    }

    def _worker(idx: int) -> str:
        return capture_single_frame(idx, output_paths[idx], chrome_path=chrome)

    max_workers = max(1, min(workers, len(frame_indices)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_worker, idx): idx for idx in frame_indices}
        for future in concurrent.futures.as_completed(futures):
            # Raise exception if worker failed
            future.result()

    return [output_paths[idx] for idx in sorted(frame_indices)]


def capture_all_frames(
    output_dir: str,
    workers: int = 8,
    chrome_path: Optional[str] = None,
) -> List[str]:
    """Capture all 300 storyboard frames (0..299) to output_dir."""
    from scripts.storyboard import TOTAL_FRAMES

    return capture_frames(
        start_frame=0,
        end_frame=TOTAL_FRAMES,
        output_dir=output_dir,
        workers=workers,
        chrome_path=chrome_path,
    )

