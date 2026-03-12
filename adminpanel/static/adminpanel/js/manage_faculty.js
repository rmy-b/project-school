const openBtn = document.getElementById("openAddModal");
const modal = document.getElementById("addFacultyModal");
const closeBtn = document.getElementById("closeModal");

openBtn.onclick = function() {
    modal.style.display = "flex";
}

closeBtn.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
const toggles = document.querySelectorAll(".faculty-toggle");

toggles.forEach(toggle => {

    toggle.addEventListener("change", function() {

        const facultyId = this.dataset.id;
        const status = this.checked;

        fetch("/adminpanel/toggle-faculty-status/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                faculty_id: facultyId,
                status: status
            })
        })
        .then(response => response.json())
        .then(data => {

            if(data.success){
                console.log("Status updated");
            } else {
                alert("Something went wrong");
            }

        });

    });

});
function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }

        }

    }

    return cookieValue;

}

const editButtons = document.querySelectorAll(".edit-btn");
const editModal = document.getElementById("editFacultyModal");

editButtons.forEach(btn => {

btn.addEventListener("click", function(){

document.getElementById("editFacultyId").value = this.dataset.id;
document.getElementById("editName").value = this.dataset.name;
document.getElementById("editQualification").value = this.dataset.qualification;
document.getElementById("editUsername").value = this.dataset.username;

editModal.style.display = "flex";

});

});

const resetBtn = document.getElementById("resetPasswordBtn");
const passwordSection = document.getElementById("newPasswordSection");

resetBtn.onclick = function(){

passwordSection.style.display = "block";
}
// CLOSE EDIT MODAL
const closeEditBtn = document.querySelector(".close-edit");

closeEditBtn.onclick = function() {
    editModal.style.display = "none";
}

// CANCEL BUTTON
const cancelBtn = document.querySelector(".cancel-btn");

cancelBtn.onclick = function() {
    editModal.style.display = "none";
}


// DELETE MODAL
const deleteButtons = document.querySelectorAll(".delete-btn");
const deleteModal = document.getElementById("deleteFacultyModal");

const deleteFacultyId = document.getElementById("deleteFacultyId");
const deleteMessage = document.getElementById("deleteMessage");

deleteButtons.forEach(btn => {

btn.addEventListener("click", function(){

const facultyId = this.dataset.id;
const facultyName = this.dataset.name;

deleteFacultyId.value = facultyId;

deleteMessage.innerText =
"Do you want to delete faculty '" + facultyName + "' ?";

deleteModal.style.display = "flex";

});

});


// CLOSE DELETE MODAL
const closeDeleteBtn = document.querySelector(".close-delete");

closeDeleteBtn.onclick = function(){
deleteModal.style.display = "none";
}


// CANCEL DELETE
const cancelDeleteBtn = document.querySelector(".cancel-delete-btn");

cancelDeleteBtn.onclick = function(){
deleteModal.style.display = "none";
}