"""
This module provides the version information for the pydantic-shapely package.

It imports the necessary modules based on the Python version and retrieves the
version of the package based on the version as registered in Python.

Attributes:
    DIST_NAME (str): The name of the package. should be changed in case the package
    is renamed.
    __version__ (str): The version of the package.

"""

import sys

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    DIST_NAME = "pydantic-shapely"
    __version__ = version(DIST_NAME)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
