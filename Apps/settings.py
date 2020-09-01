# This Python file uses the following encoding: utf-8
import os

import redis

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")

# slow database query threshold (in seconds)
# DATABASE_QUERY_TIMEOUT = 0.5
# SQLALCHEMY_RECORD_QUERIES = True
EXPIRATION = 36000


def get_db_uri(dbinfo):
    ENGINE = dbinfo.get("ENGINE") or "mysql"
    DRIVER = dbinfo.get("DRIVER") or "pymysql"
    USER = dbinfo.get("USER") or "root"
    PASSWORD = dbinfo.get("PASSWORD") or "root"
    HOST = dbinfo.get("HOST") or "localhost"
    PORT = dbinfo.get("PORT") or "3306"
    NAME = dbinfo.get("NAME") or "test"
    return "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(ENGINE, DRIVER, USER, PASSWORD, HOST, PORT, NAME)


class Config:
    DEBUG = True

    TESTING = False

    SECRET_KEY = os.urandom(24)

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    PER_PAGE = 20

    CMS_USER_ID = "fgdgggr"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/test?charset=utf8'
    # SESSION_TYPE = "redis"
    #
    # SESSION_REDIS = redis.Redis(password='12345')


class DevelopConfig(Config):
    DEBUG = True

    DATABASE = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "test"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


class TestingConfig(Config):
    TESTING = True

    DATABASE = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "wtw",
        "PASSWORD": "88888888",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "NAME": "pa_test"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


class StagingConfig(Config):
    DEBUG = True
    DATABASE = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "wtw",
        "PASSWORD": "88888888",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        # "NAME": "pa_staging"
        "NAME": "animal_test"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


class ProductConfig(Config):
    DATABASE = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "wtw",
        "PASSWORD": "88888888",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "NAME": "pa_product"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


envs = {
    "develop": DevelopConfig,
    "default": Config,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "product": ProductConfig
}

ADMINS = ("pa_admin", "pa_admin1")
FILEPATH_PREFIX = "/static/uploads/layers"

UPLOAD_DIR = os.path.join(BASE_DIR, 'static/uploads/layers')
