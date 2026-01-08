import requests
import hmac
import hashlib
import base64
import time
import config
import log_util
from config import MT_HEADERS, MT_HOST


def _generate_sign(method, path):
    """
    生成签名
    :param method: 请求方法
    :param path: 路径
    :return: 签名与时间戳
    """

    timestamp = int(time.time() * 1000)  # 毫秒时间戳
    data_to_sign = f"{method}&{path}&{timestamp}"

    # 使用 HMAC-SHA1 生成签名
    signature = hmac.new(
        config.MT_SECRET.encode('utf-8'),
        data_to_sign.encode('utf-8'),
        hashlib.sha1
    ).digest()

    # 转换为 Base64 编码
    sign = base64.b64encode(signature).decode('utf-8')

    return {
        '_timestamp': timestamp,
        '_sgin': sign
    }

def _build_form_data(method, path, body=None):
    """
    构建 formdata
    :param method: 请求方法
    :param path:  请求路径
    :param body:  请求体
    :return: formdata
    """
    form_data = {}
    if body:
        form_data.update(body)

    result = _generate_sign(method, path)
    form_data.update(result)

    return form_data

def post(path, data=None, *_args, ignore_status=False, is_json_data=False):
    url = MT_HOST + path
    headers = MT_HEADERS.copy()

    if is_json_data:
        headers['Content-Type'] = 'application/json'
        sign_data = _generate_sign("POST", path)
        full_data = {**(data or {}), **sign_data}
        response = requests.post(url, headers=headers, json=full_data)
    else:
        form_data = _build_form_data("POST", path, data)
        response = requests.post(url, headers=headers, data=form_data)

    if not response.ok and ignore_status == False:
        raise Exception(f"HTTP error! status: 【{response.status_code}】 reason: {response.reason}",response)

    result = response.json()
    if not result.get('code') == '0' and ignore_status == False:
        raise Exception(f"HTTP error! result: {result}")

    if result.get('code') == '0':
        return result.get('data')
    return result