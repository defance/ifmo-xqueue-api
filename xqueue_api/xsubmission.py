# -*- coding=utf-8 -*-

import json
from utils import deep_update
from xobject import XObjectResult, XObject


class XSubmission(XObject):
    """
    Пользовательское решение, полученное через метод api get_submission.
    """

    # Данные, полученные от xqueue
    submission_id = None
    grader_payload = None
    student_info = {}
    student_response = None

    # Данные, записываемые при оценивании
    is_graded = False
    grade = 0
    feedback = None
    correctness = False
    grader_id = None

    def init_api_response(self, api_response):

        parent = super(XSubmission, self)
        if hasattr(parent, 'init_api_response'):
            parent.init_api_response(api_response=api_response)

        self.submission_id = header['submission_id']

        # xqueue_body
        body = json.loads(self.body)
        self.grader_payload = body['grader_payload']
        self.student_info = json.loads(body['student_info'])
        self.student_response = body['student_response']

    def set_grade(self, grade, feedback=None, grader=None, correctness=False):
        self.is_graded = True
        self.grade = grade
        self.feedback = feedback
        self.grader_id = grader
        self.correctness = correctness

    def prepare_put(self):

        assert self.is_graded, "XSubmission should be graded first"

        parent = super(XSubmission, self)
        result = {}
        if hasattr(parent, 'prepare_put'):
            result = parent.prepare_put()

        xqueue_header = {
            'submission_id': self.submission_id,
        }

        xqueue_body = {
            'msg': self.feedback,
            'correct': self.correctness,
            'score': self.grade,
            'grader_id': self.grader_id,
        }

        return deep_update(result, {
            'xqueue_header': xqueue_header,
            'xqueue_body': xqueue_body,
        })


class XSubmissionResult(XObjectResult):

    msg = None
    score = None
    correct = None
    grader_id = None

    def init_query_dict(self, query_dict):

        parent = super(XSubmissionResult, self)
        if hasattr(parent, 'init_query_dict'):
            parent.init_query_dict()

        body = json.loads(self.body)
        self.msg = body['msg']
        self.score = body['score']
        self.correct = body['correct']
        self.grader_id = body['grader_id']

