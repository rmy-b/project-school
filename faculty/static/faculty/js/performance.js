document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // SUBJECT BAR CHART
    // =========================
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
                    borderRadius: 7,
                    barThickness: 70
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    // =========================
    // PIE CHART
    // =========================
    const clusterDiv = document.getElementById("clusterChartData");

    if (clusterDiv) {
        const top = Number(clusterDiv.dataset.top || 0);
        const average = Number(clusterDiv.dataset.average || 0);
        const needs = Number(clusterDiv.dataset.needs || 0);

        const total = top + average + needs;

        // Prevent empty pie chart crash
        if (total > 0) {
            const pieCanvas = document.getElementById("clusterPieChart");

            if (pieCanvas) {
                const pieCtx = pieCanvas.getContext("2d");

                new Chart(pieCtx, {
                    type: "pie",
                    data: {
                        labels: ["Top Performers", "Average Students", "Needs Attention"],
                        datasets: [{
                            data: [top, average, needs],
                            backgroundColor: [
                                "#4CAF50",
                                "#FFC107",
                                "#F44336"
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        layout: { 
                            padding:10
                        },
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return `${context.label}: ${context.raw} students`;
                                    }
                                }
                            }
                        }
                    }
                });
            }
        }
    }

    // =========================
    // SCROLL TO RISK TABLE
    // =========================
    const viewBtn = document.getElementById("viewRiskBtn");
    const riskSection = document.getElementById("riskSection");

    if (viewBtn && riskSection) {
        viewBtn.addEventListener("click", function () {
            riskSection.scrollIntoView({ behavior: "smooth" });
        });
    }

});