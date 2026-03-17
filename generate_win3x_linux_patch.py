#!/usr/bin/env python3
"""
generate_win3x_linux_patch.py
Generates the eXoWin3x Linux Patch from the base eXoWin3x Windows collection.

Usage:
    python3 generate_win3x_linux_patch.py [--win3x-dir PATH] [--output-dir PATH]

Reads:  eXoWin3x/Content/!Win3Xmetadata.zip  (per-game Windows scripts)
Writes: eXoWin3x-Linux-Patch/               (distributable patch directory)

After running, merge eXoWin3x-Linux-Patch/ into eXoWin3x/ (or let the
included Setup script do it automatically).
"""

import argparse
import io
import os
import re
import stat
import sys
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_WIN3X  = SCRIPT_DIR / "eXoWin3x"
DEFAULT_OUTPUT = SCRIPT_DIR / "eXoWin3x-Linux-Patch"

# ---------------------------------------------------------------------------
# Constant text: boilerplate shared by every per-game .bsh script
# ---------------------------------------------------------------------------
BASH_HEADER = r"""#!/usr/bin/env bash
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

if [[ "$OSTYPE" == "darwin"* ]]
then
    source "$scriptDir/$(basename -- "${BASH_SOURCE%.bsh}.msh")"
    exit 0
fi

if [ "${BASH_VERSINFO:-0}" -lt 5 ]
then
    printf "\n\e[1;31;47mThe version of bash currently running is too old.\e[0m\n\n"
    printf "Please run the \e[1;33;40minstall_dependencies.command\e[0m script.\n"
    printf "Then, follow the instructions to install the required dependencies.\n"
    read -s -n 1 -p "Press any key to abort."
    printf "\n\n"
    exit 0
fi

function goto
{
    shortcutName=$1
    newPosition=$(sed -n -e "/: $shortcutName$/{:a;n;p;ba};" "$scriptDir/$(basename -- "$BASH_SOURCE")" )
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

# Dependency check block (Linux-specific flatpak check)
BASH_DEPCHECK = r"""
missingDependencies=no
if [[ "$OSTYPE" == "linux-gnu"* ]]
then
    ! [[ `which flatpak` ]] && missingDependencies=yes
    ! [[ `flatpak list 2>/dev/null | grep "retro_exo\.dosbox-ece-r4482"` ]] && missingDependencies=yes
else
    missingDependencies=yes
fi
! [[ `which curl` ]] && missingDependencies=yes
! [[ `which python3` ]] && missingDependencies=yes
! [[ `which sed` ]] && missingDependencies=yes
! [[ `which unzip` ]] && missingDependencies=yes
! [[ `which wget` ]] && missingDependencies=yes

if [ $missingDependencies == "yes" ]
then
    printf "\n\e[1;31;47mOne or more dependencies are missing.\e[0m\n\n"
    printf "Please run the \e[1;33;40minstall_dependencies.command\e[0m script.\n"
    printf "Then, follow the instructions to install the required dependencies.\n"
    read -s -n 1 -p "Press any key to abort."
    printf "\n\n"
    exit 0
fi
"""

# Footer for per-game launch .bsh
LAUNCH_BSH_FOOTER = r"""
var="${PWD}"
for i in .
do
    gamedir="${PWD##*/}"
done
for f in *\).bsh
do
    gamename2="${f}"
done
gamename="${gamename2::-4}"
indexname="${gamename::-7}"
cd ..
cd ..
cd ..
eval source ./util/launch.bsh && exit 0
[[ $0 != $BASH_SOURCE ]] && return
"""

# Footer for per-game install .bsh
INSTALL_BSH_FOOTER = r"""
folder="${PWD}"
eval source ../../../util/install.bsh && exit 0
: exit
[[ $0 != $BASH_SOURCE ]] && return
"""

# Footer for Extras/Alternate Launcher .bsh
ALT_BSH_FOOTER = r"""
cd ..
var="${PWD}"
for i in .
do
    gamedir="${PWD##*/}"
done
for f in *\).bsh
do
    gamename2="${f}"
done
gamename="${gamename2::-4}"
indexname="${gamename::-7}"
cd ..
cd ..
cd ..
eval source ./util/AltLauncher.bsh && exit 0
[[ $0 != $BASH_SOURCE ]] && return
"""

# .command file (terminal-launcher, works on both Linux and macOS)
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
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "gnome-terminal-" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "xfce4-terminal" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "kgx" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "xterm" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "Eterm" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "x-terminal-emul" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "mate-terminal" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "terminator" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "urxvt" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "rxvt" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "termit" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "terminology" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "tilix" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "kitty" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `ps -o sid= -p "$$" | xargs ps -o ppid= -p | xargs ps -o comm= -p` = "aterm" ]
    then
        source "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")"
        exit 0
    elif [ `which konsole` ]
    then
        konsole -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which gnome-terminal` ]
    then
        gnome-terminal -- /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which xfce4-terminal` ]
    then
        xfce4-terminal -x /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which kgx` ]
    then
        kgx -e "/usr/bin/env bash \"$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")\" $@" &
        exit 0
    elif [ `which xterm` ]
    then
        xterm -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which uxterm` ]
    then
        uxterm -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which eterm` ]
    then
        Eterm -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which x-terminal-emulator` ]
    then
        x-terminal-emulator -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which mate-terminal` ]
    then
        eval mate-terminal -e \"/usr/bin/env bash \\\"$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")\\\" $@\" "$@" &
        exit 0
    elif [ `which terminator` ]
    then
        terminator -x /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which urxvt` ]
    then
        urxvt -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which rxvt` ]
    then
        rxvt -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which termit` ]
    then
        termit -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which lxterm` ]
    then
        lxterm -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which terminology` ]
    then
        terminology -e "/usr/bin/env bash \"$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")\" $@" &
        exit 0
    elif [ `which tilix` ]
    then
        tilix -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which kitty` ]
    then
        kitty -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    elif [ `which aterm` ]
    then
        aterm -e /usr/bin/env bash "$PWD/$(basename -- "${BASH_SOURCE%.command}.bsh")" "$@" &
        exit 0
    else
        exit ERRCODE "Weird system achievement unlocked: None of the 18 supported terminal emulators are installed."
    fi
elif [[ "$OSTYPE" == "darwin"* ]]
then
    source "$PWD/$(basename -- "${BASH_SOURCE%.command}.msh")"
    exit 0
else
    exit ERRCODE "Unsupported OS"
fi
"""

# ---------------------------------------------------------------------------
# Global launch.bsh (installed to eXo/util/launch.bsh)
# ---------------------------------------------------------------------------
GLOBAL_LAUNCH_BSH = r"""#!/usr/bin/env bash
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

if [[ "$OSTYPE" == "darwin"* ]]
then
    source "$scriptDir/$(basename -- "${BASH_SOURCE%.bsh}.msh")"
    exit 0
fi

if [ "${BASH_VERSINFO:-0}" -lt 5 ]
then
    printf "\n\e[1;31;47mThe version of bash currently running is too old.\e[0m\n\n"
    printf "Please run the \e[1;33;40minstall_dependencies.command\e[0m script.\n"
    printf "Then, follow the instructions to install the required dependencies.\n"
    read -s -n 1 -p "Press any key to abort."
    printf "\n\n"
    exit 0
fi

declare -a scriptDirStack

function goto
{
    shortcutName=$1
    newPosition=$(sed -n -e "/: $shortcutName$/{:a;n;p;ba};" "$scriptDir/$(basename -- "$BASH_SOURCE")" )
    eval "$newPosition"
    exit
}
alias :="goto"

# Apply global display-preference overrides from SEL files
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

goto english && [[ $0 != $BASH_SOURCE ]] && return

: english
[ ! -e ./eXoWin3x/"${gamedir}"/ ] && goto none && [[ $0 != $BASH_SOURCE ]] && return

: launch
dosindex=`grep -i "^${gamename}" ./util/dosbox_linux.txt 2>/dev/null | tail -1 | tr -d "\r"`
dosbox1="${dosindex#*:}"
dosbox="${dosbox1#*:}"
[ -z "$dosbox" ] && dosbox="flatpak run com.retro_exo.dosbox-ece-r4482"

: start
clear
# Determine the conf file — use dosbox2.conf if present (alternate config for some games)
local_conf="${var}/dosbox_linux.conf"
[ -e "${var}/dosbox2_linux.conf" ] && local_conf="${var}/dosbox2_linux.conf"

eval "$(echo "${dosbox}" | sed -e "s/\\$/\\\\$/g")" \
    -conf "\"$(echo "${local_conf}" | sed -e "s/\\$/\\\\$/g")\"" \
    -conf "\"./emulators/dosbox/options_linux.conf\"" \
    -nomenu -noconsole
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

[ $errorlevel == '2' ] && goto no && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '1' ] && goto yes && [[ $0 != $BASH_SOURCE ]] && return

: yes
cd "${var}"
scriptDirStack["${#scriptDirStack[@]}"]="$scriptDir"
eval source install.bsh
scriptDir="${scriptDirStack["${#scriptDirStack[@]}"-1]}"
unset scriptDirStack["${#scriptDirStack[@]}"-1]
function goto
{
    shortcutName=$1
    newPosition=$(sed -n -e "/: $shortcutName$/{:a;n;p;ba};" "$scriptDir/$(basename -- "$BASH_SOURCE")" )
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

# Global launch.msh (macOS redirect stub — placed in util/ for macOS users
# until the real macOS launcher is layered on by the macOS patch)
GLOBAL_LAUNCH_MSH_STUB = r"""#!/usr/bin/env bash
if [[ "$LD_PRELOAD" =~ "gameoverlayrenderer" ]]
then
    LD_PRELOAD=""
fi
[[ $0 == $BASH_SOURCE ]] && cd "$( dirname "$0")"
scriptDir="$(cd "$( dirname "$BASH_SOURCE")" && pwd)"

if [[ "$OSTYPE" == "linux-gnu"* ]]
then
    source "$scriptDir/$(basename -- "${BASH_SOURCE%.msh}.bsh")"
    exit 0
fi

printf "\n\e[1;31;47mNo macOS launcher is installed.\e[0m\n\n"
printf "Please apply the eXoWin3x macOS patch.\n"
read -s -n 1 -p "Press any key to abort."
printf "\n\n"
exit 1
"""

# ---------------------------------------------------------------------------
# Global install.bsh (installed to eXo/util/install.bsh)
# ---------------------------------------------------------------------------
GLOBAL_INSTALL_BSH = r"""#!/usr/bin/env bash
if [[ "$LD_PRELOAD" =~ "gameoverlayrenderer" ]]
then
    LD_PRELOAD=""
fi
[[ $0 == $BASH_SOURCE ]] && cd "$( dirname "$0")"
scriptDir="$(cd "$( dirname "$BASH_SOURCE")" && pwd)"
[ $# -gt 0 ] && parameterone="$1"

if [[ "$OSTYPE" == "darwin"* ]]
then
    source "$scriptDir/$(basename -- "${BASH_SOURCE%.bsh}.msh")"
    exit 0
fi

if [ "${BASH_VERSINFO:-0}" -lt 5 ]
then
    printf "\n\e[1;31;47mThe version of bash currently running is too old.\e[0m\n\n"
    read -s -n 1 -p "Press any key to abort."
    printf "\n\n"
    exit 0
fi

function goto
{
    shortcutName=$1
    newPosition=$(sed -n -e "/: $shortcutName$/{:a;n;p;ba};" "$scriptDir/$(basename -- "$BASH_SOURCE")" )
    eval "$newPosition"
    exit
}
alias :="goto"

conf="${folder}"

goto start && [[ $0 != $BASH_SOURCE ]] && return

: start
# Check if already installed (offer uninstall)
if [ -e ./eXoWin3x/"${gamedir}"/ ]
then
    goto dele
fi

: check
# Check if the game zip exists locally
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
[ $errorlevel == '1' ] && goto dl && [[ $0 != $BASH_SOURCE ]] && return

: dl
# Check if another download is in progress
[ -e ./eXoWin3x/inprogress.txt ] && goto inprogress && [[ $0 != $BASH_SOURCE ]] && return
touch ./eXoWin3x/inprogress.txt
cd eXoWin3x
wget -np -c -R "index.html*" "https://exorlp.xyz/public/eXo/eXoWin3x/Games/${gamename}.zip"
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

[ $errorlevel == '3' ] && goto end && [[ $0 != $BASH_SOURCE ]] && return
[ $errorlevel == '2' ] && goto erase && [[ $0 != $BASH_SOURCE ]] && return
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
[ $errorlevel == '1' ] && goto aspect && [[ $0 != $BASH_SOURCE ]] && return

: aspect
sed -i -e "s|aspect=false|aspect=true|g" "${conf}/dosbox_linux.conf"
goto next && [[ $0 != $BASH_SOURCE ]] && return

: aspect2
sed -i -e "s|aspect=true|aspect=false|g" "${conf}/dosbox_linux.conf"

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
sed -i -e "s|fullscreen=true|fullscreen=false|g" "${conf}/dosbox_linux.conf"
goto scaler1 && [[ $0 != $BASH_SOURCE ]] && return

: full
sed -i -e "s|fullscreen=false|fullscreen=true|g" "${conf}/dosbox_linux.conf"
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
[ $errorlevel == '1' ] && goto sy && [[ $0 != $BASH_SOURCE ]] && return

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
        [1] ) errorlevel=1
                break;;
        [2] ) errorlevel=2
                break;;
        [3] ) errorlevel=3
                break;;
        [4] ) errorlevel=4
                break;;
        [5] ) errorlevel=5
                break;;
        [6] ) errorlevel=6
                break;;
        [7] ) errorlevel=7
                break;;
        [8] ) errorlevel=8
                break;;
        [9] ) errorlevel=9
                break;;
        [0] ) errorlevel=10
                break;;
        *     ) printf "Invalid input.\n";;
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
sc=none
goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scaln3x
sc=normal3x
goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scalhq2x
sc=hq2x
goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scalhq3x
sc=hq3x
goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scal2xs
sc=2xsai
goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scals2xs
sc=super2xsai
goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scalam2x
sc=advmame2x
goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scalam3x
sc=advmame3x
goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: scaltv2x
sc=tv2x
goto scaler && [[ $0 != $BASH_SOURCE ]] && return
: normal2x
sc=normal2x
goto scaler && [[ $0 != $BASH_SOURCE ]] && return

: scaler
sed -i -e "s|scaler=none|scaler=${sc}|g"         "${conf}/dosbox_linux.conf"
sed -i -e "s|scaler=normal3x|scaler=${sc}|g"     "${conf}/dosbox_linux.conf"
sed -i -e "s|scaler=hq2x|scaler=${sc}|g"         "${conf}/dosbox_linux.conf"
sed -i -e "s|scaler=hq3x|scaler=${sc}|g"         "${conf}/dosbox_linux.conf"
sed -i -e "s|scaler=2xsai|scaler=${sc}|g"        "${conf}/dosbox_linux.conf"
sed -i -e "s|scaler=super2xsai|scaler=${sc}|g"   "${conf}/dosbox_linux.conf"
sed -i -e "s|scaler=advmame2x|scaler=${sc}|g"    "${conf}/dosbox_linux.conf"
sed -i -e "s|scaler=advmame3x|scaler=${sc}|g"    "${conf}/dosbox_linux.conf"
sed -i -e "s|scaler=tv2x|scaler=${sc}|g"         "${conf}/dosbox_linux.conf"
sed -i -e "s|scaler=normal2x|scaler=${sc}|g"     "${conf}/dosbox_linux.conf"
goto end && [[ $0 != $BASH_SOURCE ]] && return

: erase
rm -rf ./eXoWin3x/"${gamedir}"/
goto end && [[ $0 != $BASH_SOURCE ]] && return

: inprogress
clear
echo ""
echo "You are currently already downloading a game. Please complete that download"
echo "before starting another one."
echo ""
read -s -n 1 -p "Press any key to continue..."
printf "\n\n"

: end
[[ $0 != $BASH_SOURCE ]] && return
"""

# Global install.msh — stub for Linux patch (real macOS version from macOS patch)
GLOBAL_INSTALL_MSH_STUB = r"""#!/usr/bin/env bash
if [[ "$LD_PRELOAD" =~ "gameoverlayrenderer" ]]
then
    LD_PRELOAD=""
fi
[[ $0 == $BASH_SOURCE ]] && cd "$( dirname "$0")"
scriptDir="$(cd "$( dirname "$BASH_SOURCE")" && pwd)"

if [[ "$OSTYPE" == "linux-gnu"* ]]
then
    source "$scriptDir/$(basename -- "${BASH_SOURCE%.msh}.bsh")"
    exit 0
fi

printf "\n\e[1;31;47mNo macOS installer is installed.\e[0m\n\n"
printf "Please apply the eXoWin3x macOS patch.\n"
read -s -n 1 -p "Press any key to abort."
printf "\n\n"
exit 1
"""

# AltLauncher.bsh placeholder
GLOBAL_ALTLAUNCHER_BSH = r"""#!/usr/bin/env bash
if [[ "$LD_PRELOAD" =~ "gameoverlayrenderer" ]]
then
    LD_PRELOAD=""
fi
[[ $0 == $BASH_SOURCE ]] && cd "$( dirname "$0")"
scriptDir="$(cd "$( dirname "$BASH_SOURCE")" && pwd)"

if [[ "$OSTYPE" == "darwin"* ]]
then
    source "$scriptDir/$(basename -- "${BASH_SOURCE%.bsh}.msh")"
    exit 0
fi

if [ "${BASH_VERSINFO:-0}" -lt 5 ]
then
    printf "\n\e[1;31;47mThe version of bash currently running is too old.\e[0m\n\n"
    read -s -n 1 -p "Press any key to abort."
    printf "\n\n"
    exit 0
fi

function goto
{
    shortcutName=$1
    newPosition=$(sed -n -e "/: $shortcutName$/{:a;n;p;ba};" "$scriptDir/$(basename -- "$BASH_SOURCE")" )
    eval "$newPosition"
    exit
}
alias :="goto"

goto english && [[ $0 != $BASH_SOURCE ]] && return

: english
[ ! -e ./eXoWin3x/"${gamedir}"/ ] && goto none && [[ $0 != $BASH_SOURCE ]] && return

: launch
dosindex=`grep -i "^${gamename}" ./util/dosbox_linux.txt 2>/dev/null | tail -1 | tr -d "\r"`
dosbox1="${dosindex#*:}"
dosbox="${dosbox1#*:}"
[ -z "$dosbox" ] && dosbox="flatpak run com.retro_exo.dosbox-ece-r4482"

clear
local_conf="${var}/dosbox_linux.conf"
[ -e "${var}/dosbox2_linux.conf" ] && local_conf="${var}/dosbox2_linux.conf"

eval "$(echo "${dosbox}" | sed -e "s/\\$/\\\\$/g")" \
    -conf "\"$(echo "${local_conf}" | sed -e "s/\\$/\\\\$/g")\"" \
    -conf "\"./emulators/dosbox/options_linux.conf\"" \
    -nomenu -noconsole
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

# ---------------------------------------------------------------------------
# Setup eXoWin3x.bsh — the collection setup script
# ---------------------------------------------------------------------------
SETUP_BSH = r"""#!/usr/bin/env bash
# Setup eXoWin3x.bsh — Linux/macOS setup for the eXoWin3x collection.
if [[ "$LD_PRELOAD" =~ "gameoverlayrenderer" ]]
then
    LD_PRELOAD=""
fi
[[ $0 == $BASH_SOURCE ]] && cd "$( dirname "$0")"
scriptDir="$(cd "$( dirname "$BASH_SOURCE")" && pwd)"

if [[ "$OSTYPE" == "darwin"* ]]
then
    source "$scriptDir/$(basename -- "${BASH_SOURCE%.bsh}.msh")"
    exit 0
fi

if [ "${BASH_VERSINFO:-0}" -lt 5 ]
then
    printf "\n\e[1;31;47mThe version of bash currently running is too old.\e[0m\n\n"
    printf "Please install Bash 5+ (your distro's package manager should have it).\n"
    read -s -n 1 -p "Press any key to abort."
    printf "\n\n"
    exit 0
fi

function goto
{
    shortcutName=$1
    newPosition=$(sed -n -e "/: $shortcutName$/{:a;n;p;ba};" "$scriptDir/$(basename -- "$BASH_SOURCE")" )
    eval "$newPosition"
    exit
}
alias :="goto"

# ── Locate the eXoWin3x collection root ──────────────────────────────────────
# The patch must be placed alongside the eXoWin3x collection directory.
# scriptDir is eXo/util/ inside the patch, so the patch root is ../..
PATCH_DIR="$(cd "${scriptDir}/../.." && pwd)"
WIN3X_ROOT="${PATCH_DIR}"

# ── Check for required collection files ──────────────────────────────────────
if [ ! -e "${WIN3X_ROOT}/Content/!Win3Xmetadata.zip" ]
then
    clear
    echo ""
    echo "ERROR: Cannot locate !Win3Xmetadata.zip in ${WIN3X_ROOT}/Content/"
    echo ""
    echo "Please ensure you have the base eXoWin3x collection downloaded."
    echo ""
    read -s -n 1 -p "Press any key to exit."
    printf "\n\n"
    exit 1
fi

clear
echo ""
echo "======================================================="
echo "   eXoWin3x Linux Patch Setup"
echo "======================================================="
echo ""
echo "eXoWin3x collection found at:"
echo "   ${WIN3X_ROOT}"
echo ""
echo "This setup will:"
echo "  1. Extract Linux launcher scripts for all 1138 games"
echo "  2. Install global launch/install scripts"
echo "  3. Configure your display preferences"
echo ""
read -s -n 1 -p "Press any key to begin setup..."
printf "\n\n"

# ── Extract base collection metadata (XML, images index) ─────────────────────
cd "${WIN3X_ROOT}"
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

# ── Extract base game scripts ─────────────────────────────────────────────────
if [ -e "./Content/!Win3Xmetadata.zip" ]
then
    echo "Extracting per-game scripts..."
    unzip -o "./Content/!Win3Xmetadata.zip" -d . > /dev/null
    echo "Done."
fi

# ── Extract per-game Linux metadata ──────────────────────────────────────────
echo "Extracting per-game Linux scripts..."
unzip -o "${PATCH_DIR}/Content/!Win3x_linux_metadata.zip" -d . > /dev/null
echo "Done."
echo ""

# ── Extract global utility scripts ───────────────────────────────────────────
echo "Installing global launcher scripts..."
mkdir -p ./eXo/util
mkdir -p ./eXo/emulators/dosbox
unzip -o "${PATCH_DIR}/eXo/util/utilWin3x_linux.zip" -d ./eXo/util/ > /dev/null
echo "Done."
echo ""

# ── Configure display preferences ────────────────────────────────────────────
# Ensure options_linux.conf is in place (extracted from util zip above,
# but we move it to emulators/dosbox if it landed in util)
if [ -e "./eXo/util/options_linux.conf" ] && [ ! -e "./eXo/emulators/dosbox/options_linux.conf" ]
then
    mv ./eXo/util/options_linux.conf ./eXo/emulators/dosbox/options_linux.conf
fi

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
sed -i -e "s|aspect=true|aspect=${aspect}|g"   ./eXo/emulators/dosbox/options_linux.conf
sed -i -e "s|aspect=false|aspect=${aspect}|g"  ./eXo/emulators/dosbox/options_linux.conf

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
sed -i -e "s|fullscreen=true|fullscreen=${fullscreen}|g"   ./eXo/emulators/dosbox/options_linux.conf
sed -i -e "s|fullscreen=false|fullscreen=${fullscreen}|g"  ./eXo/emulators/dosbox/options_linux.conf

# ── Make scripts executable ───────────────────────────────────────────────────
echo ""
echo "Setting file permissions..."
find ./eXo/util       -name "*.bsh" -exec chmod +x {} \; 2>/dev/null
find ./eXo/util       -name "*.msh" -exec chmod +x {} \; 2>/dev/null
find ./eXo/eXoWin3x   -name "*.bsh"     -exec chmod +x {} \; 2>/dev/null
find ./eXo/eXoWin3x   -name "*.msh"     -exec chmod +x {} \; 2>/dev/null
find ./eXo/eXoWin3x   -name "*.command" -exec chmod +x {} \; 2>/dev/null
echo "Done."

clear
echo ""
echo "======================================================="
echo "   eXoWin3x Linux Patch Setup Complete!"
echo "======================================================="
echo ""
echo "To play a game:"
echo "  - Navigate to eXoWin3x/eXo/eXoWin3x/!win3x/<GameDir>/"
echo "  - Double-click the .command file, or run the .bsh file in a terminal"
echo ""
echo "The first time you launch a game it will offer to install (unzip) it."
echo ""
read -s -n 1 -p "Press any key to exit."
printf "\n\n"
"""

# Setup .msh stub
SETUP_MSH_STUB = r"""#!/usr/bin/env bash
if [[ "$LD_PRELOAD" =~ "gameoverlayrenderer" ]]
then
    LD_PRELOAD=""
fi
[[ $0 == $BASH_SOURCE ]] && cd "$( dirname "$0")"
scriptDir="$(cd "$( dirname "$BASH_SOURCE")" && pwd)"

if [[ "$OSTYPE" == "linux-gnu"* ]]
then
    source "$scriptDir/$(basename -- "${BASH_SOURCE%.msh}.bsh")"
    exit 0
fi

printf "\n\e[1;31;47mNo macOS setup is installed.\e[0m\n\n"
printf "Please apply the eXoWin3x macOS patch.\n"
read -s -n 1 -p "Press any key to abort."
printf "\n\n"
exit 1
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

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def backslash_to_forward(conf_text: str) -> str:
    """
    Convert backslash path separators to forward slashes in dosbox AUTOEXEC
    mount/imgmount lines so they work on Linux/macOS.
    Leaves other content untouched.
    """
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
    """
    Prepare a Windows dosbox.conf for use on Linux:
    - Convert backslash paths to forward slashes in AUTOEXEC
    - Clear the mapperfile= setting (mapper file isn't valid cross-platform)
    - Keep everything else identical
    """
    conf_text = backslash_to_forward(conf_text)
    # Clear mapperfile so DOSBox doesn't try to load a Windows-path mapper
    conf_text = re.sub(r'(?m)^(mapperfile\s*=).*$', r'\1', conf_text)
    return conf_text


def build_per_game_launch_bsh(game_name: str) -> str:
    """Generate the per-game launch .bsh file content."""
    return (
        BASH_HEADER
        + BASH_DEPCHECK
        + LAUNCH_BSH_FOOTER
    )


def build_per_game_install_bsh() -> str:
    """Generate the per-game install.bsh content."""
    return (
        BASH_HEADER
        + BASH_DEPCHECK
        + INSTALL_BSH_FOOTER
    )


def build_per_game_alt_bsh() -> str:
    """Generate the per-game Extras/Alternate Launcher.bsh content."""
    return (
        BASH_HEADER
        + BASH_DEPCHECK
        + ALT_BSH_FOOTER
    )


def add_file(zf: zipfile.ZipFile, arc_path: str, content: str,
             executable: bool = False) -> None:
    """Add a text file to the zipfile with optional executable bit."""
    info = zipfile.ZipInfo(arc_path)
    if executable:
        # rwxr-xr-x
        info.external_attr = (0o100755 & 0xFFFF) << 16
    else:
        # rw-r--r--
        info.external_attr = (0o100644 & 0xFFFF) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, content.encode('utf-8'))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the eXoWin3x Linux Patch from the base Windows collection."
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

    # ── Sanity checks ────────────────────────────────────────────────────────
    if not metadata_zip.is_file():
        print(f"ERROR: Cannot find {metadata_zip}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {metadata_zip} ...")
    src = zipfile.ZipFile(str(metadata_zip), 'r')

    # ── Enumerate game directories ───────────────────────────────────────────
    game_dirs: dict[str, dict] = {}   # gamedir -> {'bat': name, 'has_dosbox2': bool}

    for name in src.namelist():
        parts = name.split('/')
        # eXo/eXoWin3x/!win3x/<gamedir>/<filename>
        if len(parts) < 5:
            continue
        if parts[0] != 'eXo' or parts[1] != 'eXoWin3x' or parts[2] != '!win3x':
            continue
        gdir = parts[3]
        fname = parts[4] if len(parts) > 4 else ''
        if not gdir or not fname:
            continue

        if gdir not in game_dirs:
            game_dirs[gdir] = {'bat': '', 'has_dosbox2': False}

        if fname.endswith(').bat') and 'Alternate' not in fname:
            game_dirs[gdir]['bat'] = fname[:-4]  # strip .bat
        if fname == 'dosbox2.conf':
            game_dirs[gdir]['has_dosbox2'] = True

    total = len(game_dirs)
    print(f"Found {total} games.")

    # ── Create output directories ────────────────────────────────────────────
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'eXo' / 'util').mkdir(parents=True, exist_ok=True)
    (output_dir / 'Content').mkdir(parents=True, exist_ok=True)

    # ── Build per-game metadata zip ──────────────────────────────────────────
    meta_zip_path = output_dir / 'Content' / '!Win3x_linux_metadata.zip'
    print(f"Building {meta_zip_path} ...")

    with zipfile.ZipFile(str(meta_zip_path), 'w', zipfile.ZIP_DEFLATED) as mz:
        for idx, (gdir, info) in enumerate(sorted(game_dirs.items()), 1):
            if idx % 100 == 0 or idx == total:
                print(f"  Processing game {idx}/{total}  ({gdir}) ...")

            game_name = info['bat']
            if not game_name:
                # Fall back: derive from gdir (shouldn't happen with valid metadata)
                game_name = gdir

            base = f"eXo/eXoWin3x/!win3x/{gdir}"

            # ── dosbox_linux.conf ────────────────────────────────────────────
            dosbox_conf_key = f"eXo/eXoWin3x/!win3x/{gdir}/dosbox.conf"
            try:
                raw_conf = src.read(dosbox_conf_key).decode('utf-8', errors='replace')
                linux_conf = fix_dosbox_linux_conf(raw_conf)
            except KeyError:
                print(f"  WARNING: no dosbox.conf for {gdir}, skipping conf", file=sys.stderr)
                linux_conf = ""

            if linux_conf:
                add_file(mz, f"{base}/dosbox_linux.conf", linux_conf)

            # dosbox2_linux.conf if present
            if info['has_dosbox2']:
                dosbox2_key = f"eXo/eXoWin3x/!win3x/{gdir}/dosbox2.conf"
                try:
                    raw2 = src.read(dosbox2_key).decode('utf-8', errors='replace')
                    linux2 = fix_dosbox_linux_conf(raw2)
                    add_file(mz, f"{base}/dosbox2_linux.conf", linux2)
                except KeyError:
                    pass

            # ── Per-game launch .bsh ─────────────────────────────────────────
            launch_bsh = build_per_game_launch_bsh(game_name)
            add_file(mz, f"{base}/{game_name}.bsh", launch_bsh, executable=True)

            # ── Per-game launch .command ─────────────────────────────────────
            add_file(mz, f"{base}/{game_name}.command", COMMAND_TEMPLATE, executable=True)

            # ── Per-game install.bsh ─────────────────────────────────────────
            install_bsh = build_per_game_install_bsh()
            add_file(mz, f"{base}/install.bsh", install_bsh, executable=True)

            # ── Per-game install.command ─────────────────────────────────────
            add_file(mz, f"{base}/install.command", COMMAND_TEMPLATE, executable=True)

            # ── Extras/Alternate Launcher.bsh ────────────────────────────────
            alt_bsh = build_per_game_alt_bsh()
            add_file(mz, f"{base}/Extras/Alternate Launcher.bsh", alt_bsh, executable=True)

            # ── Extras/Alternate Launcher.command ────────────────────────────
            add_file(mz, f"{base}/Extras/Alternate Launcher.command",
                     COMMAND_TEMPLATE, executable=True)

    print(f"  Done — {total} games written.")

    # ── Build util zip (global scripts) ─────────────────────────────────────
    util_zip_path = output_dir / 'eXo' / 'util' / 'utilWin3x_linux.zip'
    print(f"Building {util_zip_path} ...")

    with zipfile.ZipFile(str(util_zip_path), 'w', zipfile.ZIP_DEFLATED) as uz:
        add_file(uz, 'launch.bsh',         GLOBAL_LAUNCH_BSH,          executable=True)
        add_file(uz, 'launch.msh',         GLOBAL_LAUNCH_MSH_STUB,     executable=True)
        add_file(uz, 'install.bsh',        GLOBAL_INSTALL_BSH,         executable=True)
        add_file(uz, 'install.msh',        GLOBAL_INSTALL_MSH_STUB,    executable=True)
        add_file(uz, 'AltLauncher.bsh',    GLOBAL_ALTLAUNCHER_BSH,     executable=True)
        add_file(uz, 'dosbox_linux.txt',   '',                         executable=False)
        # options_linux.conf placed here; setup.bsh moves it to emulators/dosbox/
        add_file(uz, 'options_linux.conf', OPTIONS_LINUX_CONF,         executable=False)

    print("  Done.")

    # ── Write Setup scripts ──────────────────────────────────────────────────
    print("Writing setup scripts ...")

    setup_bsh_path = output_dir / 'eXo' / 'util' / 'Setup eXoWin3x.bsh'
    setup_bsh_path.write_text(SETUP_BSH, encoding='utf-8')
    setup_bsh_path.chmod(setup_bsh_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    setup_msh_path = output_dir / 'eXo' / 'util' / 'Setup eXoWin3x.msh'
    setup_msh_path.write_text(SETUP_MSH_STUB, encoding='utf-8')
    setup_msh_path.chmod(setup_msh_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # Root-level .command entry point (sources setup scripts from eXo/util/)
    root_setup_command = output_dir / 'Setup eXoWin3x.command'
    root_setup_command.write_text(
        COMMAND_TEMPLATE
            .replace('$(basename -- "${BASH_SOURCE%.command}.bsh")', 'eXo/util/Setup eXoWin3x.bsh')
            .replace('$(basename -- "${BASH_SOURCE%.command}.msh")', 'eXo/util/Setup eXoWin3x.msh'),
        encoding='utf-8'
    )
    root_setup_command.chmod(
        root_setup_command.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    )

    print("  Done.")

    # ── Write README ─────────────────────────────────────────────────────────
    readme_path = output_dir / 'eXoWin3x Linux ReadMe.txt'
    readme_path.write_text(README_TEXT, encoding='utf-8')

    print()
    print("=" * 60)
    print(f"Linux patch generated at:")
    print(f"   {output_dir}")
    print()
    print("Distribute this folder alongside eXoWin3x.")
    print("Users run:  Setup eXoWin3x.command  (from the patch folder).")
    print("=" * 60)

    src.close()


README_TEXT = """\
    eXoWin3x Collection
    Linux Patch (v1.0)
    =======================================================

DESCRIPTION
-----------
This is the Linux (and macOS*) patch for the eXoWin3x collection of
Windows 3.0 / 3.1 / 3.11 games.

It adds Bash launcher scripts so all 1,138 games can be played
directly from a Linux desktop or the command line.

*macOS support requires the separate eXoWin3x macOS patch.


REQUIREMENTS
------------
- The base eXoWin3x collection (placed alongside this patch folder)
- Flatpak:       https://flatpak.org
- DOSBox-ECE flatpak (com.retro_exo.dosbox-ece-r4482)
  Install via the eXoDOS install_dependencies.command, or manually:
    flatpak install flathub com.retro_exo.dosbox-ece-r4482
- wget, curl, unzip, python3, sed  (standard on most Linux distros)
- Bash 5+  (Ubuntu 20.04+, Arch, Fedora, etc. all ship with Bash 5)
- aria2c  (optional — required for eXoGUI Lite mode torrent downloads)


SETUP
-----
1. Copy the contents of this eXoWin3x-Linux-Patch/ folder into
   your eXoWin3x/ collection folder (merge, don't replace):

     eXoWin3x/          ← copy patch contents here
       eXo/
       Content/
       ...

2. Double-click  Setup eXoWin3x.command  (from the eXoWin3x folder).

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
    Double-click the  <GameName>.command  file (or run  <GameName>.bsh
    in a terminal).  On first launch you will be asked to install
    (decompress) the game.


CONTACT
-------
Patches maintained by the eXo community.
See https://www.retro-exo.com for more information.
"""


if __name__ == '__main__':
    main()
