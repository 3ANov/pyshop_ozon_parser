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
            template_os_name_string = r"\{'key': 'OSWithoutVer', 'name': 'Операционная система', " \
                                      "'values': \[\{'text': '([^']*)', ('link': '[^']*', )*'key': 'OSWithoutVer_0'\}]\}"
            phone_characteristics_string = str(json.loads(json_data['widgetStates'][key])['characteristics'])
            # print(phone_characteristics_string)
            os_name_searched_groups = re.search(template_os_name_string, phone_characteristics_string)
            if os_name_searched_groups is None:
                os_name = ''
            else:
                os_name = os_name_searched_groups.group(1)

            template_os_version_string = "\{'key': '"+os_name+"Ver([a-zA-Z])*', 'name': '[^']*', 'values': \[\{'text': '([^']*)', ('link': '[^']*', )*'key': '[^']*'\}]\}"

            os_version_search_groups = re.search(template_os_version_string, phone_characteristics_string)
            if os_version_search_groups is None:
                os_version = ''
            else:
                os_version = os_version_search_groups.group(2)

            os_info['os_name'] = os_name
            os_info['os_version'] = os_version

            break
    return os_info