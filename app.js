let myChartInstance = null; // Store chart instance globally

async function uploadFile() {
    const fileInput = document.getElementById('excelFile');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:5000/upload', {  // Adjust URL if needed
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            alert(`Error: ${data.error}`);
            return;
        }

        updateChart(data);

    } catch (error) {
        console.error('Error uploading file:', error);
        alert('Failed to upload or process file. Check the console.');
    }
}

function updateChart(data) {
    const ctx = document.getElementById('myChart').getContext('2d');

    if (myChartInstance) {
        myChartInstance.destroy();
    }

    const datasets = [];
    const scenarioColors = {
        'Base': 'rgba(54, 162, 235, 0.8)',    // Blue
        'Upside': 'rgba(255, 99, 132, 0.8)',   // Red
        'Downside': 'rgba(255, 205, 86, 0.8)'  // Yellow
    };
    const scenarioBorderColors = {
        'Base': 'rgba(54, 162, 235, 1)',
        'Upside': 'rgba(255, 99, 132, 1)',
        'Downside': 'rgba(255, 205, 86, 1)'
    };

    for (let i = 0; i < data.scenarios.length; i++) {
        const scenario = data.scenarios[i];
        datasets.push({
            label: scenario,
            data: data.revenue_data[scenario],
            borderColor: scenarioBorderColors[scenario] || 'rgba(0, 0, 0, 1)',
            fill: false // Do not fill area under the lines
        });
    }

    myChartInstance = new Chart(ctx, {
        type: 'line', // Changed chart type to line
        data: {
            labels: data.labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}