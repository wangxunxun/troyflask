# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'beyondsoftbugzilla@163.com'
    MAIL_PASSWORD = 'wangxun2'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <beyondsoftbugzilla@163.com>'
    FLASKY_ADMIN = '59853844@qq.com'
    FLASKY_POSTS_PER_PAGE = 20
    host = "10.27.0.122"
    port = 5000
    API_SESSION_TIME_OUT = 60*60*24*7
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
#    SQLALCHEMY_DATABASE_URI= 'mysql://test:test@69.164.202.55/test'
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'data.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI= 'mysql://test:test@69.164.202.55/test'
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'data.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI= 'mysql://test:test@69.164.202.55/test'
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}