// Mood vs time chart
const ctx2 = document.getElementById('moodchart');
new Chart(ctx2, {
    type: 'line',
    data: {
    labels: Array(mooddata.length).fill('*'),
    datasets: [{
        label: 'Your Mood Over Time!',
        data: mooddata,
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