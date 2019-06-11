var express = require('express');
var path = require('path');
var bodyParser = require('body-parser');

var app = express();
app.use(express.static(path.join(__dirname, 'public')));
var urlencodedParser = bodyParser.urlencoded({ extended: false });

//connexion to mongo database
const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://Spicy_Telescope:ZmyWvqA7Bbfcol18@clusterinsaproject-5sppd.mongodb.net/test?retryWrites=true";
const client = new MongoClient(uri, { useNewUrlParser: true });
console.log('#### MON_COMPTE - Connexion à la base de donnée initialisée ! ####');
var admin;

client.connect(err => {

    var collection = client.db("ClientsDB").collection("Admin");
    
    app.get('/', function(req,res){

        collection.find({}).toArray((err, result) => {
            admin = null; //reclean the array for the next requests
            for(var i = 0; i<result.length; i++){
                admin = result[i];
            }
            admin_id = admin['_id'];
            res.render('mon_compte.ejs', {admin:admin});
        });
        

    })
    .post('/edit/', urlencodedParser, function(req,res){
        if (req.body.prenom != '' && req.body.nom != '')
            collection.updateOne({
                "_id" : admin_id },
                { $set: {"prenom" : req.body.prenom,
                        "nom" : req.body.nom,
                        "email" : req.body.email
                    }});
        res.redirect('http://forthouse.insa/mon_compte/');
    })

    .get('/scheme/', (req, res) => {

        var query_id = admin_id;
        var ObjectId = require('mongodb').ObjectID;
        var id_entry = ObjectId(query_id); // ID of the entry used to identifiate with the scheme

        var {PythonShell} = require('python-shell');
        var options = {
            mode : 'text',
            encoding : 'UTF-8',
            pythonOptions : ['-u'],
            scriptPath: './',
            args : [id_entry, 'admin'], // start at the second argument, as there is the '-u' option (see before)
            pythonPath : '/usr/bin/python2'
        
        };
        
        var py_shell = new PythonShell('../scripts_python/acquisition.py', options);
        py_shell.on('message', function(message) {
        console.log(message);
        });
        res.redirect('http://forthouse.insa/mon_compte/');
        
    })

    .use(function(req, res, next){
        
        res.redirect('http://forthouse.insa/mon_compte/');
    });

    
});

app.listen(8085);
