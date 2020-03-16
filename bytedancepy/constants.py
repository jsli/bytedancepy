# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from enum import IntEnum, unique


@unique
class ByteDanceErrorCode(IntEnum):
    """
    字节跳动接口返回码，返回码请参考 https://microapp.bytedance.com/dev/cn/mini-app/develop/server/server-api-introduction
    """

    # 系统错误
    SYSTEM_ERROR = -1

    # 请求成功
    SUCCESS = 0

    # http 包体无法解析  40001
    INVALID_HTTP_BODY = 40001

    # access_token 错误 40002
    INVALID_ACCESS_TOKEN = 40002

    # key 长度大于 128 个字节
    OUT_OF_KEY_SIZE_LIMIT = 40009

    # key 和 value 的长度和大于 1024 个字节  40010
    OUT_OF_KEY_VALUE_SIZE_LIMIT = 40010

    # 排行榜 key 对应的 value 值格式不对，具体见 warning
    INVALID_KEY_VALUE = 40011

    # 参数无效  40014
    INVALID_PARAMETER = 40014

    # 错误的 AppID
    INVALID_APP_ID = 40015

    # appname 错误  40016
    INVALID_APP_NAME = 40016

    # secret 错误
    INVALID_CREDENTIAL = 40017

    # code 错误
    INVALID_CODE = 40018

    # acode 错误
    INVALID_ACODE = 40019

    # grant_type 不是 client_credential
    INVALID_CREDENTIAL_TYPE = 40020

    # width 超过指定范围
    OUT_OF_WITH_LIMIT = 40021

    # 错误的模版 id  40037
    INVALID_TEMPLATE_ID = 40037

    # 小程序被禁止发送消息通知
    UNAUTHORIZED_SEND_TEMPLATE = 40038

    # form_id 不正确，或者过期
    INVALID_FORM_ID = 40039

    # form_id 已经被使用
    EXPIRED_FORM_ID = 40040

    # 错误的页面地址
    INVALID_PAGE_URL = 40041

    # 单用户存储 kv 超过 128 对
    OUT_OF_KEY_VALUE_PAIR_LIMIT = 60001

    # 频率限制（目前 5000 次/分钟）
    OUT_OF_FREQ_LIMIT = 60003
