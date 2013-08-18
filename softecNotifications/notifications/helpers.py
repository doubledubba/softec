import hmac
import logging

from django.http import Http404
from softecNotifications.settings import DEBUG

params = {'format': '[%(levelname)s] [%(asctime)s]: %(message)s', 'level':
        logging.DEBUG}
if not DEBUG:
    params['level'] = logging.INFO
logging.basicConfig(**params)

digest = lambda msg: hmac.HMAC(str(msg), 'dune').hexdigest()

def strToInt(val):
    'Raises 404 if str is not an int'

    if val.isdigit():
        return int(val)
    else:
        raise Http404

