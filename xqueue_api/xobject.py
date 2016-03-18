# -*- coding=utf-8 -*-

import json

from .utils import deep_update


class XObject(object):
    """
    Пользовательское решение, полученное через метод api get_submission.
    """
    api_response = None
    header = None
    submission_id = None
    submission_key = None

    body = None

    xqueue_files = {}

    feedback = ''

    def __init__(self, api_response=None, xobject=None):

        if api_response is not None:
            self.init_api_response(json.loads(api_response))

        if xobject is not None:
            self.init_xobject(xobject)

    def init_api_response(self, api_response):

        self.api_response = api_response

        # xqueue_header
        self.header = json.loads(api_response['xqueue_header'])
        self.submission_id = self.header['submission_id']
        self.submission_key = self.header['submission_key']

        self.body = api_response['xqueue_body']

        # xqueue_files
        self.xqueue_files = json.loads(api_response['xqueue_files'])

    def init_xobject(self, xobject):

        assert isinstance(xobject, XObject)

        self.init_api_response(api_response=xobject.api_response)

    @classmethod
    def create_from_xobject(cls, xobject):
        new = cls(xobject=xobject)
        return new

    def prepare_put(self):

        result = {}

        xqueue_header = {
            'submission_id': self.submission_id,
            'submission_key': self.submission_key,
        }

        xqueue_body = {
            'feedback': self.feedback,
        }

        return deep_update(result, {
            'xqueue_header': xqueue_header,
            'xqueue_body': xqueue_body,
        })

    def get_put_string(self):

        result = self.prepare_put()

        return {
            'xqueue_header': json.dumps(result['xqueue_header']),
            'xqueue_body': json.dumps(result['xqueue_body']),
        }


class XObjectResult(object):

    header = None
    lms_key = None
    lms_callback_url = None
    queue_name = None

    body = None

    def __init__(self, query_dict=None):

        if query_dict is not None:
            self.init_query_dict(query_dict)

    def init_query_dict(self, query_dict):

        self.header = json.loads(query_dict.get('xqueue_header'))
        self.lms_key = self.header['lms_key']
        self.lms_callback_url = self.header['lms_callback_url']
        self.queue_name = self.header['queue_name']

        self.body = query_dict.get('xqueue_body')

