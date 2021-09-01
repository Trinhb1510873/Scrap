def scrap_tetemarche(dom):
    dl = '//*[@id="main"]/section/div/dl'
    business_name = dom.xpath(dl + '/dd[1]')[0].text
    location = dom.xpath(dl +'/dd[2]')[0].text
    found = dom.xpath(dl + '/dd[3]')[0].text
    contact = dom.xpath(dl +'/dd[4]')[0].text
    director = dom.xpath(dl +'/dd[5]')[0].text
    business_content = dom.xpath(dl + '/dd[6]')[0].text
    customer = dom.xpath(dl +'/dd[7]')[0].text
    access = dom.xpath(dl +'/dd[8]/text()')
    access = ', '.join(str(e) for e in access)
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


def scrap_crunchbase(soup, dom):
    data = []
    for i in range(16):
        row = {}
        if i > 0:
            row['organization_name'] = dom.xpath('//sheet-grid/div/div/grid-body/div/grid-row[{0}]/grid-cell[2]/div/field-formatter/identifier-formatter/a/div/div'.format(i))[0].text
            industries = dom.xpath('//sheet-grid/div/div/grid-body/div/grid-row[{0}]/grid-cell[3]/div/field-formatter/identifier-multi-formatter/span/a/text()'.format(i))
            industries = ', '.join(str(e) for e in industries)
            row['industries'] = industries
            location = dom.xpath('//sheet-grid/div/div/grid-body/div/grid-row[{0}]/grid-cell[4]/div/field-formatter/identifier-multi-formatter/span/a/text()'.format(i))
            location = ', '.join(str(e) for e in location)
            row['location'] = location
            description = dom.xpath('//sheet-grid/div/div/grid-body/div/grid-row[{0}]/grid-cell[5]/div/field-formatter/span'.format(i))[0].text
            row['description'] = description
            company = dom.xpath('//sheet-grid/div/div/grid-body/div/grid-row[{0}]/grid-cell[6]/div/field-formatter/a'.format(i))[0].text
            row['company'] = company

            data.append(row)        
    return data