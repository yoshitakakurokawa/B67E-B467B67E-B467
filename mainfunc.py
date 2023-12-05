import os
from datetime import datetime

from dotenv import load_dotenv
import qiita
import translate
import chatgpt
import x_twitter

# '%j'は年中の日付を表す
DAY_OF_YEAR = '%j'

def main():
    # .envファイルの内容を読み込見込む
    load_dotenv()

    org_name = os.environ["ORGANIZATION_NAME"]  # 組織の名前
    try:
        articles = qiita.fetch_articles_from_organization(org_name)
        num = int(datetime.now().strftime(DAY_OF_YEAR)) % len(articles)

        if articles:
            article = articles[num]
            print(
                f"ItemId: {article['id']}, Title: {article['title']}, URL: {article['url']}"
            )
            # articleの本文を取得
            body = qiita.strip_html_tags(article["rendered_body"])
            body = qiita.strip_blanklines(body)

            # articleを英語に翻訳
            translated_text = translate.translate_j2e(body)
            print(translated_text)

            # 要約を生成
            summary = chatgpt.generate_summary(translated_text)
            print(summary)

            # ツイート
            x_twitter.post(f"自動要約\n{article['url']}\n{summary}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

