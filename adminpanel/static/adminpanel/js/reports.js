// Scroll to risk students table
document.querySelector(".view-btn").onclick = function () {
    document.getElementById("riskTable").scrollIntoView({
        behavior: "smooth"
    });
};



// -----------------------------
// Pass Rate Chart
// -----------------------------

const passLabels = passChartData.map(item => item.subject);
const passValues = passChartData.map(item => item.pass_rate);

new Chart(document.getElementById("passChart"), {

type: "bar",

data: {

labels: passLabels,

datasets: [{
label: "Pass Rate %",
data: passValues,
backgroundColor: "#c47a00",
hoverBackgroundColor:"#e39500",
borderRadius:6
}]

},

options: {

responsive:true,
maintainAspectRatio:false,

animation:{
duration:1200,
easing:'easeOutQuart'
},

plugins:{
legend:{display:false},

tooltip:{
backgroundColor:"#333",
titleColor:"#fff",
bodyColor:"#fff",
padding:10,
cornerRadius:6,
callbacks:{
label:function(context){
return context.parsed.y + "% pass rate";
}
}
}

},

scales:{
y:{
beginAtZero:true,
max:100
}
}

}

});
// -----------------------------
// Risk Students Chart
// -----------------------------

const riskLabels = riskChartData.map(item => item.subject);
const riskValues = riskChartData.map(item => item.risk);
new Chart(document.getElementById("riskChart"), {


type:'line',
options:{
indexAxis:'x'
},

data:{

labels:riskLabels,

datasets:[{

label:"At Risk Students",
data:riskValues,

backgroundColor:"#c47a00",
hoverBackgroundColor:"#c47a00",
borderRadius:4,
tension:0.5

}]

},

options:{
responsive:true,
maintainAspectRatio:false,

animation:{
duration:1200,
easing:'easeOutQuart'
},

plugins:{
legend:{display:false},

tooltip:{
callbacks:{
label:function(context){
return context.parsed.y + " students at risk";
}
}
}

}

}

});