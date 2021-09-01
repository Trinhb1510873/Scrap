from flask import Flask, jsonify, request, make_response, abort
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from scrap import scrap_crunchbase, scrap_tetemarche
from lxml import etree

app = Flask(__name__)

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('user-agent={0}'.format(user_agent))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def no_found(error):
    return make_response(jsonify({'error': 'Parameter'}), 400)


@app.route('/scrapping/api/v1/crawl', methods=['POST', "GET"])
def scrap():
    if not request.json or not 'url' in request.json:
        abort(400)
    # Lấy url từ request
    url = request.json['url']
    print('url', url)

    # Sử dụng selenium, Chrome nên phải có Chromedriver
    driver = webdriver.Chrome(executable_path=r'.\chromedriver\chromedriver.exe', options=options)
    # 20s để render trang html
    WebDriverWait(driver, 20)
    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    dom = etree.HTML(str(soup))
    data = []
    if 'tetemarche.co.jp' in url:
        data = scrap_tetemarche(dom)
    elif 'www.crunchbase.com' in url:
        data = scrap_crunchbase(soup, dom)

    driver.quit()
    return {"data": data}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)

