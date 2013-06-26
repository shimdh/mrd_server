# -*- coding: utf-8 -*-

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from mrd_srv import app

http_server = HTTPServer(WSGIContainer(app))
# http_server.bind(5000)
# http_server.start(0)
http_server.listen(5000)
IOLoop.instance().start()
