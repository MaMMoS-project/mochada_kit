.. _installing-a-development-environment:

====================================
Installing a Development Environment
====================================

To contribute to mochada_kit, please `fork <https://docs.github.com/en/get-started/quickstart/contributing-to-projects#about-forking>`_ the `repository <https://github.com/MaMMoS-project/mochada_kit>`_.


Set up a virtual environment, called *e.g.* "dev_mochada_kit" using ``venv`` in Python [#f1]_::

   python -m venv dev_mochada_kit
   
Change directories into your virtual environment and clone *your forked repository* into it (replacing "your-username" in the code below)::
   
   cd dev_mochada_kit
   git clone https://github.com/your-username/mochada_kit.git
   
Activate the virtual environment:

.. tab-set::

    .. tab-item:: Windows

        .. code-block:: powershell

            .\Scripts\Activate.ps1

    .. tab-item:: macOS

        .. code-block:: bash

            source bin/activate
			
    .. tab-item:: Linux

        .. code-block:: bash

            source bin/activate



Set the ``upstream`` remote to the main mochada_kit repository::
    
   cd mochada_kit
   git remote add upstream https://github.com/MaMMoS-project/mochada_kit.git

Install mochada_kit in editable mode with the optional dependencies for development::

   pip install -e .[dev]

.. rubric:: Footnotes

.. [#f1] You could also use a different tool of your choice for making virtual environments.