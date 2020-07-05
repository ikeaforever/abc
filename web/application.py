from . import webapi as web
from . import utils


class Application(object):
    """
    Application to delegate requests based on path.

        >>> urls = ("/hello", "hello")
        >>> app = Application(urls, globals())
        >>> class hello:
        ...     def GET(self): return "hello"
        >>>
        >>> app.request("/hello").data
        'hello'
    """

    def _cleanup(self):
        utils.ThreadedDict.clear_all()

    def __init__(self, mappings=(), fvars={}, autoreload=None):
        """
        :param mappings: urls
        :param fvars:
        :param autoreload:
        """
        if autoreload is None:
            autoreload = web.config.get("debug", False)

        self.init_mapping(mappings)
        self.fvars = fvars
        self.processors = []

    def init_mapping(self, mapping):
        self.mapping = list(utils.group(mapping, 2))

    def load(self, env):
        ctx = web.ctx
        ctx.clear()
        ctx.status = "200 OK"
        ctx.headers = []



    def add_processor(self, processor):
        """
        Adds a processor to the application.

            >>> urls = ("/(.*)", "echo")
            >>> app = application(urls, globals())
            >>> class echo:
            ...     def GET(self, name): return name
            ...
            >>>
            >>> def hello(handler): return "hello, " +  handler()
            ...
            >>> app.add_processor(hello)
            >>> app.request("/web.py").data
            'hello, web.py'
        """
        # PY3DOCTEST: b'hello, web.py'
        self.processors.append(processor)

    def wsgifun(self, *middleware):
        """
        Returns a WSGI-compatible function for this application.

        :param middleware: 中间件，对全部的wsgi函数进行封装
        :return:
        """

        def peep(iterator):
            pass

        def wsgi(env, start_response):
            self._cleanup()


        for m in middleware:
            wsgi = m(wsgi)

        return wsgi