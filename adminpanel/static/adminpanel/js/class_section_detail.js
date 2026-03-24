document.addEventListener("DOMContentLoaded", function(){

    const popup = document.getElementById("editPopup");
    const subjectInput = document.getElementById("popupSubjectId");
    const inchargeInput = document.getElementById("popupIsIncharge");
    const title = document.getElementById("popupTitle");

    const dropdownSelected = document.getElementById("dropdownSelected");
    const dropdownOptions = document.getElementById("dropdownOptions");
    const facultyInput = document.getElementById("facultyInput");

    const subjectNameMap = {};

    // MAP SUBJECT ID → NAME
    document.querySelectorAll("tr").forEach(row => {
        const nameCell = row.children[0];
        const btn = row.querySelector(".edit-btn");

        if(btn && nameCell){
            subjectNameMap[btn.dataset.subject] = nameCell.innerText;
        }
    });

    // OPEN POPUP
    document.querySelectorAll(".edit-btn").forEach(btn => {
        btn.addEventListener("click", function(){

            const subjectId = this.dataset.subject;
            const isIncharge = this.dataset.incharge === "true";
            const facultyId = this.dataset.faculty;

            if(isIncharge){
                title.innerText = "Edit Class Incharge";
                subjectInput.value = "";
                inchargeInput.value = "true";
            } else {
                title.innerText = "Change Faculty for " + subjectNameMap[subjectId];
                subjectInput.value = subjectId;
                inchargeInput.value = "false";
            }

            // RESET DROPDOWN
            document.querySelectorAll(".dropdown-item").forEach(item => {
                item.classList.remove("selected");
            });

            if(facultyId){
                const selectedItem = document.querySelector(`.dropdown-item[data-value='${facultyId}']`);
                if(selectedItem){
                    selectedItem.classList.add("selected");
                    dropdownSelected.innerText = selectedItem.innerText;
                    facultyInput.value = facultyId;
                    dropdownSelected.classList.add("filled");
                }
            } else {
                dropdownSelected.innerText = "Select Faculty";
                facultyInput.value = "";
                dropdownSelected.classList.remove("filled");
            }

            popup.style.display = "flex";
        });
    });

    // TOGGLE DROPDOWN
    dropdownSelected.addEventListener("click", function(){
        dropdownOptions.classList.toggle("show");
    });

    // SELECT OPTION
    document.querySelectorAll(".dropdown-item").forEach(item => {
        item.addEventListener("click", function(){

            // REMOVE OLD SELECTION
            document.querySelectorAll(".dropdown-item").forEach(i => i.classList.remove("selected"));

            // SET NEW
            this.classList.add("selected");

            dropdownSelected.innerText = this.innerText;
            facultyInput.value = this.dataset.value;
            dropdownSelected.classList.add("filled");

            dropdownOptions.classList.remove("show");
        });
    });

    // CLOSE POPUP
    window.closePopup = function(){
        popup.style.display = "none";
    };

    // OUTSIDE CLICK
    window.addEventListener("click", function(e){
        if(e.target === popup){
            popup.style.display = "none";
        } else if (!dropdownSelected.contains(e.target) && !dropdownOptions.contains(e.target)) {
            dropdownOptions.classList.remove("show");
        }
    });

    // AUTO HIDE ERROR
    const errorBox = document.getElementById("errorBox");

    if(errorBox){
        setTimeout(() => {
            errorBox.style.opacity = "0";
            errorBox.style.transform = "translateY(-10px)";

            setTimeout(() => {
                errorBox.style.display = "none";
            }, 300);
        }, 5000);
    }

});