v0.4.0
======

This release includes new features and modernization updates.

Breaking Changes
----------------
This release is not believed to introduce any backwards-incompatible changes.

New Features
------------

**Pandas DataFrame Support**
  Otter now supports rendering pandas DataFrames directly in reports, making it easier to include tabular data from pandas workflows.

**Package Modernization**
  The package has been modernized with migration to pyproject.toml, comprehensive unit tests, sphinx-multiversion documentation support, and CI/CD improvements.

Changes
-------

**Build System Migration**
  Migrated from setup.py to pyproject.toml for modern Python packaging standards, with setuptools-scm for version management.

**Testing Infrastructure**
  Added comprehensive unit tests for core functionality to improve code reliability and maintainability.

**Documentation Improvements**
  Added sphinx-multiversion support for documentation versioning, allowing users to browse docs for different versions.

**Python Version Support**
  Removed support for Python 3.7 and 3.8, now requiring Python 3.9 or higher.

GitHub Pull Requests
--------------------

+ `github#22 <https://github.com/transientlunatic/otter/pull/22>`_: Modernize package: migrate to pyproject.toml, add tests, sphinx-multiversion, and CI/CD
+ `github#20 <https://github.com/transientlunatic/otter/pull/20>`_: Replace deprecated pkg_resources with importlib.resources

0.3.3
=====

This is a bug-fix and security update release focused on dependency updates and package modernization.

Breaking Changes
----------------

This release is not believed to introduce any backwards-incompatible changes.

Changes
-------

**Security Updates**
  Multiple dependency updates to address security vulnerabilities, including:

  + Cryptography updated from 3.3.2 to 42.0.4
  + PyYAML updated from 3.11 to 5.4
  + Wheel updated from 0.23.0 to 0.38.1

**Module Import Improvements**
  Replaced deprecated pkg_resources with importlib.resources to address deprecation warnings and improve compatibility with modern Python.

**Build Infrastructure**
  Updated GitHub workflow and documentation building process.

GitHub Pull Requests
--------------------

+ `github#17 <https://github.com/transientlunatic/otter/pull/17>`_: Snyk security fixes
+ `github#14 <https://github.com/transientlunatic/otter/pull/14>`_: Security vulnerability fixes
+ `github#13 <https://github.com/transientlunatic/otter/pull/13>`_: Bump cryptography from 3.3.2 to 42.0.4
+ `github#12 <https://github.com/transientlunatic/otter/pull/12>`_: Security vulnerability fixes
+ `github#11 <https://github.com/transientlunatic/otter/pull/11>`_: Security vulnerability fixes
+ `github#10 <https://github.com/transientlunatic/otter/pull/10>`_: Security vulnerability fixes
+ `github#9 <https://github.com/transientlunatic/otter/pull/9>`_: Security vulnerability fixes
+ `github#8 <https://github.com/transientlunatic/otter/pull/8>`_: Security vulnerability fixes
+ `github#7 <https://github.com/transientlunatic/otter/pull/7>`_: Security vulnerability fixes
+ `github#6 <https://github.com/transientlunatic/otter/pull/6>`_: Bump wheel from 0.23.0 to 0.38.1
+ `github#5 <https://github.com/transientlunatic/otter/pull/5>`_: Bump pyyaml from 5.1 to 5.4

0.3.2
=====

This release includes Python 3.9 support and theme customization improvements.

Breaking Changes
----------------

This release is not believed to introduce any backwards-incompatible changes.

New Features
------------

**Theme Directory Specification**
  Users can now specify custom theme directories, allowing greater flexibility in report styling and branding.

**Python 3.9 Support**
  Full support for Python 3.9 has been added.

Changes
-------

**Security Updates**

  + Cryptography updated from 1.0.1 to 3.2

GitHub Pull Requests
--------------------

+ `github#4 <https://github.com/transientlunatic/otter/pull/4>`_: Bump cryptography from 3.2 to 3.3.2
+ `github#3 <https://github.com/transientlunatic/otter/pull/3>`_: Bump cryptography from 1.0.1 to 3.2

0.3.1
=====

This is a minor feature release introducing Bootstrap 4 support.

Breaking Changes
----------------

This release is not believed to introduce any backwards-incompatible changes.

Changes
-------

**Bootstrap 4 Migration**
  Updated to use Bootstrap 4 framework and added new UI elements for modern, responsive report layouts.

0.3.0
=====

"Beinn an Dothaidh"

This is a major release focusing on Python 3 support and removing legacy Python 2 compatibility.

Breaking Changes
----------------

**Python 2 Support Removed**
  Python 2 is no longer supported. Users must upgrade to Python 3 to use this version.

Changes
-------

**Improved Python 3 Support**
  Enhanced Python 3 compatibility and removed all Python 2 legacy code.

0.2.0
=====

"Beinn Dorain"

This is a major feature release introducing a new API and improved functionality.

New Features
------------

**New API for Adding Material**
  Introduced a cleaner, more Pythonic API using context managers for adding content to reports.

**Full Matplotlib Support**
  Added comprehensive support for matplotlib plots, allowing easy integration of visualizations.

**Multiple Data Type Support**
  Reports can now handle multiple data types including dictionaries, matplotlib figures, and formatted text.

**Bootstrap Components**
  Added support for various Bootstrap UI components including rows, panels, labels, and alerts.

0.0.1
=====

First release on PyPI.

Initial implementation of the Otter HTML report generator with basic functionality for creating HTML reports from Python jobs.
