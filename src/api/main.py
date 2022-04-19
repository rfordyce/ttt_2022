#!/usr/bin/env python3

import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.process


template = """\
<!DOCTYPE html>
<html>
<head>
<body>

</body>
</html>
"""


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(template)

    def post(self, request):
        response = "foo"
        self.write(response)


if __name__ == '__main__':
    print("starting webserver")
    app = tornado.web.Application([(r"/", MainHandler)])
    server = tornado.httpserver.HTTPServer(app)
    server.bind(os.environ["TORNADO_PORT"])
    server.start(os.environ["TORNADO_SERVER_COUNT"])  # N instances are forked
    tornado.ioloop.IOLoop.current().start()
