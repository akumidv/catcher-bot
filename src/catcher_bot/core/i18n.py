import os
import gettext

_LOCALES_PATH = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__), '../locales')))
_en = gettext.translation('catcher_bot', localedir=_LOCALES_PATH, languages=['en'])
_en.install()

gettext = _en.gettext
