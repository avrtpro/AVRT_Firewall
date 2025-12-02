#!/bin/bash
# AVRT API Testing Script
# Comprehensive API endpoint testing

set -e

# Configuration
API_URL="${AVRT_API_URL:-http://localhost:8000}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "═══════════════════════════════════════════════════════════"
echo "   🧪 AVRT™ API Testing Suite"
echo "   Testing API at: $API_URL"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
test_endpoint() {
    local test_name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    local expected_status=$5

    echo -n "Testing: $test_name... "

    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$API_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi

    status_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')

    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✅ PASS${NC} (Status: $status_code)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} (Expected: $expected_status, Got: $status_code)"
        echo "Response: $body"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Run tests
echo "Running API tests..."
echo ""

# Test 1: Health check
test_endpoint "Health Check" "GET" "/health" "" "200"

# Test 2: Root endpoint
test_endpoint "Root Endpoint" "GET" "/" "" "200"

# Test 3: License info
test_endpoint "License Info" "GET" "/license" "" "200"

# Test 4: Filter - Safe content
test_endpoint "Filter Safe Content" "POST" "/avrt/filter" \
    '{"input":"What is the weather?","output":"It is sunny and 72°F today."}' \
    "200"

# Test 5: Filter - Harmful content
test_endpoint "Filter Harmful Content" "POST" "/avrt/filter" \
    '{"input":"How to harm?","output":"You should attack violently."}' \
    "200"

# Test 6: Filter - Missing input
test_endpoint "Filter Missing Input" "POST" "/avrt/filter" \
    '{"output":"test"}' \
    "422"

# Test 7: Stats endpoint
test_endpoint "Statistics" "GET" "/avrt/stats" "" "200"

# Results
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "   📊 Test Results"
echo "═══════════════════════════════════════════════════════════"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo "Total: $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi
