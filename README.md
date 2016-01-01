一起来写一个web服务器的代码
===
原文: http://python.jobbole.com/81524/

## (一): 实现一个简单的http服务器
服务器创建一个套接字用于监听客户端的请求, 当我们在浏览器或者客户端模拟器中输入一个url时, 首先会和服务器建立TCP连接,
服务器端套接字bind连接,进入http请求~处理~响应的循环。

### simpleServer.py
simpleServer.py => python 实现的一个简单的http服务器

### simpleServer.js
simpleServer.js => Node 实现的一个简单的http服务器
