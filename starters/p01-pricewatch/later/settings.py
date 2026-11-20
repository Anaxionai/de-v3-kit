"""PriceWatch's settings, read from settings.toml.

Task 23: move this file into the package, as pricewatch/pricewatch/settings.py, and
settings.toml into the product folder.
"""


def load_settings(path: str = "settings.toml") -> dict:
    """Read the settings file with tomllib and return its values as a dictionary.

    Open the file in binary mode: tomllib.load needs open(path, "rb").
    Pass these values to your functions instead of the constants typed into the code.
    """
    raise NotImplementedError("TODO(task 23): write load_settings(path)")
