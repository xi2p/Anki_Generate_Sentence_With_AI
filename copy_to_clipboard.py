from __future__ import annotations

from aqt import mw
from aqt.utils import tooltip

# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect

# import all of the Qt GUI library
from aqt.qt import *

def _copy_current_card_fields() -> None:
    reviewer = mw.reviewer
    card = reviewer.card if reviewer else None
    if not card:
        tooltip("No card is currently displayed.")
        return

    note = card.note()
    lines = [f"{name}: {value}" for name, value in note.items()]
    text = "\n".join(lines)
    mw.app.clipboard().setText(text)
    tooltip("Card fields copied to clipboard.")