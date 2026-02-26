try:
    from openai import OpenAI, api_key
except ImportError:
    import subprocess
    subprocess.check_call(["pip3", "install", "openai"])
    from openai import OpenAI

import json


with open("_api_key", "r") as f:
    api_key = f.read().strip()

client = OpenAI(
    api_key=api_key, # 请替换成您的ModelScope Access Token
    base_url="https://api.deepseek.com"
)

system_prompt = """
根据以下日语单词信息，额外生成包含此单词的例句，用来填充例句库。你需要生成2条。你的结果应该直接以json格式输出，包含句子、注音句子、简体汉语翻译，不使用markdown格式，例：
{1: ["あと1時間で着くはずです", "あと1 時間[じかん]で 着[つ]く<b>はず</b>です", "再过一小时应该到了"], 2: ...}
"""

def _generate_example_sentences(prompt: str) -> dict:
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
    response = client.chat.completions.create(
        model="deepseek-chat", # ModelScope Model-Id
        messages=[
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        stream=False
    )

    return json.loads(response.choices[0].message.content)
