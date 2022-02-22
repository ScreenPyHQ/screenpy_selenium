"""
Questions an Actor can ask about the state of a web application.
"""

from .attribute import Attribute
from .browser_title import BrowserTitle
from .browser_url import BrowserURL
from .cookies import Cookies
from .element import Element
from .list import List
from .number import Number
from .selected import Selected
from .text import Text
from .text_of_the_alert import TextOfTheAlert

# Natural-language-enabling syntactic sugar
TheAttribute = Attribute
TheBrowserTitle = BrowserTitle
TheBrowserURL = BrowserURL
TheCookies = Cookies
TheElement = Element
TheList = List
TheNumber = Number
TheSelected = Selected
TheText = Text
TheTextOfTheAlert = TextOfTheAlert


__all__ = [
    "Attribute",
    "BrowserTitle",
    "BrowserURL",
    "Cookies",
    "Element",
    "List",
    "Number",
    "Selected",
    "Text",
    "TextOfTheAlert",
    "TheAttribute",
    "TheBrowserTitle",
    "TheBrowserURL",
    "TheCookies",
    "TheElement",
    "TheList",
    "TheNumber",
    "TheSelected",
    "TheText",
    "TheTextOfTheAlert",
]
