
document.addEventListener('DOMContentLoaded', main );

let timeoutId = null;
function main() {

    setupEventListeners();

}

function findSimilarity() {

    const movie = document.getElementsByClassName('movie');
    const movie1 = movie[0].value;
    const movie2 = movie[1].value;

    console.log(movie1, movie2);

}


function setupEventListeners() {

    const movie = document.getElementsByClassName('movie');
    
    for (let i = 0; i < movie.length; i++) {
        movie[i].addEventListener('input', handleSelectChange);
    };

}

async function handleSelectChange(event) {

    const selectedMovie = this.value;
    
    clearTimeout(timeoutId);

    timeoutId = setTimeout(async () => {

    const response = await fetch('/get-movie-list', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selectedMovie })
    })

    const data = await response.json();

    const movies = []
    //parse the movies from the response
    data.forEach( d => {
        movies.push( d[0] )
    });

    console.log(movies)

    updateAutocomplete(movies, selectedMovie, event);

    }, 400);

};

function updateAutocomplete(movies, userInput, event) {
    
    var resultsContainer = event.target.nextElementSibling;
    resultsContainer.innerHTML = ''; // Clear previous results
    this.innerHTML = '';
    
    if (userInput.length > 0) {
        // Filter the movie list based on the input
        var filteredMovies = movies.filter(function(movie) {
            return movie.toLowerCase().includes(userInput);
        });

        // Show suggestions
        filteredMovies.forEach(function(movie) {
            var div = document.createElement('div');
            div.textContent = movie;
            div.addEventListener('click', function() {
                event.target.value = movie; // Update input with movie name
                resultsContainer.innerHTML = ''; // Clear suggestions
                resultsContainer.style.display = 'none'; // Hide suggestions
            });
            resultsContainer.appendChild(div);
        });

        resultsContainer.style.display = 'block'; // Show suggestions
    } else {
        resultsContainer.style.display = 'none'; // Hide suggestions
    }
}

// Hide suggestions when clicking outside
document.addEventListener('click', function(e) {
    if (e.target.class !== 'movie') {
        document.getElementById('autocomplete-results').style.display = 'none';
    }
});
