Release Process
===============

Detailed description of the automated release process.

See :doc:`workflow` for the complete description of the release workflow.

Overview
--------

1. Push code changes to ``main``
2. GitHub Actions calculates new version
3. Release is created
4. PyPI and PlatformIO are updated
5. Both have identical version

Semantic Versioning
-------------------

* ``feat:`` → Minor Bump (0.X.0)
* ``fix:`` → Patch Bump (0.0.X)
* ``BREAKING CHANGE:`` → Major Bump (X.0.0)

See Also
--------

* :doc:`workflow` - Development workflow
