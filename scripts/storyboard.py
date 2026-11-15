"""Terminal Storyboard Engine for starship-batman-powerline showcase video.

Computes discrete terminal states across a 10.0-second timeline (300 frames @ 30 fps)
demonstrating authentic developer workflows with the Batman TAS Powerline theme:
1. Opening prompt in home directory
2. Navigation into Git repository (…/gotham-app)
3. Git branch checkout (feature/batmobile) and Node.js runtime detection
4. Docker Compose service start triggering the Alert Crimson Docker segment
5. Test suite execution and return to blinking rest state
"""

from typing import Dict, List, Any

TOTAL_FRAMES = 300
FPS = 30

# Starship Batman TAS color palette tokens copied verbatim from starship.toml
PALETTE: Dict[str, str] = {
    "joker_purple": "#805ad5",
    "cape_blue": "#0f3460",
    "signal_yellow": "#ecc94b",
    "robin_green": "#2f855a",
    "alert_crimson": "#c53030",
    "gotham_midnight": "#16213e",
    "gotham_dark": "#1a1a2e",
    "gotham_fog": "#e2e8f0",
    "silver_highlight": "#cbd5e0",
}


def _interpolate_typing(text: str, start_frame: int, end_frame: int, current_frame: int) -> str:
    """Linearly interpolate typing progress across a frame range."""
    if current_frame < start_frame:
        return ""
    if current_frame >= end_frame:
        return text
    progress = (current_frame - start_frame) / (end_frame - start_frame)
    num_chars = int(progress * len(text))
    return text[:num_chars]


def get_terminal_state(frame_idx: int) -> Dict[str, Any]:
    """Calculate the terminal visual state for a given frame index (0 to TOTAL_FRAMES - 1).

    Returns a dictionary containing:
        - segments: list[dict] with keys `text`, `bg`, `fg`, `icon`
        - command: str (currently typed command buffer)
        - cursor: bool (cursor visibility state)
        - history: list[dict] previous executed commands, outputs, and prompt segments
    """
    frame = max(0, min(frame_idx, TOTAL_FRAMES - 1))

    # Standard cursor blink: 15 frames visible (500ms), 15 frames hidden (500ms)
    cursor = bool((frame // 15) % 2 == 0)

    # Reusable segment definitions
    seg_user = {
        "text": "jpwhite",
        "bg": PALETTE["joker_purple"],
        "fg": PALETTE["gotham_fog"],
        "icon": "",
    }
    seg_dir_home = {
        "text": "~",
        "bg": PALETTE["cape_blue"],
        "fg": PALETTE["gotham_fog"],
        "icon": "",
    }
    seg_dir_repo = {
        "text": "…/gotham-app",
        "bg": PALETTE["cape_blue"],
        "fg": PALETTE["gotham_fog"],
        "icon": "",
    }
    seg_git_main = {
        "text": "main",
        "bg": PALETTE["signal_yellow"],
        "fg": PALETTE["gotham_dark"],
        "icon": "branch",
    }
    seg_git_feature = {
        "text": "feature/batmobile",
        "bg": PALETTE["signal_yellow"],
        "fg": PALETTE["gotham_dark"],
        "icon": "branch",
    }
    seg_node = {
        "text": "v22.12.0",
        "bg": PALETTE["robin_green"],
        "fg": PALETTE["gotham_fog"],
        "icon": "node",
    }
    seg_docker = {
        "text": "batcave",
        "bg": PALETTE["alert_crimson"],
        "fg": PALETTE["gotham_fog"],
        "icon": "docker",
    }
    seg_time_1510 = {
        "text": "15:10",
        "bg": PALETTE["gotham_midnight"],
        "fg": PALETTE["silver_highlight"],
        "icon": "heart",
    }
    seg_time_1511 = {
        "text": "15:11",
        "bg": PALETTE["gotham_midnight"],
        "fg": PALETTE["silver_highlight"],
        "icon": "heart",
    }

    # Completed history records
    hist_cd = {
        "command": "cd gotham-app",
        "output": [],
        "segments": [seg_user, seg_dir_home, seg_time_1510],
    }
    hist_git_checkout = {
        "command": "git checkout -b feature/batmobile",
        "output": ["Switched to a new branch 'feature/batmobile'"],
        "segments": [seg_user, seg_dir_repo, seg_git_main, seg_node, seg_time_1510],
    }
    hist_docker_compose = {
        "command": "docker compose up -d",
        "output": [
            "[+] Running 2/2",
            " ✔ Network batcave_default    Created",
            " ✔ Container batcave-api     Started",
        ],
        "segments": [seg_user, seg_dir_repo, seg_git_feature, seg_node, seg_time_1511],
    }
    hist_pnpm_test = {
        "command": "pnpm test",
        "output": [
            "PASS test/signal.spec.ts",
            "PASS test/turboboost.spec.ts",
            "Tests: 12 passed, 12 total",
        ],
        "segments": [seg_user, seg_dir_repo, seg_git_feature, seg_node, seg_docker, seg_time_1511],
    }

    # Timeline calculation across 5 phases
    if frame < 55:
        # Phase 1: Opening & Navigation (0.0s – 1.8s, frames 0–54)
        segments = [seg_user, seg_dir_home, seg_time_1510]
        history: List[Dict[str, Any]] = []
        if frame < 15:
            command = ""
        elif frame < 43:
            command = _interpolate_typing("cd gotham-app", 15, 42, frame)
        else:
            command = "cd gotham-app"

    elif frame < 118:
        # Phase 2: Git & Runtime Navigation (1.8s – ~3.9s, frames 55–117)
        segments = [seg_user, seg_dir_repo, seg_git_main, seg_node, seg_time_1510]
        history = [hist_cd]
        if frame < 65:
            command = ""
        elif frame < 109:
            command = _interpolate_typing("git checkout -b feature/batmobile", 65, 108, frame)
        else:
            command = "git checkout -b feature/batmobile"

    elif frame < 175:
        # Phase 2 end / Phase 3: Switched Branch & Docker Command (frames 118–174)
        segments = [seg_user, seg_dir_repo, seg_git_feature, seg_node, seg_time_1511]
        history = [hist_cd, hist_git_checkout]
        if frame < 135:
            command = ""
        elif frame < 165:
            command = _interpolate_typing("docker compose up -d", 135, 164, frame)
        else:
            command = "docker compose up -d"

    elif frame < 245:
        # Phase 3 end / Phase 4: Docker Active & Run Tests (frames 175–244)
        segments = [seg_user, seg_dir_repo, seg_git_feature, seg_node, seg_docker, seg_time_1511]
        history = [hist_cd, hist_git_checkout, hist_docker_compose]
        if frame < 215:
            command = ""
        elif frame < 235:
            command = _interpolate_typing("pnpm test", 215, 234, frame)
        else:
            command = "pnpm test"

    else:
        # Phase 5: Rest State (frames 245–299)
        segments = [seg_user, seg_dir_repo, seg_git_feature, seg_node, seg_docker, seg_time_1511]
        history = [hist_cd, hist_git_checkout, hist_docker_compose, hist_pnpm_test]
        command = ""

    return {
        "segments": segments,
        "command": command,
        "cursor": cursor,
        "history": history,
    }
