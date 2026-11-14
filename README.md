# 🦇 Starship Batman Powerline Preset

[![License](https://img.shields.io/github/license/jpwhite3/starship-batman-powerline?color=805ad5)](LICENSE)
[![Starship Prompt](https://img.shields.io/badge/Starship-Prompt-ecc94b?logo=starship&logoColor=1a1a2e)](https://starship.rs)
[![Gotham Approved](https://img.shields.io/badge/Gotham-Approved-e53e3e)](https://github.com/jpwhite3/batman-tas-theme)

> A high-contrast, Dark Deco [Starship](https://starship.rs/) prompt preset inspired by **Batman: The Animated Series (1990s)** and built upon the popular `pastel-powerline` layout.

---

## The Dark Knight Prompt

`pastel-powerline` is one of Starship's most popular powerline presets, but light pastel backgrounds with default white terminal text can wash out and strain the eyes.

**Starship Batman Powerline** fixes legibility issues by pairing colors from the authentic 1990s Batman TAS palette:
- **High-contrast readability**: Dark Gotham Midnight text on bright Bat-Signal Yellow; luminous Gotham Fog text on deep villain purple, cape blue, and robin green.
- **100% Feature Parity**: Retains all Powerline glyphs, directory substitutions, git status indicators, Docker context, and 14 programming language runtimes from `pastel-powerline`.
- **Reusable Starship Palette**: Configured cleanly with a central `[palettes.batman_tas]` table.

```text
 jpwhite  …/code/batman-tas-theme   main   v26.13.1  ♥ 14:35 
```

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

## 🎨 Batman TAS Color Palette

The colors in this preset are drawn directly from the 1990s Batman animated series:

| Segment | Role | Background | Foreground | Preview |
|---|---|---|---|---|
| **OS & Username** | Start Cap / Identity | Joker Purple (`#805ad5`) | Gotham Fog (`#e2e8f0`) | ` username ` |
| **Directory** | Path & Context | Batman's Cape (`#0f3460`) | Gotham Fog (`#e2e8f0`) | `  ~/projects ` |
| **Git Branch & Status** | Version Control | Bat-Signal Yellow (`#ecc94b`) | Gotham Dark (`#1a1a2e`) | `   main ` |
| **Language Runtimes** | C, Go, Node, Rust, etc. | Robin Emerald (`#2f855a`) | Gotham Fog (`#e2e8f0`) | `   v26 ` |
| **Docker Context** | Containers | Alert Crimson (`#c53030`) | Gotham Fog (`#e2e8f0`) | `   default ` |
| **Time & End Cap** | System Clock / Close | Gotham Midnight (`#16213e`) | Silver Highlight (`#cbd5e0`) | `  ♥ 14:35  ` |

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
