from openai import OpenAI
from aqt.utils import getOnlyText, show_critical
import json
import os


def enter_api_key():
    _api_key = getOnlyText("Enter your DeepSeek API key:", title="API Key Required", default="", parent=None)
    if not _api_key:
        show_critical("API key is required to use the DeepSeek API. Please enter a valid API key.")

    with open("_api_key", "w") as _f:
        _f.write(_api_key.strip())


# if not os.path.exists("_api_key"):
#     enter_api_key()






def generate_example_sentences(system_prompt: str, word_description: str) -> dict:
    """
    为当前卡片的单词生成例句数据。
    :param system_prompt: 系统提示词。
    :param word_description: 对当前卡片进行描述的信息，包含读音、词义、用法等信息，以便AI根据这些信息生成相关的例句数据。
    :return: 包含生成的例句数据的字典，格式为{1: [句子, 注音句子, 简体汉语翻译], 2: ...}
    """
    # prompt = """
    # [名]はず
    # 词义: （客观性的）应该；预计；箭尾
    # 例1: 司会者の彼女は来るはずだ
    # 例1Furigana: 司会者[しかいしゃ]の 彼女[かのじょ]は 来[く]る<b>はず</b>だ
    # 例1译: 她作为主持人，应该会来的
    # 例2: あと1時間で着くはずです
    # 例2Furigana: あと1 時間[じかん]で 着[つ]く<b>はず</b>です
    # 例3: 再过一小时应该到了
    # """
    with open("_api_key", "r") as f:
        api_key = f.read().strip()

    client = OpenAI(
        api_key=api_key,  # 请替换成您的ModelScope Access Token
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model="deepseek-chat", # ModelScope Model-Id
        messages=[
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': word_description
            }
        ],
        stream=False
    )

    return json.loads(response.choices[0].message.content)
