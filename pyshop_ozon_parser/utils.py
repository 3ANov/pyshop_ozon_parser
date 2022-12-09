from urllib import parse


def ozon_api_url_creator(input_url):
    output_url = 'https://www.ozon.ru/api/composer-api.bx/page/json/v2' \
                 '?url='+parse.urlparse(input_url).path +\
                 '?'+parse.urlparse(input_url).query +\
                 '&layout_container=pdpPage2column' \
                 '&layout_page_index=2'

    return output_url