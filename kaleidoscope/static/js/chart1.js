// Word count vs time chart
const ctx = document.getElementById('linechart');
console.log("mf");

function addLineChart(){
    return new Chart(ctx, {
        type: 'line',
        data: {
        labels: yeardata,
        datasets: [{
            label: 'Your Word Count Over Time!',
            data: worddata,
            borderWidth: 1
        }]
        },
        options: {
        scales: {
            y: {
            beginAtZero: true
            }
        }
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    addLineChart();
});
console.log("you gay");