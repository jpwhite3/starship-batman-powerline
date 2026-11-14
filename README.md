# 🦇 Starship Batman Powerline Preset

[![License](https://img.shields.io/github/license/jpwhite3/starship-batman-powerline?color=805ad5)](LICENSE)
[![Starship Prompt](https://img.shields.io/badge/Starship-Prompt-ecc94b?logo=starship&logoColor=1a1a2e)](https://starship.rs)
[![Gotham Approved](https://img.shields.io/badge/Gotham-Approved-e53e3e)](https://github.com/jpwhite3/batman-tas-theme)

> A high-contrast, Dark Deco [Starship](https://starship.rs/) prompt preset inspired by **Batman: The Animated Series (1990s)** and built upon the popular `pastel-powerline` layout.

<p align="center">
  <img src="assets/preview.svg" alt="Starship Batman Powerline Preview" width="100%">
</p>

---

## The Dark Knight Prompt

`pastel-powerline` is one of Starship's most popular powerline presets, but light pastel backgrounds with default white terminal text can wash out and strain the eyes.

**Starship Batman Powerline** fixes legibility issues by pairing colors from the authentic 1990s Batman TAS palette:
- **High-contrast readability**: Dark Gotham Midnight text on bright Bat-Signal Yellow; luminous Gotham Fog text on deep villain purple, cape blue, and robin green.
- **100% Feature Parity**: Retains all Powerline glyphs, directory substitutions, git status indicators, Docker context, and 14 programming language runtimes from `pastel-powerline`.
- **Reusable Starship Palette**: Configured cleanly with a central `[palettes.batman_tas]` table.

---

## 🎨 Batman TAS Color Palette

<p align="center">
  <img src="assets/palette.svg" alt="Batman TAS Color Palette" width="100%">
</p>

| Segment | Role | Background Color | Foreground Color |
|---|---|---|---|
| **OS & Username** | Start Cap / Identity | <img src="assets/swatches/joker-purple.svg" width="16" height="16" valign="middle" /> `#805ad5` Joker Purple | <img src="assets/swatches/gotham-fog.svg" width="16" height="16" valign="middle" /> `#e2e8f0` Gotham Fog |
| **Directory** | Path & Context | <img src="assets/swatches/cape-blue.svg" width="16" height="16" valign="middle" /> `#0f3460` Batman's Cape | <img src="assets/swatches/gotham-fog.svg" width="16" height="16" valign="middle" /> `#e2e8f0` Gotham Fog |
| **Git Branch & Status** | Version Control | <img src="assets/swatches/signal-yellow.svg" width="16" height="16" valign="middle" /> `#ecc94b` Bat-Signal Yellow | <img src="assets/swatches/gotham-dark.svg" width="16" height="16" valign="middle" /> `#1a1a2e` Gotham Dark |
| **Language Runtimes** | C, Go, Node, Rust, etc. | <img src="assets/swatches/robin-green.svg" width="16" height="16" valign="middle" /> `#2f855a` Robin Emerald | <img src="assets/swatches/gotham-fog.svg" width="16" height="16" valign="middle" /> `#e2e8f0` Gotham Fog |
| **Docker Context** | Containers | <img src="assets/swatches/alert-crimson.svg" width="16" height="16" valign="middle" /> `#c53030` Alert Crimson | <img src="assets/swatches/gotham-fog.svg" width="16" height="16" valign="middle" /> `#e2e8f0` Gotham Fog |
| **Time & End Cap** | System Clock / Close | <img src="assets/swatches/gotham-midnight.svg" width="16" height="16" valign="middle" /> `#16213e` Gotham Midnight | <img src="assets/swatches/silver-highlight.svg" width="16" height="16" valign="middle" /> `#cbd5e0` Silver Highlight |

---

## ⚡ Quick Install

### Prerequisites
- [Starship](https://starship.rs/) installed (`starship --version`)
- A [Nerd Font](https://www.nerdfonts.com/) installed and set in your terminal (e.g. FiraCode Nerd Font, JetBrainsMono Nerd Font)

### One-Line Install (Recommended)

Run in your terminal to back up your current configuration and install the Batman Powerline preset:

```bash
# Backup existing starship configuration (if present)
[ -f ~/.config/starship.toml ] && cp ~/.config/starship.toml ~/.config/starship.toml.bak

# Download the Batman Powerline preset
curl -fsSL https://raw.githubusercontent.com/jpwhite3/starship-batman-powerline/main/starship.toml -o ~/.config/starship.toml
```

### Manual Install

```bash
# Clone the repository
git clone https://github.com/jpwhite3/starship-batman-powerline.git

# Copy into Starship's configuration directory
cp starship-batman-powerline/starship.toml ~/.config/starship.toml
```

---

## 🛠️ Supported Language Runtimes

Includes full symbol and version detection for 14+ language runtimes:
`Node.js` • `Bun` • `Rust` • `Go` • `Python` • `C/C++` • `Java` • `Kotlin` • `Gradle` • `Maven` • `Elixir` • `Elm` • `Haskell` • `Julia` • `Nim` • `Scala`

---

## 🦇 Companion VS Code Theme

Love this aesthetic in your terminal? Bring Gotham City into your code editor too with the **[Batman TAS Theme for VS Code](https://github.com/jpwhite3/batman-tas-theme)**!

---

## 📄 License

[MIT](LICENSE) © [John White (jpwhite3)](https://github.com/jpwhite3)
