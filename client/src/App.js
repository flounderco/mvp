import React, { useState, useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import './App.css';

function App() {
  const [chartData, setChartData] = useState(null);
  const chartRef = useRef(null);
  useEffect(() => {
    fetchDefaultData();
  }, []);

  const fetchDefaultData = async () => {
    try {
        const response = await fetch('http://localhost:5000/default-data');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setChartData(data);
    } catch (error) {
        console.error('Error fetching default data:', error);
        alert('Failed to fetch default data. Check the console.', error);
    }
  };

  const handleFileUpload = async (event) => {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('file', file);

      try {
          const response = await fetch('http://localhost:5000/upload', {
              method: 'POST',
              body: formData,
          });

          if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
          }

          const data = await response.json();
          setChartData(data);

      } catch (error) {
          console.error('Error uploading file:', error);
          alert('Failed to upload or process file. Check the console.');
      }
  };

  useEffect(() => {
      if (chartData) {
          const ctx = document.getElementById('myChart').getContext('2d');

          if (chartRef.current) {
              chartRef.current.destroy();
          }

          const datasets = [];
          const scenarioColors = {
              'Base': 'rgba(54, 162, 235, 0.8)',
              'Upside': 'rgba(255, 99, 132, 0.8)',
              'Downside': 'rgba(255, 205, 86, 0.8)'
          };
          const scenarioBorderColors = {
              'Base': 'rgba(54, 162, 235, 1)',
              'Upside': 'rgba(255, 99, 132, 1)',
              'Downside': 'rgba(255, 205, 86, 1)'
          };

          for (let i = 0; i < chartData.scenarios.length; i++) {
              const scenario = chartData.scenarios[i];
              datasets.push({
                  label: scenario,
                  data: chartData.revenue_data[scenario],
                  borderColor: scenarioBorderColors[scenario] || 'rgba(0, 0, 0, 1)',
                  fill: false
              });
          }

          chartRef.current = new Chart(ctx, {
              type: 'line',
              data: {
                  labels: chartData.labels,
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
  }, [chartData]);

  return (
      <div className="App">
          <h1>Upload Excel File</h1>
          <input type="file" id="excelFile" accept=".xlsx" onChange={handleFileUpload} />
          <div id="chart-container">
              <canvas id="myChart"></canvas>
          </div>
      </div>
  );
}

export default App;
