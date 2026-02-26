# recognizable dictionaries
EGGROLLS_JLPT10K_V3 = "eggrolls-JLPT10k-v3"
LAN_BAO_SHU_CHAO_ZHI_BAI_JIN_BAN = "蓝宝书超值白金版"


def recognize_dictionary(card) -> str | None:
    """
    识别卡片所属的词典。
    通过检查卡片的标签来确定它属于哪个词典。
    """
    tags = card.note().tags
    for tag in tags:
        if EGGROLLS_JLPT10K_V3 in tag:
            return EGGROLLS_JLPT10K_V3
        elif LAN_BAO_SHU_CHAO_ZHI_BAI_JIN_BAN in tag:
            return LAN_BAO_SHU_CHAO_ZHI_BAI_JIN_BAN
    return None
