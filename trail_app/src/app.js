const express = require('express');
const path = require('path');
const hbs = require('hbs');
const request = require('request');
let {PythonShell} = require('python-shell');
const fs = require('fs');
const geolocation = require('./utils/geolocation');
const recommendation = './src/utils/recommendation.py'

var trail_name_1 = 's'
var trail_name_2 = 's'
var trail_difficulty_1 = 's'
var trail_difficulty_2 = 's'


const app = express();
const port = 3000;

// Defining paths for express config
const publicDirectoryPath = path.join(__dirname, '../public');
const templatesPath = path.join(__dirname, '../templates/views');
const partialsPath = path.join(__dirname, '../templates/partials');

// Setting up handlerbars
app.set('view engine', 'hbs');
app.set('views', templatesPath);
hbs.registerPartials(partialsPath);

// Setup static directory to use
app.use(express.static(publicDirectoryPath));

app.get('', (req, res) => {
    res.render('index', {
        title: 'Trail_App',
        name: 'AubieHacks'
    })
})

app.get('/result', (req, res) => {
    res.render('result', {
        title: 'Result',
        name: AubieHacks
    })
})

app.get('/location', (req, res) => {
    if(!req.query.address) {
        return res.send({
            error: 'You must provide an address!'
        })
    }
    const location = req.query.address;
    const distance = req.query.distance;
    const difficulty = req.query.difficulty;

    geolocation(location, (error, { latitude, longitude, location } = {}) => {
        if(error) {
            return res.send({
                error
            });
        }
        const message = 'Latitude: ' + latitude + ' Longitude: ' + longitude + ' distance: ' + distance +
        ' difficulty: ' + difficulty;

        let params = {
            args: [latitude, longitude, distance, difficulty]
        }
        PythonShell.run(recommendation, params, function(error, result) {
            if(error) {
                console.log(error);
                return res.send({
                    error
                })
            } else {
                var file = fs.readFile('./src/utils/result.json', (error, result) => {
                    if(error) {
                        console.log(error);
                    } else {
                        console.l
                    }
                })
            }
        })

        res.send({
            latitude: latitude,
            longitude: longitude,
            location: location,
            trail_name_1: trail_name_1
        });

    })
})

app.listen(port, () => {
    console.log("Server is up and running at port 3000");
})