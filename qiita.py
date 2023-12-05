import requests
import json
import os
import re

from dotenv import load_dotenv


def fetch_articles_from_organization(org_name, per_page=10):
    """
    組織名から記事を取得します。

    Args:
        org_name (str): 組織名。
        per_page (int): 1ページあたりのアイテム数。

    Returns:
        list: 記事のリスト。

    """
    url = "https://qiita.com/api/v2/items"
    params = {
        "page": 1,  # ページ番号
        "per_page": per_page,  # 1ページあたりのアイテム数
        "query": f"org:{org_name}",  # 組織名で検索
    }
    headers = {"Authorization": "Bearer " + os.getenv("QIITA_ACCESS_TOKEN")}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        articles = json.loads(response.text)
        return articles
    else:
        print("Failed to fetch articles" + response.text)
        raise Exception(f"Failed to fetch articles. Status code: {response.status_code}, Response: {response.text}")
        return None


def strip_html_tags(text):
    """
    HTMLタグを取り除きます。

    Args:
        text (str): HTMLタグを取り除く文字列。

    Returns:
        str: HTMLタグを取り除いた文字列。

    Examples:
        >>> strip_html_tags("<h1>タイトル</h1>")
        "タイトル"
    """
    return re.sub(re.compile("<.*?>"), "", text)


def strip_blanklines(text):
    """
    空行と行頭行末の空白を取り除きます。

    Args:
        text (str): 空行と行頭行末の空白を取り除く文字列。

    Returns:
        str: 空行と行頭行末の空白を取り除いた文字列。

    Examples:
        >>> strip_blanklines("  \n  \n  \n  本文  \n  \n  ")
        "本文"
    """
    return "\n".join(filter(None, map(lambda x: x.strip(), text.split("\n"))))


def generate_filename(title, max_length=255):
    """
    タイトルからファイル名を生成します。特殊文字はハイフンに置き換えられ、最大長は255文字に制限されます。

    Args:
        title (str): ファイル名を生成するためのタイトル。
        max_length (int, optional): ファイル名の最大長。デフォルトは255。

    Returns:
        str: 生成されたファイル名。
    """
    filename = re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '-', title)
    return filename[:max_length]


if __name__ == "__main__":
    # .envファイルの内容を読み込見込む
    load_dotenv()
    org_name = os.getenv("ORGANIZATION_NAME")  # 組織の名前
    if org_name is None:
        raise Exception("Environment variable 'ORGANIZATION_NAME' is not set.")
    articles = fetch_articles_from_organization(org_name)

    if articles:
        for article in articles:
            print(
                f"ItemId: {article['id']}, Title: {article['title']}, URL: {article['url']}"
            )
            body = strip_html_tags(article["rendered_body"])
            body = strip_blanklines(body)
            print(f"Body: {body}")
            filename = generate_filename(article['title'])
            with open(f"{filename}.txt", "w") as f:
                f.write(body)
