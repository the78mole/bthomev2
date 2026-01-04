# BThomeV2 Documentation

This directory contains the Sphinx documentation for the BThomeV2 library.

## Languages

- **English** (primary): Main documentation in English
- **German**: Available via Sphinx internationalization (i18n)

## Building the Documentation

### Prerequisites

Install uv if not already available:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Quick Build (Recommended)

Use the build script with uv:

```bash
# Build both English and German documentation
./build-all.sh

# Build English documentation only
./build.sh

# Build German documentation only
./build.sh --language de

# Clean build (all languages)
./build-all.sh --clean
```

### Manual Build with uv

```bash
# Build English
uv run --with sphinx --with sphinx-rtd-theme --with myst-parser \
  --with sphinx-intl sphinx-build -b html . _build/html

# Build German
uv run --with sphinx --with sphinx-rtd-theme --with myst-parser \
  --with sphinx-intl sphinx-build -b html -D language=de . _build/html/de
```

### Traditional Build with Make

If you prefer using make:

```bash
# Install dependencies first
pip install -r requirements.txt

# Build English
make html

# Build German
make html -D language=de
```

## Opening Documentation

After building:

```bash
# Open English documentation
firefox _build/html/index.html

# Or with the build script output link
```

## Structure

- `conf.py` - Sphinx configuration
- `index.rst` - Main page
- `installation.rst` - Installation guide
- `quickstart.rst` - Quick start guide
- `library/` - Library documentation
- `tools/` - Tool documentation
- `development/` - Development documentation
- `locale/` - Translations (German, etc.)

## Translation

To contribute translations, see [I18N.md](I18N.md) for detailed instructions.

Quick start:

```bash
cd docs
./setup_translation.sh
# Edit .po files in locale/de/LC_MESSAGES/
make html -D language=de
```

## ReadTheDocs Integration

The documentation is automatically built on ReadTheDocs with each push.
Configuration: `.readthedocs.yaml` in repository root.

### Language Versions

ReadTheDocs can build multiple language versions. To enable:

1. Go to project settings on ReadTheDocs
2. Navigate to "Translations"
3. Add "de" as a language
4. Both English and German will be built automatically
5. Users can switch languages in the docs navigation
