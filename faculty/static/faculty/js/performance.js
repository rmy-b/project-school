document.addEventListener("DOMContentLoaded", function () {

    const chartDiv = document.getElementById("chartData");

    if (chartDiv) {
        const labels = JSON.parse(chartDiv.dataset.labels);
        const values = JSON.parse(chartDiv.dataset.values);

        const ctx = document.getElementById("subjectChart").getContext("2d");

        new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Average Marks",
                    data: values,
                    backgroundColor: "#c8870a",
                    borderRadius:7,
                    barThickness:90
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true, max: 100 }
                }
            }
        });
    }

    // Scroll to At-Risk Students
    const viewBtn = document.getElementById("viewRiskBtn");
    const riskSection = document.getElementById("riskSection");

    if (viewBtn && riskSection) {
        viewBtn.addEventListener("click", function () {
            riskSection.scrollIntoView({ behavior: "smooth" });
        });
    }

});