#!/bin/bash
#
# OS4AI - Hardware-Aware Consciousness Platform
# One-click installation for macOS
#
# Usage: curl -fsSL https://raw.githubusercontent.com/midnightnow/os4ai/main/install.sh | bash
#

set -e

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "=================================================="
echo "  OS4AI - Hardware-Aware Consciousness Platform"
echo "  Installation Script v2.0"
echo "=================================================="
echo -e "${NC}"

# Check macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}ERROR: OS4AI requires macOS 12.0 or later${NC}"
    exit 1
fi

# Check macOS version
OS_VERSION=$(sw_vers -productVersion | cut -d. -f1)
if [[ "$OS_VERSION" -lt 12 ]]; then
    echo -e "${RED}ERROR: OS4AI requires macOS 12.0 (Monterey) or later${NC}"
    echo "Current version: $(sw_vers -productVersion)"
    exit 1
fi
echo -e "${GREEN}macOS version OK ($(sw_vers -productVersion))${NC}"

# Step 1: Check/Install Homebrew
echo ""
echo -e "${YELLOW}Step 1/5: Checking Homebrew...${NC}"
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add brew to PATH for Apple Silicon
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
fi
echo -e "${GREEN}Homebrew OK${NC}"

# Step 2: Install system dependencies
echo ""
echo -e "${YELLOW}Step 2/5: Installing system dependencies...${NC}"
brew install blueutil 2>/dev/null || true
echo -e "${GREEN}blueutil OK${NC}"

# Step 3: Check Python 3
echo ""
echo -e "${YELLOW}Step 3/5: Checking Python 3.10+...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "Installing Python 3..."
    brew install python@3.12
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(sys.version_info.minor)')
if [[ "$PYTHON_VERSION" -lt 10 ]]; then
    echo -e "${YELLOW}Python 3.10+ recommended. Installing...${NC}"
    brew install python@3.12
fi
echo -e "${GREEN}Python 3 OK ($(python3 --version))${NC}"

# Step 4: Install Python packages
echo ""
echo -e "${YELLOW}Step 4/5: Installing Python packages...${NC}"
pip3 install --quiet --upgrade pip
pip3 install --quiet streamlit plotly numpy scipy
echo -e "${GREEN}Python packages OK${NC}"

# Step 5: Clone/Update OS4AI
echo ""
echo -e "${YELLOW}Step 5/5: Installing OS4AI...${NC}"

OS4AI_DIR="$HOME/os4ai"

if [[ -d "$OS4AI_DIR" ]]; then
    echo "Updating existing installation..."
    cd "$OS4AI_DIR"
    git pull origin main 2>/dev/null || true
else
    echo "Cloning OS4AI..."
    git clone https://github.com/midnightnow/os4ai.git "$OS4AI_DIR"
fi

# Create launch scripts
cat > "$OS4AI_DIR/launch.sh" << 'LAUNCH'
#!/bin/bash
cd "$(dirname "$0")"
streamlit run os4ai_streamlit.py --server.port 8501
LAUNCH
chmod +x "$OS4AI_DIR/launch.sh"

cat > "$OS4AI_DIR/launch_tinhat.sh" << 'TINHAT'
#!/bin/bash
cd "$(dirname "$0")"
streamlit run tinhat_toolkit.py --server.port 8503
TINHAT
chmod +x "$OS4AI_DIR/launch_tinhat.sh"

echo -e "${GREEN}OS4AI installed to $OS4AI_DIR${NC}"

# Done!
echo ""
echo -e "${CYAN}=================================================="
echo "  Installation Complete!"
echo "==================================================${NC}"
echo ""
echo -e "To launch ${GREEN}OS4AI Dashboard${NC}:"
echo -e "  ${YELLOW}cd $OS4AI_DIR && ./launch.sh${NC}"
echo ""
echo -e "To launch ${GREEN}TinHat Toolkit${NC}:"
echo -e "  ${YELLOW}cd $OS4AI_DIR && ./launch_tinhat.sh${NC}"
echo ""
echo -e "Or run directly:"
echo -e "  ${YELLOW}streamlit run $OS4AI_DIR/os4ai_streamlit.py${NC}"
echo ""
echo -e "${CYAN}Dashboards:${NC}"
echo "  OS4AI:  http://localhost:8501"
echo "  TinHat: http://localhost:8503"
echo ""
echo -e "${GREEN}Enjoy your hardware consciousness! ${NC}"
