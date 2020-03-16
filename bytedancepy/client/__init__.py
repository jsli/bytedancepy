# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from bytedancepy.client import api
from bytedancepy.client.base import BaseByteDanceClient


class ByteDanceClient(BaseByteDanceClient):

    """
    字节跳动 API 操作类
    通过这个类可以操作字节跳动 API
    """

    API_BASE_URL = 'https://developer.toutiao.com/api/apps/'

    wxa = api.MicroApp()

    def __init__(self, appid, secret, access_token=None,
                 session=None, timeout=None, auto_retry=True):
        super(ByteDanceClient, self).__init__(
            appid, access_token, session, timeout, auto_retry
        )
        self.appid = appid
        self.secret = secret

    def fetch_access_token(self):
        """
        access_token 是小程序的全局唯一调用凭据，开发者调用小程序支付时需要使用 access_token。access_token 的有效期为 2 个小时，需要定时刷新 access_token，重复获取会导致之前一次获取的 access_token 的有效期缩短为 5 分钟。
        详情请参考
        https://microapp.bytedance.com/dev/cn/mini-app/develop/server/interface-request-credential/getaccesstoken
        :return: 返回的 JSON 数据包
        """
        return self._fetch_access_token(
            url='https://developer.toutiao.com/api/apps/token',
            params={
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.secret
            }
        )
