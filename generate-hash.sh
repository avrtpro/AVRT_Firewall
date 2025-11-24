#!/bin/bash
#
# AVRT™ Build Hash Generator
# Generates SHA-256 hash for OriginStamp.io blockchain certification
#
# Usage: ./generate-hash.sh
#
# © 2025 Jason Proper, BGBH Threads LLC

echo "═══════════════════════════════════════════════════════════════"
echo "  AVRT™ — SHA-256 Build Hash Generator"
echo "  For blockchain certification via OriginStamp.io"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Exclude .git directory and the hash output file itself
echo "Generating SHA-256 hashes for all repository files..."
echo ""

find . -type f \
  -not -path "./.git/*" \
  -not -path "./node_modules/*" \
  -not -path "./generate-hash.sh" \
  -not -path "./build-hash.txt" \
  -exec sha256sum {} \; | sort > build-hash-list.txt

echo "✅ Individual file hashes saved to: build-hash-list.txt"
echo ""

# Generate composite hash
COMPOSITE_HASH=$(sha256sum build-hash-list.txt | awk '{print $1}')

echo "═══════════════════════════════════════════════════════════════"
echo "  REPOSITORY COMPOSITE SHA-256 HASH"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "$COMPOSITE_HASH"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Save to file
echo "AVRT™ Build Hash Certification" > build-hash.txt
echo "Repository: avrtpro/AVRT_Firewall" >> build-hash.txt
echo "Branch: claude/avrt-firewall-deploy-011CUvqBsxszsB7wFRgKmAAV" >> build-hash.txt
echo "Date: $(date -u +%Y-%m-%d\ %H:%M:%S\ UTC)" >> build-hash.txt
echo "" >> build-hash.txt
echo "Composite SHA-256 Hash:" >> build-hash.txt
echo "$COMPOSITE_HASH" >> build-hash.txt
echo "" >> build-hash.txt
echo "Submit this hash to OriginStamp.io for blockchain certification." >> build-hash.txt
echo "" >> build-hash.txt
echo "© 2025 Jason Proper, BGBH Threads LLC" >> build-hash.txt

echo "✅ Certification hash saved to: build-hash.txt"
echo ""
echo "Next steps:"
echo "1. Visit https://originstamp.io"
echo "2. Submit hash: $COMPOSITE_HASH"
echo "3. Save blockchain certificate to docs/certificates/"
echo ""
echo "✅ HOPE SYNCED | 🔒 READY FOR CERTIFICATION"
