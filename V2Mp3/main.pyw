#!/usr/bin/env python3

import sys
from os import chdir
from os.path import dirname

sys.path.insert(0, dirname(
    dirname(__file__)))  # Ensure main module can be found by Python.

chdir(dirname(
    __file__))  # Set current working directory to the directory of the module.

from V2Mp3.appEvents.events import GUILoop

#&============================================================================#


def main() -> None:
    """Program entry point.

    - Responsible for processing GUI events and responses.

    ---

    :returns: start program
    :rtype: None
    """

    return GUILoop()


if __name__ == '__main__':
    main()
