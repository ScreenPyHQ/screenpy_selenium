"""
 ░█▀▀▀█ █▀▀ █▀▀█ █▀▀ █▀▀ █▀▀▄ ░█▀▀█ █  █   ░█▀▀▀█ █▀▀ █   █▀▀ █▀▀▄  ▀  █  █ █▀▄▀█
  ▀▀▀▄▄ █   █▄▄▀ █▀▀ █▀▀ █  █ ░█▄▄█ █▄▄█    ▀▀▀▄▄ █▀▀ █   █▀▀ █  █ ▀█▀ █  █ █ ▀ █
 ░█▄▄▄█ ▀▀▀ ▀ ▀▀ ▀▀▀ ▀▀▀ ▀  ▀ ░█    ▄▄▄█   ░█▄▄▄█ ▀▀▀ ▀▀▀ ▀▀▀ ▀  ▀ ▀▀▀  ▀▀▀ ▀   ▀
"""
try:
    # importlib.metadata is present in Python 3.8 and later
    import importlib.metadata as importlib_metadata  # type: ignore
except ImportError:
    # use the shim package importlib-metadata pre-3.8
    import importlib_metadata  # type: ignore

metadata = importlib_metadata.metadata("screenpy_selenium")

__title__ = metadata["Name"]
__description__ = metadata["Summary"]
__url__ = metadata["Home-page"]
__version__ = metadata["Version"]
__author__ = metadata["Author"]
__author_email__ = metadata["Author-email"]
__license__ = metadata["License"]
__copyright__ = f"2022 {__author__}"
