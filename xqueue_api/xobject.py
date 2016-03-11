# -*- coding=utf-8 -*-

import json
from utils import deep_update


class XObject(object):
    """
    Пользовательское решение, полученное через метод api get_submission.
    """
    header = None
    submission_key = None

    body = None

    xqueue_files = {}

    def __init__(self, api_response=None):

        if api_response is not None:
            self.init_api_response(json.loads(api_response))

    def init_api_response(self, api_response):

        # xqueue_header
        self.header = json.loads(api_response['xqueue_header'])
        self.submission_key = self.header['submission_key']

        self.body = api_response['xqueue_body']

        # xqueue_files
        self.xqueue_files = json.loads(api_response['xqueue_files'])

    def prepare_put(self):

        xqueue_header = {
            'submission_key': self.submission_key,
        }

        xqueue_body = {
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
        self.lms_key = header['lms_key']
        self.lms_callback_url = header['lms_callback_url']
        self.queue_name = header['queue_name']

        self.body = query_dict.get('xqueue_body')

