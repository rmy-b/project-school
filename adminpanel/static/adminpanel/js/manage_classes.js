let oldSections = [];
let oldSubjects = [];
let confirmCallback = null;

const confirmPopup = document.getElementById("confirmPopup");
const confirmMessage = document.getElementById("confirmMessage");
const confirmOkBtn = document.getElementById("confirmOkBtn");

document.getElementById("addClassBtn")
.addEventListener("click", function(){

});


// ADD CLASS POPUP
const addBtn = document.getElementById("addClassBtn");
const addPopup = document.getElementById("addClassPopup");

addBtn.onclick = () => addPopup.style.display = "flex";

function closeAddClassPopup() {
    addPopup.style.display = "none";
}


// SECTION POPUP
const sectionPopup = document.getElementById("sectionPopup");

document.querySelectorAll(".manage-section-btn")
.forEach(btn => {
    btn.addEventListener("click", function() {

        const classId = this.dataset.classId;
        const sections = this.dataset.sections.split(",");
        oldSections = sections;

        // set class id
        document.getElementById("sectionClassId").value = classId;

        // 🔥 RESET ALL CHECKBOXES FIRST
        document.querySelectorAll("#sectionPopup input[type=checkbox]")
        .forEach(cb => cb.checked = false);

        // 🔥 CHECK EXISTING SECTIONS
        document.querySelectorAll("#sectionPopup input[type=checkbox]")
        .forEach(cb => {
            if (sections.includes(cb.value)) {
                cb.checked = true;
            }
        });

        sectionPopup.style.display = "flex";
    });
});

document.querySelector("#sectionPopup form")
.addEventListener("submit", function(e){

    const checked = [];
    
    document.querySelectorAll("#sectionPopup input[type=checkbox]:checked")
    .forEach(cb => checked.push(cb.value));

    // 🔥 find removed sections
    const removed = oldSections.filter(sec => sec && !checked.includes(sec));

    if (removed.length > 0){
        e.preventDefault(); // stop first

        showConfirm(
            "Delete sections: " + removed.join(", ") + " ?",
            function(){
                e.target.submit(); // ✅ submit manually
            }
        );
    }
});

function closeSectionPopup() {
    sectionPopup.style.display = "none";
}


// SUBJECT POPUP
const subjectPopup = document.getElementById("subjectPopup");

document.querySelectorAll(".manage-subject-btn")
.forEach(btn => {
    btn.addEventListener("click", function() {

        const classId = this.dataset.classId;
        const subjects = this.dataset.subjects.split(",");
        oldSubjects = subjects;

        document.getElementById("subjectClassId").value = classId;

        // reset
        document.querySelectorAll("#subjectPopup input[type=checkbox]")
        .forEach(cb => cb.checked = false);

        // check existing
        document.querySelectorAll("#subjectPopup input[type=checkbox]")
        .forEach(cb => {
            if (subjects.includes(cb.value)) {
                cb.checked = true;
            }
        });

        subjectPopup.style.display = "flex";
    });
});

document.querySelector("#subjectPopup form")
.addEventListener("submit", function(e){

    const checked = [];

    document.querySelectorAll("#subjectPopup input[type=checkbox]:checked")
    .forEach(cb => checked.push(cb.value));

    const removed = oldSubjects.filter(sub => sub && !checked.includes(sub));

    if (removed.length > 0){
        e.preventDefault();

        showConfirm(
            "Remove subjects: " + removed.join(", ") + " ?",
            function(){
                e.target.submit();
            }
        );

    }
});

function closeSubjectPopup() {
    subjectPopup.style.display = "none";
}


// DELETE POPUP

document.querySelectorAll(".delete-class-btn")
.forEach(btn => {
    btn.addEventListener("click", function() {
        document.getElementById("deleteClassId").value = this.dataset.classId;
        deletePopup.style.display = "flex";
    });
});

function closeDeletePopup() {
    deletePopup.style.display = "none";
}

function showConfirm(message, callback){
    confirmMessage.innerText = message;
    confirmCallback = callback;
    confirmPopup.style.display = "flex";
}

function closeConfirmPopup(){
    confirmPopup.style.display = "none";
}

confirmOkBtn.onclick = function(){
    if(confirmCallback){
        confirmCallback();
    }
    closeConfirmPopup();
};


// ===== CLOSE POPUP ON OUTSIDE CLICK =====
window.addEventListener("click", function(e){

    if(e.target === sectionPopup){
        sectionPopup.style.display = "none";
    }

    if(e.target === subjectPopup){
        subjectPopup.style.display = "none";
    }

    if(e.target === addPopup){
        addPopup.style.display = "none";
    }

    if(e.target === confirmPopup){
        confirmPopup.style.display = "none";
    }

});