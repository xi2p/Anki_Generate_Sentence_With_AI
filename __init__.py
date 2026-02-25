from __future__ import annotations

from aqt import mw
from aqt.utils import tooltip

# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect

# import all of the Qt GUI library
from aqt.qt import *

# import the function that we designed
from .copy_to_clipboard import _copy_current_card_fields



# _copy_current_card_fields
action = QAction("Copy Details", mw)
qconnect(action.triggered, _copy_current_card_fields)
mw.form.menuTools.addAction(action)
