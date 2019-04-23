"""
This module is called when the package is executed as a module.
"""

import sys


if __name__ == "__main__":
    from spotifinder_backend.main import main

    sys.exit(main())
