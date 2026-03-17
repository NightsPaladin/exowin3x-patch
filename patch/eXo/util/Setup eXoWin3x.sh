#!/usr/bin/env bash
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
