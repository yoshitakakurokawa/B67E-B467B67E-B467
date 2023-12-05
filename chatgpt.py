import os
import openai
from dotenv import load_dotenv
from translate import translate_j2e

# .envファイルの内容を読み込見込む
load_dotenv()


def generate_summary(article):
    """
    OpenAIのChatGPTモデルを使用して、与えられた記事の要約を生成します。

    Args:
        article (str): 要約する記事。

    Returns:
        str: 生成された要約。
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a technology spokesperson for an IT company. You will introduce Qiita's articles on Twitter.",
                },
                {"role": "assistant", "content": article},
                {
                    "role": "user",
                    "content": "We would like you to create an attractive introduction in Japanese that will make people want to read the article, using the Japanese character limit of 100 characters. Please make #Qiita a required tag and add other hashtags that match the content.The answer will be used as is in the post, so no reply or explanation is required.",
                },
            ],
            max_tokens=110,
        )
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

    summary = response["choices"][0]["message"]["content"].strip()
    return summary
