# author:windy
# datetime:2021/11/3 11:05 上午
# software: PyCharm

import json
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


def api_002():
    login_url = 'https://openapi-uat.lifekh.com/open_web/gateway.do'

    headers2 = {
        "Connection": "keep-alive",
        "termtyp": "ANDROID",
        "channel": "Portal",
        "projectname": "SuperApp",
        "appid": "SuperApp",
        "phonemodel": "python-api-test",
        "deviceId": "python_api_test",
        "content-type": "application/json; charset=UTF-8"
    }
    biz_content = {}
    privateKey = """MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAKfUj13CGKkxEtcmCg3IdQBMyXV46Cdwf+dLX1bmtaAkbPY5ov1zQrNaLICl+tc+zi6L8tqtjA3WS3P9YZiI9FMSCo8lImPrG1RTs7CM1Y6tzl8K/qsecQ44UPvEzlGRfGXttSqdmFYzsSWNIFidz6kXFszCBdYun7EDFnf7WDtXAgMBAAECgYBe/VLLqUDV+h2EwlXsaSm3qr5Xi8AyGl16JtHmWJwx8IvvbL3Qn7z/0CjiA4+O5lBCThl9Jb7gUgrQsnfboqBNues6XyCuiXypubI0sTh0UcrS0dZDSdqlJpGoIlsA2QnYfBEB5Czo+0E4b7+UVBr3F5pYVzu+0iyqcAcQwXUckQJBAPbkjcdYMdAprmis8r24DaX7qvKEDxunlSvW5kpJd+k3+toUpOQtpb7+rNOrlEJFU4SNjYfLgQzUby0AEYyMZJkCQQCuBWg+4lxFzud1tsGmeIu7sp7qwyoutYU2+KBTBvbSs0LD48kOBIDnIztJb8UOi14+ZydSxO32Ac2PiwY98qVvAkBAVjKz/cGNUy9Fy7u9wJad6EUVyV/+ft8ae3eraBW9Sn8uES8e3t5QNSFoT0/lLRekdRaqildotnr6KQhprbQRAkEAnpPs2Akcfry57Wn588I7y3JNIK9yXBgr6dkM+DwLZhvWxn1ndK+j630OhLAmiUd1PTZw/hrYoeoosRrGOGNKXwJBAK6YuCYRZsNd6LNbM/9iTkdJi5LoKwY4mPxegjlAXczdUIx3ylIzF+b36K6Zrr/b/HwEsUYrCpQJr/U1dKBcZs0="""
    biz_content["mobile"] = "855010145010"
    biz_content["couponNo"] = "WNJ210908154513449"

    need_sign = {}
    need_sign['biz_content'] = biz_content
    need_sign['app_id'] = '1624010948354'
    need_sign['charset'] = 'UTF-8'
    need_sign['service'] = 'send.choice.coupon'
    need_sign['timestamp'] = '2020-09-07 16:07:50'
    need_sign['version'] = '1.0'
    biz_content_str = json.dumps(need_sign, sort_keys=True)
    biz_content_dict = eval(biz_content_str)
    unsign_data = ''

    for k, v in biz_content_dict.items():
        if type(v) is dict:
            unsign_data += str(k) + '=' + str(v).replace(' ', '') + '&'
        else:
            unsign_data += str(k) + '=' + str(v) + '&'
    unsign_data = unsign_data[0:-1].replace("'", '"')
    print(unsign_data)
    from api import rsa_sign_by_private_key
    sign = rsa_sign_by_private_key(unsign_data, privateKey)
    print(sign)
    login_body = {"app_id":"1624010948354",
                  "biz_content":"{\"couponNo\":\"WNJ210908154513449\",\"mobile\":\"855010145010\"}",
                  "charset":"UTF-8",
                  "open_id":"",
                  "service":"send.choice.coupon",
                  "sign_type":"RSA",
                  "timestamp":"2020-09-07 16:07:50",
                  "version":"1.0"
                  }
    login_body["sign"] = sign
    #
    print(login_body)
    #
    return app_api_post(login_url, login_body, headers2)


if __name__ == '__main__':
    print(api_002())