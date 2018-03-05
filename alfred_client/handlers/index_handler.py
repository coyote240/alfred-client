import tornado.web


class IndexHandler(tornado.web.RequestHandler):

    def head(self):
        self.finish()
