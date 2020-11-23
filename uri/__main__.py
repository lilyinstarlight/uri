import argparse
import logging
import signal

from uri import config


def main():
    parser = argparse.ArgumentParser(description='serve up a temporary uri redirect service')
    parser.add_argument('-a', '--address', dest='address', help='address to bind')
    parser.add_argument('-p', '--port', type=int, dest='port', help='port to bind')
    parser.add_argument('-t', '--template', dest='template', help='template directory to use')
    parser.add_argument('-l', '--log', dest='log', help='log directory to use')
    parser.add_argument('-s', '--store', dest='store', help='uri of store backend')
    parser.add_argument('-i', '--interval', dest='interval', help='number of hours to keep files')
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
            config.http_log = None
        else:
            config.log = args.log + '/uri.log'
            config.http_log = args.log + '/http.log'

    if args.store:
        config.store = args.store

    if args.interval:
        config.interval = args.interval * 3600

    if args.service:
        config.service = args.service

    config._apply()


    from uri import __version__
    from uri import http


    log = logging.getLogger('uri')

    log.info('uri ' + __version__ + ' starting...')

    # start everything
    http.start()


    # cleanup function
    def exit(signum, frame):
        http.stop()


    # use the function for both SIGINT and SIGTERM
    for sig in signal.SIGINT, signal.SIGTERM:
        signal.signal(sig, exit)

    # join against the HTTP server
    http.join()


if __name__ == '__main__':
    main()
