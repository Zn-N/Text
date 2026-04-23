import requests
from bs4 import BeautifulSoup
import json


def parse_wechat_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...',
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取标题
        title_tag = soup.find('h1', class_='rich_media_title') or soup.find(id='activity-name')
        title = title_tag.text.strip() if title_tag else "标题未找到"

        # 提取正文
        content_tag = soup.find('div', class_='rich_media_content') or soup.find(id='js_content')
        content = content_tag.text.strip() if content_tag else "正文未找到"

        return {"title": title, "content": content, "link": url}
    except Exception as e:
        return {"error": str(e)}


# 用于处理HTTP请求的函数（以Flask为例）
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/parse', methods=['POST'])
def parse():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    result = parse_wechat_article(url)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)