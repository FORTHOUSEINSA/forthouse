var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');
var {PythonShell} = require('python-shell');

var app = express();
var urlencodedParser = bodyParser.urlencoded({ extended: false });

app.use(express.static(path.join(__dirname, 'public')));

//connexion to mongo database
const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://Spicy_Telescope:ZmyWvqA7Bbfcol18@clusterinsaproject-5sppd.mongodb.net/test?retryWrites=true";
const client = new MongoClient(uri, { useNewUrlParser: true });
console.log('#### DATABASE - Connexion à la base de donnée initialisée ! ####');
var client_database = []; /*creation of a temp database array to transfer all the data
from mongoDB to nodeJS to EJS templates */

client.connect(err => {

    var collection = client.db("ClientsDB").collection("ClientsCollection");
    
    app.get('/', function(req,res){

        collection.find({}).toArray((err, result) => {
            client_database = []; //reclean the array for the next requests
            for(var i = 0; i<result.length; i++){
                client_database.push(result[i]);
            }
            res.render('database.ejs', {database:client_database});
        });
        

    })
    .post('/add_entry/', urlencodedParser, function(req,res){
        if (req.body.firstname != '' && req.body.lastname != '')
            collection.insertOne({
                'firstname': req.body.firstname,
                'lastname': req.body.lastname,
                'schema' : 'NULL'
            });
        res.redirect('http://forthouse.insa/database/');
    })

    .get('/launch_script/:index', (req, res) => {

        var query_id = client_database[req.params.index]['_id'];
        var ObjectId = require('mongodb').ObjectID;
        var id_entry = ObjectId(query_id); // ID of the entry used to identifiate with the scheme

        var {PythonShell} = require('python-shell');
        var options = {
            mode : 'text',
            encoding : 'UTF-8',
            pythonOptions : ['-u'],
            scriptPath: './',
            args : [id_entry,'client'], // this is the second argument, as there is the '-u' option (see before)
            pythonPath : '/usr/bin/python2'
        
        };
        
        var py_shell = new PythonShell('../scripts_python/acquisition.py', options);
        py_shell.on('message', function(message) {
        console.log(message);
        });
        res.redirect('http://forthouse.insa/database/');
        
    })

    .get('/delete_entry/:index', function(req,res){
        var query_id = client_database[req.params.index]['_id'];
        var ObjectId = require('mongodb').ObjectID;
        collection.deleteOne({
            _id: ObjectId(query_id)
        });
        res.redirect('http://forthouse.insa/database/');
    })


    .use(function(req, res, next){
        
        res.redirect('/');
    });

    
});

app.listen(8082);
client.close();
