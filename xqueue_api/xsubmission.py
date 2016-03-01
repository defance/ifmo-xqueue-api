# -*- coding=utf-8 -*-

import json


class XSubmission(object):
    """
    Пользовательское решение, полученное через метод api get_submission.
    """

    def __init__(self, api_response=None):

        # Данные, полученные от xqueue
        self.xqueue_files = {}
        self.submission_id = None
        self.submission_key = None
        self.grader_payload = None
        self.student_info = {}
        self.student_response = None

        # Данные, записываемые при оценивании
        self.is_graded = False
        self.grade = 0
        self.feedback = None
        self.grader = None
        self.correctness = False

        if api_response is not None:
            self._init_api_response(api_response)

    def _init_api_response(self, api_response):

        # Десериализация
        api_response = json.loads(api_response)

        # xqueue_files
        self.xqueue_files = json.loads(api_response['xqueue_files'])

        # xqueue_header
        header = json.loads(api_response['xqueue_header'])
        self.submission_id = header['submission_id']
        self.submission_key = header['submission_key']

        # xqueue_body
        body = json.loads(api_response['xqueue_body'])
        self.grader_payload = body['grader_payload']
        self.student_info = json.loads(body['student_info'])
        self.student_response = body['student_response']

    def set_grade(self, grade, feedback=None, grader=None, correctness=False):
        self.is_graded = True
        self.grade = grade
        self.feedback = feedback
        self.grader = grader
        self.correctness = correctness

    def get_put_string(self):
        assert self.is_graded, "Submission must be graded first"

        xqueue_header = {
            'submission_id': self.submission_id,
            'submission_key': self.submission_key,
        }

        xqueue_body = {
            'msg': self.feedback,
            'correct': self.correct,
            'score': self.grade,
            'grader_id': self.grader_id,
        }

        return {
            'xqueue_header': json.dumps(xqueue_header),
            'xqueue_body': json.dumps(xqueue_body),
        }
