import tornado.web
import tornado.ioloop
import time
import tornado


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    @tornado.gen.coroutine
    def get(self):
        """对应http的get请求方式"""
        loop = tornado.ioloop.IOLoop.instance()
        yield loop.run_in_executor(None, self.sleep)
        self.write("Hello You!")

    def sleep(self):
        time.sleep(5)
        self.write('sleep OK')


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()