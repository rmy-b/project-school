document.addEventListener("DOMContentLoaded", function () {

const classDropdown = document.getElementById("classDropdown");
const sectionDropdown = document.getElementById("sectionDropdown");

const popup = document.getElementById("studentPopup");
const addStudentBtn = document.getElementById("addStudentBtn");

const popupClass = document.getElementById("popupClass");
const popupSection = document.getElementById("popupSection");

const selectedText = document.getElementById("selectedClassSection");


// --------------------
// CLASS CHANGE
// --------------------

classDropdown.addEventListener("change", function(){

    const classId = this.value;

    sectionDropdown.innerHTML = "<option value=''>Select Section</option>";

    fetch(`/adminpanel/get-sections/?class_id=${classId}`)
    .then(response => response.json())
    .then(data => {

        data.forEach(section => {

            const option = document.createElement("option");

            option.value = section.id;
            option.textContent = section.name;

            sectionDropdown.appendChild(option);

        });

    });

});


// --------------------
// SECTION CHANGE
// AUTO FILTER
// --------------------

sectionDropdown.addEventListener("change", function(){

    const classId = classDropdown.value;
    const sectionId = this.value;

    if(classId && sectionId){

        const url = new URL(window.location.href);

        url.searchParams.set("class", classId);
        url.searchParams.set("section", sectionId);

        window.location.href = url.toString();

    }

});


// --------------------
// OPEN POPUP
// --------------------

addStudentBtn.addEventListener("click", function(){

    const classId = classDropdown.value;
    const sectionId = sectionDropdown.value;

    const classText =
    classDropdown.options[classDropdown.selectedIndex].text;

    const sectionText =
    sectionDropdown.options[sectionDropdown.selectedIndex].text;

    if(!classId || !sectionId){

        alert("Please select Class and Section first");
        return;

    }

    popupClass.value = classId;
    popupSection.value = sectionId;

    selectedText.innerText =
    `Class: ${classText} | Section: ${sectionText}`;

    popup.style.display = "flex";

});

});


// --------------------
// CLOSE POPUP  
// --------------------

function closePopup(){

document.getElementById("studentPopup").style.display = "none";

}

// =============================
// EDIT STUDENT POPUP
// =============================

const editPopup = document.getElementById("editStudentPopup");

const editStudentId = document.getElementById("editStudentId");
const editRoll = document.getElementById("editRoll");
const editName = document.getElementById("editName");
const editUsername = document.getElementById("editUsername");

const resetPasswordBtn = document.getElementById("resetPasswordBtn");
const newPasswordField = document.getElementById("newPasswordField");


// OPEN EDIT POPUP

document.querySelectorAll(".edit-btn").forEach(button => {

button.addEventListener("click", function(){

const studentId = this.dataset.studentId;
const roll = this.dataset.roll;
const name = this.dataset.name;
const username = this.dataset.username;

editStudentId.value = studentId;
editRoll.value = roll;
editName.value = name;
editUsername.value = username;

editPopup.style.display = "flex";

});

});


// CLOSE EDIT POPUP

function closeEditPopup(){

editPopup.style.display = "none";

}


// RESET PASSWORD BUTTON

resetPasswordBtn.addEventListener("click", function(){

newPasswordField.style.display = "block";

});


// =============================
// DELETE STUDENT POPUP
// =============================

const deletePopup = document.getElementById("deletePopup");
const deleteStudentId = document.getElementById("deleteStudentId");

document.querySelectorAll(".delete-btn").forEach(button => {

button.addEventListener("click", function(){

const studentId = this.dataset.studentId;

deleteStudentId.value = studentId;

deletePopup.style.display = "flex";

});

});


function closeDeletePopup(){

deletePopup.style.display = "none";

}


// =============================
// TOGGLE ACTIVE / INACTIVE
// =============================

document.querySelectorAll(".status-toggle").forEach(toggle => {

toggle.addEventListener("change", function(){

const studentId = this.dataset.studentId;

fetch("/adminpanel/toggle-student-status/", {

method: "POST",

headers: {
"Content-Type": "application/x-www-form-urlencoded",
"X-CSRFToken": getCSRFToken()
},

body: `student_id=${studentId}`

});

});

});


// GET CSRF TOKEN

function getCSRFToken() {

return document.querySelector('[name=csrfmiddlewaretoken]').value;

}

// =============================
// CLOSE POPUP WHEN CLICK OUTSIDE
// =============================

window.addEventListener("click", function(event){

const addPopup = document.getElementById("studentPopup");
const editPopup = document.getElementById("editStudentPopup");
const deletePopup = document.getElementById("deletePopup");

if(event.target === addPopup){
addPopup.style.display = "none";
}

if(event.target === editPopup){
editPopup.style.display = "none";
}

if(event.target === deletePopup){
deletePopup.style.display = "none";
}

});

