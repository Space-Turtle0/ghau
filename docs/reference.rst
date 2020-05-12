Reference
=========

Main Class
----------
Most interactions with ghau will be done through the main Update class. Details regarding it can
be found below:

.. autoclass:: ghau.Update
   :members:

Reboot Functions
----------------
There are also a few added functions to make rebooting easier.

These functions build the reboot command for you to place in the reboot parameter
of :class:`ghau.Update`. They also provide ghau the ability to stop :ref:`Update Loops`.

Because of this, it is highly recommended you utilize these functions if you are rebooting.

.. automodule:: ghau
   :members: python, exe, cmd