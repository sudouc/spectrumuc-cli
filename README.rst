SpectrumUC CLI
==============

Command line application for managing nodes and projects in SpectrumUC

Help
----

For help on commands and subcommands:

    $ ./spectrumuc-runner.py  -h

Flexible invocation
*******************

The application can be run right from the source directory, in two different
ways:

1) Treating the spectrumuc directory as a package *and* as the main script:

     $ python -m spectrumuc arg1 arg2

2) Using the spectrumuc-runner.py wrapper:

     $ ./spectrumuc-runner.py arg1 arg2


Installation sets up 'suc' command
**************************************

Situation before installation::

    $ spectrumuc
    bash: spectrumuc: command not found

Installation right from the source tree (or via pip from PyPI)::

    $ python setup.py install

Now, the ``spectrumuc`` command is available::

    $ spectrumuc arg1 arg2


On Unix-like systems, the installation places a ``spectrumuc`` script into a
centralized ``bin`` directory, which should be in your ``PATH``. On Windows,
``spectrumuc.exe`` is placed into a centralized ``Scripts`` directory which
should also be in your ``PATH``.
