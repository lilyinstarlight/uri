import json
import time
import http.client

from uri import config


def get(alias):
    # connect to API
    if config.store_https:
        conn = http.client.HTTPSConnection(config.store)
    else:
        conn = http.client.HTTPConnection(config.store)

    # request given alias
    conn.request('GET', config.store_endpoint + 'store/uri/' + alias)

    # get response
    response = conn.getresponse()

    # check for 404
    if response.status == 404:
        raise KeyError()

    # get data
    redirect = {'location': response.read().decode('utf-8')}

    return redirect


def put(alias, location):
    # connect to API
    if config.store_https:
        conn = http.client.HTTPSConnection(config.store)
    else:
        conn = http.client.HTTPConnection(config.store)

    # request given alias
    conn.request('HEAD', config.store_endpoint + 'store/uri/' + alias)

    # get response
    response = conn.getresponse()
    response.read()

    # check for existing alias
    if response.status == 200:
        raise KeyError()
    elif response.status == 400:
        raise NameError()
    else:
        raise ValueError()

    # determine if this is a put or a post
    if alias:
        method = 'PUT'
    else:
        method = 'POST'

    # make a metadata request
    conn.request(method, config.store_endpoint + 'api/uri/' + alias, headers={'Content-Type': 'application/json'}, body=json.dumps({'filename': None, 'size': len(location), 'type': 'text/uri-list', 'expire': time.time() + config.interval, 'locked': True}).encode('utf-8'))

    # get response
    response = conn.getresponse()

    # load data response
    data = json.loads(response.read().decode('utf-8'))

    # note bad requests
    if response.status != 201:
        raise ValueError()

    # make a data request
    conn.request('PUT', config.store_endpoint + 'store/uri/' + data['alias'], body=location.encode('utf-8'))

    # get response
    response = conn.getresponse()
    response.read()

    # note bad requests
    if response.status != 204:
        raise ValueError()

    return data['alias']
