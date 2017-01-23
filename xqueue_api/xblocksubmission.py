# -*- coding=utf-8 -*-

import json

from .xsubmission import XSubmission, XSubmissionResult


class XBlockSubmission(XSubmission):
    """
    Пользовательское решение, полученное через метод api get_submission.
    """

    # Данные, полученные от xqueue
    sender = None

    def init_api_response(self, api_response):

        parent = super(XBlockSubmission, self)
        if hasattr(parent, 'init_api_response'):
            parent.init_api_response(api_response=api_response)

        # xqueue_body
        body = json.loads(self.body)
        self.sender = body.get('submission_sender')


class XBlockSubmissionResult(XSubmissionResult):

    pass
