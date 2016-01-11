# coding: utf-8

import socket
import StringIO
import sys

class WSGIServer(object):

    address_family = socket.AF_INET  # => 套接字家族(网络家族)
    socket_type = socket.SOCK_STREAM  # => 套接字类型(面向连接)
    request_queue_size = 1  # => 每次连接接受的请求大小

    def __init__(self, server_address):
        # 服务器端创建监听套接字
        # 用于监听客户端的连接
        self.listen_socket = listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )
        # 允许重复使用相同的地址(re use address)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 服务器端套接字绑定服务器IP地址
        listen_socket.bind(server_address)
        # 服务器端套接字监听客户端连接请求
        listen_socket.listen(self.request_queue_size)
        # 返回 (server_IP, port) 元祖
        host, port = self.listen_socket.getsockname()[:2]
        # getfqdn = get fully qualified domain name fron host
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        # Return headers set by Web framework/Web application
        # WSGI规范: Web framework/Web application 返回返回头部
        # ==> headers_set
        self.headers_set = []

    def set_app(self, application):
        # python application
        self.application = application

    def serve_forever(self):
        # 永久监听(除人为或异常终端)
        listen_socket = self.listen_socket
        while True:
            # New client connection
            # 服务器端套接字接受客户端请求, 建立TCP连接
            # 返回客户端IP, 同时创建一个连接套接字用于服务器与客户端的通信
            self.client_connection, client_address = listen_socket.accept()
            # Handle one request and close the client connection. Then
            # loop over to wait for another client connection
            # 进入{ 请求-->连接-->响应 }循环 ==> handle_one_request()
            self.handle_one_request()

    def handle_one_request(self):
        # 每次接受 1024 kb 的请求
        self.request_data = request_data = self.client_connection.recv(1024)
        # Print formatted request data a la 'curl -v'
        print(''.join(
            '&lt; {line}n'.format(line=line)
            for line in request_data.splitlines()
        ))  # => '&lt; line1n&lt; line2n&lt; line3n' ?

        self.parse_request(request_data)

        # Construct environment dictionary using request data
        env = self.get_environ()

        # It's time to call our application callable and get
        # back a result that will become HTTP response body
        # python applocation(or web framework) 接受环境变量字典 ==>
        # self.get_environ(), 以及服务器端的回调函数, 返回响应
        # ==> WSGI 规范
        result = self.application(env, self.start_response)

        # Construct a response and send it back to the client
        # 调用 finish_response 函数, 将python application 处理的响应
        # 返还给客户端
        self.finish_response(result)

    def parse_request(self, text):
        # text ==> request_data
        request_line = text.splitlines()[0]  # => this is the first line of the request_data
        request_line = request_line.rstrip('rn')  # => S.rstrip([chars])return a copy of request_line
        # but remove characters in chars instead => string or unicode
        # Break down the request line into components
        (self.request_method,  # GET
         self.path,            # /hello
         self.request_version  # HTTP/1.1
         ) = request_line.split()

    def get_environ(self):
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = StringIO.StringIO(self.request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        # CGI 环境变量
        env['REQUEST_METHOD']    = self.request_method    # GET
        env['PATH_INFO']         = self.path              # /hello
        env['SERVER_NAME']       = self.server_name       # localhost
        env['SERVER_PORT']       = str(self.server_port)  # 8888
        return env

    def start_response(self, status, response_headers, exc_info=None):
        # Add necessary server headers
        # 终于看到了传说中的 start_response 回调函数 !!!
        server_headers = [
            ('Date', 'Tue, 31 Mar 2015 12:54:48 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        # python application 处理的response头信息
        self.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. We simplicity's sake we'll ignore that detail
        # for now.
        # return self.finish_response

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}rn'.format(status=status)
            for header in response_headers:
                response += '{0}: {1}rn'.format(*header)
            response += 'rn'
            for data in result:
                response += data
            # Print formatted response data a la 'curl -v'
            print(''.join(
                '&gt; {line}n'.format(line=line)
                for line in response.splitlines()
            ))
            self.client_connection.sendall(response)
        finally:
            self.client_connection.close()

SERVER_ADDRESS = (HOST, PORT) = '', 8888

def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server

if __name__ == '__main__':
    if len(sys.argv) &lt; 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print('WSGIServer: Serving HTTP on port {port} ...n'.format(port=PORT))
    httpd.serve_forever()

