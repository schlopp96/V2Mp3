#!/usr/bin/env python3

import sys
from os import chdir
from os.path import dirname

sys.path.insert(0, dirname(
    dirname(__file__)))  # Ensure main module can be found by Python.

chdir(dirname(
    __file__))  # Set current working directory to the directory of this file.

from V2Mp3.appEvents.events import _event_loop

#&============================================================================#


def main() -> None:
    """Program entry point.

    - Responsible for processing GUI events and responses.

    ---

    :returns: Program window.
    :rtype: None
    """

    return _event_loop()


if __name__ == '__main__':
    main()
