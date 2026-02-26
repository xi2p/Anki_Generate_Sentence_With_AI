from __future__ import annotations

from aqt import mw
from aqt.utils import tooltip

# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect

# import all of the Qt GUI library
from aqt.qt import *


# recognizable dictionaries
EGGROLLS_JLPT10K_V3 = "eggrolls-JLPT10k-v3"


def _recognize_dictionary(card) -> str | None:
    """
    识别卡片所属的词典。
    通过检查卡片的标签来确定它属于哪个词典。
    """
    tags = card.note().tags
    for tag in tags:
        if EGGROLLS_JLPT10K_V3 in tag:
            return EGGROLLS_JLPT10K_V3
    return None


def _expand_sample_sentences() -> None:
    """
    填充示例句子字段。
    对于每个卡片，都会有四个例句的字段簇：
        - SentTypeN
        - SentKanjiN
        - SentFurigana4N
        - SentDefSCN
        - SentDefTCN
        - SentAudioN
    其中N是1到4的数字，表示不同的例句。每个卡片都已经有一些例句，但是数量不一，即有些卡片可能只有一个例句，而有些卡片可能有四个例句。
    本方法的目标是为每个卡片的空例句字段簇填充示例句子数据。为了方便，我们给每个字段簇填充相同的示例句子数据。
    """
    # 获取当前显示的卡片
    reviewer = mw.reviewer
    card = reviewer.card if reviewer else None
    if not card:
        tooltip("No card is currently displayed.")
        return

    # 获取卡片的笔记对象
    note = card.note()

    # 识别当前卡片是来源于哪个词典
    dictionary = _recognize_dictionary(card)

    if dictionary is None:
        tooltip("The current card does not belong to a recognized dictionary.")
        return

    elif dictionary == EGGROLLS_JLPT10K_V3:
        # 为每个示例句子字段簇填充示例句子数据
        for n in range(1, 4+1):
            # 检查例句是否为空
            sent_type_n = "SentType{}".format(n)
            sent_kanji_n = "SentKanji{}".format(n)
            sent_furigana_n = "SentFurigana{}".format(n)
            sent_def_scn_n = "SentDefSC{}".format(n)
            sent_def_tcn_n = "SentDefTC{}".format(n)
            sent_audio_n = "SentAudio{}".format(n)

            if not note[sent_kanji_n].strip():  # 如果例句字段为空
                note[sent_type_n] = "AI例"
                note[sent_kanji_n] = "これはサンプルの例文です。"
                note[sent_furigana_n] = "これはサンプルの例文[れいぶん]です。"
                note[sent_def_scn_n] = "这是一个示例句子。"
                note[sent_def_tcn_n] = "這是一個示例句子。"
                note[sent_audio_n] = ""



    # 刷新
    mw.col.update_note(note)
    mw.reset()


def _delete_expanded_sentences() -> None:
    """
    删除填充的示例句子字段。
    """
    # 获取当前显示的卡片
    reviewer = mw.reviewer
    card = reviewer.card if reviewer else None
    if not card:
        tooltip("No card is currently displayed.")
        return

    # 获取卡片的笔记对象
    note = card.note()

    # 识别当前卡片是来源于哪个词典
    dictionary = _recognize_dictionary(card)

    if dictionary is None:
        tooltip("The current card does not belong to a recognized dictionary.")
        return

    elif dictionary == EGGROLLS_JLPT10K_V3:
        # 清除填充的例句
        for n in range(1, 4+1):
            # 检查例句是否为空
            sent_type_n = "SentType{}".format(n)
            sent_kanji_n = "SentKanji{}".format(n)
            sent_furigana_n = "SentFurigana{}".format(n)
            sent_def_scn_n = "SentDefSC{}".format(n)
            sent_def_tcn_n = "SentDefTC{}".format(n)
            sent_audio_n = "SentAudio{}".format(n)

            if note[sent_kanji_n].strip():
                if note[sent_type_n] == "AI例":
                    note[sent_type_n] = ""
                    note[sent_kanji_n] = ""
                    note[sent_furigana_n] = ""
                    note[sent_def_scn_n] = ""
                    note[sent_def_tcn_n] = ""
                    note[sent_audio_n] = ""



    # 刷新
    mw.col.update_note(note)
    mw.reset()
