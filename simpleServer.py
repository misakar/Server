# coding: utf-8
"""
so, this is a simple python http server use socket

web server => create socket => listen
client => TCP => web server => http req => sockent => bind <=> socket connection
===> response

this is the first simple web server: but it can not server flask django .. python web app
if you want to server this web app, you need realize some interface: WSGI
"""

import socket

HOST, PORT = '', 8888  # (HOST, PORT): ip and port

# create a server side socket: socket family: AF_INET, socket type: SOCK_STREAM
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server side socket bind server host and port
listen_socket.bind((HOST, PORT))
# server side socket listen
listen_socket.listen(1)

print "Server http on port %d" % PORT

while True:
    # 服务器端套接字被动接受客户端连接, 创建一个新的套接字: client_connection
    # 用于与客户端通信
    client_connection, client_address = listen_socket.accept()
    # 获取请求(最大传输量为 1024)
    request = client_connection.recv(1024)
    print request
    http_response = """
HTTP/1.1 200 OK

hello python http server
"""
    # 完整发送TCP数据
    client_connection.sendall(http_response)
    # 服务器端套接字关闭连接
    client_connection.close()
