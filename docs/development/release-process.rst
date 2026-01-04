Release-Prozess
===============

Detaillierte Beschreibung des automatisierten Release-Prozesses.

Siehe :doc:`workflow` für die vollständige Beschreibung des Release-Workflows.

Übersicht
---------

1. Code-Änderungen pushen nach ``main``
2. GitHub Actions berechnet neue Version
3. Release wird erstellt
4. PyPI und PlatformIO werden aktualisiert
5. Beide haben identische Version

Semantic Versioning
-------------------

* ``feat:`` → Minor Bump (0.X.0)
* ``fix:`` → Patch Bump (0.0.X)
* ``BREAKING CHANGE:`` → Major Bump (X.0.0)

Siehe auch
----------

* :doc:`workflow` - Entwicklungs-Workflow
