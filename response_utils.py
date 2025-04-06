from typing import Any, Dict, Union
from flask import jsonify

def make_response(data: Any = None, message: str = "Success", code: int = 200) -> Dict:
    """
    统一的成功响应格式
    :param data: 响应数据
    :param message: 响应消息
    :param code: 响应状态码
    :return: 统一格式的响应字典
    """
    response = {
        "code": code,
        "message": message,
        "data": data
    }
    return jsonify(response)

def make_error_response(message: str = "Error", code: int = 400) -> Dict:
    """
    统一的错误响应格式
    :param message: 错误消息
    :param code: 错误状态码
    :return: 统一格式的错误响应字典
    """
    response = {
        "code": code,
        "message": message,
        "data": None
    }
    return jsonify(response)