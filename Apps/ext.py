# This Python file uses the following encoding: utf-8
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_wtf import CSRFProtect
from flask_caching import Cache

db = SQLAlchemy()

migrate = Migrate()

bootstrap = Bootstrap()

toolbar = DebugToolbarExtension()

auth_token = HTTPTokenAuth()
auth_cms = HTTPBasicAuth()
auth_pa = HTTPBasicAuth()

cache = Cache(
    config={
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_PASSWORD": ""
    }
)


# csrf = CSRFProtect()


def ext_init(app):
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    bootstrap.init_app(app=app)
    # toolbar.init_app(app=app)
    cache.init_app(app=app)
    # csrf.init_app(app=app)