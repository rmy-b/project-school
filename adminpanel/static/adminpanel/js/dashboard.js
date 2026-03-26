document.addEventListener("DOMContentLoaded", function () {

    // ================= PASS CHART =================
    const passCtx = document.getElementById("passChart").getContext("2d");

    new Chart(passCtx, {
        type: "bar",
        data: {
            labels: passChartData.map(i => i.class),
            datasets: [{
                label: "Pass %",
                data: passChartData.map(i => i.rate),
                backgroundColor: "#c47a00",
                borderRadius: 6,
                barThickness: 50
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,

            animation: {
                duration: 1200,
                easing: "easeOutQuart"
            },

            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: "#fff",
                    titleColor: "#333",
                    bodyColor: "#c47a00",
                    borderColor: "#eee",
                    borderWidth: 1
                }
            },

            layout: {
                padding: {
                    top: 10,
                    bottom: 50,
                    left: 10,
                    right: 10
                }
            },

            scales: {
                x: {
                    offset: true,   
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: "#666",
                        padding: 8
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        color: "#666"
                    },
                    grid: {
                        color: "#eee"
                    }
                }
            }
        }
    });


    // ================= RISK CHART =================
    const riskCtx = document.getElementById("riskChart").getContext("2d");

    // Gradient fill
    const gradient = riskCtx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, "rgba(196,122,0,0.35)");
    gradient.addColorStop(1, "rgba(196,122,0,0)");

    new Chart(riskCtx, {
        type: "line",
        data: {
            labels: riskChartData.map(i => i.class),
            datasets: [{
                label: "At Risk",
                data: riskChartData.map(i => i.risk),
                borderColor: "#c47a00",
                backgroundColor: gradient,
                fill: true,
                tension: 0.45,  
                pointRadius: 5,
                pointBackgroundColor: "#c47a00",
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,

            animation: {
                duration: 1400,
                easing: "easeOutQuart"
            },

            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: "#fff",
                    titleColor: "#333",
                    bodyColor: "#c47a00",
                    borderColor: "#eee",
                    borderWidth: 1,
                    displayColors: true
                }
            },

            layout: {
                padding: {
                    top: 10,
                    bottom: 50,
                    left: 10,
                    right: 10
                }
            },

            scales: {
                x: {
                    offset: true,   
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: "#666",
                        padding: 8
                    }
                },
                y: {
                    beginAtZero: true,
                    max:25,
                    ticks: {
                        stepSize: 5,
                        color: "#666"
                    },
                    grid: {
                        color: "#eee"
                    }
                }
            }
        }
    });

});