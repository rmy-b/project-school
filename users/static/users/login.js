const roles = document.querySelectorAll(".role-box");
const hiddenInput = document.getElementById("selectedRole");

roles.forEach(role => {
    role.addEventListener("click", () => {

        roles.forEach(r => r.classList.remove("active"));

        role.classList.add("active");

        hiddenInput.value = role.getAttribute("data-role");
    });
});
