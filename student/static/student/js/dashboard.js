document.addEventListener("DOMContentLoaded", function () {

document.getElementById("menuToggle").onclick = function(){
    document.getElementById("sidebar").classList.toggle("hide");
};

const gridStyle = {
    color: "rgba(0,0,0,0.05)",
    borderDash: [3,4]
};

new Chart(document.getElementById("marksChart"), {
    type: "bar",
    data: {
        labels: subjectNames,
        datasets: [{
            data: subjectScores,
            backgroundColor: ["#FCD34D","#FBBF24","#F59E0B","#D97706","#B45309"],
            borderRadius: 7,
            barThickness: 50
        }]
    },
    options: {
        plugins:{ legend:{display:false}},
        scales:{
            y:{ beginAtZero:true, max:100, grid:gridStyle },
            x:{ grid:{display:false} }
        }
    }
});
// #3B82F6"
new Chart(document.getElementById("attendanceChart"), {
    type: "bar",
    data: {
        labels: attendanceMonths,
        datasets: [{
            data: attendancePercentages,
            backgroundColor:"#8ca5cc",
            borderRadius: 7,
            barThickness: 50
        }]
    },
    options:{
        plugins:{ legend:{display:false}},
        scales:{
            y:{ beginAtZero:true, max:100, grid:gridStyle },
            x:{ grid:{display:false} }
        }
    }
});

});
