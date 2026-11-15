"""HTML/SVG Terminal Stage Template for starship-batman-powerline showcase video.

Renders a pixel-perfect 1920x1080 stage featuring:
- Dark Deco terminal window matching preview.svg and Batman: The Animated Series aesthetic.
- Powerline segments with seamless zero-gap vector chevrons.
- Crisp vector SVG icons: branch, node, docker, heart.
- Scrollback history lines and active prompt line with blinking cursor.
"""

import html
from typing import Dict, List, Any


# Starship Batman TAS color palette tokens
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

# Vector SVG icons (crisp inline glyphs)
ICONS: Dict[str, str] = {
    "branch": (
        '<svg class="seg-icon" viewBox="0 0 14 14" width="15" height="15" fill="currentColor">'
        '<path d="M10 3a2 2 0 1 0-3 1.73V7a2 2 0 0 1-2 2H4.73A2 2 0 1 0 4.73 11H5a4 4 0 0 0 4-4V4.73A2 2 0 0 0 10 3z'
        'M3 10a1 1 0 1 1 1 1 1 1 0 0 1-1-1zm6-7a1 1 0 1 1-1 1 1 1 0 0 1 1-1z" />'
        "</svg>"
    ),
    "node": (
        '<svg class="seg-icon" viewBox="0 0 16 16" width="15" height="15">'
        '<path d="M8 1 L14 4.5 L14 11.5 L8 15 L2 11.5 L2 4.5 Z" stroke="currentColor" stroke-width="1.4" fill="none" />'
        '<circle cx="8" cy="8" r="2.2" fill="currentColor" />'
        "</svg>"
    ),
    "docker": (
        '<svg class="seg-icon" viewBox="0 0 18 18" width="16" height="16" fill="currentColor">'
        '<rect x="3" y="5.5" width="2" height="1.8" rx="0.3" />'
        '<rect x="5.5" y="5.5" width="2" height="1.8" rx="0.3" />'
        '<rect x="8" y="5.5" width="2" height="1.8" rx="0.3" />'
        '<rect x="5.5" y="3.2" width="2" height="1.8" rx="0.3" />'
        '<rect x="8" y="3.2" width="2" height="1.8" rx="0.3" />'
        '<rect x="10.5" y="5.5" width="2" height="1.8" rx="0.3" />'
        '<path d="M16.5 8.8c-.3 0-.6.1-.9.2-.5-1-1.6-1.5-2.8-1.5-.2 0-.4 0-.6.1V7.5H1.5V10c0 3.2 2.7 5 6.5 5 '
        '4.5 0 7.4-2.3 8-5.7.3 0 .5-.1.8-.1.5 0 .9-.3.9-.8 0-.4-.4-.8-.9-.8zM12.5 11a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5z" />'
        "</svg>"
    ),
    "heart": (
        '<svg class="seg-icon" viewBox="0 0 16 16" width="13" height="13" fill="currentColor">'
        '<path d="M8 14.2l-.7-.6C2.5 9.2 0 6.9 0 4.1 0 1.8 1.8 0 4.1 0c1.3 0 2.6.6 3.4 1.6C8.3.6 9.6 0 10.9 0 '
        '13.2 0 15 1.8 15 4.1c0 2.8-2.5 5.1-7.3 9.5l-.7.6z" />'
        "</svg>"
    ),
}


def _format_command(cmd: str) -> str:
    """Highlight command tokens for authentic developer terminal styling."""
    if not cmd:
        return ""
    parts = cmd.split(" ", 1)
    binary = html.escape(parts[0])
    bin_html = f'<span class="cmd-bin">{binary}</span>'
    if len(parts) > 1:
        rest = html.escape(parts[1])
        return f'{bin_html} <span class="cmd-args">{rest}</span>'
    return bin_html


def _format_output_line(line: str) -> str:
    """Colorize output lines matching CLI tool conventions (Vitest, Docker, Git)."""
    escaped = html.escape(line)
    if escaped.startswith("PASS"):
        return (
            '<span class="badge-pass">PASS</span>'
            f'<span class="output-text-bright">{escaped[4:]}</span>'
        )
    if "✔" in escaped:
        escaped = escaped.replace("✔", '<span class="icon-check">✔</span>')
        return f'<span class="output-text">{escaped}</span>'
    if escaped.startswith("[+]"):
        escaped = escaped.replace("[+]", '<span class="icon-bracket">[+]</span>')
        return f'<span class="output-text-bright">{escaped}</span>'
    if "Tests:" in escaped:
        escaped = escaped.replace(
            "12 passed", '<span class="text-pass">12 passed</span>'
        )
        return f'<span class="output-summary">{escaped}</span>'
    return f'<span class="output-text-dim">{escaped}</span>'


def _render_powerline_bar(segments: List[Dict[str, Any]], terminal_bg: str = "#1a1a2e") -> str:
    """Render powerline segments with zero-gap vector chevron transitions."""
    parts = ['<div class="powerline-bar">']
    n = len(segments)
    for i, seg in enumerate(segments):
        bg = seg["bg"]
        fg = seg["fg"]
        text = seg["text"]
        icon_name = seg.get("icon", "")

        first_cls = " seg-first" if i == 0 else ""
        icon_svg = ICONS.get(icon_name, "")
        icon_html = f'<span class="seg-icon-box">{icon_svg}</span>' if icon_svg else ""

        # Content segment
        parts.append(
            f'<div class="seg{first_cls}" style="background-color: {bg}; color: {fg};">'
            f'{icon_html}<span class="seg-text">{html.escape(text)}</span>'
            f'</div>'
        )

        # Chevron transition: points right, filled with current segment bg,
        # placed over the next segment's bg (or terminal bg if last segment).
        next_bg = segments[i + 1]["bg"] if i + 1 < n else terminal_bg
        parts.append(
            f'<div class="chevron-box" style="background-color: {next_bg};">'
            f'<svg viewBox="0 0 16 38" preserveAspectRatio="none">'
            f'<path d="M0,0 L16,19 L0,38 Z" fill="{bg}" />'
            f'</svg>'
            f'</div>'
        )
    parts.append("</div>")
    return "".join(parts)


def generate_terminal_html(state: Dict[str, Any]) -> str:
    """Generate complete 1920x1080 HTML/SVG document representing a terminal state."""
    history = state.get("history", [])
    active_segments = state.get("segments", [])
    active_cmd = state.get("command", "")
    cursor_visible = state.get("cursor", True)

    # Render scrollback history items
    history_html_parts = []
    for item in history:
        item_segs = item.get("segments", [])
        item_cmd = item.get("command", "")
        item_output = item.get("output", [])

        bar_html = _render_powerline_bar(item_segs)
        cmd_html = _format_command(item_cmd)

        history_html_parts.append(
            f'<div class="term-row prompt-row">'
            f'{bar_html}'
            f'<div class="cmd-box">{cmd_html}</div>'
            f'</div>'
        )

        if item_output:
            output_lines = [
                f'<div class="output-line">{_format_output_line(line)}</div>'
                for line in item_output
            ]
            history_html_parts.append(
                f'<div class="term-row output-row">{"".join(output_lines)}</div>'
            )

    history_html = "".join(history_html_parts)

    # Render active prompt line
    active_bar = _render_powerline_bar(active_segments)
    formatted_active_cmd = _format_command(active_cmd)
    cursor_style = "visibility: visible;" if cursor_visible else "visibility: hidden;"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Batman Powerline Showcase</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      width: 1920px;
      height: 1080px;
      overflow: hidden;
      background: radial-gradient(ellipse at 50% 30%, #16213e 0%, #0a0c14 70%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'SF Mono', Monaco, Menlo, Consolas, 'Ubuntu Mono', 'Courier New', monospace;
      -webkit-font-smoothing: antialiased;
    }}

    /* Terminal Window Container */
    .terminal-window {{
      width: 1560px;
      height: 900px;
      background-color: #1a1a2e;
      border: 2px solid #1e3a5f;
      border-radius: 12px;
      box-shadow: 0 35px 90px rgba(0, 0, 0, 0.75), 0 0 50px rgba(30, 58, 95, 0.35);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    /* Titlebar */
    .titlebar {{
      height: 44px;
      background-color: #16213e;
      border-bottom: 1px solid #101827;
      display: flex;
      align-items: center;
      padding: 0 18px;
      position: relative;
      flex-shrink: 0;
    }}

    .window-buttons {{
      display: flex;
      gap: 9px;
      z-index: 2;
    }}

    .window-button {{
      width: 12px;
      height: 12px;
      border-radius: 50%;
    }}

    .btn-close {{ background-color: #e53e3e; }}
    .btn-minimize {{ background-color: #ecc94b; }}
    .btn-maximize {{ background-color: #38a169; }}

    .window-title {{
      position: absolute;
      left: 0;
      width: 100%;
      text-align: center;
      color: #8A92B2;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      font-size: 14px;
      font-weight: 500;
      letter-spacing: 0.2px;
      pointer-events: none;
    }}

    /* Terminal Body */
    .terminal-body {{
      flex: 1;
      padding: 36px 42px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      overflow: hidden;
    }}

    /* Row Layout */
    .term-row {{
      display: flex;
      align-items: center;
    }}

    .prompt-row {{
      min-height: 38px;
    }}

    .output-row {{
      flex-direction: column;
      align-items: flex-start;
      margin-top: -6px;
      margin-bottom: 6px;
      padding-left: 6px;
      gap: 4px;
    }}

    /* Powerline Bar & Segments */
    .powerline-bar {{
      display: flex;
      align-items: stretch;
      height: 38px;
      flex-shrink: 0;
    }}

    .seg {{
      display: inline-flex;
      align-items: center;
      padding: 0 14px;
      font-weight: 600;
      font-size: 16.5px;
      white-space: nowrap;
      height: 38px;
      line-height: 38px;
    }}

    .seg-first {{
      border-radius: 19px 0 0 19px;
      padding-left: 20px;
    }}

    .seg-icon-box {{
      display: inline-flex;
      align-items: center;
      margin-right: 8px;
    }}

    .seg-icon {{
      display: block;
    }}

    .seg-text {{
      display: inline-block;
      letter-spacing: 0.2px;
    }}

    /* Seamless Chevrons */
    .chevron-box {{
      width: 16px;
      height: 38px;
      flex-shrink: 0;
      display: block;
      position: relative;
      margin-left: -1px;
      margin-right: -1px;
      z-index: 1;
    }}

    .chevron-box svg {{
      width: 16px;
      height: 38px;
      display: block;
      shape-rendering: geometricPrecision;
    }}

    /* Command & Cursor */
    .cmd-box {{
      margin-left: 14px;
      display: flex;
      align-items: center;
      font-size: 17px;
      font-weight: 500;
      white-space: pre;
    }}

    .cmd-bin {{
      color: #ecc94b;
      font-weight: 600;
    }}

    .cmd-args {{
      color: #f7fafc;
    }}

    .cursor {{
      display: inline-block;
      width: 10px;
      height: 23px;
      background-color: #ecc94b;
      margin-left: 2px;
      vertical-align: middle;
      border-radius: 1px;
      opacity: 0.95;
    }}

    /* Terminal Output Typography */
    .output-line {{
      font-size: 15.5px;
      line-height: 25px;
      white-space: pre;
      font-family: inherit;
    }}

    .output-text {{
      color: #cbd5e0;
    }}

    .output-text-bright {{
      color: #e2e8f0;
    }}

    .output-text-dim {{
      color: #a0aec0;
    }}

    .output-summary {{
      color: #e2e8f0;
      font-weight: 600;
    }}

    .badge-pass {{
      background-color: #2f855a;
      color: #e2e8f0;
      font-weight: 700;
      font-size: 13.5px;
      padding: 2px 7px;
      border-radius: 3px;
      margin-right: 8px;
      letter-spacing: 0.5px;
    }}

    .icon-check {{
      color: #38a169;
      font-weight: bold;
    }}

    .icon-bracket {{
      color: #ecc94b;
      font-weight: bold;
    }}

    .text-pass {{
      color: #38a169;
      font-weight: bold;
    }}
  </style>
</head>
<body>
  <div class="terminal-window">
    <div class="titlebar">
      <div class="window-buttons">
        <div class="window-button btn-close"></div>
        <div class="window-button btn-minimize"></div>
        <div class="window-button btn-maximize"></div>
      </div>
      <div class="window-title">🦇 batman-powerline — zsh</div>
    </div>
    <div class="terminal-body">
      {history_html}
      <div class="term-row prompt-row">
        {active_bar}
        <div class="cmd-box">
          {formatted_active_cmd}
          <span class="cursor" style="{cursor_style}"></span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""


def render_html_for_state(state: Dict[str, Any]) -> str:
    """Alias for generate_terminal_html for interface compatibility."""
    return generate_terminal_html(state)
