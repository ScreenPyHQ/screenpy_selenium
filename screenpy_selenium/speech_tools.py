"""
Helpful tools for making good English out of ScreenPy+Selenium.
"""

from selenium.webdriver.common.keys import Keys

KEY_NAMES = {
    getattr(Keys, key_name): key_name
    for key_name in dir(Keys)
    if key_name.isupper() and not key_name.startswith("LEFT_")
}
