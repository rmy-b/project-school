// PASS CHART
const passLabels = passChartData.map(i => i.class);
const passValues = passChartData.map(i => i.rate);

new Chart(document.getElementById("passChart"), {
    type: "bar",
    data: {
        labels: passLabels,
        datasets: [{
            data: passValues,
            backgroundColor: "#c47a00",
            barPercentage: 0.5
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});


// RISK CHART (BAR is better than line here)
const riskLabels = riskChartData.map(i => i.class);
const riskValues = riskChartData.map(i => i.risk);

new Chart(document.getElementById("riskChart"), {
    type: "line",
    data: {
        labels: riskLabels,
        datasets: [{
            data: riskValues,
            backgroundColor: "#c4a700",
            borderColor:"#bb1010",
            barPercentage: 0.5
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        
    }
});