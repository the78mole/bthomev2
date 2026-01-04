# BThomeV2 Dokumentation

Diese Dokumentation wird mit Sphinx erstellt und auf
[Read the Docs](https://bthomev2.readthedocs.io/) veröffentlicht.

## Lokales Bauen

```bash
# Requirements installieren
pip install -r requirements.txt

# Dokumentation bauen
make html

# Im Browser öffnen
firefox _build/html/index.html
```

## Struktur

- `conf.py` - Sphinx-Konfiguration
- `index.rst` - Hauptseite
- `installation.rst` - Installationsanleitung
- `quickstart.rst` - Quick Start Guide
- `library/` - Library-Dokumentation
- `tools/` - Tool-Dokumentation
- `development/` - Entwicklungs-Dokumentation

## ReadTheDocs Integration

Die Dokumentation wird automatisch auf ReadTheDocs gebaut bei jedem Push.
Konfiguration siehe `.readthedocs.yaml` im Repository-Root.
