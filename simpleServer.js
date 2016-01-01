// this is a simple server written by node js

var http = require('http')

var PORT = 8881;

http.createServer(function(req, res){
    res.writeHead({'Content-Type' : 'text/html'});
    res.write("hello neo1218");
    res.end('hello nodejs');
}).listen(PORT);

console.log("http server is running on %d", PORT)
