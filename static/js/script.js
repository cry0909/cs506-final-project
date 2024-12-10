// Function to render a chart using Chart.js
function renderChart(chartId, chartData) {
    const ctx = document.getElementById(chartId).getContext('2d');
    new Chart(ctx, {
        type: 'line', // Line chart type
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
                        text: chartData.xLabel || 'X-Axis',
                    },
                },
                y: {
                    title: {
                        display: true,
                        text: chartData.yLabel || 'Y-Axis',
                    },
                },
            },
        },
    });
}

// Fetch and render all charts dynamically from `data-*` attributes
document.addEventListener('DOMContentLoaded', () => {
    // Select all canvas elements with `data-chart` attributes
    const chartElements = document.querySelectorAll('canvas[data-chart]');
    chartElements.forEach((chartElement) => {
        const chartId = chartElement.id; // Chart ID (e.g., 'avgWaitTimeChart', 'predVsActualChart')
        const chartData = JSON.parse(chartElement.getAttribute('data-chart')); // Data for the chart
        renderChart(chartId, chartData);
    });
});
