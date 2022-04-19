#!/usr/bin/env python3

import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.process

import aioredis

template = """\
<!DOCTYPE html>
<html>
<head>
<body>

</body>
</html>
"""


class MainHandler(tornado.web.RequestHandler):

    def initialize(self, redis):
        self.redis = redis

    def get(self):
        self.write(template)

    def post(self, request):
        response = "foo"
        self.write(response)


def main():
    redis = aioredis.from_url(f"redis://{os.environ['ADDRESS_CACHE']}")
    app = tornado.web.Application([(r"/", MainHandler, {"redis": redis})])
    server = tornado.httpserver.HTTPServer(app)
    server.bind(os.environ["TORNADO_PORT"])
    #server.start(os.environ["TORNADO_SERVER_COUNT"])  # N instances are forked
    server.start()
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
