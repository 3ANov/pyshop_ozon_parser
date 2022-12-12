from urllib import parse
import json
import re


def ozon_api_url_creator(input_url):
    output_url = 'https://www.ozon.ru/api/composer-api.bx/page/json/v2' \
                 '?url='+parse.urlparse(input_url).path +\
                 '?'+parse.urlparse(input_url).query +\
                 '&layout_container=pdpPage2column' \
                 '&layout_page_index=2'

    return output_url


def parse_json_find_os_info(input_json_text):
    json_data = json.loads(input_json_text)
    os_info = {'os_name': '', 'os_version': ''}

    for key, value in json_data['widgetStates'].items():
        if 'webCharacteristics' in key:
            phone_characteristics_string = str(json.loads(json_data['widgetStates'][key])['characteristics'])

            template_os_version_string = "\{'key': '(?P<os_ver>((?P<os_name>([^']*))Ver[(sion)|]*))', 'name': '[^']* (?P=os_name)', 'values': \[\{'text': '((?P=os_name)([^']*))', ('link': '[^']*', )*'key': '((?P=os_ver)[^']*)'\}]\}"

            os_version_search_groups = re.search(template_os_version_string, phone_characteristics_string)

            template_os_name_string = r"\{'key': 'OSWithoutVer', 'name': 'Операционная система', " \
                                      "'values': \[\{'text': '([^']*)', ('link': '[^']*', )*'key': 'OSWithoutVer_0'\}]\}"

            os_name_searched_groups = re.search(template_os_name_string, phone_characteristics_string)

            if os_version_search_groups is None and os_name_searched_groups is None:
                os_info['os_version'] = ''
                os_info['os_name'] = ''
            elif os_version_search_groups is None:
                os_info['os_version'] = ''
                os_info['os_name'] = os_name_searched_groups.group(1)
            elif os_name_searched_groups is None:
                os_info['os_version'] = os_version_search_groups.group(5)
                os_info['os_name'] = os_version_search_groups.group('os_name')
            else:
                os_info['os_name'] = os_name_searched_groups.group(1)
                os_info['os_version'] = os_version_search_groups.group(5)

            break
    return os_info