#!/usr/bin/env python3

import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.process

# apparently modern redis-py now bundles aioredis (wow!)
# from redis.asyncio import Redis
from redis import asyncio as aioredis  # FIXME as instructed, but uses builtin name? yuck

TEMPLATE = """\
<!DOCTYPE html>
<html>
<head>
<body>
    <div>
        <img src="data:image/png;base64, {webcam_view}" alt="webcam_view" />
        <img src="data:image/jpeg;base64, {img_cnt}" alt="webcam_view" />
        <img src="data:image/jpeg;base64, {img_prb}" alt="webcam_view" />
    </div>
</body>
</html>
"""


class MainHandler(tornado.web.RequestHandler):

    def initialize(self, redis_handle):
        self.Q = redis_handle

    async def get(self):
        # FIXME mad ugly
        # FIXME at least .gather these from a list
        webcam_view = await self.Q.get("webcam_view")
        img_cnt = await self.Q.get("img_cnt")
        img_prb = await self.Q.get("img_prb")
        self.write(TEMPLATE.format(
            webcam_view=webcam_view.decode(),
            img_cnt=img_cnt.decode(),
            img_prb=img_prb.decode(),
        ))  # is it ok to let these be utf-8 autodecoded?

    def post(self, request):
        response = "foo"
        self.write(response)

    # https://stackoverflow.com/a/33000023/
    # ws_client.write_message({
    #     "img": base64.b64encode(img_data),
    #     "desc": img_description,
    # })


def main():
    app = tornado.web.Application([(
        r"/",
        MainHandler,
        {
            "redis_handle": aioredis.from_url(f"redis://{os.environ['ADDRESS_CACHE']}"),
        }
    )])
    server = tornado.httpserver.HTTPServer(app)
    # server.bind(os.environ["TORNADO_PORT"])
    server.bind(8888)  # FIXME this is the default - is it required?
    #server.start(os.environ["TORNADO_SERVER_COUNT"])  # N instances are forked
    server.start()
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
