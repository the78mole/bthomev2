#!/bin/bash
# Build Sphinx documentation using uv

set -e

cd "$(dirname "$0")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Building BThomeV2 Documentation with uv${NC}"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed"
    echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Parse command line arguments
LANGUAGE="en"
CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -l|--language)
            LANGUAGE="$2"
            shift 2
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [-l|--language <en|de>] [-c|--clean]"
            exit 1
            ;;
    esac
done

# Clean if requested
if [ "$CLEAN" = true ]; then
    echo -e "${BLUE}Cleaning build directory...${NC}"
    rm -rf _build/
fi

# Build documentation
echo -e "${BLUE}Building documentation (language: $LANGUAGE)...${NC}"

if [ "$LANGUAGE" = "de" ]; then
    uv run --with sphinx --with sphinx-rtd-theme --with myst-parser --with sphinx-intl sphinx-build -b html -D language=de . _build/html/de
    echo -e "${GREEN}✓ German documentation built successfully${NC}"
    echo -e "Open: file://$(pwd)/_build/html/de/index.html"
else
    uv run --with sphinx --with sphinx-rtd-theme --with myst-parser --with sphinx-intl sphinx-build -b html . _build/html
    echo -e "${GREEN}✓ English documentation built successfully${NC}"
    echo -e "Open: file://$(pwd)/_build/html/index.html"
fi
