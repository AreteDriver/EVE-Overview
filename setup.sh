#!/bin/bash
# Setup script for EVE Overview

set -e

echo "================================"
echo "EVE Overview Setup Script"
echo "================================"
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Error: This application is designed for Linux only."
    exit 1
fi

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "Error: Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi
echo "✓ Python $PYTHON_VERSION found"

# Check for system dependencies
echo ""
echo "Checking system dependencies..."

MISSING_DEPS=()

for cmd in wmctrl xdotool convert import xwd; do
    if ! command -v $cmd &> /dev/null; then
        MISSING_DEPS+=($cmd)
    else
        echo "✓ $cmd found"
    fi
done

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    echo "Missing system dependencies: ${MISSING_DEPS[@]}"
    echo ""
    echo "Please install them using your package manager:"
    echo ""
    
    # Detect distro and show appropriate command
    if [ -f /etc/debian_version ]; then
        echo "  sudo apt-get install wmctrl xdotool imagemagick x11-apps"
    elif [ -f /etc/redhat-release ]; then
        echo "  sudo dnf install wmctrl xdotool ImageMagick xorg-x11-apps"
    elif [ -f /etc/arch-release ]; then
        echo "  sudo pacman -S wmctrl xdotool imagemagick xorg-xwd"
    else
        echo "  Install: wmctrl, xdotool, ImageMagick, x11-apps"
    fi
    echo ""
    
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
    read -p "Recreate it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment created"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip upgraded"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Python dependencies installed"

# Create launcher script
echo ""
echo "Creating launcher script..."
cat > eve-overview.sh << 'EOF'
#!/bin/bash
# EVE Overview Launcher

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Run setup.sh first."
    exit 1
fi

source venv/bin/activate
python src/main.py "$@"
EOF

chmod +x eve-overview.sh
echo "✓ Launcher script created: eve-overview.sh"

# Create config directory
echo ""
echo "Creating configuration directory..."
mkdir -p ~/.config/eve-overview/profiles
echo "✓ Configuration directory created"

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "To run EVE Overview:"
echo "  ./eve-overview.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python src/main.py"
echo ""
