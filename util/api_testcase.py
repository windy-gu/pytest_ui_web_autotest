# author:windy
# datetime:2021/11/3 11:05 上午
# software: PyCharm

import json
import time
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
        "appversion": "2.24.0",
        "phonemodel": "python-api-test",
        "deviceId": "python_api_test",
        "signver": "1.0"
    }
    body = {}
    response_data = app_api_post(api_url, api_body=body, header=headers)
    print(response_data)
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
    # 请求头参数
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
    # biz_content 需要的动态参数mobile和couponNo
    biz_content = {}
    privateKey = """MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAKfUj13CGKkxEtcmCg3IdQBMyXV46Cdwf+dLX1bmtaAkbPY5ov1zQrNaLICl+tc+zi6L8tqtjA3WS3P9YZiI9FMSCo8lImPrG1RTs7CM1Y6tzl8K/qsecQ44UPvEzlGRfGXttSqdmFYzsSWNIFidz6kXFszCBdYun7EDFnf7WDtXAgMBAAECgYBe/VLLqUDV+h2EwlXsaSm3qr5Xi8AyGl16JtHmWJwx8IvvbL3Qn7z/0CjiA4+O5lBCThl9Jb7gUgrQsnfboqBNues6XyCuiXypubI0sTh0UcrS0dZDSdqlJpGoIlsA2QnYfBEB5Czo+0E4b7+UVBr3F5pYVzu+0iyqcAcQwXUckQJBAPbkjcdYMdAprmis8r24DaX7qvKEDxunlSvW5kpJd+k3+toUpOQtpb7+rNOrlEJFU4SNjYfLgQzUby0AEYyMZJkCQQCuBWg+4lxFzud1tsGmeIu7sp7qwyoutYU2+KBTBvbSs0LD48kOBIDnIztJb8UOi14+ZydSxO32Ac2PiwY98qVvAkBAVjKz/cGNUy9Fy7u9wJad6EUVyV/+ft8ae3eraBW9Sn8uES8e3t5QNSFoT0/lLRekdRaqildotnr6KQhprbQRAkEAnpPs2Akcfry57Wn588I7y3JNIK9yXBgr6dkM+DwLZhvWxn1ndK+j630OhLAmiUd1PTZw/hrYoeoosRrGOGNKXwJBAK6YuCYRZsNd6LNbM/9iTkdJi5LoKwY4mPxegjlAXczdUIx3ylIzF+b36K6Zrr/b/HwEsUYrCpQJr/U1dKBcZs0="""
    biz_content["mobile"] = "855010145010"
    biz_content["couponNo"] = "WNJ220120161949011"

    # 需要私钥加签的参数
    need_sign = {}
    need_sign['biz_content'] = biz_content
    need_sign['app_id'] = '1624010948354'
    need_sign['charset'] = 'UTF-8'
    need_sign['service'] = 'send.choice.coupon'
    need_sign['timestamp'] = '2020-09-07 16:07:50'
    need_sign['version'] = '1.0'
    print("需要加密的原始数据：" + str(need_sign))

    # 对加签的内容根据key值进行序列化排序
    biz_content_str = json.dumps(need_sign, sort_keys=True)

    biz_content_dict = eval(biz_content_str)  # 转为字典dict类型
    print(biz_content_str)
    unsign_data = ''

    for k, v in biz_content_dict.items():
        # 将key值和value值通过 "=" 拼接，不同键值通过 "&"连接
        if type(v) is dict:
            unsign_data += str(k) + '=' + str(v).replace(' ', '') + '&'
        else:
            unsign_data += str(k) + '=' + str(v) + '&'
    unsign_data = unsign_data[0:-1].replace("'", '"')
    print("待加密的内容：" + unsign_data)
    from api import rsa_sign_by_private_key
    sign = rsa_sign_by_private_key(unsign_data, privateKey)
    print("加签后内容：" + sign)
    login_body = {"app_id":"1624010948354",
                  "biz_content":"{\"couponNo\":\"WNJ220120161949011\",\"mobile\":\"855010145010\"}",
                  "charset":"UTF-8",
                  "open_id":"",
                  "service":"send.choice.coupon",
                  "sign_type":"RSA",
                  "timestamp":"2020-09-07 16:07:50",
                  "version":"1.0"
                  }
    login_body["sign"] = sign
    #
    print("请求body："+str(login_body))
    #
    return app_api_post(login_url, login_body, headers2)


def api_003_create_ord():
    login_url = 'https://openapi-uat.lifekh.com/open_web/gateway.do'
    # 请求头参数
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
    # biz_content 需要的动态参数mobile和couponNo
    biz_content = {}
    privateKey = """MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAKC9PfqjQfRjXViXuhY19kGD4hUGe7ygLfN8NemHB84RV30hhoaUp+DcKJ8qtQq/OlYrU93tNqNSRE4IWu0bX7NnMy9wmdF1zwshhUj/vHkofLrnsjm5sPWtDB2y8S6nw98P1Y4xE2EL/gfr08Sg21blrkki0Ge+Tl8v1UO7O27TAgMBAAECgYArbTVTg8wL5NSRXNyvp4CSjrkECS5g9b20bLh8ETkwmUrTybz4my0H+TMYXYdwEd4G7cnIyY/bbBx8IJHAQYcHGXbyfX1WvW6Tec/98nBsy4MborWoS35EhkHGg3dEi8pZS8sQLuiJ1mjSzN+Mse4EuC8SlMnWyRMGtb26b90/8QJBANWbDePORJ33g6VVBzdyjVt8HTmF795QYXZqh7ofNw6Y/Nxsfr56D+aMqF+jFdIVspVqyZ2DD5Mo+fggI/tibqUCQQDApCHVNIPAi351HJFxGXBTwYDEKPLUbdn7YF4O1Dj2uqu/n13Ilj2zU+siFuycPoEl2IYlCD1SEhxsTP4CayYXAkBFkRoU9zihudrGHcsb49Ll2KYr9dMJNGSJjGhn1YK43lp771nX7yj+jRDJFPQmV6qxvvWqtuR7qPzAMreFR6mBAkAcZFRkMvA0IZsKsaIx9BjdD0jmIE7hxir5ZJOYRej7XDnR7TAKTzJaysR96rkGsiOgq0/iB1vaS7cKszJAswATAkB5OuEAZwE1jbc/QNvE58TWN9mmZaJCyAE6IhYCq2vlUPeGwT9Jt3bhmFQlmbfgotnCMX2wkjYoMAlYHv+LsSqz"""
    biz_content["businessOrderState"] = {"km": "kmKH状态", "en": "enUS状态", "zh": "中文状态"}
    biz_content["showContent"] = {"km": "kmKH内容", "en": "enUS内容", "zh": "中文内容"}
    biz_content["title"] = {"km": "kmKH_title内容", "en": "enUS_title内容", "zh": "中文_title内容"}
    biz_content["showUrl"] = "https://cbu01.alicdn.com/img/ibank/O1CN01DnPiyZ1eVFncFnYYF_!!2210172793876-0-cib.jpg"
    biz_content["userNo"] = "1289443376494931968"
    biz_content["payType"] = "11"
    biz_content["actualPayAmount"] = "0.21"
    biz_content["totalPayableAmount"] = "0.21"
    biz_content["businessOrderId"] = "111111"
    biz_content["notifyUrl"] = "http://www.baidu.com"
    biz_content["returnUrl"] = "SuperApp://SuperApp/CashierResult?businessLine=YumNow&orderNo="
    biz_content["subBizEntity"] = "42"
    biz_content["merchantNo"] = "04134701"
    biz_content["businessContent"] = {"PAY_NOW": 1}

    # 需要私钥加签的参数
    need_sign = {}
    need_sign['biz_content'] = biz_content
    need_sign['app_id'] = '1603310269'
    need_sign['charset'] = 'UTF-8'
    need_sign['service'] = 'create.transaction.order'
    # need_sign['sign_type'] = 'RSA'
    need_sign['timestamp'] = '2022-04-20 16:07:50'
    need_sign['version'] = '1.0'
    print("need_sign的原始数据：" + str(need_sign))

    # 对加签的内容根据key值进行序列化排序
    nees_sign_str = json.dumps(need_sign, sort_keys=True)

    need_sign_dict = eval(nees_sign_str)  # 转为字典dict类型
    print(nees_sign_str)
    unsign_data = ''

    for k, v in need_sign_dict.items():
        # 将key值和value值通过 "=" 拼接，不同键值通过 "&"连接
        if type(v) is dict:
            unsign_data += str(k) + '=' + str(v).replace(' ', '') + '&'
        else:
            unsign_data += str(k) + '=' + str(v) + '&'
    unsign_data = unsign_data[0:-1].replace("'", '"')
    print("待加密的内容：" + unsign_data)
    biz_content_str = unsign_data.split('biz_content=')[1].split('&charset')[0]  # 提取biz_content内容
    print(biz_content_str)
    from api import rsa_sign_by_private_key
    sign = rsa_sign_by_private_key(unsign_data, privateKey)
    print("加签后内容：" + sign)
    login_body = {"app_id": need_sign['app_id'],
                  "biz_content": biz_content_str,
                  "charset": need_sign['charset'],
                  "service": need_sign['service'],
                  "sign_type": "RSA",
                  "timestamp": need_sign['timestamp'],
                  "version": need_sign['version']
                  }
    login_body["sign"] = sign
    #
    print("请求body：" + str(login_body))
    #
    return app_api_post(login_url, login_body, headers2)


def api_004_finish_ord(ord_no: str):
    login_url = 'https://openapi-uat.lifekh.com/open_web/gateway.do'
    # 请求头参数
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
    # biz_content 需要的动态参数mobile和couponNo
    biz_content = {}
    privateKey = """MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAKC9PfqjQfRjXViXuhY19kGD4hUGe7ygLfN8NemHB84RV30hhoaUp+DcKJ8qtQq/OlYrU93tNqNSRE4IWu0bX7NnMy9wmdF1zwshhUj/vHkofLrnsjm5sPWtDB2y8S6nw98P1Y4xE2EL/gfr08Sg21blrkki0Ge+Tl8v1UO7O27TAgMBAAECgYArbTVTg8wL5NSRXNyvp4CSjrkECS5g9b20bLh8ETkwmUrTybz4my0H+TMYXYdwEd4G7cnIyY/bbBx8IJHAQYcHGXbyfX1WvW6Tec/98nBsy4MborWoS35EhkHGg3dEi8pZS8sQLuiJ1mjSzN+Mse4EuC8SlMnWyRMGtb26b90/8QJBANWbDePORJ33g6VVBzdyjVt8HTmF795QYXZqh7ofNw6Y/Nxsfr56D+aMqF+jFdIVspVqyZ2DD5Mo+fggI/tibqUCQQDApCHVNIPAi351HJFxGXBTwYDEKPLUbdn7YF4O1Dj2uqu/n13Ilj2zU+siFuycPoEl2IYlCD1SEhxsTP4CayYXAkBFkRoU9zihudrGHcsb49Ll2KYr9dMJNGSJjGhn1YK43lp771nX7yj+jRDJFPQmV6qxvvWqtuR7qPzAMreFR6mBAkAcZFRkMvA0IZsKsaIx9BjdD0jmIE7hxir5ZJOYRej7XDnR7TAKTzJaysR96rkGsiOgq0/iB1vaS7cKszJAswATAkB5OuEAZwE1jbc/QNvE58TWN9mmZaJCyAE6IhYCq2vlUPeGwT9Jt3bhmFQlmbfgotnCMX2wkjYoMAlYHv+LsSqz"""
    biz_content["aggregateOrderFinalState"] = "11"  # 11：完成 （会进入结算状态），12：取消（支付完成的会自动退款）
    biz_content["aggregateOrderNo"] = ord_no

    # 需要私钥加签的参数
    need_sign = {}
    need_sign['biz_content'] = biz_content
    need_sign['app_id'] = '1603310269'
    need_sign['charset'] = 'UTF-8'
    need_sign['service'] = 'confirm.transaction.order'
    # need_sign['sign_type'] = 'RSA'
    need_sign['timestamp'] = '2022-04-20 16:07:50'
    need_sign['version'] = '1.0'
    print("need_sign的原始数据：" + str(need_sign))

    # 对加签的内容根据key值进行序列化排序
    nees_sign_str = json.dumps(need_sign, sort_keys=True)

    need_sign_dict = eval(nees_sign_str)  # 转为字典dict类型
    print(nees_sign_str)
    unsign_data = ''

    for k, v in need_sign_dict.items():
        # 将key值和value值通过 "=" 拼接，不同键值通过 "&"连接
        if type(v) is dict:
            unsign_data += str(k) + '=' + str(v).replace(' ', '') + '&'
        else:
            unsign_data += str(k) + '=' + str(v) + '&'
    unsign_data = unsign_data[0:-1].replace("'", '"')
    print("待加密的内容：" + unsign_data)
    biz_content_str = unsign_data.split('biz_content=')[1].split('&charset')[0]  # 提取biz_content内容
    print(biz_content_str)
    from api import rsa_sign_by_private_key
    sign = rsa_sign_by_private_key(unsign_data, privateKey)
    print("加签后内容：" + sign)
    login_body = {"app_id": need_sign['app_id'],
                  "biz_content": biz_content_str,
                  "charset": need_sign['charset'],
                  "service": need_sign['service'],
                  "sign_type": "RSA",
                  "timestamp": need_sign['timestamp'],
                  "version": need_sign['version']
                  }
    login_body["sign"] = sign
    #
    print("请求body：" + str(login_body))
    #
    return app_api_post(login_url, login_body, headers2)


def api_005_application_test(app_id: str, ord_no: str):
    login_url = 'https://openapi-uat.lifekh.com/open_web/gateway.do'
    # 请求头参数
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
    # biz_content 需要的动态参数mobile和couponNo
    biz_content = ord_no
    privateKey = """MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBAKaEnENEGlooCd/QWYtIJ1VNxtH1D75s72SCS6zCyIF7vtN8+S/spBVxcMebDgyaZgn/lshf/2RPbQi9PUotJ5nkspvqSh93SoYgg11MM/phGsABQLD1UTAgyRk5OZ5/MakDncZTnyDuNjgyQ1GhCrx3dLNQs/U7B979IIECas4DAgMBAAECgYEAj069dR6dV03yAY68IaR9RWrkWzl+zTHPbT69hfc0vEsVVcnOYzJTnKi+mOqW0r3mZ2ByEgycLWY1vjmvD7GAzApw2+ZJDgSh05bEnuu/uxmjJe7BX7n8gBMEZdsvqJ4/bSDonrQlauFQVJpvjQz3n51uG/ZVmBDTUpK+2S1rgTECQQDgO41MwAJsl1GRp642T02KFEh0Z/MdBI+FpwxSN5rSB5F/PZShSmoCI78GU7gTRDGbdQODAlI1p16Ku+436R4HAkEAvhvewKp0tNyweZQ+cFKAlsyphfgKDhe7O6kop57cD9IRfOySxRyzVUlEQ2tSb9M/oLRc4HNOu5P+PsVJmK0RJQJBAKVNIYBX+DGHZ7mBrJsa4SWOiE9QJlfY+djkad/eYAK/U5JCmmRA0F9dbMBETWneltdsbrdQqbwl8ztBCX8sGlcCQCZl0K8PfrUNIiPcWmQrdcd/nPnvKHDCQFIDj6+TeZVEc73MtrRTYLFoM/5+Dc+CVoaqB1xaTdu7P44EISJSSnUCQQCtghaFoP7oRJzH8fseDvOqyU3bhLeAYCf0Pcxt5dW4Vtf7vBvz63BprR5YtkzOW3JV7TvyNKjqMISJTROnWisk"""


    # 需要私钥加签的参数
    need_sign = {}
    need_sign['biz_content'] = biz_content
    need_sign['app_id'] = app_id
    need_sign['charset'] = 'UTF-8'
    need_sign['service'] = 'payment.query'
    need_sign['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    need_sign['version'] = '1.0'
    print("need_sign的原始数据：" + str(need_sign))

    # 对加签的内容根据key值进行序列化排序
    nees_sign_str = json.dumps(need_sign, sort_keys=True)

    need_sign_dict = eval(nees_sign_str)  # 转为字典dict类型
    print(nees_sign_str)
    unsign_data = ''

    for k, v in need_sign_dict.items():
        # 将key值和value值通过 "=" 拼接，不同键值通过 "&"连接
        if type(v) is dict:
            unsign_data += str(k) + '=' + str(v).replace(' ', '') + '&'
        else:
            unsign_data += str(k) + '=' + str(v) + '&'
    unsign_data = unsign_data[0:-1].replace("'", '"')
    print("待加密的内容：" + unsign_data)
    biz_content_str = unsign_data.split('biz_content=')[1].split('&charset')[0]  # 提取biz_content内容
    print(biz_content_str)
    from api import rsa_sign_by_private_key
    sign = rsa_sign_by_private_key(unsign_data, privateKey)
    print("加签后内容：" + sign)
    login_body = {"app_id": need_sign['app_id'],
                  "biz_content": biz_content_str,
                  "charset": need_sign['charset'],
                  "service": need_sign['service'],
                  "sign_type": "RSA",
                  "timestamp": need_sign['timestamp'],
                  "version": need_sign['version']
                  }
    login_body["sign"] = sign
    #
    print("请求body：" + str(login_body))
    #
    return app_api_post(login_url, login_body, headers2)


if __name__ == '__main__':
    # print(api_002())
    print(api_003_create_ord())
    # print(api_004_finish_ord("1517062598539964416"))
    # print(api_005_application_test(app_id="1517077510405431296", ord_no="12334444566"))

