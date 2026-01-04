#!/bin/bash
# Initialize German translation for BThomeV2 documentation

set -e

echo "=== BThomeV2 Documentation - German Translation Setup ==="
echo ""

# Check if we're in the docs directory
if [ ! -f "conf.py" ]; then
    echo "Error: Please run this script from the docs/ directory"
    exit 1
fi

# Install requirements
echo "1. Installing requirements..."
pip install -q -r requirements.txt

# Extract translatable strings
echo "2. Extracting translatable strings..."
make gettext

# Initialize German locale
echo "3. Initializing German locale..."
sphinx-intl update -p _build/gettext -l de

# Create .gitkeep for locale directory
mkdir -p locale/de/LC_MESSAGES
touch locale/.gitkeep

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Edit .po files in locale/de/LC_MESSAGES/"
echo "  2. Build German docs: make html -D language=de"
echo "  3. View result: firefox _build/html/index.html"
echo ""
echo "For more info, see I18N.md"
