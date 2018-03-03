import json
import logging

from functools import partial

from requests import session
from requests.exceptions import ConnectionError, Timeout

from .xobject import XObject
from .xsubmission import XSubmission


logger = logging.getLogger(__name__)


class XQueueException(Exception):
    pass


class XQueueSession(object):

    base_url = None
    authorized = False
    session = None
    timeout = 15
    queue = None

    def __init__(self, base_url=None, username=None, password=None, autoconnect=False, queue=None):
        self.base_url = base_url
        self.session = session()
        self.queue = queue

        if autoconnect:
            self.authorized, _ = self.login(username, password)

    def login(self, username, password):
        logger.info('Авторизация в queue (имя пользователя: {})'.format(username))
        return self._make_request("/login/",
                                  method="POST",
                                  data={"username": username, "password": password})

    def get_len(self, queue=None):

        if queue is None:
            queue = self.queue

        logger.info('Получение длины очереди {}'.format(queue))
        return self._make_request("/get_queuelen/",
                                  data={'queue_name': queue})

    def logout(self):
        logger.info('Выход из системы')
        return self._make_request("/logout/")

    def get_submission(self, queue=None):

        if queue is None:
            queue = self.queue

        logger.info('Получение пользовательского решения в очереди {}'.format(queue))
        return self._make_request("/get_submission/",
                                  data={'queue_name': queue})

    def get_xobject(self, queue=None, target_class=XObject):

        assert issubclass(target_class, XObject)

        result, submission = self.get_submission(queue=queue)
        if result:
            return result, target_class(api_response=submission)
        else:
            return result, submission

    def put_result(self, data):

        logger.info('Отправка результата проверки')
        return self._make_request("/put_result/",
                                  method="POST",
                                  data=data)

    def put_xresult(self, submission):

        assert isinstance(submission, XObject), "submission must be XObject instance"

        self.put_result(data=submission.get_put_string())

    def submit(self, data):

        return self._make_request("/submit/",
                                  method="POST",
                                  data=data)

    def _make_request(self, url, method="GET", data=None):

        request_method = {
            "GET": partial(self.session.get, params=data),
            "POST": partial(self.session.post, data=data),
        }.get(method, None)

        if request_method is None:
            error_message = "Unknown method: %s" % method
            return False, error_message

        request_url = self.base_url + url

        try:
            logger.debug('Отправка запроса: [{}] {}'.format(method, request_url))
            logger.debug(data)
            response = request_method(request_url, timeout=self.timeout)
        except ConnectionError or Timeout:
            error_message = "Connection error to %s" % request_url
            return False, error_message

        if response.status_code not in [200]:
            logger.error('Неверный код ответа сервера: ожидался 200, получен {}'.format(response.status_code))
            error_message = "Server %s returned status_code=%d" % (request_url, response.status_code)
            return False, error_message

        if hasattr(response, "text"):
            text = response.text
        elif hasattr(response, "content"):
            text = response.content
        else:
            error_message = "Could not get response from http object."
            return False, error_message

        logger.debug('Ответ сервера: [{}] {}'.format(response.status_code, text))
        return self._parse_xreply(text)

    @staticmethod
    def _parse_xreply(xreply):
        try:
            xreply = json.loads(xreply)
        except ValueError:
            error_message = "Failed to parse xreply"
            return False, error_message

        if "return_code" in xreply:
            return_code = (xreply["return_code"] == 0)
            content = xreply["content"]
        elif "success" in xreply:
            return_code = xreply["success"]
            content = xreply
        else:
            error_message = "Cannot find a valid success or return code."
            return False, error_message

        if return_code not in [True, False]:
            error_message = "Invalid return code."
            return False, error_message

        return return_code, content
