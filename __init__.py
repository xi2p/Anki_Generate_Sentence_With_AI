from __future__ import annotations

from aqt import mw
from aqt.utils import tooltip

# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect

# import all of the Qt GUI library
from aqt.qt import *

# import the function that we designed
from .copy_to_clipboard import copy_current_card_fields
from .expand_example_sentences import expand_sample_sentences, delete_expanded_sentences
from ._ai import enter_api_key
from .generate_passages import get_ai_prompt


# separator
separator = QAction(mw)
separator.setSeparator(True)
mw.form.menuTools.addAction(separator)

# copy_current_card_fields
action = QAction("Copy Details", mw)
qconnect(action.triggered, copy_current_card_fields)
mw.form.menuTools.addAction(action)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

# separator
separator = QAction(mw)
separator.setSeparator(True)
mw.form.menuTools.addAction(separator)

# enter API key
api_key_action = QAction("Enter API Key", mw)
qconnect(api_key_action.triggered, enter_api_key)
mw.form.menuTools.addAction(api_key_action)

# expand_sample_sentences
expand_action = QAction("Expand Sample Sentences", mw)
qconnect(expand_action.triggered, expand_sample_sentences)
mw.form.menuTools.addAction(expand_action)

# delete_expanded_sentences
delete_action = QAction("Delete Expanded Sentences", mw)
qconnect(delete_action.triggered, delete_expanded_sentences)
mw.form.menuTools.addAction(delete_action)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

# separator
separator = QAction(mw)
separator.setSeparator(True)
mw.form.menuTools.addAction(separator)

# get ai prompt to generate passage
get_ai_prompt_action = QAction("Get Prompt to Generate Passage", mw)
qconnect(get_ai_prompt_action.triggered, get_ai_prompt)
mw.form.menuTools.addAction(get_ai_prompt_action)

