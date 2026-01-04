#!/bin/bash

# Build script for all language versions of BThomeV2 documentation
# This script builds both English and German versions

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Building BThomeV2 Documentation (All Languages)${NC}"
echo ""

# Parse arguments
CLEAN=false
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--clean)
            CLEAN=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--clean]"
            exit 1
            ;;
    esac
done

# Clean if requested
if [ "$CLEAN" = true ]; then
    echo -e "${YELLOW}Cleaning build directory...${NC}"
    rm -rf _build
    echo ""
fi

# Build English version
echo -e "${BLUE}Building English documentation...${NC}"
./build.sh --language en
echo ""

# Build German version
echo -e "${BLUE}Building German documentation...${NC}"
./build.sh --language de
echo ""

# Success message
echo -e "${GREEN}✓ All documentation versions built successfully${NC}"
echo ""
echo "English: file://$(pwd)/_build/html/index.html"
echo "German:  file://$(pwd)/_build/html/de/index.html"
