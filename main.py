from flask import Flask, jsonify, request, make_response, abort
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

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
    # print(html)

    soup = BeautifulSoup(html, "html.parser")

    sheet_grid = soup.find('sheet-grid')
    grid_header = sheet_grid.find('grid-header')
    grid_column_header_list = grid_header.find_all('grid-column-header')
    data = []
    for item in grid_column_header_list:
        print(item.text)

    grid_body = sheet_grid.find('grid-body')
    grid_row_list = grid_body.find_all('grid-row')
    for grid_row in grid_row_list:
        row = {}
        for grid_cell in grid_row.find_all('grid-cell'):
            column_id = grid_cell.get('data-columnid')
            div = grid_cell.find('div', class_="cb-absolute-to-cover layout-row layout-align-start-center")
            if column_id == 'identifier':
                number = div.find('div', class_="flex-none cb-text-color-medium cb-margin-medium-left ng-star-inserted")
                if number is not None:
                    organization_name = div.find('a',
                                                 class_="component--field-formatter field-type-identifier link-accent ng-star-inserted")
                    organization_name = number.text + organization_name.text
                    row['organization_name'] = organization_name
            elif column_id == 'categories':
                span = div.find('span', class_="component--field-formatter field-type-identifier-multi")
                if span is not None:
                    row['industries'] = span.text
            elif column_id == 'location_identifiers':
                span = div.find('span', class_="component--field-formatter field-type-identifier-multi")
                if span is not None:
                    row['location'] = span.text
            elif column_id == 'short_description':
                span_description = div.find('span',
                                            class_="component--field-formatter field-type-text_long ng-star-inserted")
                if span_description is not None:
                    row['description'] = span_description.text
            elif column_id == 'rank_org_company':
                if (div.find('a',
                             class_="component--field-formatter field-type-integer link-accent ng-star-inserted") is not None):
                    company = div.find('a',
                                       class_="component--field-formatter field-type-integer link-accent ng-star-inserted")
                    row['company'] = company.text
            else:
                pass
        data.append(row)
    driver.quit()
    return {"data": data}


if __name__ == "__main__":
    app.run(host='172.16.160.226', port=5005)
