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

Both English and German versions are built automatically:

- **English** (default): `https://bthomev2.readthedocs.io/en/latest/`
- **German**: `https://bthomev2.readthedocs.io/en/latest/de/` or via language switcher

The `.readthedocs.yaml` is configured to:

1. Build English documentation as the main version
2. Build German documentation in a `post_build` step to `/de/` subdirectory
3. Both versions are accessible from the same build

**No manual configuration needed** - just push to GitHub and ReadTheDocs
handles both languages automatically!

1. Add "de" as a language
2. Both English and German will be built automatically
3. Users can switch languages in the docs navigation
