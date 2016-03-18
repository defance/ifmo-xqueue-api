import json
import hashlib
import pytz
import collections

from datetime import datetime


dateformat = '%Y%m%d%H%M%S'


def create_submission(header=None, body=None):
    return {
        "xqueue_header": header,
        "xqueue_body": body,
    }


def create_submission_header(lms_callback=None, lms_key=None, queue_name=None):
    return json.dumps({
            "lms_callback": lms_callback,
            "lms_key": lms_key,
            "queue_name": queue_name,
        })


def create_student_info(anonymous_student_id=None, submission_time=None):
    return json.dumps({
        "anonymous_student_id": anonymous_student_id,
        "submission_time": submission_time,
    })


def make_hashkey(seed):
    """
    Generate a string key by hashing
    """
    h = hashlib.md5()
    h.update(str(seed))
    return h.hexdigest()


def now():
    return datetime.now(pytz.UTC).strftime(dateformat)


def default_time(fn):
    def default_timed(*args, **kwargs):
        qtime = kwargs.get('qtime')
        if qtime is None:
            qtime = now()
        kwargs['qtime'] = qtime
        return fn(*args, **kwargs)
    return default_timed


def deep_update(d, u):
    for k, v in u.iteritems():
        if isinstance(d, collections.Mapping):
            if isinstance(v, collections.Mapping):
                r = deep_update(d.get(k, {}), v)
                d[k] = r
            else:
                d[k] = u[k]
        else:
            d = {k: u[k]}
    return d
