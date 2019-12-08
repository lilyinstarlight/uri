import json
import time
import http.client
import urllib.parse

from uri import config


def get(alias):
    # connect to API
    url = urllib.parse.urlparse(config.store)

    if url.scheme == 'https':
        conn = http.client.HTTPSConnection(url.netloc)
    else:
        conn = http.client.HTTPConnection(url.netloc)

    # request given alias
    conn.request('GET', url.path.rstrip('/') + '/store/uri/' + alias)

    # get response
    response = conn.getresponse()

    # check for 404
    if response.status == 404:
        raise KeyError(alias)

    # get data
    redirect = {'location': response.read().decode('utf-8')}

    return redirect


def put(alias, location):
    # connect to API
    url = urllib.parse.urlparse(config.store)

    if url.scheme == 'https':
        conn = http.client.HTTPSConnection(url.netloc)
    else:
        conn = http.client.HTTPConnection(url.netloc)

    # determine if this is a put or a post
    if alias:
        method = 'PUT'
    else:
        method = 'POST'

    # make a metadata request
    conn.request(method, url.path.rstrip('/') + '/api/uri/' + alias, headers={'Content-Type': 'application/json'}, body=json.dumps({'filename': None, 'size': len(location), 'type': 'text/uri-list', 'expire': time.time() + config.interval, 'locked': True}).encode('utf-8'))

    # get response
    response = conn.getresponse()

    # load data response
    data = json.loads(response.read().decode('utf-8'))

    # note bad requests - existing alias, bad name, and unknown error
    if response.status == 403:
        raise KeyError(alias)
    elif response.status == 404:
        raise NameError('alias ' + repr(alias) + ' invalid')
    elif response.status != 201:
        raise ValueError('invalid alias: ' + repr(alias))

    # make a data request
    conn.request('PUT', url.path.rstrip('/') + '/store/uri/' + data['alias'], body=location.encode('utf-8'))

    # get response
    response = conn.getresponse()
    response.read()

    # note bad requests
    if response.status != 204:
        raise ValueError('failed to make alias: ' + repr(alias))

    return data['alias']
