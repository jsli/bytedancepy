#!/usr/bin/env python
# encoding: utf-8

from bytedancepy.client import ByteDanceClient

from bytedancepy.session.redisstorage import RedisStorage
from redis import Redis

class ByteDance(object):

    def __init__(self, app=None):

        self._bytedance_client = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        config = app.config
        config.setdefault('BYTEDANCE_APPID', None)
        config.setdefault('BYTEDANCE_SECRET', None)
        config.setdefault('BYTEDANCE_TYPE', 0)
        config.setdefault('BYTEDANCE_SESSION_TYPE', 'redis')
        config.setdefault('BYTEDANCE_SESSION_PREFIX', 'flask-bytedancepy')
        config.setdefault('BYTEDANCE_AUTO_RETRY', True)
        config.setdefault('BYTEDANCE_TIMEOUT', None)

        assert config['BYTEDANCE_APPID'] is not None
        assert config['BYTEDANCE_SECRET'] is not None
        assert config['BYTEDANCE_SESSION_REDIS_URL'] is not None

        if config.get('BYTEDANCE_SESSION_REDIS_URL'):
            redis = Redis.from_url(config['BYTEDANCE_SESSION_REDIS_URL'])
        else:
            redis = Redis(
                host=config.get('BYTEDANCE_SESSION_REDIS_HOST', 'localhost'),
                port=config.get('BYTEDANCE_SESSION_REDIS_PORT', 6379),
                db=config.get('BYTEDANCE_SESSION_REDIS_DB', 0),
                password=config.get('BYTEDANCE_SESSION_REDIS_PASS', None)
            )
        session_interface = RedisStorage(redis, prefix=config['BYTEDANCE_SESSION_PREFIX'])

        self._bytedance_client = ByteDanceClient(
            config['BYTEDANCE_APPID'],
            config['BYTEDANCE_SECRET'],
            session=session_interface,
            timeout=config['BYTEDANCE_TIMEOUT'],
            auto_retry=config['BYTEDANCE_AUTO_RETRY'],
        )

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['bytedancepy'] = self

    def __getattr__(self, name):
        return getattr(self._bytedance_client, name)
