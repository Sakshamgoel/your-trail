console.log('Frontend js script up and running');


const weatherForm = document.querySelector('form');
const start_location = document.querySelector('input');
const distance = document.querySelector('#max-distance');
const difficulty = document.querySelector('#max-difficulty')
const messageOne = document.querySelector('#message-1');
const messageTwo = document.querySelector('#message-2');
const messageThree = document.querySelector('#message-3');

const table = document.getElementById('result-table');

var latitude = 32.6099;
var longitude = -85.4808;

weatherForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const location = start_location.value;
    const max_distance = distance.value;
    const max_difficulty = difficulty.value;

    var max_difficulty_int = 0;
    if(max_difficulty == 'Easy') {
        max_difficulty_int = 1;
    } else if(max_difficulty == 'Intermediate') {
        max_difficulty_int = 2;
    } else if(max_difficulty == 'Expert') {
        max_difficulty_int = 3;
    } else {
        max_difficulty_int = 4;
    }

    console.log(location);
    console.log(max_distance);
    console.log(max_difficulty_int);

    const url = '/location?address=' + location + '&distance=' + max_distance + '&difficulty=' + max_difficulty_int;

    messageOne.textContent = 'Loading...';
    messageTwo.textContent = '';
    messageThree.textContent = '';

    fetch(url).then((response) => {
        response.json().then((data) => {
            if(data.error) {
                messageOne.textContent = 'Error: ' + data.error;
                console.log(data.error);
            } else {
                messageOne.textContent = 'Location: ' + data.location;
                messageTwo.textContent = 'Latitude: ' + data.latitude + ' Longitude: ' + data.longitude;


                console.log(data);
                latitude = data.latitude;
                longitude = data.longitude;
                trail_name_1 = data.trail_name_1;
                // name = data.name;

                // console.log(name);
                
                initMap();
            }
        })
    })
})

function initMap() {
    const auburn = {lat: latitude, lng: longitude};

    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: auburn
    });

    const marker = new google.maps.Marker({
        position: auburn,
        map: map,
      });
}