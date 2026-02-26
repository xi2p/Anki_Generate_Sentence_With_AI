"""
这个模块的作用是：随机获取复习中的语法/单词，生成一段AI提示词，并复制到用户粘贴板。
用户使用这个提示词，自行到各种AI网页输入，获取AI生成的文章。
"""
from __future__ import annotations

from typing import List, Tuple

from aqt import mw
from aqt.utils import tooltip

# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect, ask_user

# import all of the Qt GUI library
from aqt.qt import *

from anki.cards import Card

import random


WORD_CARD_NUM = 30
GRAMMAR_CARD_NUM = 5


def _get_reviewing_cards() -> Tuple[List[Card], List[Card]]:
    """
    从所有复习中的卡片里随机抽一定量的卡片，包括单词卡和语法卡
    """
    # 获取单词卡片
    deck_prefix = "NEW-JLPT::eggrolls-JLPT10k-v3"
    query = f'deck:"{deck_prefix}" -is:new'
    # 获取卡片ID列表
    card_ids = mw.col.find_cards(query)
    # 获取卡片对象列表
    word_cards = [mw.col.get_card(cid) for cid in card_ids]

    # 获取语法卡片
    deck_prefix = "蓝宝书N1-N5【超值白金版】::文法カード"
    query = f'deck:"{deck_prefix}" -is:new'
    card_ids = mw.col.find_cards(query)
    grammar_cards = [mw.col.get_card(cid) for cid in card_ids]

    # 抽取卡片
    word_cards = random.sample(word_cards, min([WORD_CARD_NUM, len(word_cards)]))
    grammar_cards = random.sample(grammar_cards, min([GRAMMAR_CARD_NUM, len(grammar_cards)]))

    return word_cards, grammar_cards

def get_ai_prompt() -> str:
    """
    获取用于生成文章的AI提示词
    """
    word_cards, grammar_cards = _get_reviewing_cards()
    prompt = "你是一个日语学习助手，请使用以下词汇和语法点，写一篇连贯的日语文章，并在末尾配上汉语翻译和讲解。文章应尽量自然，难度与给定词汇、语法匹配，包含所有指定的词汇和语法点。对于用到的语法、单词，应该给予加粗\n"
    prompt += "【包含以下词汇】\n"

    index = 0
    for card in word_cards:
        note = card.note()
        index += 1
        prompt += "===== 词汇{} =====\n".format(index)
        for name, value in note.items():
            if value:
                prompt += "{}: {}\n".format(name, value)

    index = 0
    for card in grammar_cards:
        note = card.note()
        index += 1
        prompt += "===== 语法{} =====\n".format(index)
        for name, value in note.items():
            if value:
                prompt += "{}: {}\n".format(name, value)

    def __copy_to_clipboard(confirm: bool):
        if confirm:
            QApplication.clipboard().setText(prompt)
            tooltip("提示词已复制到剪贴板！")

    ask_user(
        "提示词已生成，包含{}个词汇，{}个语法。\n确认以复制到剪切板。".format(len(word_cards), len(grammar_cards)),
        __copy_to_clipboard
    )


