from requests import request


class XQueueRequest(object):

    result_code = None
    data = None
    xobject = None

    def __init__(self, init_request=None, content=None):

        if isinstance(content, basestring):
            self._init_str(content)

    def _init_str(self, content):
        pass

    def has_xobject(self):
        return self.xobject is not None


