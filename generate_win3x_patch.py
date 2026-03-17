#!/usr/bin/env python3
"""
generate_win3x_patch.py
Generates the eXoWin3x Cross-Platform Patch from the base eXoWin3x Windows
collection.  Produces a single unified patch (eXoWin3x-Patch/) that supports
both Linux and macOS using .sh files with OS-detection if-blocks for any
platform-specific steps.  .command files are provided for double-click
launching on both platforms.

Usage:
    python3 generate_win3x_patch.py [--win3x-dir PATH] [--output-dir PATH]

Reads:  eXoWin3x/Content/!Win3Xmetadata.zip  (per-game Windows scripts)
Writes: eXoWin3x-Patch/                       (distributable patch directory)
"""

import argparse
import os
import re
import stat
import sys
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR     = Path(__file__).resolve().parent
DEFAULT_WIN3X  = SCRIPT_DIR / "eXoWin3x"
DEFAULT_OUTPUT = SCRIPT_DIR / "eXoWin3x-Patch"

# ---------------------------------------------------------------------------
# Constant text: boilerplate shared by every per-game .sh script
# ---------------------------------------------------------------------------
SH_HEADER = r"""#!/usr/bin/env bash
if [[ "$LD_PRELOAD" =~ "gameoverlayrenderer" ]]
then
    LD_PRELOAD=""
fi
[[ $0 == $BASH_SOURCE ]] && cd "$( dirname "$0")"
scriptDir="$(cd "$( dirname "$BASH_SOURCE")" && pwd)"
[ $# -gt 0 ] && parameterone="$1"
[ $# -gt 1 ] && parametertwo="$2"
[ $# -gt 2 ] && parameterthree="$3"
[ $# -gt 3 ] && parameterfour="$4"

if [ "${BASH_VERSINFO:-0}" -lt 5 ]
then
    printf "\n\e[1;31;47mThe version of bash currently running is too old.\e[0m\n\n"
    if [[ "$OSTYPE" == "darwin"* ]]
    then
        printf "Install Bash 5 via Homebrew:  brew install bash\n"
    else
        printf "Please run the \e[1;33;40minstall_dependencies.command\e[0m script.\n"
        printf "Then, follow the instructions to install the required dependencies.\n"
    fi
    read -s -n 1 -p "Press any key to abort."
    printf "\n\n"
    exit 0
fi

if [[ "$OSTYPE" == "darwin"* ]]
then
    for _p in /opt/homebrew/bin /opt/homebrew/sbin /usr/local/bin /usr/local/sbin
    do
        [[ -d "$_p" && ":$PATH:" != *":$_p:"* ]] && export PATH="$_p:$PATH"
    done
    unset _p
fi

if [[ "$OSTYPE" == "darwin"* ]]; then _SED=gsed; else _SED=sed; fi

function goto
{
    shortcutName=$1
    newPosition=$(${_SED} -n -e "/: $shortcutName$/{:a;n;p;ba};" "$scriptDir/$(basename -- "$BASH_SOURCE")" )
    eval "$newPosition"
    exit
}
alias :="goto"

function dynchoice
{
    local choices="$1"
    local textpmt="$2"
    local numofchoices="${#choices}"
    local choicesu="${choices^^}"
    local choicesl="${choices,,}"
    if [ "$numofchoices" -eq 10 ]
    then
        while true
        do
            read -p "$textpmt " choice
            case $choice in
                [${choicesu:0:1}${choicesl:0:1}]* ) errorlevel=1
                        break;;
                [${choicesu:1:1}${choicesl:1:1}]* ) errorlevel=2
                        break;;
                [${choicesu:2:1}${choicesl:2:1}]* ) errorlevel=3
                        break;;
                [${choicesu:3:1}${choicesl:3:1}]* ) errorlevel=4
                        break;;
                [${choicesu:4:1}${choicesl:4:1}]* ) errorlevel=5
                        break;;
                [${choicesu:5:1}${choicesl:5:1}]* ) errorlevel=6
                        break;;
                [${choicesu:6:1}${choicesl:6:1}]* ) errorlevel=7
                        break;;
                [${choicesu:7:1}${choicesl:7:1}]* ) errorlevel=8
                        break;;
                [${choicesu:8:1}${choicesl:8:1}]* ) errorlevel=9
                        break;;
                [${choicesu:9:1}${choicesl:9:1}]* ) errorlevel=10
                        break;;
                *     ) printf "Invalid input.\n";;
            esac
        done
    elif [ "$numofchoices" -eq 9 ]
    then
        while true
        do
            read -p "$textpmt " choice
            case $choice in
                [${choicesu:0:1}${choicesl:0:1}]* ) errorlevel=1
                        break;;
                [${choicesu:1:1}${choicesl:1:1}]* ) errorlevel=2
                        break;;
                [${choicesu:2:1}${choicesl:2:1}]* ) errorlevel=3
                        break;;
                [${choicesu:3:1}${choicesl:3:1}]* ) errorlevel=4
                        break;;
                [${choicesu:4:1}${choicesl:4:1}]* ) errorlevel=5
                        break;;
                [${choicesu:5:1}${choicesl:5:1}]* ) errorlevel=6
                        break;;
                [${choicesu:6:1}${choicesl:6:1}]* ) errorlevel=7
                        break;;
                [${choicesu:7:1}${choicesl:7:1}]* ) errorlevel=8
                        break;;
                [${choicesu:8:1}${choicesl:8:1}]* ) errorlevel=9
                        break;;
                *     ) printf "Invalid input.\n";;
            esac
        done
    elif [ "$numofchoices" -eq 8 ]
    then
        while true
        do
            read -p "$textpmt " choice
            case $choice in
                [${choicesu:0:1}${choicesl:0:1}]* ) errorlevel=1
                        break;;
                [${choicesu:1:1}${choicesl:1:1}]* ) errorlevel=2
                        break;;
                [${choicesu:2:1}${choicesl:2:1}]* ) errorlevel=3
                        break;;
                [${choicesu:3:1}${choicesl:3:1}]* ) errorlevel=4
                        break;;
                [${choicesu:4:1}${choicesl:4:1}]* ) errorlevel=5
                        break;;
                [${choicesu:5:1}${choicesl:5:1}]* ) errorlevel=6
                        break;;
                [${choicesu:6:1}${choicesl:6:1}]* ) errorlevel=7
                        break;;
                [${choicesu:7:1}${choicesl:7:1}]* ) errorlevel=8
                        break;;
                *     ) printf "Invalid input.\n";;
            esac
        done
    elif [ "$numofchoices" -eq 7 ]
    then
        while true
        do
            read -p "$textpmt " choice
            case $choice in
                [${choicesu:0:1}${choicesl:0:1}]* ) errorlevel=1
                        break;;
                [${choicesu:1:1}${choicesl:1:1}]* ) errorlevel=2
                        break;;
                [${choicesu:2:1}${choicesl:2:1}]* ) errorlevel=3
                        break;;
                [${choicesu:3:1}${choicesl:3:1}]* ) errorlevel=4
                        break;;
                [${choicesu:4:1}${choicesl:4:1}]* ) errorlevel=5
                        break;;
                [${choicesu:5:1}${choicesl:5:1}]* ) errorlevel=6
                        break;;
                [${choicesu:6:1}${choicesl:6:1}]* ) errorlevel=7
                        break;;
                *     ) printf "Invalid input.\n";;
            esac
        done
    elif [ "$numofchoices" -eq 6 ]
    then
        while true
        do
            read -p "$textpmt " choice
            case $choice in
                [${choicesu:0:1}${choicesl:0:1}]* ) errorlevel=1
                        break;;
                [${choicesu:1:1}${choicesl:1:1}]* ) errorlevel=2
                        break;;
                [${choicesu:2:1}${choicesl:2:1}]* ) errorlevel=3
                        break;;
                [${choicesu:3:1}${choicesl:3:1}]* ) errorlevel=4
                        break;;
                [${choicesu:4:1}${choicesl:4:1}]* ) errorlevel=5
                        break;;
                [${choicesu:5:1}${choicesl:5:1}]* ) errorlevel=6
                        break;;
                *     ) printf "Invalid input.\n";;
            esac
        done
    elif [ "$numofchoices" -eq 5 ]
    then
        while true
        do
            read -p "$textpmt " choice
            case $choice in
                [${choicesu:0:1}${choicesl:0:1}]* ) errorlevel=1
                        break;;
                [${choicesu:1:1}${choicesl:1:1}]* ) errorlevel=2
                        break;;
                [${choicesu:2:1}${choicesl:2:1}]* ) errorlevel=3
                        break;;
                [${choicesu:3:1}${choicesl:3:1}]* ) errorlevel=4
                        break;;
                [${choicesu:4:1}${choicesl:4:1}]* ) errorlevel=5
                        break;;
                *     ) printf "Invalid input.\n";;
            esac
        done
    elif [ "$numofchoices" -eq 4 ]
    then
        while true
        do
            read -p "$textpmt " choice
            case $choice in
                [${choicesu:0:1}${choicesl:0:1}]* ) errorlevel=1
                        break;;
                [${choicesu:1:1}${choicesl:1:1}]* ) errorlevel=2
                        break;;
                [${choicesu:2:1}${choicesl:2:1}]* ) errorlevel=3
                        break;;
                [${choicesu:3:1}${choicesl:3:1}]* ) errorlevel=4
                        break;;
                *     ) printf "Invalid input.\n";;
            esac
        done
    elif [ "$numofchoices" -eq 3 ]
    then
        while true
        do
            read -p "$textpmt " choice
            case $choice in
                [${choicesu:0:1}${choicesl:0:1}]* ) errorlevel=1
                        break;;
                [${choicesu:1:1}${choicesl:1:1}]* ) errorlevel=2
                        break;;
                [${choicesu:2:1}${choicesl:2:1}]* ) errorlevel=3
                        break;;
                *     ) printf "Invalid input.\n";;
            esac
        done
    elif [ "$numofchoices" -eq 2 ]
    then
        while true
        do
            read -p "$textpmt " choice
            case $choice in
                [${choicesu:0:1}${choicesl:0:1}]* ) errorlevel=1
                        break;;
                [${choicesu:1:1}${choicesl:1:1}]* ) errorlevel=2
                        break;;
                *     ) printf "Invalid input.\n";;
            esac
        done
    fi
}
"""

# Combined dependency check block
SH_DEPCHECK = r"""
# Source exo_lib_win3x.sh for shared helpers (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]
then
    _EXO_LIB="$(cd "$scriptDir/../../../util" 2>/dev/null && pwd)/exo_lib_win3x.sh"
    if [[ -f "$_EXO_LIB" ]]; then source "$_EXO_LIB"; fi
fi

missingDependencies=no
if [[ "$OSTYPE" == "darwin"* ]]
then
    for _t in dosbox-staging gsed curl python3 unzip wget
    do
        ! command -v "$_t" &>/dev/null && missingDependencies=yes
    done
elif [[ "$OSTYPE" == "linux-gnu"* ]]
then
    ! [[ `which flatpak` ]] && missingDependencies=yes
    ! [[ `flatpak list 2>/dev/null | grep "retro_exo\.dosbox-ece-r4482"` ]] && missingDependencies=yes
    ! [[ `which curl` ]] && missingDependencies=yes
    ! [[ `which python3` ]] && missingDependencies=yes
    ! [[ `which sed` ]] && missingDependencies=yes
    ! [[ `which unzip` ]] && missingDependencies=yes
    ! [[ `which wget` ]] && missingDependencies=yes
else
    missingDependencies=yes
fi

if [ $missingDependencies == "yes" ]
then
    printf "\n\e[1;31;47mOne or more dependencies are missing.\e[0m\n\n"
    if [[ "$OSTYPE" == "darwin"* ]]
    then
        printf "Install with Homebrew:\n"
        printf "   brew install bash dosbox-staging gnu-sed curl wget python3 unzip\n\n"
    else
        printf "Please run the \e[1;33;40minstall_dependencies.command\e[0m script.\n"
        printf "Then, follow the instructions to install the required dependencies.\n"
    fi
    read -s -n 1 -p "Press any key to abort."
    printf "\n\n"
    exit 0
fi
"""

# Footer for per-game launch .sh
LAUNCH_SH_FOOTER = r"""
var="${PWD}"
for i in .
do
    gamedir="${PWD##*/}"
done
for f in *\).sh
do
    gamename2="${f}"
done
gamename="${gamename2::-3}"
indexname="${gamename::-7}"
cd ..
cd ..
cd ..
eval source ./util/launch.sh && exit 0
[[ $0 != $BASH_SOURCE ]] && return
"""

# Footer for per-game install .sh
INSTALL_SH_FOOTER = r"""
folder="${PWD}"
eval source ../../../util/install.sh && exit 0
: exit
[[ $0 != $BASH_SOURCE ]] && return
"""

# Footer for Extras/Alternate Launcher .sh
ALT_SH_FOOTER = r"""
cd ..
var="${PWD}"
for i in .
do
    gamedir="${PWD##*/}"
done
for f in *\).sh
do
    gamename2="${f}"
done
gamename="${gamename2::-3}"
indexname="${gamename::-7}"
cd ..
cd ..
cd ..
eval source ./util/AltLauncher.sh && exit 0
[[ $0 != $BASH_SOURCE ]] && return
"""

# .command file — terminal-launcher for both Linux and macOS.
# On Linux it detects and opens a terminal emulator, then sources the .sh.
# On macOS the file is opened directly in Terminal.app, so it sources .sh directly.
COMMAND_TEMPLATE = r"""#!/usr/bin/env bash
if [[ "$LD_PRELOAD" =~ "gameoverlayrenderer" ]]
then
    LD_PRELOAD=""
fi
cd "$( dirname "$BASH_SOURCE")"

if [[ "$OSTYPE" == "linux-gnu"* ]]
then
    if [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "konsole" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "gnome-terminal-" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "xfce4-terminal" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "kgx" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "xterm" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "Eterm" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "x-terminal-emul" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "mate-terminal" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "terminator" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "urxvt" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "rxvt" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "termit" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "terminology" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "tilix" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "kitty" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "aterm" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
        exit 0
    elif [ `which konsole` ]
    then
        konsole -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which gnome-terminal` ]
    then
        gnome-terminal -- /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which xfce4-terminal` ]
    then
        xfce4-terminal -x /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which kgx` ]
    then
        kgx -e "/usr/bin/env bash \"$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")\" $@" &
        exit 0
    elif [ `which xterm` ]
    then
        xterm -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which uxterm` ]
    then
        uxterm -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which eterm` ]
    then
        Eterm -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which x-terminal-emulator` ]
    then
        x-terminal-emulator -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which mate-terminal` ]
    then
        eval mate-terminal -e \"/usr/bin/env bash \\\"$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")\\\" $@\" "$@" &
        exit 0
    elif [ `which terminator` ]
    then
        terminator -x /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which urxvt` ]
    then
        urxvt -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which rxvt` ]
    then
        rxvt -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which termit` ]
    then
        termit -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which lxterm` ]
    then
        lxterm -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which terminology` ]
    then
        terminology -e "/usr/bin/env bash \"$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")\" $@" &
        exit 0
    elif [ `which tilix` ]
    then
        tilix -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which kitty` ]
    then
        kitty -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    elif [ `which aterm` ]
    then
        aterm -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")" "$@" &
        exit 0
    else
        exit ERRCODE "Weird system achievement unlocked: None of the 18 supported terminal emulators are installed."
    fi
elif [[ "$OSTYPE" == "darwin"* ]]
then
    source "$PWD/$(basename -- "${BASH_SOURCE%.command}.sh")"
    exit 0
else
    exit ERRCODE "Unsupported OS"
fi
"""

# ---------------------------------------------------------------------------
# Global launch.sh — cross-platform DOSBox launcher
# ---------------------------------------------------------------------------
GLOBAL_LAUNCH_SH = r"""#!/usr/bin/env bash
# launch.sh — eXoWin3x cross-platform game launcher (Linux and macOS).
# Sourced (not executed directly) from per-game .sh scripts.
if [[ "$LD_PRELOAD" =~ "gameoverlayrenderer" ]]
then
    LD_PRELOAD=""
fi
[[ $0 == $BASH_SOURCE ]] && cd "$( dirname "$0")"
scriptDir="$(cd "$( dirname "$BASH_SOURCE")" && pwd)"

if [ "${BASH_VERSINFO:-0}" -lt 5 ]
then
    if [[ "$OSTYPE" == "darwin"* ]]
    then
        printf "\n\e[1;31;47mBash 5 is required.  brew install bash\e[0m\n\n"
    else
        printf "\n\e[1;31;47mThe version of bash currently running is too old.\e[0m\n\n"
        printf "Please run the \e[1;33;40minstall_dependencies.command\e[0m script.\n"
        printf "Then, follow the instructions to install the required dependencies.\n"
    fi
    read -s -n 1 -p "Press any key to abort."
    printf "\n\n"
    exit 0
fi

if [[ "$OSTYPE" == "darwin"* ]]
then
    for _p in /opt/homebrew/bin /opt/homebrew/sbin /usr/local/bin /usr/local/sbin
    do
        [[ -d "$_p" && ":$PATH:" != *":$_p:"* ]] && export PATH="$_p:$PATH"
    done
    unset _p
fi

if [[ "$OSTYPE" == "darwin"* ]]; then _SED=gsed; else _SED=sed; fi

declare -a scriptDirStack

function goto
{
    shortcutName=$1
    newPosition=$(${_SED} -n -e "/: $shortcutName$/{:a;n;p;ba};" "$scriptDir/$(basename -- "$BASH_SOURCE")" )
    eval "$newPosition"
    exit
}
alias :="goto"

# Apply global display-preference overrides from SEL files
if [[ "$OSTYPE" == "darwin"* ]]
then
    [ -e ./util/AYES.SEL ] && gsed -i "s|aspect=false|aspect=true|g"   ./emulators/dosbox/options_macos.conf
    [ -e ./util/ANO.SEL ]  && gsed -i "s|aspect=true|aspect=false|g"   ./emulators/dosbox/options_macos.conf
    [ -e ./util/FULL.SEL ] && gsed -i "s|fullscreen=false|fullscreen=true|g"  ./emulators/dosbox/options_macos.conf
    [ -e ./util/WIN.SEL ]  && gsed -i "s|fullscreen=true|fullscreen=false|g"  ./emulators/dosbox/options_macos.conf
    [ -e ./util/SML.SEL ]  && gsed -i "s|windowresolution=1280x960|windowresolution=640x480|g"   ./emulators/dosbox/options_macos.conf
    [ -e ./util/SML.SEL ]  && gsed -i "s|windowresolution=2560x1920|windowresolution=640x480|g"  ./emulators/dosbox/options_macos.conf
    [ -e ./util/MED.SEL ]  && gsed -i "s|windowresolution=640x480|windowresolution=1280x960|g"   ./emulators/dosbox/options_macos.conf
    [ -e ./util/MED.SEL ]  && gsed -i "s|windowresolution=2560x1920|windowresolution=1280x960|g" ./emulators/dosbox/options_macos.conf
    [ -e ./util/LRG.SEL ]  && gsed -i "s|windowresolution=640x480|windowresolution=2560x1920|g"  ./emulators/dosbox/options_macos.conf
    [ -e ./util/LRG.SEL ]  && gsed -i "s|windowresolution=1280x960|windowresolution=2560x1920|g" ./emulators/dosbox/options_macos.conf
else
    [ -e ./util/AYES.SEL ] && sed -i -e "s|aspect=false|aspect=true|g" ./emulators/dosbox/options_linux.conf
    [ -e ./util/ANO.SEL ]  && sed -i -e "s|aspect=true|aspect=false|g" ./emulators/dosbox/options_linux.conf
    [ -e ./util/FULL.SEL ] && sed -i -e "s|fullscreen=false|fullscreen=true|g" ./emulators/dosbox/options_linux.conf
    [ -e ./util/WIN.SEL ]  && sed -i -e "s|fullscreen=true|fullscreen=false|g" ./emulators/dosbox/options_linux.conf
    [ -e ./util/SML.SEL ]  && sed -i -e "s|windowresolution=1280x960|windowresolution=640x480|g"   ./emulators/dosbox/options_linux.conf
    [ -e ./util/SML.SEL ]  && sed -i -e "s|windowresolution=2560x1920|windowresolution=640x480|g"  ./emulators/dosbox/options_linux.conf
    [ -e ./util/MED.SEL ]  && sed -i -e "s|windowresolution=640x480|windowresolution=1280x960|g"   ./emulators/dosbox/options_linux.conf
    [ -e ./util/MED.SEL ]  && sed -i -e "s|windowresolution=2560x1920|windowresolution=1280x960|g" ./emulators/dosbox/options_linux.conf
    [ -e ./util/LRG.SEL ]  && sed -i -e "s|windowresolution=640x480|windowresolution=2560x1920|g"  ./emulators/dosbox/options_linux.conf
    [ -e ./util/LRG.SEL ]  && sed -i -e "s|windowresolution=1280x960|windowresolution=2560x1920|g" ./emulators/dosbox/options_linux.conf
fi

goto english && [[ $0 != $BASH_SOURCE ]] && return

: english
[ ! -e ./eXoWin3x/"${gamedir}"/ ] && goto none && [[ $0 != $BASH_SOURCE ]] && return

: launch
if [[ "$OSTYPE" == "darwin"* ]]
then
    dosindex=$(grep -i "^${gamename}" ./util/dosbox_macos.txt 2>/dev/null | tail -1 | tr -d '\r')
    dosbox="${dosindex#*:}"
    dosbox="${dosbox#*:}"
    [ -z "$dosbox" ] && dosbox="dosbox-staging"
else
    dosindex=`grep -i "^${gamename}" ./util/dosbox_linux.txt 2>/dev/null | tail -1 | tr -d "\r"`
    dosbox1="${dosindex#*:}"
    dosbox="${dosbox1#*:}"
    [ -z "$dosbox" ] && dosbox="flatpak run com.retro_exo.dosbox-ece-r4482"
fi

: start
clear
local_conf="${var}/dosbox_linux.conf"
[ ! -e "$local_conf" ] && local_conf="${var}/dosbox.conf"
if [[ "$OSTYPE" == "darwin"* ]]
then
    [ -e "${var}/dosbox2_linux.conf" ] && local_conf="${var}/dosbox2_linux.conf"
    [ ! -e "${var}/dosbox2_linux.conf" ] && [ -e "${var}/dosbox2.conf" ] && local_conf="${var}/dosbox2.conf"
    read -ra _dosbox_cmd <<< "$dosbox"
    "${_dosbox_cmd[@]}" \
        -conf "${local_conf}" \
        -conf "./emulators/dosbox/options_macos.conf" \
        -nomenu -noconsole
else
    [ -e "${var}/dosbox2_linux.conf" ] && local_conf="${var}/dosbox2_linux.conf"
    eval "$(echo "${dosbox}" | sed -e "s/\\$/\\\\$/g")" \
        -conf "\"$(echo "${local_conf}" | sed -e "s/\\$/\\\\$/g")\"" \
        -conf "\"./emulators/dosbox/options_linux.conf\"" \
        -nomenu -noconsole
fi
rm -f stdout.txt stderr.txt
[[ "$(ls -1 glide.* 2>/dev/null | wc -l)" -gt 0 ]] && rm -f glide.*
[ -e ./eXoWin3x/CWSDPMI.swp ] && rm -f ./eXoWin3x/CWSDPMI.swp
goto end && [[ $0 != $BASH_SOURCE ]] && return

: none
clear
echo ""
echo "Game has not been installed"
echo ""
echo ""
echo "Would you like to install the game?"
echo ""
while true
do
    read -p "(y/n)? " choice
    case $choice in
        [Yy]* ) errorlevel=1
                break;;
        [Nn]* ) errorlevel=2
                break;;
        *     ) printf "Invalid input.\n";;
    esac
done

[ $errorlevel == '2' ] && goto no  && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '1' ] && goto yes && [[ $0 != $BASH_SOURCE ]] && return

: yes
cd "${var}"
scriptDirStack["${#scriptDirStack[@]}"]="$scriptDir"
eval source install.sh
scriptDir="${scriptDirStack["${#scriptDirStack[@]}"-1]}"
unset scriptDirStack["${#scriptDirStack[@]}"-1]
function goto
{
    shortcutName=$1
    newPosition=$(${_SED} -n -e "/: $shortcutName$/{:a;n;p;ba};" "$scriptDir/$(basename -- "$BASH_SOURCE")" )
    eval "$newPosition"
    exit
}
cd ..
clear
goto launch && [[ $0 != $BASH_SOURCE ]] && return

: no
goto end && [[ $0 != $BASH_SOURCE ]] && return

: end
[[ $0 != $BASH_SOURCE ]] && return
"""

# ---------------------------------------------------------------------------
# Global install.sh — cross-platform game installer
# ---------------------------------------------------------------------------
GLOBAL_INSTALL_SH = r"""#!/usr/bin/env bash
# install.sh — eXoWin3x cross-platform game installer (Linux and macOS).
if [[ "$LD_PRELOAD" =~ "gameoverlayrenderer" ]]
then
    LD_PRELOAD=""
fi
[[ $0 == $BASH_SOURCE ]] && cd "$( dirname "$0")"
scriptDir="$(cd "$( dirname "$BASH_SOURCE")" && pwd)"
[ $# -gt 0 ] && parameterone="$1"

if [ "${BASH_VERSINFO:-0}" -lt 5 ]
then
    if [[ "$OSTYPE" == "darwin"* ]]
    then
        printf "\n\e[1;31;47mBash 5 is required.  brew install bash\e[0m\n\n"
    else
        printf "\n\e[1;31;47mThe version of bash currently running is too old.\e[0m\n\n"
        printf "Please run the \e[1;33;40minstall_dependencies.command\e[0m script.\n"
        printf "Then, follow the instructions to install the required dependencies.\n"
    fi
    read -s -n 1 -p "Press any key to abort."
    printf "\n\n"
    exit 0
fi

if [[ "$OSTYPE" == "darwin"* ]]
then
    for _p in /opt/homebrew/bin /opt/homebrew/sbin /usr/local/bin /usr/local/sbin
    do
        [[ -d "$_p" && ":$PATH:" != *":$_p:"* ]] && export PATH="$_p:$PATH"
    done
    unset _p
fi

if [[ "$OSTYPE" == "darwin"* ]]; then _SED=gsed; else _SED=sed; fi

function goto
{
    shortcutName=$1
    newPosition=$(${_SED} -n -e "/: $shortcutName$/{:a;n;p;ba};" "$scriptDir/$(basename -- "$BASH_SOURCE")" )
    eval "$newPosition"
    exit
}
alias :="goto"

conf="${folder}"

goto start && [[ $0 != $BASH_SOURCE ]] && return

: start
if [ -e ./eXoWin3x/"${gamedir}"/ ]
then
    goto dele
fi

: check
if [ -e "./eXoWin3x/${gamename}.zip" ]
then
    goto unzip
fi

: download
clear
echo ""
echo "It appears you have not downloaded this game yet."
echo ""
echo "${gamename}"
echo ""
echo "Would you like to download it?"
echo ""
while true
do
    read -p "[Y]es or [N]o " choice
    case $choice in
        [Yy]* ) errorlevel=1
                break;;
        [Nn]* ) errorlevel=2
                break;;
        *     ) printf "Invalid input.\n";;
    esac
done

[ $errorlevel == '2' ] && goto end && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '1' ] && goto dl  && [[ $0 != $BASH_SOURCE ]] && return

: dl
[ -e ./eXoWin3x/inprogress.txt ] && goto inprogress && [[ $0 != $BASH_SOURCE ]] && return
touch ./eXoWin3x/inprogress.txt
cd eXoWin3x
if command -v wget &>/dev/null
then
    wget -np -c -R "index.html*" "https://exorlp.xyz/public/eXo/eXoWin3x/Games/${gamename}.zip"
else
    curl -L -C - -o "${gamename}.zip" "https://exorlp.xyz/public/eXo/eXoWin3x/Games/${gamename}.zip"
fi
cd ..
rm -f ./eXoWin3x/inprogress.txt
clear
echo ""
if [ -e "./eXoWin3x/${gamename}.zip" ]
then
    echo "Game Downloaded Successfully"
else
    echo "There was an error downloading the game. Exiting..."
    read -s -n 1 -p "Press any key to continue..."
    printf "\n\n"
    goto end && [[ $0 != $BASH_SOURCE ]] && return
fi
goto unzip && [[ $0 != $BASH_SOURCE ]] && return

: unzip
cd eXoWin3x
unzip -o "${gamename}.zip"
cd ..
goto config && [[ $0 != $BASH_SOURCE ]] && return

: dele
clear
echo ""
echo "This game is already installed."
echo ""
echo "Would you like to [R]einstall, [U]ninstall, or [C]ancel?"
echo ""
while true
do
    read -p "[R/U/C]? " choice
    case $choice in
        [Rr]* ) errorlevel=1
                break;;
        [Uu]* ) errorlevel=2
                break;;
        [Cc]* ) errorlevel=3
                break;;
        *     ) printf "Invalid input.\n";;
    esac
done

[ $errorlevel == '3' ] && goto end           && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '2' ] && goto erase         && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '1' ] && goto erase_reinstall && [[ $0 != $BASH_SOURCE ]] && return

: erase_reinstall
rm -rf ./eXoWin3x/"${gamedir}"/
goto check && [[ $0 != $BASH_SOURCE ]] && return

: config
clear
echo ""
echo "Would you like to enable Aspect Correction?"
echo ""
while true
do
    read -p "[Y]es or [N]o " choice
    case $choice in
        [Yy]* ) errorlevel=1
                break;;
        [Nn]* ) errorlevel=2
                break;;
        *     ) printf "Invalid input.\n";;
    esac
done

[ $errorlevel == '2' ] && goto aspect2 && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '1' ] && goto aspect  && [[ $0 != $BASH_SOURCE ]] && return

: aspect
_conf_file="${conf}/dosbox_linux.conf"
[ ! -e "$_conf_file" ] && _conf_file="${conf}/dosbox.conf"
${_SED} -i "s|aspect=false|aspect=true|g" "$_conf_file"
goto next && [[ $0 != $BASH_SOURCE ]] && return

: aspect2
_conf_file="${conf}/dosbox_linux.conf"
[ ! -e "$_conf_file" ] && _conf_file="${conf}/dosbox.conf"
${_SED} -i "s|aspect=true|aspect=false|g" "$_conf_file"

: next
clear
echo ""
echo "Would you like [F]ullscreen or [W]indowed?"
echo ""
while true
do
    read -p "[F/W]? " choice
    case $choice in
        [Ff]* ) errorlevel=1
                break;;
        [Ww]* ) errorlevel=2
                break;;
        *     ) printf "Invalid input.\n";;
    esac
done

[ $errorlevel == '2' ] && goto wind && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '1' ] && goto full && [[ $0 != $BASH_SOURCE ]] && return

: wind
_conf_file="${conf}/dosbox_linux.conf"; [ ! -e "$_conf_file" ] && _conf_file="${conf}/dosbox.conf"
${_SED} -i "s|fullscreen=true|fullscreen=false|g" "$_conf_file"
goto scaler1 && [[ $0 != $BASH_SOURCE ]] && return

: full
_conf_file="${conf}/dosbox_linux.conf"; [ ! -e "$_conf_file" ] && _conf_file="${conf}/dosbox.conf"
${_SED} -i "s|fullscreen=false|fullscreen=true|g" "$_conf_file"
goto scaler1 && [[ $0 != $BASH_SOURCE ]] && return

: scaler1
clear
echo ""
echo "Would you like to change your graphics scaler/filter?"
echo ""
while true
do
    read -p "[Y]es or [N]o " choice
    case $choice in
        [Yy]* ) errorlevel=1
                break;;
        [Nn]* ) errorlevel=2
                break;;
        *     ) printf "Invalid input.\n";;
    esac
done

[ $errorlevel == '2' ] && goto end && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '1' ] && goto sy  && [[ $0 != $BASH_SOURCE ]] && return

: sy
clear
echo ""
echo "Press 1 for no scaler"
echo "Press 2 for normal3x"
echo "Press 3 for hq2x"
echo "Press 4 for hq3x"
echo "Press 5 for 2xsai"
echo "Press 6 for super2xsai"
echo "press 7 for advmame2x"
echo "press 8 for advmame3x"
echo "press 9 for tv2x"
echo "Press 0 for normal2x"
echo ""
while true
do
    read -p "Please choose (0-9): " choice
    case $choice in
        [1] ) errorlevel=1;  break;;
        [2] ) errorlevel=2;  break;;
        [3] ) errorlevel=3;  break;;
        [4] ) errorlevel=4;  break;;
        [5] ) errorlevel=5;  break;;
        [6] ) errorlevel=6;  break;;
        [7] ) errorlevel=7;  break;;
        [8] ) errorlevel=8;  break;;
        [9] ) errorlevel=9;  break;;
        [0] ) errorlevel=10; break;;
        *   ) printf "Invalid input.\n";;
    esac
done

[ $errorlevel == '10' ] && goto normal2x && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '9'  ] && goto scaltv2x && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '8'  ] && goto scalam3x && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '7'  ] && goto scalam2x && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '6'  ] && goto scals2xs && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '5'  ] && goto scal2xs  && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '4'  ] && goto scalhq3x && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '3'  ] && goto scalhq2x && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '2'  ] && goto scaln3x  && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '1'  ] && goto scalno   && [[ $0 != $BASH_SOURCE ]] && return

: scalno
sc=none;       goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scaln3x
sc=normal3x;   goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scalhq2x
sc=hq2x;       goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scalhq3x
sc=hq3x;       goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scal2xs
sc=2xsai;      goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scals2xs
sc=super2xsai; goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scalam2x
sc=advmame2x;  goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scalam3x
sc=advmame3x;  goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scaltv2x
sc=tv2x;       goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: normal2x
sc=normal2x

: scaler
_conf_file="${conf}/dosbox_linux.conf"; [ ! -e "$_conf_file" ] && _conf_file="${conf}/dosbox.conf"
for _s in none normal3x hq2x hq3x 2xsai super2xsai advmame2x advmame3x tv2x normal2x
do
    ${_SED} -i "s|scaler=${_s}|scaler=${sc}|g" "$_conf_file"
done
goto end && [[ $0 != $BASH_SOURCE ]] && return

: erase
rm -rf ./eXoWin3x/"${gamedir}"/
goto end && [[ $0 != $BASH_SOURCE ]] && return

: inprogress
clear
echo ""
echo "A download is already in progress. Please wait for it to finish."
echo ""
read -s -n 1 -p "Press any key to continue..."
printf "\n\n"

: end
[[ $0 != $BASH_SOURCE ]] && return
"""

# ---------------------------------------------------------------------------
# Global AltLauncher.sh — cross-platform alternate launcher
# ---------------------------------------------------------------------------
GLOBAL_ALTLAUNCHER_SH = r"""#!/usr/bin/env bash
# AltLauncher.sh — eXoWin3x cross-platform alternate launcher (Linux and macOS).
if [[ "$LD_PRELOAD" =~ "gameoverlayrenderer" ]]
then
    LD_PRELOAD=""
fi
[[ $0 == $BASH_SOURCE ]] && cd "$( dirname "$0")"
scriptDir="$(cd "$( dirname "$BASH_SOURCE")" && pwd)"

if [ "${BASH_VERSINFO:-0}" -lt 5 ]
then
    if [[ "$OSTYPE" == "darwin"* ]]
    then
        printf "\n\e[1;31;47mBash 5 is required.  brew install bash\e[0m\n\n"
    else
        printf "\n\e[1;31;47mThe version of bash currently running is too old.\e[0m\n\n"
        printf "Please run the \e[1;33;40minstall_dependencies.command\e[0m script.\n"
        printf "Then, follow the instructions to install the required dependencies.\n"
    fi
    read -s -n 1 -p "Press any key to abort."
    printf "\n\n"
    exit 0
fi

if [[ "$OSTYPE" == "darwin"* ]]
then
    for _p in /opt/homebrew/bin /opt/homebrew/sbin /usr/local/bin /usr/local/sbin
    do
        [[ -d "$_p" && ":$PATH:" != *":$_p:"* ]] && export PATH="$_p:$PATH"
    done
    unset _p
fi

if [[ "$OSTYPE" == "darwin"* ]]; then _SED=gsed; else _SED=sed; fi

function goto
{
    shortcutName=$1
    newPosition=$(${_SED} -n -e "/: $shortcutName$/{:a;n;p;ba};" "$scriptDir/$(basename -- "$BASH_SOURCE")" )
    eval "$newPosition"
    exit
}
alias :="goto"

goto english && [[ $0 != $BASH_SOURCE ]] && return

: english
[ ! -e ./eXoWin3x/"${gamedir}"/ ] && goto none && [[ $0 != $BASH_SOURCE ]] && return

: launch
if [[ "$OSTYPE" == "darwin"* ]]
then
    dosindex=$(grep -i "^${gamename}" ./util/dosbox_macos.txt 2>/dev/null | tail -1 | tr -d '\r')
    dosbox="${dosindex#*:}"; dosbox="${dosbox#*:}"
    [ -z "$dosbox" ] && dosbox="dosbox-staging"
else
    dosindex=`grep -i "^${gamename}" ./util/dosbox_linux.txt 2>/dev/null | tail -1 | tr -d "\r"`
    dosbox1="${dosindex#*:}"
    dosbox="${dosbox1#*:}"
    [ -z "$dosbox" ] && dosbox="flatpak run com.retro_exo.dosbox-ece-r4482"
fi

clear
local_conf="${var}/dosbox_linux.conf"
[ ! -e "$local_conf" ] && local_conf="${var}/dosbox.conf"
if [[ "$OSTYPE" == "darwin"* ]]
then
    read -ra _cmd <<< "$dosbox"
    "${_cmd[@]}" -conf "${local_conf}" -conf "./emulators/dosbox/options_macos.conf" -nomenu -noconsole
else
    [ -e "${var}/dosbox2_linux.conf" ] && local_conf="${var}/dosbox2_linux.conf"
    eval "$(echo "${dosbox}" | sed -e "s/\\$/\\\\$/g")" \
        -conf "\"$(echo "${local_conf}" | sed -e "s/\\$/\\\\$/g")\"" \
        -conf "\"./emulators/dosbox/options_linux.conf\"" \
        -nomenu -noconsole
fi
rm -f stdout.txt stderr.txt
[[ "$(ls -1 glide.* 2>/dev/null | wc -l)" -gt 0 ]] && rm -f glide.*
[ -e ./eXoWin3x/CWSDPMI.swp ] && rm -f ./eXoWin3x/CWSDPMI.swp
goto end && [[ $0 != $BASH_SOURCE ]] && return

: none
clear
echo ""
echo "Game has not been installed. Please run the install script first."
echo ""
read -s -n 1 -p "Press any key to continue..."
printf "\n\n"

: end
[[ $0 != $BASH_SOURCE ]] && return
"""

# exo_lib_win3x.sh — shared macOS helpers (unchanged; macOS-specific)
EXO_LIB_WIN3X = r"""#!/usr/bin/env bash
# exo_lib_win3x.sh — Shared macOS helpers for eXoWin3x.
# Source this file from launch.sh on macOS; do not execute directly.

# ── Homebrew PATH ─────────────────────────────────────────────────────────────
for _p in /opt/homebrew/bin /opt/homebrew/sbin /usr/local/bin /usr/local/sbin
do
    [[ -d "$_p" && ":$PATH:" != *":$_p:"* ]] && export PATH="$_p:$PATH"
done
unset _p

# ── Root detection ────────────────────────────────────────────────────────────
WIN3X_UTIL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIN3X_EXO="$(cd "$WIN3X_UTIL/.." && pwd)"
WIN3X_ROOT="$(cd "$WIN3X_EXO/.." && pwd)"
WIN3X_DIR="$WIN3X_EXO/eXoWin3x"

# ── Bash version guard ────────────────────────────────────────────────────────
if [[ "${BASH_VERSINFO[0]:-0}" -lt 5 ]]; then
    printf "\n\033[1;31;47mBash 5+ required. Install via Homebrew: brew install bash\033[0m\n\n"
    exit 1
fi

# ── Dependency check ──────────────────────────────────────────────────────────
function win3x_check_deps {
    [[ "$OSTYPE" != "darwin"* ]] && return 0
    local missing=()
    for t in dosbox-staging gsed curl python3 unzip wget; do
        command -v "$t" &>/dev/null || missing+=("$t")
    done
    if [[ "${#missing[@]}" -gt 0 ]]; then
        printf "\n\033[1;31;47mMissing: %s\033[0m\n\n" "${missing[*]}"
        printf "Install: brew install %s\n\n" "${missing[*]}"
        exit 1
    fi
}

# ── DOSBox lookup (macOS) ─────────────────────────────────────────────────────
# Sets WIN3X_DOSBOX to the command for the given game name.
function win3x_find_dosbox {
    local name="$1"
    local entry=""
    entry=$(grep -i "^${name}" "$WIN3X_UTIL/dosbox_macos.txt" 2>/dev/null | tail -1 | tr -d '\r')
    WIN3X_DOSBOX="${entry#*:}"
    WIN3X_DOSBOX="${WIN3X_DOSBOX#*:}"
    [[ -z "$WIN3X_DOSBOX" ]] && WIN3X_DOSBOX="dosbox-staging"
}
"""

LAUNCH_HELPER_SH = r"""#!/usr/bin/env bash
# launch_helper.sh — Cross-platform GUI bridge for eXoWin3x.
# Usage: launch_helper.sh <gamedir> <gamename>
#
# Sets context vars from CLI args then sources the platform-appropriate launcher.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "$OSTYPE" == "darwin"* ]]; then
    source "$SCRIPT_DIR/exo_lib_win3x.sh"
fi

gamedir="$1"
gamename="$2"
indexname="${gamename::-7}"

if [[ "$OSTYPE" == "darwin"* ]]; then
    var="$WIN3X_DIR/!win3x/$gamedir"
    cd "$WIN3X_EXO"
else
    WIN3X_EXO="$(cd "$SCRIPT_DIR/.." && pwd)"
    var="$WIN3X_EXO/eXoWin3x/!win3x/$gamedir"
    cd "$WIN3X_EXO"
fi

export gamedir gamename indexname var

source "$SCRIPT_DIR/launch.sh"
"""

# options_linux.conf
OPTIONS_LINUX_CONF = """\
[sdl]
fullscreen=false
fulldouble=false
fullresolution=0x0
windowresolution=1280x960
output=opengl
autolock=true
sensitivity=100
waitonerror=true
priority=higher,normal
mapperfile=
usescancodes=true

[render]
frameskip=0
aspect=true
scaler=normal2x
"""

# options_macos.conf
OPTIONS_MACOS_CONF = """\
[sdl]
fullscreen=false
fulldouble=false
fullresolution=0x0
windowresolution=1280x960
output=opengl
autolock=true
sensitivity=100
waitonerror=true
priority=higher,normal
mapperfile=
usescancodes=true

[render]
frameskip=0
aspect=true
scaler=normal2x
"""

# dosbox_linux.txt — empty placeholder; users add per-game flatpak overrides here
DOSBOX_LINUX_TXT = """\
# eXoWin3x Linux per-game DOSBox overrides.
# Format:  <GameName>:<dosbox command>
# Example: 3D Maze (1991):flatpak run com.retro_exo.dosbox-ece-r4482
# Leave empty to use the default flatpak DOSBox for all games.
"""

# dosbox_macos.txt — empty placeholder; users add per-game macOS overrides here
DOSBOX_MACOS_TXT = """\
# eXoWin3x macOS per-game DOSBox overrides.
# Format:  <GameName>:<dosbox command>
# Example: 3D Maze (1991):dosbox-staging
# Leave empty to use dosbox-staging for all games.
"""

# ---------------------------------------------------------------------------
# Setup eXoWin3x.sh — unified cross-platform setup script
# ---------------------------------------------------------------------------
SETUP_SH = r"""#!/usr/bin/env bash
# Setup eXoWin3x.sh — Cross-platform setup for the eXoWin3x collection.
# Supports Linux (Flatpak/DOSBox-ECE) and macOS (Homebrew/DOSBox-Staging).
if [[ "$LD_PRELOAD" =~ "gameoverlayrenderer" ]]
then
    LD_PRELOAD=""
fi
[[ $0 == $BASH_SOURCE ]] && cd "$( dirname "$0")"
scriptDir="$(cd "$( dirname "$BASH_SOURCE")" && pwd)"

if [ "${BASH_VERSINFO:-0}" -lt 5 ]
then
    if [[ "$OSTYPE" == "darwin"* ]]
    then
        printf "\n\e[1;31;47mBash 5 is required.  brew install bash\e[0m\n\n"
    else
        printf "\n\e[1;31;47mThe version of bash currently running is too old.\e[0m\n\n"
        printf "Please install Bash 5+ (your distro's package manager should have it).\n"
    fi
    read -s -n 1 -p "Press any key to abort."
    printf "\n\n"
    exit 0
fi

if [[ "$OSTYPE" == "darwin"* ]]
then
    for _p in /opt/homebrew/bin /opt/homebrew/sbin /usr/local/bin /usr/local/sbin
    do
        [[ -d "$_p" && ":$PATH:" != *":$_p:"* ]] && export PATH="$_p:$PATH"
    done
    unset _p
fi

if [[ "$OSTYPE" == "darwin"* ]]; then _SED=gsed; else _SED=sed; fi

PATCH_DIR="$(cd "${scriptDir}/../.." && pwd)"
WIN3X_ROOT="${PATCH_DIR}"

if [ ! -e "${WIN3X_ROOT}/Content/!Win3Xmetadata.zip" ]
then
    clear
    echo ""
    echo "ERROR: !Win3Xmetadata.zip not found in ${WIN3X_ROOT}/Content/"
    echo ""
    echo "Please ensure you have the base eXoWin3x collection downloaded."
    echo ""
    read -s -n 1 -p "Press any key to exit."
    printf "\n\n"
    exit 1
fi

# macOS: verify Homebrew dependencies are installed
if [[ "$OSTYPE" == "darwin"* ]]
then
    missingDeps=no
    for _t in dosbox-staging gsed curl python3 unzip wget
    do
        ! command -v "$_t" &>/dev/null && missingDeps=yes
    done
    if [ "$missingDeps" = "yes" ]
    then
        clear
        echo ""
        echo "One or more dependencies are missing."
        echo ""
        echo "Please install the following with Homebrew:"
        echo "   brew install bash dosbox-staging gnu-sed curl wget python3 unzip"
        echo ""
        echo "If Homebrew is not installed, visit https://brew.sh"
        echo ""
        read -s -n 1 -p "Press any key to exit."
        printf "\n\n"
        exit 1
    fi
fi

clear
echo ""
echo "======================================================="
echo "   eXoWin3x Patch Setup"
echo "======================================================="
echo ""
echo "eXoWin3x collection found at:"
echo "   ${WIN3X_ROOT}"
echo ""
echo "This setup will:"
echo "  1. Extract per-game launcher scripts for all 1138 games"
echo "  2. Install global launch/install scripts"
echo "  3. Configure your display preferences"
echo ""
read -s -n 1 -p "Press any key to begin setup..."
printf "\n\n"

cd "${WIN3X_ROOT}"

# Extract base collection metadata (XML, images index) if present
if [ -e "./Content/XOWin3xMetadata.zip" ]
then
    echo "Extracting base collection metadata (XML, images)..."
    python3 - "./Content/XOWin3xMetadata.zip" "." <<'PYEOF'
import sys, zipfile, os, unicodedata

def safe_name(name):
    result = ""
    for ch in name:
        norm = unicodedata.normalize("NFKD", ch)
        ascii_part = norm.encode("ascii", "ignore").decode("ascii")
        result += ascii_part if ascii_part else "_"
    return result

zip_path, dest = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(zip_path) as zf:
    for info in zf.infolist():
        name = info.filename
        try:
            name.encode("ascii")
        except UnicodeEncodeError:
            name = safe_name(name)
        target = os.path.join(dest, name)
        if info.is_dir():
            os.makedirs(target, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with zf.open(info) as src, open(target, "wb") as dst:
                dst.write(src.read())
PYEOF
    echo "Done."
fi

# Extract base game scripts from the Windows collection metadata
if [ -e "./Content/!Win3Xmetadata.zip" ]
then
    echo "Extracting per-game scripts..."
    unzip -o "./Content/!Win3Xmetadata.zip" -d . > /dev/null
    echo "Done."
fi

# Extract cross-platform launcher scripts from this patch
if [ -e "${PATCH_DIR}/Content/!Win3x_metadata.zip" ]
then
    echo "Extracting cross-platform launcher scripts..."
    unzip -o "${PATCH_DIR}/Content/!Win3x_metadata.zip" -d . > /dev/null
    echo "Done."
fi
echo ""

# Install global utility scripts
echo "Installing global launcher scripts..."
mkdir -p ./eXo/util
mkdir -p ./eXo/emulators/dosbox
unzip -o "${PATCH_DIR}/eXo/util/utilWin3x.zip" -d ./eXo/util/ > /dev/null
echo "Done."
echo ""

# Place conf files in the correct location
if [[ "$OSTYPE" == "darwin"* ]]
then
    if [ -e "./eXo/util/options_macos.conf" ] && [ ! -e "./eXo/emulators/dosbox/options_macos.conf" ]
    then
        mv ./eXo/util/options_macos.conf ./eXo/emulators/dosbox/options_macos.conf
    fi
else
    if [ -e "./eXo/util/options_linux.conf" ] && [ ! -e "./eXo/emulators/dosbox/options_linux.conf" ]
    then
        mv ./eXo/util/options_linux.conf ./eXo/emulators/dosbox/options_linux.conf
    fi
fi

# Configure display preferences
clear
echo ""
echo "Would you like Aspect Ratio Correction enabled by default? (corrects 4:3 on widescreen)"
echo ""
while true
do
    read -p "[Y]es / [N]o: " choice
    case $choice in
        [Yy]* ) aspect="true";  break;;
        [Nn]* ) aspect="false"; break;;
        *     ) printf "Invalid input.\n";;
    esac
done

if [[ "$OSTYPE" == "darwin"* ]]
then
    gsed -i "s|aspect=true|aspect=${aspect}|g"   ./eXo/emulators/dosbox/options_macos.conf
    gsed -i "s|aspect=false|aspect=${aspect}|g"  ./eXo/emulators/dosbox/options_macos.conf
else
    sed -i -e "s|aspect=true|aspect=${aspect}|g"   ./eXo/emulators/dosbox/options_linux.conf
    sed -i -e "s|aspect=false|aspect=${aspect}|g"  ./eXo/emulators/dosbox/options_linux.conf
fi

clear
echo ""
echo "Would you like the default display mode to be [F]ullscreen or [W]indowed?"
echo ""
while true
do
    read -p "[F]ullscreen / [W]indowed: " choice
    case $choice in
        [Ff]* ) fullscreen="true";  break;;
        [Ww]* ) fullscreen="false"; break;;
        *     ) printf "Invalid input.\n";;
    esac
done

if [[ "$OSTYPE" == "darwin"* ]]
then
    gsed -i "s|fullscreen=true|fullscreen=${fullscreen}|g"   ./eXo/emulators/dosbox/options_macos.conf
    gsed -i "s|fullscreen=false|fullscreen=${fullscreen}|g"  ./eXo/emulators/dosbox/options_macos.conf
else
    sed -i -e "s|fullscreen=true|fullscreen=${fullscreen}|g"   ./eXo/emulators/dosbox/options_linux.conf
    sed -i -e "s|fullscreen=false|fullscreen=${fullscreen}|g"  ./eXo/emulators/dosbox/options_linux.conf
fi

# Make scripts executable
echo ""
echo "Setting file permissions..."
find ./eXo/util     -name "*.sh"      -exec chmod +x {} \; 2>/dev/null
find ./eXo/util     -name "*.command" -exec chmod +x {} \; 2>/dev/null
find ./eXo/eXoWin3x -name "*.sh"      -exec chmod +x {} \; 2>/dev/null
find ./eXo/eXoWin3x -name "*.command" -exec chmod +x {} \; 2>/dev/null
echo "Done."

clear
echo ""
echo "======================================================="
echo "   eXoWin3x Patch Setup Complete!"
echo "======================================================="
echo ""
if [[ "$OSTYPE" == "darwin"* ]]
then
    echo "Requirements:"
    echo "   brew install bash dosbox-staging gnu-sed curl wget python3 unzip"
    echo ""
fi
echo "To play a game:"
echo "  - Navigate to eXoWin3x/eXo/eXoWin3x/!win3x/<GameDir>/"
echo "  - Double-click the .command file"
if [[ "$OSTYPE" == "linux-gnu"* ]]
then
    echo "  - Or run the .sh file directly in a terminal"
fi
echo ""
echo "The first launch of each game will offer to install (unzip) it."
echo ""
read -s -n 1 -p "Press any key to exit."
printf "\n\n"
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def backslash_to_forward(conf_text: str) -> str:
    """Convert backslash path separators to forward slashes in dosbox AUTOEXEC
    mount/imgmount lines so they work on Linux/macOS."""
    lines = conf_text.split('\n')
    in_autoexec = False
    result = []
    for line in lines:
        stripped = line.strip().lower()
        if stripped == '[autoexec]':
            in_autoexec = True
        if in_autoexec and ('mount' in stripped or 'imgmount' in stripped):
            line = line.replace('\\', '/')
        result.append(line)
    return '\n'.join(result)


def fix_dosbox_linux_conf(conf_text: str) -> str:
    """Prepare a Windows dosbox.conf for use on Linux/macOS:
    - Convert backslash paths to forward slashes in AUTOEXEC
    - Clear the mapperfile= setting (not valid cross-platform)
    """
    conf_text = backslash_to_forward(conf_text)
    conf_text = re.sub(r'(?m)^(mapperfile\s*=).*$', r'\1', conf_text)
    return conf_text


def build_per_game_launch_sh() -> str:
    return SH_HEADER + SH_DEPCHECK + LAUNCH_SH_FOOTER


def build_per_game_install_sh() -> str:
    return SH_HEADER + SH_DEPCHECK + INSTALL_SH_FOOTER


def build_per_game_alt_sh() -> str:
    return SH_HEADER + SH_DEPCHECK + ALT_SH_FOOTER


def add_file(zf: zipfile.ZipFile, arc_path: str, content: str,
             executable: bool = False) -> None:
    """Add a UTF-8 text file to the zipfile with optional executable bit."""
    info = zipfile.ZipInfo(arc_path)
    info.external_attr = ((0o100755 if executable else 0o100644) & 0xFFFF) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, content.encode('utf-8'))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the eXoWin3x Cross-Platform Patch (Linux + macOS)."
    )
    parser.add_argument(
        '--win3x-dir', default=str(DEFAULT_WIN3X),
        help=f"Path to the eXoWin3x base directory (default: {DEFAULT_WIN3X})"
    )
    parser.add_argument(
        '--output-dir', default=str(DEFAULT_OUTPUT),
        help=f"Output path for the generated patch (default: {DEFAULT_OUTPUT})"
    )
    args = parser.parse_args()

    win3x_dir  = Path(args.win3x_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    metadata_zip = win3x_dir / 'Content' / '!Win3Xmetadata.zip'

    if not metadata_zip.is_file():
        print(f"ERROR: Cannot find {metadata_zip}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {metadata_zip} ...")
    src = zipfile.ZipFile(str(metadata_zip), 'r')

    # Enumerate game directories
    game_dirs: dict[str, dict] = {}   # gamedir -> {'bat': name, 'has_dosbox2': bool}

    for name in src.namelist():
        parts = name.split('/')
        # eXo/eXoWin3x/!win3x/<gamedir>/<filename>
        if len(parts) < 5:
            continue
        if parts[0] != 'eXo' or parts[1] != 'eXoWin3x' or parts[2] != '!win3x':
            continue
        gdir  = parts[3]
        fname = parts[4] if len(parts) > 4 else ''
        if not gdir or not fname:
            continue

        if gdir not in game_dirs:
            game_dirs[gdir] = {'bat': '', 'has_dosbox2': False}

        if fname.endswith(').bat') and 'Alternate' not in fname:
            game_dirs[gdir]['bat'] = fname[:-4]   # strip .bat
        if fname == 'dosbox2.conf':
            game_dirs[gdir]['has_dosbox2'] = True

    total = len(game_dirs)
    print(f"Found {total} games.")

    # Create output directories
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'eXo' / 'util').mkdir(parents=True, exist_ok=True)
    (output_dir / 'Content').mkdir(parents=True, exist_ok=True)

    # Build per-game metadata zip
    meta_zip_path = output_dir / 'Content' / '!Win3x_metadata.zip'
    print(f"Building {meta_zip_path} ...")

    with zipfile.ZipFile(str(meta_zip_path), 'w', zipfile.ZIP_DEFLATED) as mz:
        for idx, (gdir, info) in enumerate(sorted(game_dirs.items()), 1):
            if idx % 100 == 0 or idx == total:
                print(f"  Processing game {idx}/{total}  ({gdir}) ...")

            game_name = info['bat']
            if not game_name:
                game_name = gdir  # fallback; shouldn't happen with valid metadata

            base = f"eXo/eXoWin3x/!win3x/{gdir}"

            # dosbox_linux.conf (path-corrected copy of dosbox.conf)
            dosbox_conf_key = f"eXo/eXoWin3x/!win3x/{gdir}/dosbox.conf"
            try:
                raw_conf  = src.read(dosbox_conf_key).decode('utf-8', errors='replace')
                linux_conf = fix_dosbox_linux_conf(raw_conf)
            except KeyError:
                print(f"  WARNING: no dosbox.conf for {gdir}, skipping conf", file=sys.stderr)
                linux_conf = ""

            if linux_conf:
                add_file(mz, f"{base}/dosbox_linux.conf", linux_conf)

            if info['has_dosbox2']:
                dosbox2_key = f"eXo/eXoWin3x/!win3x/{gdir}/dosbox2.conf"
                try:
                    raw2   = src.read(dosbox2_key).decode('utf-8', errors='replace')
                    linux2 = fix_dosbox_linux_conf(raw2)
                    add_file(mz, f"{base}/dosbox2_linux.conf", linux2)
                except KeyError:
                    pass

            # Per-game launch .sh + .command
            add_file(mz, f"{base}/{game_name}.sh",      build_per_game_launch_sh(),  executable=True)
            add_file(mz, f"{base}/{game_name}.command", COMMAND_TEMPLATE,            executable=True)

            # Per-game install .sh + .command
            add_file(mz, f"{base}/install.sh",      build_per_game_install_sh(), executable=True)
            add_file(mz, f"{base}/install.command", COMMAND_TEMPLATE,            executable=True)

            # Extras/Alternate Launcher .sh + .command
            add_file(mz, f"{base}/Extras/Alternate Launcher.sh",
                     build_per_game_alt_sh(), executable=True)
            add_file(mz, f"{base}/Extras/Alternate Launcher.command",
                     COMMAND_TEMPLATE, executable=True)

    print(f"  Done — {total} games written.")

    # Build global util zip
    util_zip_path = output_dir / 'eXo' / 'util' / 'utilWin3x.zip'
    print(f"Building {util_zip_path} ...")

    with zipfile.ZipFile(str(util_zip_path), 'w', zipfile.ZIP_DEFLATED) as uz:
        add_file(uz, 'launch.sh',          GLOBAL_LAUNCH_SH,       executable=True)
        add_file(uz, 'install.sh',         GLOBAL_INSTALL_SH,      executable=True)
        add_file(uz, 'AltLauncher.sh',     GLOBAL_ALTLAUNCHER_SH,  executable=True)
        add_file(uz, 'exo_lib_win3x.sh',   EXO_LIB_WIN3X,          executable=False)
        add_file(uz, 'launch_helper.sh',   LAUNCH_HELPER_SH,       executable=True)
        add_file(uz, 'dosbox_linux.txt',   DOSBOX_LINUX_TXT,       executable=False)
        add_file(uz, 'dosbox_macos.txt',   DOSBOX_MACOS_TXT,       executable=False)
        add_file(uz, 'options_linux.conf', OPTIONS_LINUX_CONF,     executable=False)
        add_file(uz, 'options_macos.conf', OPTIONS_MACOS_CONF,     executable=False)

    print("  Done.")

    # Write Setup scripts
    print("Writing setup scripts ...")

    setup_sh_path = output_dir / 'eXo' / 'util' / 'Setup eXoWin3x.sh'
    setup_sh_path.write_text(SETUP_SH, encoding='utf-8')
    setup_sh_path.chmod(setup_sh_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # Root-level .command entry point — sources the setup .sh from eXo/util/
    root_command = output_dir / 'Setup eXoWin3x.command'
    root_command.write_text(
        COMMAND_TEMPLATE
            .replace('$(basename -- "${BASH_SOURCE%.command}.sh")', 'eXo/util/Setup eXoWin3x.sh'),
        encoding='utf-8'
    )
    root_command.chmod(root_command.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print("  Done.")

    # Write README
    readme_path = output_dir / 'eXoWin3x ReadMe.txt'
    readme_path.write_text(README_TEXT, encoding='utf-8')

    print()
    print("=" * 60)
    print(f"Cross-platform patch generated at:")
    print(f"   {output_dir}")
    print()
    print("Distribute this folder alongside eXoWin3x.")
    print("Users run:  Setup eXoWin3x.command  (from the patch folder).")
    print("=" * 60)

    src.close()


README_TEXT = """\
    eXoWin3x Collection
    Cross-Platform Patch (v1.0)
    =======================================================

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
"""


if __name__ == '__main__':
    main()
