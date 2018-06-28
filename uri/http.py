import html
import time
import urllib.parse

import fooster.web, fooster.web.form, fooster.web.page

from uri import config, uri


class Interface(fooster.web.page.PageHandler, fooster.web.form.FormHandler):
    directory = config.template
    page = 'index.html'
    message = ''

    def format(self, page):
        return page.format(message=self.message)

    def do_post(self):
        try:
            alias = self.request.body['alias']
            location = self.request.body['uri']
        except (KeyError, TypeError):
            raise fooster.web.HTTPError(400)

        try:
            alias = uri.put(alias, location)

            self.message = 'Successfully created at <a href="' + config.service + '/' + urllib.parse.quote(alias) + '">' + config.service + '/' + html.escape(alias) + '</a>.'
        except KeyError:
            self.message = 'This alias already exists. Wait until it expires or choose another.'
        except NameError:
            self.message = 'This alias is not valid. Choose one made up of alphanumeric characters only.'
        except ValueError:
            self.message = 'Could not upload data for some reason. Perhaps you should try again.'

        return self.do_get()


class ErrorInterface(fooster.web.page.PageErrorHandler):
    directory = config.template
    page = 'error.html'


class Redirect(fooster.web.HTTPHandler):
    def do_get(self):
        alias = self.groups['alias']

        try:
            redirect = uri.get(alias)
        except KeyError:
            raise fooster.web.HTTPError(404)

        # set headers
        self.response.headers['Location'] = redirect['location']

        # return file-like object
        return 307, ''


alias = '(?P<alias>[a-zA-Z0-9._-]+)'

http = None

routes = {}
error_routes = {}


routes.update({'/': Interface, '/' + alias: Redirect})
error_routes.update(fooster.web.page.new_error(handler=ErrorInterface))


def start():
    global http

    http = fooster.web.HTTPServer(config.addr, routes, error_routes, timeout=60, keepalive=60)
    http.start()


def stop():
    global http

    http.stop()
    http = None


def join():
    global http

    http.join()
