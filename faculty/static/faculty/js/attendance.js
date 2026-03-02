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

/* LIVE TOGGLE UPDATE */
document.querySelectorAll('.toggle input').forEach(toggle => {
    toggle.addEventListener('change', function () {
        const row = this.closest('tr');
        const statusText = row.querySelector('.status-text');

        const presentCard = document.querySelector('.summary .present strong');
        const absentCard = document.querySelector('.summary .absent strong');

        let presentCount = parseInt(presentCard.innerText);
        let absentCount = parseInt(absentCard.innerText);

        if (this.checked) {
            statusText.innerText = "Present";
            statusText.style.color = "#0f9d58";
            presentCard.innerText = presentCount + 1;
            absentCard.innerText = absentCount - 1;
        } else {
            statusText.innerText = "Absent";
            statusText.style.color = "#d93025";
            presentCard.innerText = presentCount - 1;
            absentCard.innerText = absentCount + 1;
        }
    });
});