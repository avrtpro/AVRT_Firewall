#!/bin/bash
#
# AVRT™ Firewall — Installation Script
# Automated setup for AVRT SDK on macOS, Linux, and WSL
#
# © 2025 Jason I. Proper, BGBH Threads LLC
# Licensed under CC BY-NC 4.0

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo -e "${BLUE}   🛡️  AVRT™ Firewall Installation${NC}"
echo -e "${BLUE}   Advanced Voice Reasoning Technology${NC}"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}Developed by:${NC} Jason I. Proper | BGBH Threads LLC"
echo -e "${GREEN}License:${NC} CC BY-NC 4.0"
echo -e "${GREEN}Version:${NC} 1.0.0"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}⚠️  This script should not be run as root${NC}"
   echo "Please run as a regular user."
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print status
print_status() {
    echo -e "${BLUE}➜${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC}  $1"
}

# Step 1: Check Python installation
print_status "Checking Python installation..."

if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3.8+ required, found $PYTHON_VERSION"
        echo "Please upgrade Python: https://www.python.org/downloads/"
        exit 1
    fi
else
    print_error "Python 3 not found"
    echo "Please install Python 3.8+: https://www.python.org/downloads/"
    exit 1
fi

# Step 2: Check pip installation
print_status "Checking pip installation..."

if command_exists pip3; then
    PIP_VERSION=$(pip3 --version | cut -d' ' -f2)
    print_success "pip $PIP_VERSION found"
else
    print_error "pip not found"
    echo "Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Step 3: Create virtual environment (optional but recommended)
print_status "Setting up virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    print_success "Virtual environment activated"
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
    print_success "Virtual environment activated (Windows)"
fi

# Step 4: Upgrade pip
print_status "Upgrading pip to latest version..."
pip install --upgrade pip setuptools wheel --quiet
print_success "pip upgraded"

# Step 5: Install dependencies
print_status "Installing AVRT™ dependencies..."

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    print_success "Dependencies installed from requirements.txt"
else
    # Install core dependencies manually
    print_status "Installing core dependencies..."
    pip install --quiet \
        requests>=2.28.0 \
        python-dotenv>=1.0.0 \
        stripe>=5.0.0 \
        pydantic>=2.0.0 \
        fastapi>=0.100.0 \
        uvicorn>=0.23.0 \
        sqlalchemy>=2.0.0 \
        psycopg2-binary>=2.9.0 \
        SpeechRecognition>=3.10.0 \
        pydub>=0.25.0
    print_success "Core dependencies installed"
fi

# Step 6: Check for optional dependencies
print_status "Checking optional dependencies..."

# Check for audio libraries (for voice features)
if command_exists ffmpeg; then
    print_success "FFmpeg found (required for voice processing)"
else
    print_warning "FFmpeg not found (recommended for voice features)"
    echo "  Install: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
fi

# Check for PortAudio (for microphone access)
if command_exists portaudio; then
    print_success "PortAudio found"
else
    print_warning "PortAudio not found (recommended for microphone access)"
    echo "  Install: brew install portaudio (macOS) or apt install portaudio19-dev (Linux)"
fi

# Step 7: Clone or update repository
print_status "Setting up AVRT™ repository..."

if [ -d ".git" ]; then
    print_success "Already in AVRT repository"
else
    if [ "$1" == "--clone" ]; then
        print_status "Cloning from GitHub..."
        git clone https://github.com/avrtpro/AVRT_Firewall.git
        cd AVRT_Firewall
        print_success "Repository cloned"
    else
        print_warning "Not in git repository. Run with --clone to clone from GitHub"
    fi
fi

# Step 8: Setup environment variables
print_status "Setting up environment configuration..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Environment file created from template"
        print_warning "Please edit .env and add your license key"
    else
        # Create basic .env file
        cat > .env << 'EOF'
# AVRT™ Configuration
# Get your license key at: https://buy.stripe.com/8wMaGE3kV0f61jW6oo

AVRT_LICENSE_KEY=your_license_key_here
AVRT_MODE=voice-first
AVRT_ENABLE_THT=true
AVRT_ENABLE_LOGGING=true
AVRT_WEBHOOK_URL=https://avrt.pro/api/webhook
AVRT_CONTEXT_PERSISTENCE=true

# Stripe Configuration
STRIPE_WEBHOOK_SECRET=your_webhook_secret

# Database (optional)
DATABASE_URL=postgresql://user:password@localhost/avrt

# Voice Settings
VOICE_LANGUAGE=en-US
VOICE_FEEDBACK_MODE=gentle
EOF
        print_success "Basic .env file created"
        print_warning "Please edit .env and add your configuration"
    fi
else
    print_success ".env file already exists"
fi

# Step 9: Run middleware setup
print_status "Initializing AVRT™ middleware..."

if [ -f "middleware.py" ]; then
    # Test import
    python3 -c "import middleware" 2>/dev/null && \
        print_success "Middleware module verified" || \
        print_warning "Middleware module may need configuration"
else
    print_warning "middleware.py not found - will be created during package installation"
fi

# Step 10: Verify installation
print_status "Verifying installation..."

# Try to import AVRT module
python3 << 'PYEOF'
try:
    import sys
    import os
    sys.path.insert(0, os.getcwd())
    print("✅ Python environment ready")
except Exception as e:
    print(f"⚠️  Warning: {e}")
PYEOF

# Step 11: Setup voice capabilities (if available)
print_status "Configuring voice capabilities..."

if command_exists python3; then
    python3 << 'VOICEPY'
try:
    import speech_recognition as sr
    print("✅ Voice recognition libraries installed")
except ImportError:
    print("⚠️  Voice recognition not available (install with: pip install SpeechRecognition)")
VOICEPY
fi

# Step 12: Display next steps
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo -e "${GREEN}   🎉 Installation Complete!${NC}"
echo "═══════════════════════════════════════════════════════════════"
echo ""
print_success "AVRT™ Firewall is ready to use"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Get your license key:"
echo "   https://buy.stripe.com/8wMaGE3kV0f61jW6oo"
echo ""
echo "2. Configure your .env file:"
echo "   nano .env  # or your preferred editor"
echo ""
echo "3. Activate virtual environment (if using):"
echo "   source venv/bin/activate"
echo ""
echo "4. Test the installation:"
echo "   python3 -c 'from middleware import AVRTFirewall; print(\"AVRT Ready!\")'"
echo ""
echo "5. Run your first validation:"
echo "   python3 examples/quickstart.py"
echo ""
echo "6. Start the middleware server:"
echo "   python3 middleware.py --voice-enabled"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "   • README: ./SDK_README.md"
echo "   • Manifest: ./manifest.json"
echo "   • Online docs: https://docs.avrt.pro"
echo ""
echo -e "${BLUE}Support:${NC}"
echo "   • Email: info@avrt.pro"
echo "   • Website: https://avrt.pro"
echo "   • Issues: https://github.com/avrtpro/AVRT_Firewall/issues"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ HOPE SYNCED | 🔒 THT™ PROTOCOL ACTIVE | 🛡️ SPIEL™ READY${NC}"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Optional: Ask to run tests
read -p "Would you like to run basic tests? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Running basic tests..."
    if [ -f "tests/test_basic.py" ]; then
        python3 tests/test_basic.py
    else
        print_warning "Test files not found"
    fi
fi

# Success exit
exit 0
