document.querySelectorAll(".edit-btn").forEach(btn => {
    btn.addEventListener("click", function () {
        const row = this.closest("tr");
        const internalInput = row.querySelector('input[name^="internal_"]');
        const externalInput = row.querySelector('input[name^="external_"]');

        const internalText = row.querySelector(".mark-text");
        const externalText = row.querySelectorAll(".mark-text")[1];


        const totalCell = row.querySelector(".total");

         // EDIT MODE
        if (internalInput.style.display === "none") {
            internalInput.style.display = "inline-block";
            externalInput.style.display = "inline-block";

            internalText.style.display = "none";
            externalText.style.display = "none";

            this.innerHTML = '<img src="/static/faculty/icons/save.svg" width="18">';
        }
        // SAVE MODE
        else {
            let internal = parseFloat(internalInput.value || 0);
            let external = parseFloat(externalInput.value || 0);

            if (internal > 30) {
                alert("Internal marks cannot be more than 30");
                return;
            }
            if (external > 70) {
                alert("External marks cannot be more than 70");
                return;
            }

            let total = internal + external;
            totalCell.innerText = total;

            internalText.innerText = internal;
            externalText.innerText = external;

            internalInput.style.display = "none";
            externalInput.style.display = "none";

            internalText.style.display = "inline";
            externalText.style.display = "inline";

            this.innerHTML = '<img src="/static/faculty/icons/pencil.svg" width="18">';
        }
    });
});