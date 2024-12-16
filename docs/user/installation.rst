============
Installation
============

mochada_kit is designed to be platform-indepenent. Python >= 3.6 is required. 

mochada_kit
-----------

Please clone the `repository <https://github.com/MaMMoS-project/mochada_kit>`_ and install it as an editable package using ``pip`` (that way you can easily pull updates from the repo and they will be active without needing to reinstall anything):

.. code-block::

   git clone https://github.com/MaMMoS-project/mochada_kit.git
   cd mochada_kit
   pip install -e .


Dependencies
------------

``h5py``: if you do not already have it, `h5py <https://docs.h5py.org/en/stable/index.html>`_ will be installed by pip during installation of mochada_kit.

``pyyaml``: if you do not already have it, `pyyaml <https://pyyaml.org/>`_ will be installed by pip during installation of mochada_kit.

plantuml
++++++++

To generate the diagrams, you need to have ``plantuml.jar`` saved on your system. Please see `the plantuml download site <https://plantuml.com/download>`_ for download and licensing options.

java
++++

In order to run `plantuml <https://plantuml.com/>`_, you also need `java <https://www.java.com/en/download/help/index_installing.html>`_. To check if you already have java installed, you can type this command at the terminal:

.. code-block::

   java -version


To uninstall mochada_kit:
-------------------------

.. code-block::

   pip uninstall mochada_kit
