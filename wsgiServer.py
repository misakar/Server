# coding: utf-8
"""
wsgiServer.py :=> a simple WSGI Server server python web app

"""

import socket
import StringIO
import sys


class WSGIServer(object):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self, server_address):
        self.listen_socket = listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(server_address)
        listen_socket.listen(self.request_queue_size)
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.header_sets = []

    def set_app(self, application):
        self.application = application

    def server_forever(self):
        listen_socket = self.listen_socket
        while True:
            self.client_connection, client_address = listen_socket.accept()
            self.handle_one_request()

    def handle_one_request(self):
        self.request_data = request_data = self.client_connection.recv(1024)
        print ''.join(
            '&it; %s n' % line for line in request_data.splitlines()
        )
        self.parse_request(request_data)

        env = self.get_environ()

        result = self.application(env, self.start_response)
        self.finish_response(result)

    def parse_request(self, text):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('rn')
        (self.request_method,
         self.path,
         self.request_version) = request_line.split()

    def get_environ(self):
        env = {}
        env['wsgi.version']             = (1, 0)
        env['wsgi.url_scheme']          = 'http'
        env['wsgi.input']               = StringIO.StringIo(self.request_data)
        env['wsgi.errors']              = sys.stderr
        env['wsgi.multithread']         = False
        env['wsgi.multiprocess']        = False
        env['wsgi.run_once']            = False
        env['REQUEST_METHOD']           = self.request_method
        env['PATH_INFO']                = self.path
        env['SERVER_NAME']              = self.server_name
        env['SERVER_PORT']              = self.server_port
        return env

    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date', 'Fir, 1 Jan 2016 16:46:22 GMT'),
            ('Server', 'WSGIServer 0.2')
        ]
        self.header_sets = [status, response_headers + server_headers]

    def finish_response(self, result):
        try:
            status, response_headers = self.header_sets
            response = 'HTTP/1.1 %srn' % status
            for header in response_headers:
                pass
