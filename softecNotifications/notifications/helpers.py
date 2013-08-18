import hmac

from django.http import Http404


digest = lambda msg: hmac.HMAC(str(msg), 'dune').hexdigest()

def strToInt(val):
    'Raises 404 if str is not an int'

    if val.isdigit():
        return int(val)
    else:
        raise Http404
