function create_chart_object(data, element_id, options) {
    const labels = Object.keys(data);

    const players = new Set();
    for (const key in data) {
        const innerDict = data[key];
        Object.keys(innerDict).forEach(innerKey => players.add(innerKey));
    }

    const persons = Array.from(players);
    const datasets = persons.map(person => {
        return {
            label: person,
            data: labels.map(t => data[t][person]),
            fill: false,
            // tension: 0.2
        };
    });

    const config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: options
    };

    new Chart(
        document.getElementById(element_id),
        config
    );
}

const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top'
        }
    },
    scales: {
        x: {
            title: {
                display: true,
                text: 'Tournament'
            }
        },
        y: {
            // title: {
            //     display: true,
            //     text: 'Place'
            // },
            reverse: false,
            ticks: {
                stepSize: 1
            },
            beginAtZero: true,
        }
    },
    // maintainAspectRatio: false  // Allows independent height control
}

async function generate_graph(json_file_path, element_id, options) {
    fetch(json_file_path)
        .then(response => {
            if (!response.ok) {
                throw new Error(`error: ${response}`);
            }
            return response.json();
        })
        .then(data => {
            create_chart_object(data, element_id, options);
        })
        .catch(error => {
            console.error('Error fetching JSON:', error);
        });
}

function generate_boxes(number_of_tiers) {
    var annotations = {}

    for (let i = 0; i < number_of_tiers; i += 2) {
        annotations['box' + i] = {
            type: 'box',
            yMin: i / number_of_tiers,
            yMax: (i + 1) / number_of_tiers,
            backgroundColor: 'rgba(0,0,0,0.1)',
            borderWidth: 0
        }
    }
    return annotations;
}


var options1 = structuredClone(options);
options1.scales.y.reverse = true;
options1.scales.y.beginAtZero = false;
generate_graph('docs/assets/places_per_tournament.json', 'places_per_tournament', options1);

generate_graph('docs/assets/points_per_tournament.json', 'points_per_tournament', options);
generate_graph('docs/assets/points_per_match_per_tournament.json', 'points_per_match_per_tournament', options);
generate_graph('docs/assets/coefficient_per_tournament.json', 'coefficient_per_tournament', options);


var options2 = structuredClone(options);
options2.plugins.annotation = {
    annotations: generate_boxes(4)
};

generate_graph('docs/assets/five_tournament_rolling_coefficient.json', 'five_tournament_rolling_coefficient', options2);

var options_gd = structuredClone(options);
options_gd.plugins.annotation = {
    annotations: {
        center: {
            type: 'line',
            yMin: 0,
            yMax: 0,
        }
    }
}

generate_graph('docs/assets/goal_difference.json', 'goal_difference', options_gd);
generate_graph('docs/assets/goals_for.json', 'goals_for', options);
generate_graph('docs/assets/goals_against.json', 'goals_against', options);
generate_graph('docs/assets/all_tournament_rolling_coefficient.json', 'all_tournament_rolling_coefficient', options);
