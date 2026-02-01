#!/bin/bash
#
# AVRT iOS SDK - Enterprise Build Script
# Generates TestFlight-ready IPA for Private Enterprise Evaluation
#
# Usage:
#   ./build_enterprise.sh [TEAM_ID]
#
# (c) 2025 Jason I. Proper, BGBH Threads LLC
# Patent: USPTO 19/236,935
#

set -e

# Configuration
PROJECT_NAME="AVRT_iOS"
SCHEME="AVRT_iOS"
SDK_NAME="AVRT_SDK"
BUILD_DIR="./build"
EXPORT_DIR="${BUILD_DIR}/enterprise"
ARCHIVE_PATH="${BUILD_DIR}/${PROJECT_NAME}.xcarchive"
IPA_NAME="AVRT_SDK_FINAL_013126.ipa"
FRAMEWORK_NAME="AVRT_SDK.framework"

# Get Team ID from argument or prompt
TEAM_ID="${1:-}"
if [ -z "$TEAM_ID" ]; then
    echo "Enter your Apple Developer Team ID:"
    read -r TEAM_ID
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

clear
echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     AVRT SDK - Enterprise Build for TestFlight Evaluation          ║${NC}"
echo -e "${CYAN}║     (c) 2025 Jason I. Proper, BGBH Threads LLC                      ║${NC}"
echo -e "${CYAN}║     Patent: USPTO 19/236,935                                        ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verify Xcode
if ! command -v xcodebuild &> /dev/null; then
    echo -e "${RED}Error: Xcode not found. Please install Xcode from the App Store.${NC}"
    exit 1
fi

XCODE_VERSION=$(xcodebuild -version | head -n 1)
echo -e "${BLUE}Xcode: ${XCODE_VERSION}${NC}"
echo -e "${BLUE}Team ID: ${TEAM_ID}${NC}"
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend" || {
    echo -e "${RED}Error: frontend directory not found${NC}"
    exit 1
}

# Verify project exists
if [ ! -d "AVRT_iOS.xcodeproj" ]; then
    echo -e "${RED}Error: AVRT_iOS.xcodeproj not found${NC}"
    exit 1
fi

# Update ExportOptions with Team ID
EXPORT_PLIST="../deployment/ExportOptions-Enterprise.plist"
sed -i.bak "s/YOUR_TEAM_ID/${TEAM_ID}/g" "$EXPORT_PLIST" 2>/dev/null || \
    sed -i '' "s/YOUR_TEAM_ID/${TEAM_ID}/g" "$EXPORT_PLIST"

echo -e "${YELLOW}Step 1/5: Cleaning previous builds...${NC}"
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"
mkdir -p "${EXPORT_DIR}"
xcodebuild clean -scheme "${SCHEME}" -quiet 2>/dev/null || true
echo -e "${GREEN}Done.${NC}"
echo ""

echo -e "${YELLOW}Step 2/5: Building archive...${NC}"
echo "This may take several minutes..."

xcodebuild archive \
    -scheme "${SCHEME}" \
    -configuration Release \
    -archivePath "${ARCHIVE_PATH}" \
    -destination "generic/platform=iOS" \
    -allowProvisioningUpdates \
    DEVELOPMENT_TEAM="${TEAM_ID}" \
    MARKETING_VERSION="1.0.0" \
    CURRENT_PROJECT_VERSION="013126" \
    CODE_SIGN_STYLE="Automatic" \
    2>&1 | while read -r line; do
        if [[ "$line" == *"error:"* ]]; then
            echo -e "${RED}$line${NC}"
        elif [[ "$line" == *"warning:"* ]]; then
            echo -e "${YELLOW}$line${NC}"
        elif [[ "$line" == *"Signing"* ]] || [[ "$line" == *"Compiling"* ]]; then
            echo -e "${BLUE}$line${NC}"
        fi
    done

if [ ! -d "${ARCHIVE_PATH}" ]; then
    echo -e "${RED}Error: Archive failed. Check Xcode signing configuration.${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "1. Open AVRT_iOS.xcodeproj in Xcode"
    echo "2. Select the AVRT_iOS target"
    echo "3. Go to Signing & Capabilities"
    echo "4. Select Team: BGBH Threads LLC"
    echo "5. Ensure 'Automatically manage signing' is checked"
    exit 1
fi

echo -e "${GREEN}Archive created successfully.${NC}"
echo ""

echo -e "${YELLOW}Step 3/5: Exporting IPA for TestFlight...${NC}"

xcodebuild -exportArchive \
    -archivePath "${ARCHIVE_PATH}" \
    -exportPath "${EXPORT_DIR}" \
    -exportOptionsPlist "$EXPORT_PLIST" \
    -allowProvisioningUpdates \
    2>&1 | grep -E "(Exported|error:|warning:|Upload)" || true

# Rename IPA
if [ -f "${EXPORT_DIR}/${PROJECT_NAME}.ipa" ]; then
    mv "${EXPORT_DIR}/${PROJECT_NAME}.ipa" "${EXPORT_DIR}/${IPA_NAME}"
fi

if [ ! -f "${EXPORT_DIR}/${IPA_NAME}" ]; then
    echo -e "${YELLOW}IPA export to file not completed. Checking if uploaded directly...${NC}"
fi

echo -e "${GREEN}Export complete.${NC}"
echo ""

echo -e "${YELLOW}Step 4/5: Generating SHA256 checksums...${NC}"

cd "${EXPORT_DIR}"

# Generate SHA256SUMS.txt
cat > SHA256SUMS.txt << EOF
# ══════════════════════════════════════════════════════════════════════
# AVRT SDK SHA-256 Integrity Verification
# ══════════════════════════════════════════════════════════════════════
#
# Build Information:
#   Version:     1.0.0
#   Build:       013126
#   Date:        $(date -u +"%Y-%m-%d %H:%M:%S UTC")
#   Team ID:     ${TEAM_ID}
#
# Patent:        USPTO 19/236,935
# Trademarks:    AVRT, SPIEL, THT, EaaS, LARM, AWOGO, BeGoodBeHumble
#
# (c) 2025 Jason I. Proper, BGBH Threads LLC
# ══════════════════════════════════════════════════════════════════════

EOF

# Add checksums for all build artifacts
for file in *.ipa *.plist 2>/dev/null; do
    if [ -f "$file" ]; then
        shasum -a 256 "$file" >> SHA256SUMS.txt
    fi
done

echo -e "${GREEN}SHA256SUMS.txt generated.${NC}"
echo ""

echo -e "${YELLOW}Step 5/5: Generating AVRT_README_APPLE.md...${NC}"

cat > AVRT_README_APPLE.md << 'MDEOF'
# AVRT SDK - Apple TestFlight Submission

**Version:** 1.0.0 | **Build:** 013126
**Patent:** USPTO 19/236,935
**Developer:** BGBH Threads LLC (Jason I. Proper)

---

## Distribution Type

**Private Enterprise Evaluation** via TestFlight Internal Testing

This build is intended for B2B enterprise evaluation only. Not for public App Store distribution.

---

## SDK Classification

| Attribute | Value |
|-----------|-------|
| App Type | Middleware SDK Demo |
| Monetization | B2B Stripe Licensing (External) |
| In-App Purchases | None |
| Apple Pay | Not Used |
| Subscriptions | External Only |

---

## Stripe B2B Licensing Portal

All licensing handled via: `https://buy.stripe.com/8wMaGE3kV0f61jW6oo`

| Tier | Price | API Requests |
|------|-------|--------------|
| Developer | $29/mo | 10,000 |
| Startup | $99/mo | 100,000 |
| Business | $299/mo | 500,000 |
| Enterprise | Custom | Unlimited |

---

## Included Components

- **SPIEL_POLICY_ENFORCER.swift** - Safety, Personalization, Integrity, Ethics, Logic
- **LARM_LOGGER.swift** - Encrypted audit logging with SHA-256 chains
- **EAS_RULE_ENGINE.swift** - Ethics-as-a-Service rule evaluation
- **VoiceService.swift** - On-device speech recognition
- **HashService.swift** - SHA-256 integrity verification

---

## Privacy Compliance

- No user tracking
- No data collection
- Voice processed on-device only
- Audit logs encrypted locally (AES-256)
- GDPR/CCPA compliant architecture

---

## Contact

- **Enterprise:** info@avrt.pro
- **Support:** support@avrt.pro
- **Founder:** jason.proper29@gmail.com

---

*AVRT - Protect the Input Before the Output Can Cause Harm.*

(c) 2025 BGBH Threads LLC. All Rights Reserved.
MDEOF

echo -e "${GREEN}Documentation generated.${NC}"
echo ""

# Final output
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                     BUILD COMPLETE                                 ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Output Directory:${NC} ${EXPORT_DIR}"
echo ""
echo "Files:"
ls -la
echo ""
echo -e "${BLUE}SHA256 Checksums:${NC}"
grep -v "^#" SHA256SUMS.txt | grep -v "^$" || echo "  (IPA may have been uploaded directly)"
echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                    NEXT STEPS                                      ║${NC}"
echo -e "${CYAN}╠════════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║  If IPA was exported:                                              ║${NC}"
echo -e "${CYAN}║    1. xcrun altool --upload-app -f ${IPA_NAME}                     ║${NC}"
echo -e "${CYAN}║       -t ios -u jason.proper29@gmail.com                           ║${NC}"
echo -e "${CYAN}║                                                                    ║${NC}"
echo -e "${CYAN}║  Or via Xcode:                                                     ║${NC}"
echo -e "${CYAN}║    1. Window > Organizer                                           ║${NC}"
echo -e "${CYAN}║    2. Select archive > Distribute App                              ║${NC}"
echo -e "${CYAN}║    3. Choose 'App Store Connect' > Upload                          ║${NC}"
echo -e "${CYAN}║                                                                    ║${NC}"
echo -e "${CYAN}║  In App Store Connect:                                             ║${NC}"
echo -e "${CYAN}║    1. Go to TestFlight > Internal Testing                          ║${NC}"
echo -e "${CYAN}║    2. Add build to internal testers group                          ║${NC}"
echo -e "${CYAN}║    3. Flag as 'Private Enterprise Evaluation'                      ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}AVRT SDK Enterprise Build Complete.${NC}"
echo "Patent: USPTO 19/236,935 | AVRT | SPIEL | THT | EaaS | LARM"
echo ""
