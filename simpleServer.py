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

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

print "Server http on port %d" % PORT

while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print request
    http_response = """
HTTP/1.1 200 OK

hello python http server
"""
    client_connection.sendall(http_response)
    client_connection.close()
