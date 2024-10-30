.. image:: https://img.shields.io/pypi/v/pytest-flake8.svg?label=pytest-flake8
   :target: https://pypi.org/project/pytest-flake8
   :alt: Package


.. image:: https://readthedocs.org/projects/pytest-flake8/badge
   :target: https://pytest-flake8.readthedocs.io/en/latest
   :alt: Documentation


.. image:: https://github.com/coherent-oss/pytest-flake8/actions/workflows/main.yml/badge.svg?label=test
   :target: https://github.com/PyCQA/flake8/actions?query=workflow=main
   :alt: Tests


.. image:: https://img.shields.io/pypi/v/flake8.svg?label=flake8
    :target: https://github.com/PyCQA/flake8
    :alt: Flake8


.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff


.. image:: https://img.shields.io/badge/skeleton-2024-informational
   :target: https://blog.jaraco.com/skeleton
   :alt: skeleton


pytest plugin for efficiently checking PEP8 compliance 
======================================================

Usage
-----

Install it into a test environment, then run tests with the option.

.. code-block:: bash

    pytest --flake8

Every file ending in ``.py`` will be discovered and checked with
flake8.

.. note::

    If optional flake8 plugins are installed, those will
    be used automatically. No provisions have been made for
    configuring these via `pytest`_.

.. warning::

    Running flake8 tests on your project is likely to cause a number 
    of issues. The plugin allows one to configure on a per-project and
    per-file basis which errors or warnings to ignore, see
    flake8-ignore_.

.. _flake8-ignore:

Configuring Flake8
------------------

See the Flake8
`docs on configuring <https://flake8.pycqa.org/en/latest/user/configuration.html>`_.

FAQs
-----

All the Flake8 tests are skipping!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By design, results are cached and only changed files are checked.

To bypass this caching mechanism, run the following command:

.. code-block:: bash

    pytest --cache-clear --flake8

Run tests with [tox](https://tox.wiki) (e.g. `pipx run tox`).

For more information, take a look at the `skeleton <https://blog.jaraco.com/skeleton/>`_.


Notes
-----

For more info on `pytest`_ see http://pytest.org

The code is partially based on Ronny Pfannschmidt's `pytest-codecheckers`_ plugin.

.. _`pytest`: http://pytest.org
.. _`flake8`: https://pypi.python.org/pypi/flake8
.. _`pycodestyle`: https://pypi.python.org/pypi/pycodestyle
.. _`pytest-codecheckers`: https://pypi.python.org/pypi/pytest-codecheckers
