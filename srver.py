# -*- coding: utf-8 -*-
from flask import Flask
import serverconfig
import view_users


app = Flask(__name__)


def index():
    return 'Hello World'

index.methods = ['GET']


app.add_url_rule('/register', 'register', view_users.register)
app.add_url_rule('/', 'index', index)

if __name__ == '__main__':
    app.debug = True
    # app.run(host='0.0.0.0')
    app.run(host=serverconfig.HOST, port=serverconfig.PORT)
