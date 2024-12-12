=====
Setup
=====

In order that mochada_kit can use plantuml, we need to provide the path to ``plantuml.jar`` to the Python functions. 
You can do this each time simply by passing in the path, or you can generate a configuration file which will save 
this information in your home folder, so that you don't have to enter it in the Python functions every time. 
To set up the configuration, run:

.. code-block::

   mochada_kit config -p path/to/my/plantuml.jar

and this will write ``.mochada_kit/config.json`` to the current user's home folder. You can now use the Python functions 
in mochada_kit and the program will already know where ``plantuml.jar`` is located and will be able to run it.