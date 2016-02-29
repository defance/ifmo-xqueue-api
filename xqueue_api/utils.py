from datetime import datetime
import json
import hashlib
import pytz

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


def make_xheader(lms_callback_url, lms_key, queue_name):
    """
    Generate header for delivery and reply of queue request.

    Xqueue header is a JSON-serialized dict:
        { 'lms_callback_url': url to which xqueue will return the request (string),
          'lms_key': secret key used by LMS to protect its state (string),
          'queue_name': designate a specific queue within xqueue server, e.g. 'MITx-6.00x' (string)
        }
    """
    return json.dumps({
        'lms_callback_url': lms_callback_url,
        'lms_key': lms_key,
        'queue_name': queue_name
    })


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