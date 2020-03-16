# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import hmac
import json

from bytedancepy.client.api.base import BaseByteDanceAPI
from bytedancepy.exceptions import InvalidSignatureSessionKeyException


class MicroApp(BaseByteDanceAPI):

    API_BASE_URL = 'https://developer.toutiao.com/api/apps/'

    # def get_access_token(self):
    #     """
    #     access_token 是小程序的全局唯一调用凭据，开发者调用小程序支付时需要使用 access_token。access_token 的有效期为 2 个小时，需要定时刷新 access_token，重复获取会导致之前一次获取的 access_token 的有效期缩短为 5 分钟。
    #     详情请参考
    #     https://microapp.bytedance.com/dev/cn/mini-app/develop/server/interface-request-credential/getaccesstoken
    #     """
    #     return self._post(
    #         'token',
    #         params = {
    #             'grant_type': 'client_credential',
    #             'appid': self.appid,
    #             'secret': self.secret
    #         }
    #     )

    def code_to_session(self, code, anonymous_code=None):
        """
        通过login接口获取到登录凭证后，开发者可以通过服务器发送请求的方式获取session_key和openId。
        详情请参考
        https://microapp.bytedance.com/dev/cn/mini-app/develop/server/log-in/code2session

        :param code:
        :param anonymous_code:
        :return:
        """
        res = self._get(
            'jscode2session',
            params={
                'appid': self.appid,
                'secret': self.secret,
                'code': code,
                'anonymous_code': anonymous_code
            }
        )

        session_key = res['session_key']
        openid = res['openid']
        anonymous_openid = res.get('anonymous_openid', None)

        self.session.set(
            self._get_user_session_key(openid),
            session_key,
            60
        )
        self.session.persist(
            self._get_user_session_key(openid)
        )

        if anonymous_openid:
            self.session.set(
                self._get_user_session_key(anonymous_openid),
                session_key,
                60
            )
            self.session.persist(
                self._get_user_session_key(anonymous_openid)
            )

        return res

    def set_user_storage(self, openid, key, value):
        """
        以 key-value 形式上报用户数据到字节跳动的云存储服务。
        详情请参考
        https://microapp.bytedance.com/dev/cn/mini-app/develop/server/data-caching/setuserstorage

        :param openid:
        :param key:
        :param value:
        :return:
        """
        return self._post(
            'set_user_storage?openid=%s&signature=%s&sig_method=hmac_sha256' % (openid, self._get_user_signature(openid)),
            data = {
                'kv_list': [
                    {key: value}
                ]
            }
        )

    def remove_user_storage(self, openid, key):
        """
        删除上报到字节跳动的云存储服务的 key-value 数据。
        详情请参考
        https://microapp.bytedance.com/dev/cn/mini-app/develop/server/data-caching/removeuserstorage

        :param openid:
        :param key:
        :param value:
        :return:
        """
        return self._post(
            'remove_user_storage?openid=%s&signature=%s&sig_method=hmac_sha256' % (openid, self._get_user_signature(openid)),
            data={
                'kv_list': [
                    key
                ]
            }
        )

    # TODO:
    def create_qr_code(self, appname='duoyin', path=None, width='430', line_color='{"r":0,"g":0,"b":0}', background=None, set_icon='FALSE'):
        """
        获取小程序/小游戏的二维码。该二维码可通过任意 app 扫码打开，能跳转到开发者指定的对应字节系 app 内拉起小程序/小游戏， 并传入开发者指定的参数。通过该接口生成的二维码，永久有效，暂无数量限制。
        详情请参考
        https://microapp.bytedance.com/dev/cn/mini-app/develop/server/qr-code/createqrcode

        :param appname:
        :param path: path
        :param width: width
        :param line_color:
        :param background:
        :param set_icon:
        :return:
        """
        return self._post(
            'qrcode',
            data={
                'access_token': self.access_token,
                'appname': appname,
                'width': width,
                'line_color': line_color,
                'path': path,
                'background': background,
                'set_icon': set_icon
            }
        )

    def send_template(self, touser, template_id, form_id, data, page=None):
        """
        获取小程序/小游戏的二维码。该二维码可通过任意 app 扫码打开，能跳转到开发者指定的对应字节系 app 内拉起小程序/小游戏， 并传入开发者指定的参数。通过该接口生成的二维码，永久有效，暂无数量限制。
        详情请参考
        https://microapp.bytedance.com/dev/cn/mini-app/develop/server/qr-code/createqrcode

        :param touser:
        :param template_id:
        :param data:
        :param page:
        :param form_id
        :return:
        """
        return self._post(
            'game/template/send',
            data={
                'access_token': self.access_token,
                'touser': touser,
                'template_id': template_id,
                'form_id': form_id,
                'page': page,
                'data': data,
            }
        )

    def _get_user_signature(self, openid, body):
        """
        获取 JSAPI 签名

        :param openid:
        :param body:
        :return: 签名
        """
        session_key = self.session.get('bytedance:session_key:{openid}'.format(openid=openid), None)
        if not session_key:
            raise InvalidSignatureSessionKeyException

        signature = hmac.new(session_key).update(json.dumps(body, sort_keys=True)).hexdigest()
        return signature

    @classmethod
    def _get_user_session_key(cls, openid):
        return 'bytedance:session_key:{openid}'.format(openid=openid)
