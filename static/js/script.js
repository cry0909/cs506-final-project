document.addEventListener('DOMContentLoaded', () => {
    const predictButton = document.getElementById('predict-button');
    const resultMessage = document.getElementById('result-message');

    // Handle prediction on button click
    if (predictButton) {
        predictButton.addEventListener('click', async () => {
            const day = document.getElementById('day').value;
            const time = document.getElementById('time').value;

            if (!day || !time) {
                resultMessage.textContent = "Please select a day and time.";
                return;
            }

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ day, time }),
                });

                if (!response.ok) {
                    const error = await response.json();
                    resultMessage.textContent = error.error || "An error occurred.";
                    return;
                }

                const result = await response.json();
                resultMessage.textContent = `The predicted wait time for ${result.day} at ${result.time}:00 is ${result.predicted_wait_time} minutes.`;
            } catch (error) {
                resultMessage.textContent = "Failed to fetch prediction. Please try again.";
            }
        });
    }

    // Function to render a chart using Chart.js
    function renderChart(chartId, chartData) {
        const ctx = document.getElementById(chartId).getContext('2d');
        new Chart(ctx, {
            type: 'line', // Chart type
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                    },
                    tooltip: {
                        enabled: true,
                    },
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Hour',
                        },
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Wait Time (mins)',
                        },
                    },
                },
            },
        });
    }

    // Dynamically render all charts from the page's data-chart attributes
    document.querySelectorAll('canvas[data-chart]').forEach((canvas) => {
        const chartData = JSON.parse(canvas.getAttribute('data-chart'));
        renderChart(canvas.id, chartData);
    });
});
