import os

from dotenv import load_dotenv
from google.cloud import translate


# Google Translateで英語に翻訳
def translate_j2e(text):
    """
    日本語を英語に翻訳します。

    Args:
        text (str): 翻訳する日本語の文章。

    Returns:
        str: 翻訳された英語の文章。

    Examples:
        >>> translate_j2e("こんにちは")
        "Hello"
    """
    client = translate.TranslationServiceClient()
    location = "global"
    project_id = os.getenv('GOOGLE_TRANSLATE_PROJECT_ID')
    if project_id is None:
        raise ValueError("環境変数 'GOOGLE_TRANSLATE_PROJECT_ID' が設定されていません。")
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "ja-JP",
            "target_language_code": "en-US",
        }
    )

    translated_text = "".join(translation.translated_text for translation in response.translations)

    return translated_text


import sys

if __name__ == "__main__":
    # .envファイルの内容を読み込見込む
    load_dotenv()
    
    if len(sys.argv) < 2:
        print("Usage: python translate.py <filename>")
        sys.exit(1)

    # ファイルを読み込み、翻訳を行う
    try:
        with open(sys.argv[1]) as f:
            article = f.read()
            translated_text = translate_j2e(article)
            print(translated_text)
    except Exception as e:
        print(f"エラーが発生しました: {e}")

