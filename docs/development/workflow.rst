Development Workflow
====================

This document describes the complete development workflow for the BThomeV2 project, including repository structure, testing, versioning, and automated releases.

Repository Structure
--------------------

The project is organized as a monorepo containing both the C++ library and Python testing tool:

.. code-block:: text

   bthomev2/
   ├── src/                          # C++ Library source
   │   ├── BThomeV2.cpp             # Core implementation
   │   ├── BThomeV2.h               # Public API
   │   ├── BThomeV2_ESP32.cpp       # ESP32 platform
   │   └── BThomeV2_nRF52.cpp       # nRF52 platform (broken)
   ├── examples/                     # Example projects
   │   ├── ESP32_Basic/
   │   ├── ESP32_Button/
   │   ├── ESP32_MultipleSensors/
   │   └── nRF52_Basic/
   ├── tools/                        # Python tool
   │   ├── bthome_logger.py         # Main tool
   │   ├── pyproject.toml           # Python package config
   │   └── README.md
   ├── docs/                         # Sphinx documentation
   │   ├── conf.py
   │   ├── index.rst
   │   └── ...
   ├── .github/workflows/            # CI/CD
   │   ├── release.yml              # Main release workflow
   │   ├── pypi-publish.yml         # PyPI publishing
   │   └── pio-publish.yml          # PlatformIO publishing
   ├── library.json.template         # PlatformIO template
   ├── library.properties.template   # Arduino IDE template
   ├── platformio.ini.example        # PIO example config
   ├── CHANGELOG.md                  # Version history
   ├── CONTRIBUTING.md               # Contribution guide
   └── README.md                     # Project overview

Development Setup
-----------------

Prerequisites
~~~~~~~~~~~~~

* **For C++ Library:**

  * PlatformIO Core
  * ESP32 board (for testing)
  * Serial monitor tool

* **For Python Tool:**

  * Python 3.8+
  * uv or pip
  * Bluetooth LE adapter

* **For Documentation:**

  * Python 3.8+
  * Sphinx and dependencies

Clone and Install
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone repository
   git clone https://github.com/the78mole/bthomev2.git
   cd bthomev2

   # Install Python tool for development
   cd tools
   uv venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   uv pip install -e .

   # Build documentation
   cd ../docs
   pip install -r requirements.txt
   make html

Testing Workflow
----------------

The project uses a unique testing approach where the C++ library and Python tool work together.

Local Testing Process
~~~~~~~~~~~~~~~~~~~~~~

1. **Develop C++ code:**

   .. code-block:: bash

      cd examples/ESP32_Basic
      vim src/main.cpp

2. **Compile and upload:**

   .. code-block:: bash

      pio run --target upload

3. **Monitor serial output:**

   .. code-block:: bash

      pio device monitor

4. **Test with Python tool:**

   .. code-block:: bash

      # In another terminal
      cd tools
      uv run bthome_logger.py -f "ESP32-Basic"

5. **Verify functionality:**

   * Check sensor values appear correctly
   * Verify RSSI signal strength
   * Confirm update intervals work

Example Test Session
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Terminal 1: Build and monitor
   cd examples/ESP32_Button
   pio run --target upload && pio device monitor

   # Terminal 2: Watch BLE advertisements
   cd tools
   uv run bthome_logger.py -f "ESP32-Button"

   # Terminal 3: Make code changes
   vim src/main.cpp
   # Save and go back to Terminal 1 to rebuild

Semantic Versioning
-------------------

The project uses **Semantic Versioning** (SemVer) with **Conventional Commits**.

Version Format
~~~~~~~~~~~~~~

``MAJOR.MINOR.PATCH``

* **MAJOR:** Breaking changes (e.g., API changes)
* **MINOR:** New features (backward compatible)
* **PATCH:** Bug fixes (backward compatible)

Commit Message Format
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   <type>: <description>

   [optional body]

   [optional footer]

**Types:**

* ``feat:`` - New feature → **MINOR version bump**
* ``fix:`` - Bug fix → **PATCH version bump**
* ``feat!:`` or ``fix!:`` - Breaking change → **MAJOR version bump**
* ``docs:`` - Documentation only → **No version bump**
* ``chore:`` - Maintenance → **No version bump**
* ``refactor:`` - Code restructuring → **No version bump**
* ``test:`` - Tests → **No version bump**

Examples
~~~~~~~~

**New feature (minor):**

.. code-block:: text

   feat: add voltage sensor support

   Implements addVoltage() method for battery voltage measurements.
   Includes example and documentation.

**Bug fix (patch):**

.. code-block:: text

   fix: correct CO2 value encoding

   CO2 values were encoded as signed instead of unsigned.
   Fixes issue #123.

**Breaking change (major):**

.. code-block:: text

   feat!: change API to use SI units

   BREAKING CHANGE: Temperature now uses Kelvin instead of Celsius.
   Migration: Add 273.15 to all temperature values.

Automated Release Process
--------------------------

The project uses GitHub Actions for automated releases.

Workflow Overview
~~~~~~~~~~~~~~~~~

.. code-block:: text

   Push to main
        ↓
   ┌────────────────────┐
   │ 1. Calculate       │ → Semantic version from commits
   │    Version         │   (e.g., 0.2.3)
   └─────────┬──────────┘
             ↓
   ┌────────────────────┐
   │ 2. Create          │ → GitHub Release with tag
   │    Release         │   (e.g., v0.2.3)
   └─────────┬──────────┘
             ↓
   ┌────────────────────┐
   │ 3. Update          │ → library.json from template
   │    Library Files   │   library.properties from template
   └─────────┬──────────┘
             ↓
   ┌────────────────────┐
   │ 4. Publish         │ → PlatformIO Registry
   │    PlatformIO      │   (the78mole/BThomeV2)
   └─────────┬──────────┘
             ↓
   ┌────────────────────┐
   │ 5. Publish         │ → Test PyPI (optional)
   │    Python Tool     │   PyPI (bthome-logger)
   └────────────────────┘

Workflow Files
~~~~~~~~~~~~~~

1. **release.yml** - Main orchestration

   * Calculates semantic version
   * Creates GitHub release
   * Updates library files
   * Triggers publishing workflows

2. **pio-publish.yml** - PlatformIO publishing

   * Publishes to PlatformIO Registry
   * Uses ``PLATFORMIO_AUTH_TOKEN`` secret
   * Tracks deployment in ``platformio`` environment

3. **pypi-publish.yml** - Python package publishing

   * Publishes to Test PyPI (optional)
   * Publishes to PyPI
   * Uses ``PYPI_API_TOKEN`` secret
   * Tracks deployment in ``pypi`` environment

Version Template System
-----------------------

Library files use templates to automatically update versions.

Templates
~~~~~~~~~

**library.json.template:**

.. code-block:: json

   {
     "name": "BThomeV2",
     "version": "%%VERSION%%",
     "description": "BThome V2 library",
     "keywords": ["ble", "bthome", "sensor"],
     "repository": {
       "type": "git",
       "url": "https://github.com/the78mole/bthomev2.git"
     },
     "authors": [
       {
         "name": "the78mole",
         "email": "daniel@make-it.software"
       }
     ],
     "license": "MIT",
     "frameworks": ["arduino"],
     "platforms": ["espressif32", "nordicnrf52"]
   }

**library.properties.template:**

.. code-block:: text

   name=BThomeV2
   version=%%VERSION%%
   author=the78mole
   maintainer=the78mole <daniel@make-it.software>
   sentence=BThome V2 BLE sensor library
   paragraph=Implements BThome V2 protocol for ESP32 and nRF52
   category=Communication
   url=https://github.com/the78mole/bthomev2
   architectures=esp32,nrf52
   includes=BThomeV2.h

Update Process
~~~~~~~~~~~~~~

During release, the workflow:

1. Reads template files
2. Replaces ``%%VERSION%%`` with calculated version
3. Creates ``library.json`` and ``library.properties``
4. Commits these files
5. Creates release with updated files

Branch Strategy
---------------

The project uses a simple branching model:

Main Branch
~~~~~~~~~~~

* **Branch:** ``main``
* **Purpose:** Stable, released code
* **Protection:**

  * Requires pull request reviews
  * CI checks must pass
  * No force pushes

* **Auto-releases:** Every push to ``main`` triggers release workflow

Feature Branches
~~~~~~~~~~~~~~~~

* **Naming:** ``feature/<description>`` or ``fix/<description>``
* **Purpose:** Development of new features or fixes
* **Merge:** Via pull request to ``main``

Development Branches
~~~~~~~~~~~~~~~~~~~~

* **Naming:** ``dev/<description>``
* **Purpose:** Experimental features, major refactorings
* **Merge:** Via pull request after thorough testing

Making Changes
--------------

Step-by-Step Guide
~~~~~~~~~~~~~~~~~~

1. **Create feature branch:**

   .. code-block:: bash

      git checkout -b feature/add-tvoc-sensor

2. **Make changes:**

   .. code-block:: bash

      # Edit files
      vim src/BThomeV2.cpp src/BThomeV2.h

      # Test locally
      cd examples/ESP32_Basic
      pio run --target upload
      pio device monitor

      # Test with logger
      cd ../../tools
      uv run bthome_logger.py

3. **Commit with conventional commit:**

   .. code-block:: bash

      git add src/
      git commit -m "feat: add TVOC sensor support

      Implements addTVOC() method for volatile organic compounds
      measurement. Includes updated examples and documentation."

4. **Push and create PR:**

   .. code-block:: bash

      git push origin feature/add-tvoc-sensor
      # Create pull request on GitHub

5. **Merge to main:**

   After review and CI passes, merge PR. This automatically:

   * Calculates new version (e.g., 0.2.0 → 0.3.0)
   * Creates release
   * Publishes to PlatformIO and PyPI

GitHub Secrets
--------------

The workflows require these secrets:

Required Secrets
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Secret Name
     - Purpose
   * - ``PLATFORMIO_AUTH_TOKEN``
     - PlatformIO Registry authentication
   * - ``PYPI_API_TOKEN``
     - PyPI publishing (production)
   * - ``TEST_PYPI_API_TOKEN``
     - Test PyPI publishing (optional)

Setup Instructions
~~~~~~~~~~~~~~~~~~

**PlatformIO Token:**

.. code-block:: bash

   # Generate token
   pio account token

   # Add to GitHub:
   # Settings → Secrets → Actions → New repository secret
   # Name: PLATFORMIO_AUTH_TOKEN
   # Value: <token>

**PyPI Token:**

1. Go to https://pypi.org/manage/account/token/
2. Create token with scope: "Entire account"
3. Copy token (starts with ``pypi-``)
4. Add to GitHub secrets as ``PYPI_API_TOKEN``

GitHub Environments
~~~~~~~~~~~~~~~~~~~

Deployment tracking uses environments:

* ``pypi`` - Tracks PyPI deployments
* ``testpypi`` - Tracks Test PyPI deployments
* ``platformio`` - Tracks PlatformIO deployments

These show up in the GitHub Actions UI with deployment history.

Local Testing Before Release
-----------------------------

Test Library Locally
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Test each example
   cd examples/ESP32_Basic && pio run --target upload
   cd examples/ESP32_Button && pio run --target upload
   cd examples/ESP32_MultipleSensors && pio run --target upload

   # Verify with logger
   cd tools
   uv run bthome_logger.py -v

Test Python Tool Locally
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd tools

   # Install in development mode
   uv pip install -e .

   # Test as installed command
   bthome-logger --version
   bthome-logger -f "Test"

   # Run tests (if available)
   pytest

Test Documentation Build
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd docs

   # Install dependencies
   pip install -r requirements.txt

   # Build HTML
   make html

   # Build for other formats
   make latexpdf  # PDF output
   make epub      # ePub output

   # View result
   firefox _build/html/index.html

Troubleshooting
---------------

Release Workflow Fails
~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Workflow fails at version calculation

**Solution:**

* Check commit messages follow conventional commit format
* Ensure ``paulhatch/semantic-version`` action is up to date
* Check workflow logs for specific errors

**Problem:** PlatformIO publish fails

**Solution:**

* Verify ``PLATFORMIO_AUTH_TOKEN`` secret is set correctly
* Check token hasn't expired: ``pio account token --list``
* Verify ``library.json`` is valid JSON

**Problem:** PyPI publish fails

**Solution:**

* Check ``PYPI_API_TOKEN`` is valid
* Verify package name ``bthome-logger`` is available
* Check ``pyproject.toml`` version matches

Version Not Bumping
~~~~~~~~~~~~~~~~~~~

**Problem:** Push to main doesn't create new version

**Solution:**

* Verify commits use conventional commit format
* Check commits actually change relevant files (listed in ``paths:`` in workflow)
* Use ``feat:`` or ``fix:`` prefixes
* Check workflow run logs for version calculation step

Local Testing Doesn't Match CI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Works locally but fails in CI

**Solution:**

* Ensure PlatformIO dependencies are defined in ``platformio.ini``
* Check Python dependencies are in ``pyproject.toml``
* Verify Arduino/PlatformIO versions match CI

Best Practices
--------------

Commit Messages
~~~~~~~~~~~~~~~

* ✅ Use conventional commit format
* ✅ Write descriptive commit bodies
* ✅ Reference issues when fixing bugs
* ❌ Don't use vague messages like "fix stuff"
* ❌ Don't mix unrelated changes in one commit

Code Changes
~~~~~~~~~~~~

* ✅ Test on real hardware before committing
* ✅ Update examples if API changes
* ✅ Update documentation with new features
* ✅ Keep commits atomic and focused
* ❌ Don't commit broken code to main
* ❌ Don't skip testing steps

Documentation
~~~~~~~~~~~~~

* ✅ Update docs/ when adding features
* ✅ Include code examples in docs
* ✅ Keep README.md synchronized
* ✅ Test documentation builds locally
* ❌ Don't document features that don't exist yet

Versioning
~~~~~~~~~~

* ✅ Use semantic versioning principles
* ✅ Mark breaking changes clearly
* ✅ Keep CHANGELOG.md updated
* ❌ Don't manually edit version numbers
* ❌ Don't skip version bumps

Resources
---------

* `Conventional Commits <https://www.conventionalcommits.org/>`_
* `Semantic Versioning <https://semver.org/>`_
* `PlatformIO Registry <https://registry.platformio.org/>`_
* `GitHub Actions Documentation <https://docs.github.com/actions>`_
* `Sphinx Documentation <https://www.sphinx-doc.org/>`_

See Also
--------

* :doc:`contributing` - Contribution guidelines
* :doc:`release-process` - Detailed release process
* :doc:`../library/api` - Library API reference
* :doc:`../tools/bthome-logger` - Python tool documentation
