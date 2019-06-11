var express = require('express');
var path = require('path');

var server = express();
server.use(express.static(path.join(__dirname, 'public')));

server.get('/', (req,res) => {

    res.sendFile(__dirname + '/public/HTML/menu.html');
});

console.log('### MENU LANCE ###');
server.listen(8081);
