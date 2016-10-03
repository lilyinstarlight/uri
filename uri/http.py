import os
import time

import web, web.form, web.page

from uri import config, log, uri


alias = '([a-zA-Z0-9._-]+)'

http = None

routes = {}
error_routes = {}


class Interface(web.page.PageHandler, web.form.FormHandler):
    directory = os.path.dirname(__file__) + '/html'
    page = 'index.html'
    message = ''

    def format(self, page):
        return page.format(message=self.message)

    def do_post(self):
        try:
            alias = self.request.body['alias']
            location = self.request.body['uri']
        except (KeyError, TypeError):
            raise web.HTTPError(400)

        try:
            alias = uri.put(alias, location)

            self.message = 'Successfully created at <a href="' + config.service + '/' + alias + '">' + config.service + '/' + alias + '</a>.'
        except KeyError:
            self.message = 'This alias already exists. Wait until it expires or choose another.'
        except NameError:
            self.message = 'This alias is not valid. Choose one made up of alphanumeric characters only.'
        except ValueError:
            self.message = 'Could not upload data for some reason. Perhaps you should try again.'

        return self.do_get()


class ErrorInterface(web.page.PageErrorHandler):
    directory = os.path.dirname(__file__) + '/html'
    page = 'error.html'


class Redirect(web.HTTPHandler):
    def do_get(self):
        alias = self.groups[0]

        try:
            redirect = uri.get(alias)
        except KeyError:
            raise web.HTTPError(404)

        # set headers
        self.response.headers['Location'] = redirect['location']

        # return file-like object
        return 307, ''


routes.update({'/': Interface, '/' + alias: Redirect})
error_routes.update(web.page.new_error(handler=ErrorInterface))


def start():
    global http

    http = web.HTTPServer(config.addr, routes, error_routes, log=log.httplog)
    http.start()


def stop():
    global http

    http.stop()
    http = None
