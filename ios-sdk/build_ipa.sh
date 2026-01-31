#!/bin/bash
#
# AVRT iOS SDK - IPA Build Script
# Generates TestFlight-ready IPA with SHA-256 verification
#
# (c) 2025 Jason I. Proper, BGBH Threads LLC
# Patent: USPTO 19/236,935
#

set -e

# Configuration
PROJECT_NAME="AVRT_iOS"
SCHEME="AVRT_iOS"
BUILD_DIR="./build"
EXPORT_DIR="${BUILD_DIR}/export"
ARCHIVE_PATH="${BUILD_DIR}/${PROJECT_NAME}.xcarchive"
IPA_NAME="AVRT_SDK_FINAL_013126.ipa"
EXPORT_OPTIONS="../deployment/ExportOptions.plist"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║        AVRT iOS SDK - TestFlight Build Script                 ║"
echo "║        (c) 2025 Jason I. Proper, BGBH Threads LLC             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check for Xcode
if ! command -v xcodebuild &> /dev/null; then
    echo -e "${RED}Error: Xcode command line tools not found.${NC}"
    echo "Please install Xcode and run: xcode-select --install"
    exit 1
fi

# Get Xcode version
XCODE_VERSION=$(xcodebuild -version | head -n 1)
echo -e "${BLUE}Using: ${XCODE_VERSION}${NC}"
echo ""

# Check for project
if [ ! -d "AVRT_iOS.xcodeproj" ]; then
    echo -e "${RED}Error: AVRT_iOS.xcodeproj not found.${NC}"
    echo "Please run this script from the ios-sdk/frontend directory."
    exit 1
fi

# Clean previous builds
echo -e "${YELLOW}Step 1: Cleaning previous builds...${NC}"
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"
mkdir -p "${EXPORT_DIR}"
xcodebuild clean -scheme "${SCHEME}" -quiet
echo -e "${GREEN}Clean complete.${NC}"
echo ""

# Build archive
echo -e "${YELLOW}Step 2: Building archive...${NC}"
echo "This may take several minutes..."

xcodebuild archive \
    -scheme "${SCHEME}" \
    -configuration Release \
    -archivePath "${ARCHIVE_PATH}" \
    -destination "generic/platform=iOS" \
    -allowProvisioningUpdates \
    MARKETING_VERSION="1.0.0" \
    CURRENT_PROJECT_VERSION="013126" \
    | grep -E "(Signing|Compiling|Linking|error:|warning:)" || true

if [ ! -d "${ARCHIVE_PATH}" ]; then
    echo -e "${RED}Error: Archive build failed.${NC}"
    exit 1
fi

echo -e "${GREEN}Archive created: ${ARCHIVE_PATH}${NC}"
echo ""

# Export IPA
echo -e "${YELLOW}Step 3: Exporting IPA for TestFlight...${NC}"

if [ ! -f "${EXPORT_OPTIONS}" ]; then
    echo -e "${YELLOW}Creating ExportOptions.plist...${NC}"
    cat > "${EXPORT_OPTIONS}" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store-connect</string>
    <key>destination</key>
    <string>upload</string>
    <key>signingStyle</key>
    <string>automatic</string>
    <key>uploadSymbols</key>
    <true/>
    <key>compileBitcode</key>
    <false/>
</dict>
</plist>
PLIST
fi

xcodebuild -exportArchive \
    -archivePath "${ARCHIVE_PATH}" \
    -exportPath "${EXPORT_DIR}" \
    -exportOptionsPlist "${EXPORT_OPTIONS}" \
    -allowProvisioningUpdates \
    | grep -E "(Exported|error:|warning:)" || true

# Rename IPA
if [ -f "${EXPORT_DIR}/${PROJECT_NAME}.ipa" ]; then
    mv "${EXPORT_DIR}/${PROJECT_NAME}.ipa" "${EXPORT_DIR}/${IPA_NAME}"
fi

if [ ! -f "${EXPORT_DIR}/${IPA_NAME}" ]; then
    echo -e "${RED}Error: IPA export failed.${NC}"
    echo "You may need to configure signing in Xcode first."
    exit 1
fi

echo -e "${GREEN}IPA created: ${EXPORT_DIR}/${IPA_NAME}${NC}"
echo ""

# Generate SHA256SUMS
echo -e "${YELLOW}Step 4: Generating SHA256 checksums...${NC}"

cd "${EXPORT_DIR}"

cat > SHA256SUMS.txt << EOF
# AVRT iOS SDK SHA256 Checksums
# Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
# Build: 013126
# Patent: USPTO 19/236,935
# (c) 2025 Jason I. Proper, BGBH Threads LLC

EOF

shasum -a 256 "${IPA_NAME}" >> SHA256SUMS.txt

echo -e "${GREEN}SHA256SUMS.txt created.${NC}"
echo ""

# Display results
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    BUILD COMPLETE                             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}Build Artifacts:${NC}"
echo ""
ls -la
echo ""
echo -e "${BLUE}SHA256 Checksum:${NC}"
cat SHA256SUMS.txt | grep -v "^#"
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                 NEXT STEPS                                    ║"
echo "╠═══════════════════════════════════════════════════════════════╣"
echo "║ 1. Open Xcode > Window > Organizer                            ║"
echo "║ 2. Select the archive and click 'Distribute App'              ║"
echo "║ 3. Choose 'App Store Connect' > 'Upload'                      ║"
echo "║ 4. Or use: xcrun altool --upload-app --file ${IPA_NAME}       ║"
echo "║ 5. Check TestFlight in App Store Connect after processing     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}AVRT SDK Build Script Complete.${NC}"
echo "Patent: USPTO 19/236,935 | AVRT | SPIEL | THT | EaaS | LARM"
echo ""
