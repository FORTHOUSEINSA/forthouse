var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');

var app = express();
var urlencodedParser = bodyParser.urlencoded({ extended: false });

app.use(express.static(path.join(__dirname, 'public')));

//connexion to mongo database
const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://Spicy_Telescope:ZmyWvqA7Bbfcol18@clusterinsaproject-5sppd.mongodb.net/test?retryWrites=true";
const client = new MongoClient(uri, { useNewUrlParser: true });
console.log('#### NOTIFICATIONS - Connexion à la base de donnée initialisée ! ####');
var notif_database = []; /*creation of a temp database array to transfer all the data
from mongoDB to nodeJS to EJS templates */
client.connect(err => {

    var collection = client.db("ClientsDB").collection("ClientsNotif");

    app.get('/', (req,res) => {

        collection.find({}).toArray((err, result) => {
            notif_database = []; //reclean the array for the next requests
            for(var i = 0; i<result.length; i++){
                notif_database.push(result[i]);
            }
            res.render('notif_panel.ejs', {database:notif_database});
        });
    })

    .use((req,res,next) => {
        res.redirect('/');
    });
    
    
});


app.listen(8083);
client.close();
