import argparse
import signal


from uri import config


parser = argparse.ArgumentParser(description='serve up a temporary uri redirect service')
parser.add_argument('-a', '--address', dest='address', help='address to bind')
parser.add_argument('-p', '--port', type=int, dest='port', help='port to bind')
parser.add_argument('-t', '--template', dest='template', help='template directory to use')
parser.add_argument('-l', '--log', dest='log', help='log directory to use')
parser.add_argument('service', nargs='?', help='uri of service')

args = parser.parse_args()

if args.address:
    config.addr = (args.address, config.addr[1])

if args.port:
    config.addr = (config.addr[0], args.port)

if args.template:
    config.template = args.template

if args.log:
    if args.log == 'none':
        config.log = None
        config.httplog = None
    else:
        config.log = args.log + '/uri.log'
        config.httplog = args.log + '/http.log'

if args.service:
    config.service = args.service


from uri import name, version
from uri import log, http


log.urilog.info(name + ' ' + version + ' starting...')

# start everything
http.start()


# cleanup function
def exit():
    http.stop()


# use the function for both SIGINT and SIGTERM
for sig in signal.SIGINT, signal.SIGTERM:
    signal.signal(sig, exit)
