# # -*- coding: utf-8 -*-
# import os
#
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from Apps import app
from Apps.ext import db

manager = Manager(app)

# 使用Migrate(app,db)
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
