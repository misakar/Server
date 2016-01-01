一起来写一个web服务器的代码
===
原文: http://python.jobbole.com/81524/

## (一): 实现一个简单的http服务器
### socket 套接字
socket 的原意是插座的意思, 如果把服务器看成一个房间,
那么套接字就像一个个插座,用于提供不同的服务,
服务器端和客户端连接的端点就是套接字。

### 客户端和服务器的连接过程
服务器创建一个套接字用于监听客户端的请求, 当我们在浏览器或者客户端模拟器中输入一个url时, 首先会和服务器建立TCP连接,
服务器端套接字bind连接,进入http请求~处理~响应的循环,
即接受请求、建立连接、处理响应、返回响应。

### simpleServer.py
[simpleServer.py](https://github.com/neo1218/Server/blob/master/simpleServer.py) => python 实现的一个简单的http服务器

### simpleServer.js
[simpleServer.js](https://github.com/neo1218/Server/blob/master/simpleServer.js) => Node 实现的一个简单的http服务器

## (二): 让http服务器可以向python web application提供服务
### WSGI(Web Server Gateway Interface)
如果服务器遵循WSGI规范, 那么就可以与python web app交互

### wsgiServer.py
[wsgiServer.py](https://github.com/neo1218/Server/blob/master/wsgiServer.py) => 遵循WSGI规范的http服务器
