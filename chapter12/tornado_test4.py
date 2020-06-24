from flask import Flask
import time
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


app = Flask(__name__)


@app.route('/')
def index():
    time.sleep(10)
    return 'OK'


import tornado
from tornado import escape
from tornado import httputil
from typing import List, Tuple, Optional, Callable, Any, Dict
from types import TracebackType


class WSGIContainer_with_Thread(WSGIContainer):
    @tornado.gen.coroutine
    def __call__(self, request):
        data = {}  # type: Dict[str, Any]
        response = []  # type: List[bytes]

        def start_response(
                status: str,
                headers: List[Tuple[str, str]],
                exc_info: Optional[
                    Tuple[
                        "Optional[Type[BaseException]]",
                        Optional[BaseException],
                        Optional[TracebackType],
                    ]
                ] = None,
        ) -> Callable[[bytes], Any]:
            data["status"] = status
            data["headers"] = headers
            return response.append

        loop = tornado.ioloop.IOLoop.instance()
        app_response = yield loop.run_in_executor(None, self.wsgi_application, WSGIContainer.environ(request),
                                                  start_response)

        try:
            response.extend(app_response)
            body = b"".join(response)
        finally:
            if hasattr(app_response, "close"):
                app_response.close()
        if not data:
            raise Exception("WSGI app did not call start_response")

        status_code_str, reason = data["status"].split(" ", 1)
        status_code = int(status_code_str)
        headers = data["headers"]  # type: List[Tuple[str, str]]
        header_set = set(k.lower() for (k, v) in headers)
        body = escape.utf8(body)
        if status_code != 304:
            if "content-length" not in header_set:
                headers.append(("Content-Length", str(len(body))))
            if "content-type" not in header_set:
                headers.append(("Content-Type", "text/html; charset=UTF-8"))
        if "server" not in header_set:
            headers.append(("Server", "TornadoServer/%s" % tornado.version))

        start_line = httputil.ResponseStartLine("HTTP/1.1", status_code, reason)
        header_obj = httputil.HTTPHeaders()
        for key, value in headers:
            header_obj.add(key, value)
        assert request.connection is not None
        request.connection.write_headers(start_line, header_obj, chunk=body)
        request.connection.finish()
        self._log(status_code, request)


if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer_with_Thread(app))
    http_server.listen(5000)
    IOLoop.instance().start()