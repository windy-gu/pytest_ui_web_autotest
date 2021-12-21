# author:windy
# datetime:2021/10/21 5:09 下午
# software: PyCharm

import json
import time
import hashlib
import base64
import requests
from util.log import Log
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
from Crypto.Hash import SHA


log = Log()

app_default_headers = {
                    "termtyp": "ANDROID",
                    "channel": "Portal",
                    "projectname": "SuperApp",
                    "appid": "SuperApp",
                    "appno": "10",
                    "appversion": "2.19.0",
                    "phonemodel": "python-api-test",
                    "deviceId": "python_api_test",
                    "signver": "1.0",
                    }
web_default_headers = {}


def headers():

    pass


def body():
    pass


def get():
    pass


def rsa_sign_by_private_key(encryptData, private_key):
    """
    通过RSA私钥加签
    :param encryptData:
    :param private_key:
    :return:
    """
    privateKey = '-----BEGIN RSA PRIVATE KEY-----\n' + private_key + '\n-----END RSA PRIVATE KEY-----'
    print("privateKey:" + privateKey)
    private_keyBytes = base64.b64decode(private_key)
    priKey = RSA.importKey(private_keyBytes)
    signer = Signature_pkcs1_v1_5.new(priKey)
    data = SHA.new(encryptData.encode('utf-8'))
    signature = signer.sign(data)
    signature = base64.b64encode(signature)
    return signature.decode()


def rsa_verify_by_public_key(encryptData, public_key):
    """
    通过RSA公钥验签
    :param encryptData:
    :param public_key:
    :return:
    """
    # 若输入的

    public_keyBytes = base64.b64decode(public_key)
    priKey = RSA.importKey(public_keyBytes)
    signer = Signature_pkcs1_v1_5.new(priKey)
    data = MD5.new(encryptData.encode('utf-8'))
    signature = signer.sign(data)
    signature = base64.b64encode(signature)
    return signature.decode()


def encrypt_by_public_key(plaintext, public_key):
    """
    通过RSA公钥加密
    :param plaintext:  明文
    :param public_key: RSA公钥

    :return:           密文
    """
    publicKey = '-----BEGIN RSA PUBLIC KEY-----\n' + public_key + '\n-----END RSA PUBLIC KEY-----'
    rsakey = RSA.importKey(publicKey)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    ciphertext = base64.b64encode(cipher.encrypt(plaintext.encode(encoding='UTF-8')))
    return ciphertext.decode('utf8')


def decrypt_by_private_key(ciphertext, private_key):
    """
    通过RSA私钥解密
    :param ciphertext:  密文
    :param private_key: RSA私钥

    :return:            明文
    """
    privateKey = '-----BEGIN RSA PRIVATE KEY-----\n' + private_key + '\n-----END RSA PRIVATE KEY-----'
    rsakey = RSA.importKey(privateKey)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    plaintext = cipher.decrypt(base64.b64decode(ciphertext), None)
    return plaintext.decode('utf8')


def app_api_post(api_url: str, api_body: json, header: dict):
    """
    app中请求post接口方法
    :param api_url:   请求接口url地址，格式str
    :param api_body:  请求body参数，格式json
    :param header:    请求header参数，格式dict
    :return:          返回响应数据，格式str
    """
    temp_header = check_add_header_keys(header)
    checked_body, checked_header = check_body_header_keys(body_dict=api_body, header_dict=temp_header)
    checked_header['sign'] = api_sign(checked_body)
    if 'requestTm' in api_body and 'deviceId' in api_body:
        del checked_body['requestTm']  # 删除因sign加签导致添加到body中对应的key值
        del checked_body['deviceId']  # 删除因sign加签导致添加到body中对应的key值

    r = requests.post(url=api_url, data=json.dumps(api_body), headers=header, timeout=10)
    text = r.text
    return text


def check_add_header_keys(header_dict: dict):
    """

    :param header_dict:
    :return:
    """
    if 'requestTm' not in header_dict:
        header_dict['requestTm'] = timestamp_ms()
    if 'deviceId' not in header_dict:
        header_dict['deviceId'] = 'python_api_test'

    return header_dict


def check_body_header_keys(body_dict: dict, header_dict: dict):
    """

    :param body_dict:
    :param header_dict:
    :return:
    """
    if 'requestTm' not in body_dict and 'deviceId' not in body_dict:
        if 'requestTm' in header_dict:
            body_dict['requestTm'] = header_dict['requestTm']
        else:
            body_dict['requestTm'] = timestamp_ms()
            header_dict['requestTm'] = timestamp_ms()
        if 'deviceId' in header_dict:
            body_dict['deviceId'] = header_dict['deviceId']
        else:
            body_dict['deviceId'] = "python_api_test"
            header_dict['deviceId'] = "python_api_test"

    elif 'requestTm' in body_dict and 'deviceId' not in body_dict:
        if 'deviceId' in header_dict:
            body_dict['deviceId'] = header_dict['deviceId']
        else:
            body_dict['deviceId'] = "python_api_test"
            header_dict['deviceId'] = "python_api_test"

    elif 'requestTm' not in body_dict and 'deviceId' in body_dict:
        if 'requestTm' in header_dict:
            body_dict['requestTm'] = header_dict['requestTm']
        else:
            body_dict['requestTm'] = timestamp_ms()
            header_dict['requestTm'] = timestamp_ms()

    return body_dict, header_dict


def timestamp_ms():
    """
    返回时间戳(ms)
    :return:  时间戳(ms)，格式：str
    """
    return str(round(time.time()*1000))


def md5(need_sign_data: str):
    """
    进行md5加密
    :param need_sign_data:
    :return:
    """
    m = hashlib.md5()
    m.update(need_sign_data.encode("utf8"))
    encode_data = m.hexdigest()
    log.info('加密前内容：{}'.format(need_sign_data))
    log.info('md5加密后：{}'.format(encode_data))
    return encode_data


def api_sign(un_sign_data: dict):
    """

    :param un_sign_data:
    :return:
    """
    un_sign_data_by_sort = dict_sort(un_sign_data)  # 将body入参进行json序列化
    need_sign_data = exchange_encryption_data(un_sign_data_by_sort)  # 根据后端将原本json序列转换成后端加密所需要的序列
    return md5(need_sign_data)


def dict_sort(dict_data: dict):
    """
    此方法主要用于进行api请求body参数，按照a~z顺序进行排序
    :param dict_data: 需要进行排序的字典数据
    :return:
    """
    return json.dumps(dict_data, sort_keys=True)


def exchange_encryption_data(untreated_data: str):
    """
    此方法仅适用于根据后端的加签规格，将对应json文件进行对应的文件替换后，进行输出
    :param untreated_data:
    :return:
    """
    temp_data = untreated_data[1:-1]  # 去除首位的 { }

    # replace('"', '') 去除str中 "
    # replace(' ', '') 将多余的空格去除
    # replace(':', '=')
    # replace('},{', 'temp_placeholder')
    # replace(',', '&')
    # replace('temp_placeholder', '},{')
    data = temp_data.replace('"', '')\
                    .replace(' ', '') \
                    .replace('://', 'temp_place')\
                    .replace(':', '=')\
                    .replace('temp_place', '://')\
                    .replace('},{', 'temp_placeholder')\
                    .replace(',', '&')\
                    .replace('temp_placeholder', '},{')
    return data


if __name__ == '__main__':

    a = [1, 2, 3]
    b = [1, 2, 4]
    print(id(a[1]) == id(b[1]))

    api_url = 'https://appgateway-uat.lifekh.com/gateway_web/operator/login/password.do'
    body_dict = {"app_id": "1624010948354", "biz_content": {"couponNo": "WNJ210908154513449", "mobile": "855010145005"}, "charset": "UTF-8", "service": "send.choice.coupon", "timestamp": "2020-09-07 16:07:50", "version": "1.0"}

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
    # print(app_api_post(api_url, body_dict, headers))
    out = ''
    for k, v in body_dict.items():
        print(type(k))
        print(v)
        out += str(k) + '=' + str(v) + '&'
    out = out[0:-1]

    print(out)


