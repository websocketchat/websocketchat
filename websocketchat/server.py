# ╻ ╻┏━╸┏┓ ┏━┓┏━┓┏━╸╻┏ ┏━╸╺┳╸┏━╸╻ ╻┏━┓╺┳╸ ╻┏━┓┏━╸┏━┓╻ ╻┏━╸┏━┓ ┏━┓╻ ╻
# ┃╻┃┣╸ ┣┻┓┗━┓┃ ┃┃  ┣┻┓┣╸  ┃ ┃  ┣━┫┣━┫ ┃ ┏┛┗━┓┣╸ ┣┳┛┃┏┛┣╸ ┣┳┛ ┣━┛┗┳┛
# ┗┻┛┗━╸┗━┛┗━┛┗━┛┗━╸╹ ╹┗━╸ ╹ ┗━╸╹ ╹╹ ╹ ╹ ╹ ┗━┛┗━╸╹┗╸┗┛ ┗━╸╹┗╸╹╹   ╹

# MIT License
#
# Copyright (c) 2018  Shane R. Spencer <spencersr@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# SPDX-License-Identifier: MIT

# Author: Shane R. Spencer <spencersr@gmail.com>

import os
import sys

import re

import pytz
import datetime

import pprint

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.log
import tornado.websocket
import tornado.escape
import tornado.locks

import websocketchat.service.v1.handlers

from tornado.options import options
from tornado.options import define

_ = lambda s: s

UUID_RE_STRING = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
URL_RE_STRING = r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)'

# ┏┓ ┏━┓┏━┓┏━╸╻ ╻╺┳╸╺┳╸┏━┓╻ ╻┏━┓┏┓╻╺┳┓╻  ┏━╸┏━┓
# ┣┻┓┣━┫┗━┓┣╸ ┣━┫ ┃  ┃ ┣━┛┣━┫┣━┫┃┗┫ ┃┃┃  ┣╸ ┣┳┛
# ┗━┛╹ ╹┗━┛┗━╸╹ ╹ ╹  ╹ ╹  ╹ ╹╹ ╹╹ ╹╺┻┛┗━╸┗━╸╹┗╸

class BaseHTTPHandler(tornado.web.RequestHandler):
    def initialize(self, **kwargs):
        super(BaseHTTPHandler, self).initialize(**kwargs)
        self.kwargs = kwargs

# ┏━┓╺┳╸╻ ╻┏┓ ╻ ╻╺┳╸╺┳╸┏━┓╻ ╻┏━┓┏┓╻╺┳┓╻  ┏━╸┏━┓
# ┗━┓ ┃ ┃ ┃┣┻┓┣━┫ ┃  ┃ ┣━┛┣━┫┣━┫┃┗┫ ┃┃┃  ┣╸ ┣┳┛
# ┗━┛ ╹ ┗━┛┗━┛╹ ╹ ╹  ╹ ╹  ╹ ╹╹ ╹╹ ╹╺┻┛┗━╸┗━╸╹┗╸

class StubHTTPHandler(BaseHTTPHandler):

    def get(self, *args, **kwargs):

        print('---', self.request.body , '---')
        print('---', self.request.arguments , '---')

        self.set_header('Content-Type', 'text/plain')

        self.write(self.request.path + ' ' + str(uuid.uuid1()) + '\n')

        self.write('\n')

        self.write(
            pprint.pformat(
                dict(self.request.headers)
            ) + '\n'
        )

        self.write(
            pprint.pformat(
                dir(self.request)
            ) + '\n'
        )

        self.write(
            pprint.pformat(
                self.kwargs
            ) + '\n'
        )

        self.write(
            pprint.pformat(
                self.path_kwargs
            ) + '\n'
        )


        self.write(
            pprint.pformat(
                kwargs
            ) + '\n'
        )

        self.write(
            pprint.pformat(
                args
            ) + '\n'
        )

        for header in self.request.headers.items():
            tornado.log.gen_log.debug(f'request: header: {header[0]}: {header[1]}')

        for setting in self.application.settings.items():
            tornado.log.gen_log.debug(f'application: setting: {setting[0]}: {pprint.pformat(setting[1])}')

    head = get
    post = get

# ┏┳┓┏━┓╻┏┓╻┏╸╺┓
# ┃┃┃┣━┫┃┃┗┫┃  ┃
# ╹ ╹╹ ╹╹╹ ╹┗╸╺┛

def main():

    # ┏━┓┏━╸╺┳╸╺┳╸╻┏┓╻┏━╸┏━┓
    # ┗━┓┣╸  ┃  ┃ ┃┃┗┫┃╺┓┗━┓
    # ┗━┛┗━╸ ╹  ╹ ╹╹ ╹┗━┛┗━┛

    # Application

    define('config', default='gress.conf', type=str,
        help=_('Path to config file'),
        group=_('Application'),
        callback=lambda path: parse_config_file(path, final=False)
    )

    define('debug', default=False, type=bool,
        help=_('Debug Mode'),
        group=_('Application')
    )

    define('cookie_secret', default=False, type=bool,
        help=_('Cookie Secret'),
        group=_('Application')
    )

    # Websocket

    define('websocket_ping_interval', default=10, type=int,
        help=_('Websocket Ping Interval (Ping/Pong Keepalive)'),
        group=_('Websocket')
    )

    # HTTP Server

    define('listen_port', default=8000, type=int,
        help=_('Listen Port'),
        group=_('HTTP Server')
    )

    define('listen_host', default='localhost', type=str,
        help=_('Listen Host'),
        group=_('HTTP Server')
    )

    tornado.options.parse_command_line()

    # ┏━┓┏━╸┏━┓╻ ╻╻┏━╸┏━╸┏━┓   ╻ ╻╺┓    ┏━┓┏━┓┏━┓╻  ╻┏━╸┏━┓╺┳╸╻┏━┓┏┓╻
    # ┗━┓┣╸ ┣┳┛┃┏┛┃┃  ┣╸ ┗━┓   ┃┏┛ ┃    ┣━┫┣━┛┣━┛┃  ┃┃  ┣━┫ ┃ ┃┃ ┃┃┗┫
    # ┗━┛┗━╸╹┗╸┗┛ ╹┗━╸┗━╸┗━┛╺━╸┗┛ ╺┻╸╺━╸╹ ╹╹  ╹  ┗━╸╹┗━╸╹ ╹ ╹ ╹┗━┛╹ ╹

    services_v1_application = tornado.web.Application(
        handlers = [
            #(fr'/v1/chat/socket/({UUID_RE_STRING})$', ChatSocketWebsocketHandler),
            #(ff'/v1/chat/callback/({UUID_RE_STRING})$', ChatCallbackHTTPHandler),
            #(ff'/v1/chat/send/({UUID_RE_STRING})$', ChatSendHTTPHandler),
            #(ff'/v1/chat/receive/({UUID_RE_STRING})$', ChatReceiveHTTPHandler),
            #(ff'/v1/chat/poll/({UUID_RE_STRING})$', ChatTailHTTPHandler),
            #(fr'/v1/find/ip$', FindByIPHTTPHandler),
            #(fr'/v1/find/click$', FindByClickHTTPHandler),
            (fr'/v1/find/click$', StubHTTPHandler),
        ],
        channels={},
        locks={},
        calls=[],
        args=options.as_dict(),
        **options.group_dict('Application'),
        **options.group_dict('Websocket')
    )

    # ┏━┓┏━┓┏━┓╻  ╻┏━╸┏━┓╺┳╸╻┏━┓┏┓╻
    # ┣━┫┣━┛┣━┛┃  ┃┃  ┣━┫ ┃ ┃┃ ┃┃┗┫
    # ╹ ╹╹  ╹  ┗━╸╹┗━╸╹ ╹ ╹ ╹┗━┛╹ ╹

    application = tornado.web.Application(
        handlers = [
            (r'^/v1/.*', services_v1_application),
            (r'^/$', tornado.web.RedirectHandler, {'url': 'http://docs.websocket.chat/', 'permanent': False})
        ],
        xsrf_cookies=True,
        args=options.as_dict(),
        **options.group_dict('Application')
    )

    # ┏━┓┏━╸┏━┓╻ ╻┏━╸┏━┓
    # ┗━┓┣╸ ┣┳┛┃┏┛┣╸ ┣┳┛
    # ┗━┛┗━╸╹┗╸┗┛ ┗━╸╹┗╸

    http_server = tornado.httpserver.HTTPServer(application)

    http_server.listen(options.listen_port, address=options.listen_host)

    loop = tornado.ioloop.IOLoop.instance()

    try:
        loop_status = loop.start()
    except KeyboardInterrupt:
        loop_status = loop.stop()

    return loop_status

if __name__ == '__main__':
    main()
