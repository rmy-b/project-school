const openBtn = document.getElementById("openModal");
const closeBtn = document.getElementById("closeModal");
const modal = document.getElementById("attendanceModal");

if (openBtn) {
    openBtn.onclick = () => modal.style.display = "flex";
}

if (closeBtn) {
    closeBtn.onclick = () => modal.style.display = "none";
}

window.onclick = function(e) {
    if (e.target === modal) {
        modal.style.display = "none";
    }
};