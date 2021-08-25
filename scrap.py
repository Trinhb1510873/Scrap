def scrap_tetemarche(soup):
    dl = soup.find('dl', {'class': 'about-dl'})
    business_name = dl.find_all('dd', {'class': 'about-dl__dd'})[0].text
    location = dl.find_all('dd', {'class': 'about-dl__dd'})[1].text
    found = dl.find_all('dd', {'class': 'about-dl__dd'})[2].text
    contact = dl.find_all('dd', {'class': 'about-dl__dd'})[3].text
    director = dl.find_all('dd', {'class': 'about-dl__dd'})[4].text
    business_content = dl.find_all('dd', {'class': 'about-dl__dd'})[5].text
    customer = dl.find_all('dd', {'class': 'about-dl__dd'})[6].text
    access = dl.find_all('dd', {'class': 'about-dl__dd'})[7].text
    return {
        "商号": business_name,
        '所在地': location,
        '設立': found,
        '連絡先': contact,
        '代表取締役': director,
        '事業内容': business_content,
        '主要取引先': customer,
        'アクセス': access
    }


def scrap_crunchbase(soup):
    data = []
    sheet_grid = soup.find('sheet-grid')
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
    return data