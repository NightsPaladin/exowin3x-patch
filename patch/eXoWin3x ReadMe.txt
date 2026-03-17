    eXoWin3x Collection
    Cross-Platform Patch (v1.0)
    =======================================================

UNOFFICIAL — This is a personal project and is not affiliated with, endorsed
by, or supported by the eXoWin3x project or the retro-exo.com team.

DESCRIPTION
-----------
This is the cross-platform patch for the eXoWin3x collection of
Windows 3.0 / 3.1 / 3.11 games.

It adds Bash launcher scripts so all 1,138 games can be played on
both Linux and macOS.  A single .sh file per game handles both
platforms using OS-detection blocks — no separate .bsh / .msh files.


REQUIREMENTS
------------
Linux:
  - Flatpak:  https://flatpak.org
  - DOSBox-ECE flatpak:  com.retro_exo.dosbox-ece-r4482
      flatpak install flathub com.retro_exo.dosbox-ece-r4482
  - wget, curl, unzip, python3, sed  (standard on most distros)
  - Bash 5+  (Ubuntu 20.04+, Arch, Fedora, etc. all ship Bash 5)
  - aria2c  (optional — required for eXoGUI Lite mode torrent downloads)

macOS:
  - Homebrew:  https://brew.sh
  - Install dependencies via Homebrew:
      brew install bash dosbox-staging gnu-sed curl wget python3 unzip

  Optional (for eXoGUI Lite mode torrent downloads):
      brew install aria2c

    Important:
      • "bash"           — Bash 5 (macOS ships Bash 3.2)
      • "dosbox-staging" — the DOSBox emulator
      • "gnu-sed"        — GNU sed (macOS BSD sed is not compatible)


SETUP
-----
1. Copy the contents of this eXoWin3x-Patch/ folder into your
   eXoWin3x/ collection folder (merge, don't replace):

     eXoWin3x/          ← copy patch contents here
       eXo/
       Content/
       ...

2. Double-click  Setup eXoWin3x.command  (from the eXoWin3x folder).
   On macOS, Gatekeeper may ask you to allow the script — follow the
   prompts to approve it.

3. Follow the on-screen prompts.


PLAYING GAMES
-------------
After setup you can launch games in two ways:

  Via eXoGUI (recommended):
    A Python/PyQt6 GUI frontend is available for browsing and launching
    games.  See exogui-pyqt/README.md for setup instructions.
    eXoGUI also supports downloading individual game ZIPs on demand
    (Lite mode) via a local source or BitTorrent — requires aria2c and
    a torrent index file (see exogui-pyqt/README.md for details).

  Directly:
    Navigate to:  eXoWin3x/eXo/eXoWin3x/!win3x/<GameDir>/
    Double-click the  <GameName>.command  file (or run  <GameName>.sh
    in a terminal on Linux).  On first launch you will be offered the
    option to install (decompress) the game.


CONTACT
-------
Patches maintained by the eXo community.
See https://www.retro-exo.com for more information.
