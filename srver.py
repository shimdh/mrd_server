# -*- coding: utf-8 -*-
from gevent.wsgi import WSGIServer
from mrd_srv import app

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
