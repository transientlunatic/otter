Sphinx Multiversion Documentation
==================================

This documentation uses sphinx-multiversion to provide versioned documentation.

Building Documentation
----------------------

To build the documentation for a single version (development):

.. code-block:: bash

   cd docs
   make html

To build documentation for all versions using sphinx-multiversion:

.. code-block:: bash

   cd docs
   sphinx-multiversion . _build/html

This will generate documentation for all tagged versions and branches that match
the patterns defined in conf.py.

Configuration
-------------

The multiversion settings in conf.py control which versions are built:

- ``smv_tag_whitelist``: Pattern for tags (e.g., v1.0.0, v2.0.0)
- ``smv_branch_whitelist``: Pattern for branches (main/master)
- ``smv_remote_whitelist``: Pattern for remotes (origin)

The version selector will appear in the sidebar of all documentation pages.
