#!/bin/bash

# AVRT™ Full-Stack Deployment Script
# © 2025 Jason I. Proper / BGBH Threads LLC

set -e

echo "═══════════════════════════════════════════════════════════════"
echo "   🛡️  AVRT™ Full-Stack Deployment"
echo "   Advanced Voice Reasoning Technology"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}➜${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

if ! command -v node &> /dev/null; then
    print_error "Node.js not found. Please install Node.js 18+ first."
    exit 1
fi
print_success "Node.js found: $(node -v)"

if ! command -v npm &> /dev/null; then
    print_error "npm not found. Please install npm first."
    exit 1
fi
print_success "npm found: $(npm -v)"

# Check for .env files
if [ ! -f "backend/.env" ]; then
    print_warning "backend/.env not found. Copying from .env.example..."
    cp backend/.env.example backend/.env
    print_warning "Please edit backend/.env and add your OPENAI_API_KEY"
fi

if [ ! -f "frontend/.env" ]; then
    print_warning "frontend/.env not found. Copying from .env.example..."
    cp frontend/.env.example frontend/.env
fi

# Install backend dependencies
print_status "Installing backend dependencies..."
cd backend
npm install
if [ $? -eq 0 ]; then
    print_success "Backend dependencies installed"
else
    print_error "Failed to install backend dependencies"
    exit 1
fi
cd ..

# Install frontend dependencies
print_status "Installing frontend dependencies..."
cd frontend
npm install
if [ $? -eq 0 ]; then
    print_success "Frontend dependencies installed"
else
    print_error "Failed to install frontend dependencies"
    exit 1
fi
cd ..

# Ask user which mode to run
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Select deployment mode:"
echo "  1) Development (run locally)"
echo "  2) Production build"
echo "  3) iOS build (requires Xcode)"
echo "═══════════════════════════════════════════════════════════════"
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        print_status "Starting development servers..."
        echo ""
        print_warning "Starting backend on http://localhost:3001"
        print_warning "Starting frontend on http://localhost:5173"
        echo ""

        # Start backend in background
        cd backend
        npm run dev &
        BACKEND_PID=$!
        cd ..

        # Wait a bit for backend to start
        sleep 3

        # Start frontend in foreground
        cd frontend
        npm run dev

        # Kill backend when frontend exits
        kill $BACKEND_PID
        ;;

    2)
        print_status "Building for production..."

        # Build frontend
        print_status "Building frontend..."
        cd frontend
        npm run build
        if [ $? -eq 0 ]; then
            print_success "Frontend built successfully"
            print_success "Build output: frontend/dist/"
        else
            print_error "Frontend build failed"
            exit 1
        fi
        cd ..

        echo ""
        print_success "Production build complete!"
        echo ""
        echo "Next steps:"
        echo "  1. Deploy backend to Railway/Render/Vercel"
        echo "  2. Deploy frontend/dist to Vercel/Netlify"
        echo "  3. Update VITE_API_URL in frontend/.env"
        echo ""
        ;;

    3)
        print_status "Building for iOS..."

        # Check for Xcode
        if ! command -v xcodebuild &> /dev/null; then
            print_error "Xcode not found. iOS build requires Xcode (macOS only)"
            exit 1
        fi

        # Install Capacitor if needed
        if [ ! -d "capacitor/node_modules" ]; then
            print_status "Installing Capacitor dependencies..."
            cd capacitor
            npm install
            cd ..
        fi

        # Build frontend
        print_status "Building frontend..."
        cd frontend
        npm run build
        cd ..

        # Sync to iOS
        print_status "Syncing to iOS..."
        npx cap sync ios

        print_success "iOS build ready!"
        print_status "Opening Xcode..."
        npx cap open ios

        echo ""
        print_success "Next steps in Xcode:"
        echo "  1. Select your development team"
        echo "  2. Connect an iOS device"
        echo "  3. Click Run (⌘R) to test"
        echo "  4. Archive (⌘B) for TestFlight"
        echo ""
        ;;

    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "   ✅ HOPE SYNCED | 🔒 THT™ ACTIVE | 🛡️ SPIEL™ READY"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "   Founder: Jason I. Proper"
echo "   Patent: USPTO #19/236,935"
echo "   Contact: info@avrt.pro"
echo ""
echo "   Be Good. Be Humble. Be Protected.™"
echo "═══════════════════════════════════════════════════════════════"
