document.addEventListener("DOMContentLoaded", function () {

const toggleBtn = document.getElementById("menuToggle");

if(toggleBtn){
    toggleBtn.onclick = function(){
        document.getElementById("sidebar").classList.toggle("hide");
    };
}

const gridStyle = {
    color: "rgba(0,0,0,0.05)",
    borderDash: [3,4]
};

// MARKS CHART
const marksChart = document.getElementById("marksChart");

if(marksChart && typeof subjectNames !== "undefined" && typeof subjectScores !== "undefined"){
    new Chart(marksChart, {
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
}

// ATTENDANCE CHART
const attendanceChart = document.getElementById("attendanceChart");

if(attendanceChart && typeof attendanceMonths !== "undefined" && typeof attendancePercentages !== "undefined"){
    new Chart(attendanceChart, {
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
}

});