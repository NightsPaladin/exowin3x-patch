# eXoWin3x — Cross-Platform Patch (v1.0)

> **Unofficial** — This is a personal project and is not affiliated with, endorsed by,
> or supported by the eXoWin3x project or the retro-exo.com team.

A personal cross-platform patch for [eXoWin3x](https://www.retro-exo.com), a curated
collection of 1,138 Windows 3.0 / 3.1 / 3.11 games. This patch adds unified Bash
launcher scripts so every game can be played on both **Linux** and **macOS** from a
single set of `.sh` files with OS-detection — no separate per-platform script pairs.

---

## Requirements

**Linux:**
- **Bash 5+** — Ubuntu 20.04+, Arch, Fedora, and most modern distros include this
- **[Flatpak](https://flatpak.org)** — used to run DOSBox-ECE
- **DOSBox-ECE** Flatpak: `com.retro_exo.dosbox-ece-r4482`
- `wget`, `curl`, `unzip`, `python3`, `sed` — standard on most distros
- `aria2c` — optional; required for eXoGUI torrent/Lite mode downloads

**macOS:**
- **macOS 12 Monterey** or later
- **[Homebrew](https://brew.sh)** — used to install emulators and utilities
- **Python 3.11+** — via Homebrew (`brew install python3`), pyenv, or mise

---

## Setup

### 1. Place the collection on a drive

The collection works from any location — internal drive, external drive, or network
share. The folder containing `eXo/`, `Content/`, and `Data/` is the **collection root**.

An external drive formatted as **exFAT** is recommended if you also want to access the
collection from Windows.

### 2. Apply this patch

Copy the contents of the patch folder into your `eXoWin3x/` collection folder,
merging with the existing structure:

```
eXoWin3x/          ← merge patch contents here
  eXo/
  Content/
  ...
```

No game data or ZIP archives are modified.

### 3. Run setup

Double-click **`Setup eXoWin3x.command`**.

On macOS, Gatekeeper may prompt you to allow the script — follow the on-screen
prompts to approve it. The setup script installs dependencies and configures the
collection for your platform.

**macOS** — installs the following via Homebrew:

| Package | Purpose |
|---------|---------|
| `dosbox-staging` | Primary emulator |
| `bash` | Bash 5 (macOS ships Bash 3.2) |
| `gnu-sed` | GNU sed (required by launch scripts) |
| `aria2` | Multi-connection download manager |
| `wget` | Fallback downloader |
| `python3` | Python runtime |

**Linux** — installs the DOSBox-ECE Flatpak if not already present.

### 4. Launch the GUI

Double-click **`exogui.command`** to open eXoGUI.

See the [eXoGUI repository](https://github.com/NightsPaladin/exogui-pyqt) for full
setup and usage documentation.

---

## Playing Games Directly

Without the GUI, navigate to:

```
eXoWin3x/eXo/eXoWin3x/!win3x/<GameDir>/
```

- **macOS / Linux GUI:** double-click the `<GameName>.command` file
- **Linux terminal:** run `<GameName>.sh`

On first launch you will be offered the option to install (decompress) the game.

---

## Emulator

| Platform | Emulator | Notes |
|----------|----------|-------|
| Linux | DOSBox-ECE (Flatpak) | `com.retro_exo.dosbox-ece-r4482` |
| macOS | DOSBox Staging | Installed via Homebrew |

---

## Community & Support

- **Discord:** https://discord.gg/37FYaUZ
- **Website:** https://www.retro-exo.com/community.html
- **Wiki:** https://wiki.retro-exo.com

---

## Acknowledgements

This patch would not exist without the foundational work of the **eXoWin3x team** —
the game configurations, per-game DOSBox settings, and the Windows collection itself
that this patch builds on top of. All of the hard work of curating and configuring
1,138 games is theirs.

- **eXoWin3x project:** https://www.retro-exo.com
- **eXoWin3x on Internet Archive:** https://archive.org/details/eXoWin3x
