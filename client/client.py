import sys
import hmac
import logging
from datetime import datetime
from time import sleep

import requests
from requests.exceptions import ConnectionError

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

cid = sys.argv[1]
domain = sys.argv[2] if len(sys.argv) >= 3 else '127.0.0.1:8000'
url = 'http://' + domain

digest = hmac.HMAC(str(cid), 'dune').hexdigest()

print('Starting up client...')
print('Computer id: %s' % cid)
print('URL: %s' % url)
print('Digest: %s' % digest)



def connection(path, params={'cid': cid, 'digest': digest}):
    '''Takes path from domain name to connect to, returns request object.'''

    r = requests.post(url + path, data=params)
    return r


# Fetch CHECK_IN_RATE from server
r = connection('/update/')
if r.text.isdigit():
    CHECK_IN_RATE = int(r.text)
else:
    print('UPDATE FAILED: FALLING BACK TO DEFAULT CHECK_IN_RATE')
    CHECK_IN_RATE = 15
    print('SERVER SAYS: %s' % r.text)
print('CHECK_IN_RATE: %d' % CHECK_IN_RATE)



def check_in():
    r = connection('/check_in/')
    if r:
        if r.ok:
            print(r.text)
        else:
            print("Something went wrong")
    else:
        print('No request object returned!')

if __name__ == '__main__':
    try:
        while True:
            check_in()
            sleep(CHECK_IN_RATE)
    except KeyboardInterrupt:
        print('Killing client on %s' % datetime.now().strftime('%c'))