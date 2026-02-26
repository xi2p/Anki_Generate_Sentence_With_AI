from __future__ import annotations

from aqt import mw
from aqt.utils import tooltip

# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect

# import all of the Qt GUI library
from aqt.qt import *

from . import _ai

from .recognize_dictionary import *


def expand_sample_sentences() -> None:
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
    dictionary = recognize_dictionary(card)

    if dictionary is None:
        tooltip("The current card does not belong to a recognized dictionary.")
        return

    elif dictionary == EGGROLLS_JLPT10K_V3:
        # 为每个示例句子字段簇填充示例句子数据
        empty_sentence_n_list = []
        # 生成prompt
        system_prompt = """根据以下日语单词信息，额外生成包含此单词的例句，用来填充例句库。你需要生成%d条。你的结果应该直接以json格式输出，包含句子、注音句子、简体汉语翻译，不使用markdown格式，例：{1: ["あと1時間で着くはずです", "あと1 時間[じかん]で 着[つ]く<b>はず</b>です", "再过一小时应该到了"], 2: ...}"""

        prompt = "[{}]{}\n词义: {}".format(note["VocabPoS"], note["VocabKanji"], note["VocabDefSC"])

        for n in range(1, 4 + 1):
            # 检查例句是否为空
            sent_type_n = "SentType{}".format(n)
            sent_kanji_n = "SentKanji{}".format(n)
            sent_furigana_n = "SentFurigana{}".format(n)
            sent_def_scn_n = "SentDefSC{}".format(n)
            sent_def_tcn_n = "SentDefTC{}".format(n)
            sent_audio_n = "SentAudio{}".format(n)

            if not note[sent_kanji_n].strip():  # 如果例句字段为空
                empty_sentence_n_list.append(n)
            else:
                prompt += "例: {}\nFurigana: {}\n译: {}".format(note[sent_kanji_n], note[sent_furigana_n],
                                                                note[sent_def_scn_n])

        if len(empty_sentence_n_list) < 1:
            tooltip("All example sentence fields are already filled.")
            return

        ai_generated_sentences: list = list(_ai.generate_example_sentences(system_prompt % len(empty_sentence_n_list), prompt).values())

        index = 0
        for n in empty_sentence_n_list:
            sent_type_n = "SentType{}".format(n)
            sent_kanji_n = "SentKanji{}".format(n)
            sent_furigana_n = "SentFurigana{}".format(n)
            sent_def_scn_n = "SentDefSC{}".format(n)
            sent_def_tcn_n = "SentDefTC{}".format(n)
            sent_audio_n = "SentAudio{}".format(n)

            note[sent_type_n] = "AI例"
            note[sent_kanji_n] = ai_generated_sentences[index][0]
            note[sent_furigana_n] = ai_generated_sentences[index][1]
            note[sent_def_scn_n] = ai_generated_sentences[index][2]
            note[sent_def_tcn_n] = ai_generated_sentences[index][2]
            note[sent_audio_n] = ""

            index += 1

    elif dictionary == LAN_BAO_SHU_CHAO_ZHI_BAI_JIN_BAN:
        # 为每个示例句子字段簇填充示例句子数据
        empty_sentence_n_list = []
        # 生成prompt
        system_prompt = """根据以下日语语法信息，额外生成包含此语法的例句，用来填充例句库。你需要生成%d条。你的结果应该直接以json格式输出，包含句子、简体汉语翻译，句子中应包含假名标注、语法加粗，不使用markdown格式，例：{1: [" 今[こん] 晩[ばん]、 大[おお] 型[がた]の 台[たい] 風[ふう]がこの 地[ち] 方[ほう]へ 近[ちか]づく<b>恐[おそ]</b><b>れがあります</b>。", "今晚可能有强台风靠近该地区。"], 2: ...}"""

        prompt = "{}\n{}\n{}".format(note["Word"], note["ConnectiveType1"], note["Explain1"])

        for n in range(1, 25+1):
            # 检查例句是否为空
            example_n = "Example{}".format(n)
            chinese_n = "Chinese{}".format(n)

            if not note[example_n].strip():  # 如果例句字段为空
                empty_sentence_n_list.append(n)

            else:
                prompt += "例: {}\n译: {}".format(note[example_n], note[chinese_n])

        if len(empty_sentence_n_list) < 1:
            tooltip("All example sentence fields are already filled.")
            return

        number_of_sentence_to_generate = min([len(empty_sentence_n_list), 4]) # 最多生成4条
        ai_generated_sentences: list = list(_ai.generate_example_sentences(system_prompt % number_of_sentence_to_generate, prompt).values())

        index = 0
        for n in empty_sentence_n_list:
            if index >= number_of_sentence_to_generate:
                break

            example_n = "Example{}".format(n)
            chinese_n = "Chinese{}".format(n)

            note[example_n] = "(AI例)" + ai_generated_sentences[index][0]
            note[chinese_n] = ai_generated_sentences[index][1]

            index += 1


    # 刷新
    mw.col.update_note(note)
    mw.reset()


def delete_expanded_sentences() -> None:
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
    dictionary = recognize_dictionary(card)

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

    elif dictionary == LAN_BAO_SHU_CHAO_ZHI_BAI_JIN_BAN:
        # 清除填充的例句
        for n in range(1, 25+1):
            # 检查例句是否为空
            example_n = "Example{}".format(n)
            chinese_n = "Chinese{}".format(n)

            if note[example_n].startswith("(AI例)"):
                note[example_n] = ""
                note[chinese_n] = ""


    # 刷新
    mw.col.update_note(note)
    mw.reset()
