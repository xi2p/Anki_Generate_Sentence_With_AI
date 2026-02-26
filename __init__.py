from __future__ import annotations

from aqt import mw
from aqt.utils import tooltip

# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect

# import all of the Qt GUI library
from aqt.qt import *

# import the function that we designed
from .copy_to_clipboard import _copy_current_card_fields
from .expand_example_sentences import _expand_sample_sentences, _delete_expanded_sentences


# separator
separator = QAction(mw)
separator.setSeparator(True)
mw.form.menuTools.addAction(separator)

# _copy_current_card_fields
action = QAction("Copy Details", mw)
qconnect(action.triggered, _copy_current_card_fields)
mw.form.menuTools.addAction(action)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

# separator
separator = QAction(mw)
separator.setSeparator(True)
mw.form.menuTools.addAction(separator)

# _expand_sample_sentences
expand_action = QAction("Expand Sample Sentences", mw)
qconnect(expand_action.triggered, _expand_sample_sentences)
mw.form.menuTools.addAction(expand_action)

# _delete_expanded_sentences
delete_action = QAction("Delete Expanded Sentences", mw)
qconnect(delete_action.triggered, _delete_expanded_sentences)
mw.form.menuTools.addAction(delete_action)





