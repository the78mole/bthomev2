Entwicklungs-Workflow
=====================

Dieser Guide beschreibt den Entwicklungs-Workflow für das BThomeV2-Projekt,
das aus der Arduino Library und dem Python bthome-logger Tool besteht.

Überblick
---------

Das BThomeV2-Projekt verwendet ein modernes CI/CD-System mit automatischer
Versionierung und Publishing auf zwei Plattformen:

* **PlatformIO Registry** - Für die Arduino Library
* **PyPI** - Für das bthome-logger Tool

Beide Komponenten werden **synchron versioniert**, um Kompatibilität zu
gewährleisten.

Repository-Struktur
-------------------

.. code-block:: text

   bthomev2/
   ├── .github/workflows/        # CI/CD Workflows
   │   ├── release.yml          # Haupt-Release-Orchestrierung
   │   ├── pypi-publish.yml     # PyPI Publishing
   │   └── pio-publish.yml      # PlatformIO Publishing
   ├── src/                     # Library Source Code
   │   ├── BThomeV2.h          # Basis-Klasse Header
   │   ├── BThomeV2.cpp        # Basis-Klasse Implementation
   │   ├── BThomeV2_ESP32.cpp  # ESP32-spezifisch
   │   └── BThomeV2_nRF52.cpp  # nRF52-spezifisch
   ├── tools/                   # Python Tools
   │   ├── bthome_logger.py    # Logger-Tool
   │   ├── pyproject.toml      # Python Package Config
   │   └── README.md           # Tool-Dokumentation
   ├── examples/                # Beispiel-Projekte
   │   ├── ESP32_Basic/
   │   ├── ESP32_Button/
   │   └── ESP32_MultipleSensors/
   ├── docs/                    # Sphinx-Dokumentation
   ├── library.json.j2         # PlatformIO Manifest Template
   ├── library.properties.j2   # Arduino Manifest Template
   ├── library.json            # Generiert (0.0.0-dev)
   └── library.properties      # Generiert (0.0.0-dev)

Entwicklungs-Setup
------------------

Repository klonen
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/the78mole/bthomev2.git
   cd bthomev2

Library-Entwicklung
~~~~~~~~~~~~~~~~~~~

Für Library-Entwicklung wird PlatformIO empfohlen:

.. code-block:: bash

   # PlatformIO installieren
   pip install platformio

   # Beispiel kompilieren
   cd examples/ESP32_Basic
   pio run

   # Auf Hardware hochladen
   pio run --target upload

   # Serial Monitor
   pio device monitor

Tool-Entwicklung
~~~~~~~~~~~~~~~~

Für Tool-Entwicklung wird uv empfohlen:

.. code-block:: bash

   # uv installieren
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Tool im Development-Modus installieren
   cd tools
   uv tool install --editable .

   # Tool ausführen
   bthome-logger

Testing-Workflow
----------------

Typischer Entwicklungszyklus:

1. **Code ändern** in ``src/`` oder ``tools/``
2. **Library kompilieren und hochladen:**

   .. code-block:: bash

      cd examples/ESP32_Basic
      pio run --target upload
      pio device monitor

3. **In parallelem Terminal bthome-logger starten:**

   .. code-block:: bash

      bthome-logger -f "My-Device"

4. **Ausgaben vergleichen:**

   * Serial Monitor zeigt interne Logs
   * bthome-logger zeigt BLE-Advertisements

5. **Iterieren** bis alles funktioniert

Semantic Versioning
-------------------

Das Projekt verwendet `Semantic Versioning 2.0 <https://semver.org/>`_ mit
automatischer Versionserkennung basierend auf Commit-Messages.

Commit-Message-Format
~~~~~~~~~~~~~~~~~~~~~

Verwende **Conventional Commits**:

.. code-block:: text

   <type>: <description>

   [optional body]

   [optional footer]

**Types:**

* ``feat:`` - Neue Funktionalität → **Minor** Version Bump (0.X.0)
* ``fix:`` - Bugfix → **Patch** Version Bump (0.0.X)
* ``BREAKING CHANGE:`` - Breaking Change → **Major** Version Bump (X.0.0)
* ``docs:`` - Dokumentation (keine Version Bump)
* ``chore:`` - Wartung (keine Version Bump)

**Beispiele:**

.. code-block:: bash

   # Patch (0.0.1 → 0.0.2)
   git commit -m "fix: correct button event value for long press"

   # Minor (0.0.1 → 0.1.0)
   git commit -m "feat: add PM2.5 sensor support"

   # Major (0.1.0 → 1.0.0)
   git commit -m "feat: new API structure

   BREAKING CHANGE: renamed addTemperature to setTemperature"

Automatischer Release-Prozess
------------------------------

Der Release-Prozess ist vollständig automatisiert über GitHub Actions.

Workflow-Ablauf
~~~~~~~~~~~~~~~

1. **Push to main** (mit Änderungen in relevanten Pfaden)

   .. code-block:: bash

      git add src/BThomeV2.cpp
      git commit -m "feat: add new sensor type"
      git push origin main

2. **Version Calculation** - GitHub Actions analysiert Commits:

   * Liest bisherige Versionen (Git Tags)
   * Identifiziert Commit-Types seit letztem Release
   * Berechnet neue Version (z.B. 0.1.0 → 0.2.0)

3. **GitHub Release** - Erstellt Release:

   * Tag: ``v0.2.0``
   * Release Notes aus Commits
   * Source Code Archives

4. **PyPI Publishing** - Veröffentlicht bthome-logger:

   * Baut Python Package mit Version 0.2.0
   * Veröffentlicht auf PyPI
   * Verwendet Token-Authentifizierung

5. **PlatformIO Publishing** - Veröffentlicht Library:

   * Generiert ``library.json`` und ``library.properties`` mit Version 0.2.0
   * Veröffentlicht auf PlatformIO Registry
   * Nutzt Git Tag für Registry-Indexierung

Workflow-Dateien
~~~~~~~~~~~~~~~~

**release.yml** - Hauptorchestrator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   jobs:
     version:
       # Berechnet semantische Version
     create-release:
       # Erstellt GitHub Release
     publish-pypi:
       # Ruft pypi-publish.yml auf
     publish-platformio:
       # Ruft pio-publish.yml auf
     summary:
       # Erzeugt Zusammenfassung

**pypi-publish.yml** - PyPI Publishing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   jobs:
     build:
       # Baut Python Package
     publish-to-pypi:
       # Veröffentlicht auf PyPI mit Token

**pio-publish.yml** - PlatformIO Publishing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   jobs:
     publish-to-platformio:
       # Generiert Library-Manifeste aus Templates
       # Veröffentlicht auf PlatformIO Registry

Template-System
---------------

Library-Manifeste (``library.json`` und ``library.properties``) werden aus
Jinja2-Templates generiert:

**library.json.j2:**

.. code-block:: json

   {
     "name": "BThomeV2",
     "version": "{{ version }}",
     ...
   }

**library.properties.j2:**

.. code-block:: ini

   name=BThomeV2
   version={{ version }}
   ...

**Repository-Versionen:**

Im Repository liegen generierte Dateien mit Version ``0.0.0-dev``:

.. code-block:: bash

   # Generierung für Repository
   python3 << EOF
   import jinja2
   template = jinja2.Template(open('library.json.j2').read())
   open('library.json', 'w').write(template.render(version='0.0.0-dev'))
   EOF

**Workflow-Versionen:**

Im Workflow werden diese temporär mit der echten Version überschrieben:

.. code-block:: bash

   # Im GitHub Actions Workflow
   python3 << EOF
   import jinja2
   template = jinja2.Template(open('library.json.j2').read())
   open('library.json', 'w').write(template.render(version='${{ inputs.version }}'))
   EOF

Die generierten Dateien werden **nicht** committed, sondern nur für Publishing verwendet.

Branch-Strategie
----------------

Main Branch
~~~~~~~~~~~

* **main** - Stabiler Branch
* Alle Merges nach ``main`` triggern Release-Prozess
* Direktes Pushen nach ``main`` sollte vermieden werden

Feature Branches
~~~~~~~~~~~~~~~~

Für neue Features oder Bugfixes:

.. code-block:: bash

   # Feature Branch erstellen
   git checkout -b feature/new-sensor-support

   # Entwickeln und committen
   git add src/BThomeV2.cpp
   git commit -m "feat: add new sensor type"

   # Push und Pull Request erstellen
   git push origin feature/new-sensor-support

Nach Review und Approval wird der PR nach ``main`` gemergt.

GitHub Secrets
--------------

Folgende Secrets müssen im Repository konfiguriert sein:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Secret Name
     - Beschreibung
   * - ``PYPI_API_TOKEN``
     - PyPI API Token für Veröffentlichung
   * - ``PLATFORMIO_AUTH_TOKEN``
     - PlatformIO Registry Auth Token
   * - ``TEST_PYPI_API_TOKEN``
     - (Optional) TestPyPI Token für Testing

GitHub Environments
-------------------

Folgende Environments sollten konfiguriert sein:

* **pypi** - Für PyPI Deployments
* **platformio** - Für PlatformIO Registry Deployments
* **testpypi** - (Optional) Für TestPyPI Deployments

Diese Environments ermöglichen Deployment-Tracking in der GitHub UI.

Lokales Testing
---------------

Vor dem Push solltest du lokal testen:

Library
~~~~~~~

.. code-block:: bash

   # Kompilieren für ESP32
   cd examples/ESP32_Basic
   pio run

   # Auf Hardware testen
   pio run --target upload
   pio device monitor

Tool
~~~~

.. code-block:: bash

   # Tool im Dev-Modus installieren
   cd tools
   uv tool install --editable .

   # Testen
   bthome-logger

Dokumentation
~~~~~~~~~~~~~

.. code-block:: bash

   # Sphinx-Dokumentation bauen
   cd docs
   pip install -r requirements.txt
   make html

   # Im Browser öffnen
   firefox _build/html/index.html

Manuelles Release (Notfall)
----------------------------

Falls der automatische Workflow fehlschlägt:

PyPI (manuell)
~~~~~~~~~~~~~~

.. code-block:: bash

   cd tools
   export SETUPTOOLS_SCM_PRETEND_VERSION="0.2.0"
   python -m build
   twine upload dist/*

PlatformIO (manuell)
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Templates rendern
   python3 << EOF
   import jinja2
   version = "0.2.0"
   for tmpl in ['library.json.j2', 'library.properties.j2']:
       template = jinja2.Template(open(tmpl).read())
       out = tmpl.replace('.j2', '')
       open(out, 'w').write(template.render(version=version))
   EOF

   # Publishen
   pio pkg publish --owner the78mole --non-interactive

Best Practices
--------------

Code-Qualität
~~~~~~~~~~~~~

* ✅ Teste auf echter Hardware vor dem Push
* ✅ Verwende aussagekräftige Commit-Messages
* ✅ Halte Changes klein und fokussiert
* ✅ Dokumentiere neue Features in den Docs

Testing
~~~~~~~

* ✅ Teste mit bthome-logger
* ✅ Prüfe Serial Monitor Ausgaben
* ✅ Teste auf ESP32 (nRF52 ist derzeit broken)
* ✅ Prüfe RSSI-Werte für BLE-Reichweite

Dokumentation
~~~~~~~~~~~~~

* ✅ Update README.md bei API-Änderungen
* ✅ Update Sphinx-Docs bei neuen Features
* ✅ Füge Beispiele hinzu für neue Funktionalität
* ✅ Update CHANGELOG.md

Siehe auch
----------

* :doc:`contributing` - Contributing Guidelines
* :doc:`release-process` - Detaillierter Release-Prozess
* :doc:`../library/api` - Library API-Referenz
