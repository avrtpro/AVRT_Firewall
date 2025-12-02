#!/bin/bash
# AVRT™ Deployment Script
# Automated deployment helper for AVRT 5.1

set -e

echo "═══════════════════════════════════════════════════════════"
echo "   🛡️  AVRT™ 5.1 Deployment Script"
echo "   Advanced Voice Reasoning Technology"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."

    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found. Please install Python 3.9+"
        exit 1
    fi
    print_success "Python $(python3 --version) found"

    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_warning "Node.js not found (required for mobile app)"
    else
        print_success "Node.js $(node --version) found"
    fi

    # Check Git
    if ! command -v git &> /dev/null; then
        print_warning "Git not found"
    else
        print_success "Git $(git --version | awk '{print $3}') found"
    fi

    echo ""
}

# Deploy API Server
deploy_api() {
    print_info "Deploying AVRT API Server..."

    # Install dependencies
    if [ -f "requirements.txt" ]; then
        print_info "Installing Python dependencies..."
        pip install -r requirements.txt
        print_success "Dependencies installed"
    fi

    # Check .env file
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Copying from .env.example..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_warning "Please configure .env before running the server"
        fi
    fi

    # Test middleware
    print_info "Testing AVRT middleware..."
    python3 middleware.py --test
    print_success "Middleware tests passed"

    echo ""
    print_success "API Server ready to deploy!"
    print_info "Start with: python3 api_server.py"
    echo ""
}

# Deploy Mobile App
deploy_mobile() {
    print_info "Setting up Mobile App..."

    if [ ! -d "mobile-app" ]; then
        print_error "mobile-app directory not found"
        return 1
    fi

    cd mobile-app

    # Install dependencies
    if [ -f "package.json" ]; then
        print_info "Installing Node.js dependencies..."
        npm install
        print_success "Dependencies installed"
    fi

    # Check .env
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Copying from .env.example..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_warning "Please configure .env with your API URL"
        fi
    fi

    cd ..

    echo ""
    print_success "Mobile App ready!"
    print_info "Start with: cd mobile-app && npm start"
    echo ""
}

# Generate verification hash
generate_hash() {
    print_info "Generating verification hash..."

    if [ -f "generate-hash.sh" ]; then
        bash generate-hash.sh
    else
        print_warning "generate-hash.sh not found"
    fi

    echo ""
}

# Main deployment menu
main() {
    check_prerequisites

    echo "Select deployment option:"
    echo "1) Deploy API Server"
    echo "2) Setup Mobile App"
    echo "3) Deploy Both"
    echo "4) Generate Verification Hash"
    echo "5) Exit"
    echo ""
    read -p "Enter option [1-5]: " option

    case $option in
        1)
            deploy_api
            ;;
        2)
            deploy_mobile
            ;;
        3)
            deploy_api
            deploy_mobile
            ;;
        4)
            generate_hash
            ;;
        5)
            print_info "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid option"
            exit 1
            ;;
    esac

    echo "═══════════════════════════════════════════════════════════"
    echo "   ✅ DEPLOYMENT COMPLETE"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "📞 Support: info@avrt.pro"
    echo "🌐 Website: https://avrt.pro"
    echo "📦 GitHub: https://github.com/avrtpro/AVRT_Firewall"
    echo ""
    echo "© 2025 Jason I. Proper, BGBH Threads LLC"
    echo "Licensed under CC BY-NC 4.0"
    echo ""
}

# Run main
main
