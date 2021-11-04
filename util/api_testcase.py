# author:windy
# datetime:2021/11/3 11:05 上午
# software: PyCharm

import jsonpath
from api import encrypt_by_public_key
from util.api import app_api_post


def api_001():
    api_url = 'https://appgateway-uat.lifekh.com/gateway_web/operator/login/encryption/factor.do'
    headers = {
        'Connection': 'keep-alive',
        "termtyp": "ANDROID",
        "channel": "Portal",
        "projectname": "SuperApp",
        "appid": "SuperApp",
        "appno": "10",
        "appversion": "2.19.0",
        "phonemodel": "python-api-test",
        "deviceId": "python_api_test",
        "signver": "1.0"
    }
    body = {}
    response_data = app_api_post(api_url, api_body=body, header=headers)
    response_data = eval(response_data)
    data = {}
    data['index'] = jsonpath.jsonpath(response_data, '$.data.index')[0]
    data['publicKey'] = jsonpath.jsonpath(response_data, '$.data.publicKey')[0]

    public_key = data['publicKey']
    login_url = 'https://appgateway-uat.lifekh.com/gateway_web/operator/login/password.do'
    login_body = {"loginName": "855010143291"}
    headers2 = {
        "Connection": "keep-alive",
        "termtyp": "ANDROID",
        "channel": "Portal",
        "projectname": "SuperApp",
        "appid": "SuperApp",
        "appno": "10",
        "appversion": "2.19.0",
        "phonemodel": "python-api-test",
        "deviceId": "python_api_test",
        "signver": "1.0",
        "content-type": "application/json; charset=UTF-8"
    }

    pass_word = encrypt_by_public_key('hd123456', public_key)

    login_body["password"] = pass_word
    login_body["index"] = data["index"]

    response_data_login = app_api_post(login_url, api_body=login_body, header=headers2)
    return response_data_login


if __name__ == '__main__':
    print(api_001())