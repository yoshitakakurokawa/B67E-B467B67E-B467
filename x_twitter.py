import os
import tweepy
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

def post(text):
    """
    ツイートします。

    Args:
        text (str): ツイートする文章。

    Returns:
        None: None
    """
    consumer_key = os.getenv("X_API_KEY")
    consumer_secret = os.getenv("X_API_KEY_SECRET")
    access_token_key = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    # 環境変数が設定されていない場合のエラーハンドリング
    if not all([consumer_key, consumer_secret, access_token_key, access_token_secret]):
        raise Exception("環境変数が設定されていません。")

    # 認証
    try:
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token_key,
            access_token_secret=access_token_secret,
        )
    except Exception as e:
        raise Exception("Twitter APIへの接続に失敗しました。") from e

    # ツイート
    try:
        client.create_tweet(text=text)
    except Exception as e:
        raise Exception("ツイートの作成に失敗しました。") from e


if __name__ == "__main__":
    posttext = "API test post 3"
    try:
        post(posttext)
        print(posttext)
    except Exception as e:
        print(e)
