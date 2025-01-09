function create_chart_object(data, element_id, reverse) {
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
            data: labels.map(t => data[t][person] || null), // Handle null values
            fill: false
        };
    });

    const config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                },
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Tournament'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Place'
                    },
                    reverse: reverse,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    };

    new Chart(
        document.getElementById(element_id),
        config
    );
}

async function generate_graph(json_file_path, element_id, reverse = true) {
    fetch(json_file_path)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            create_chart_object(data, element_id, reverse);
        })
        .catch(error => {
            console.error('Error fetching JSON:', error);
        });


}

generate_graph('docs/assets/place_per_tournament.json', 'place_per_tournament', true);
generate_graph('docs/assets/points_per_tournament.json', 'points_per_tournament', false);
generate_graph('docs/assets/points_per_match_per_tournament.json', 'points_per_match_per_tournament', false);
