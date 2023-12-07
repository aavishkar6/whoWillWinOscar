document.addEventListener('DOMContentLoaded', main);

let nomineeChartval = null;

async function main() {
    setupEventListeners();
    initializeBestRatedOscarMovie();
    initializeHighestBudgetOscarMovie();

    // handle radio button listening
    

}

function setupEventListeners() {
    const yearSelect = document.getElementById('oscar_winner_date');
    const categorySelect = document.getElementById('oscar_winner_category');
    const nomination_category = document.getElementById('oscar_nomination_category');

    const radiosBestRated = document.querySelectorAll('input[type="radio"][name="rated"]');
    radiosBestRated.forEach(radio => {
        radio.addEventListener('change', handleBestRated);
    });

    const radiosHighestBudget = document.querySelectorAll('input[type="radio"][name="budget"]');
    radiosHighestBudget.forEach(radio => {
        radio.addEventListener('change', handleHighestBudget);
    });

    

    yearSelect.addEventListener('change', handleSelectChange);
    categorySelect.addEventListener('change', handleSelectChange);
    nomination_category.addEventListener('change', handleNomineeSelectChange);
}

// callback to event listeners
async function handleSelectChange() {
    try {
        const selectedYear = document.getElementById('oscar_winner_date').value;
        const selectedCategory = document.getElementById('oscar_winner_category').value;

        console.log('Selected Year:', selectedYear);
        console.log('Selected Category:', selectedCategory);

        if (selectedYear !=" " && selectedCategory !=" ") {
            const winnerData = await getOscarWinnerData(selectedYear, selectedCategory);
            console.log('Winner Data:', winnerData);

            const winner = document.getElementById('winner');
            winner.innerHTML = '';
            
            const val = document.createElement('h1');
            val.textContent = `Oscar for ${selectedCategory} in ${selectedYear} goes to ${winnerData[0].name} for the film ${winnerData[0].film}!`;

            console.log(winner);

            winner.appendChild(val);

            // Update UI with winnerData
        }
    } catch (error) {
        console.error('Error:', error);
    }

}

async function handleNomineeSelectChange() {
    try {
        const selectedCategory = this.value;

        console.log('Selected Category:', selectedCategory);

        if (selectedCategory) {
            const endpoint = `/api/nominee?category=${encodeURIComponent(selectedCategory)}`
            const response = await fetch(endpoint);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const result = await response.json();
            console.log('Nominee Data:', result);
            await nomineeChart( result );
            // return response.json();
        }
    } catch (error) {
        console.error('Error:', error);
    }

}

async function initializeBestRatedOscarMovie() {
    try {
        const response = await fetch("/api/best_rated_oscar_movies");
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const result = await response.json();
        console.log('Best Rated Oscar Movie:', result);
        await bestRatedMovie(result);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function initializeHighestBudgetOscarMovie() {
    try {
        const response = await fetch("/api/highest_budget_movie");
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const result = await response.json();
        console.log('Best Rated Oscar Movie:', result);
        await highestBudgetMovie(result);
    } catch (error) {
        console.error('Error:', error);
    }
}


async function bestRatedMovie(results) {
    try {
        console.log('Results:', results);

        const x = results.map(data => data.film);
        const y = results.map(data => data.rate);
    
        // is there is an existing chart, destroy it
        let chartStatus = Chart.getChart("bestRated"); // <canvas> id
        if (chartStatus) {
            chartStatus.destroy();
        }
        // console.log('X:', x);
        // console.log('Y:', y);

        createBarChart(x, y, "Highest Rated Oscar Movies", "bestRated");
    } catch (error) {
        console.error('Error initializing chart:', error);
    }

}

async function highestBudgetMovie(results) {
    try {
        console.log('Results:', results);

        const x = results.map(data => data.film);
        const y = results.map(data => data.budget);
    
        // is there is an existing chart, destroy it
        let chartStatus = Chart.getChart("highBudget"); // <canvas> id
        if (chartStatus) {
            chartStatus.destroy();
        }
        // console.log('X:', x);
        // console.log('Y:', y);

        createBarChart(x, y, "Highest Budget Oscar Movies", "highBudget" );
    } catch (error) {
        console.error('Error initializing chart:', error);
    }

}



async function handleBestRated(event) {
    
   console.log(this.value);

    try {
        const endpoint = `/api/best_rated_oscar_movies?category=${encodeURIComponent(this.value)}`;
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const result = await response.json();
        await bestRatedMovie(result);
    } catch (error) {
        console.error('Error:', error);
    }

}

async function handleHighestBudget(event) {

    console.log(this.value);

    try {
        const endpoint = `/api/highest_budget_movie?category=${encodeURIComponent(this.value)}`;
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const result = await response.json();
        await highestBudgetMovie(result);
    } catch (error) {
        console.error('Error:', error);

    }
}


// function to fetch data from the api
async function getOscarWinnerData(year, category) {
    const endpoint = `/api/winner?year=${encodeURIComponent(year)}&category=${encodeURIComponent(category)}`;
    const response = await fetch(endpoint);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
}

async function fetchNomineeData() {
    const response = await fetch("/api/nominee");
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
}

// function to plot charts
async function nomineeChart(results) {
    try {
        console.log('Results:', results);

        const x = results.map(data => data.year);
        const y = results.map(data => data.count);

        console.log('X:', x);
        console.log('Y:', y);

        // is there is an existing chart, destroy it
        if (nomineeChartval) {
            nomineeChartval.destroy();
            nomineeChartval = null;
        }

        createLineChart(x, y);
    } catch (error) {
        console.error('Error initializing chart:', error);
    }
}

function createLineChart(labels, data) {
    const ctx = document.getElementById('myChart').getContext('2d');

    nomineeChartval = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `Nominees for ${document.getElementById('oscar_nomination_category').value}`,
                data: data,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 3
            }]
        },
        options: {
            scales: {
                yAxes: [{ ticks: { beginAtZero: true } }]
            }
        }
    });
}

function createBarChart(labels, data, title, elementId ) {

    const ctx = document.getElementById(elementId).getContext('2d');
    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            indexAxis: 'y',
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

}