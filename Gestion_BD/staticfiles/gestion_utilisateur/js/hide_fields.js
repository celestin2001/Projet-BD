document.addEventListener("DOMContentLoaded", function() {
    function toggleFields() {
        var roleField = document.querySelector("#id_role");
        var experienceField = document.querySelector("#id_annee_experience")?.closest('.form-row');
        var bioField = document.querySelector("#id_bio")?.closest('.form-row');
        var validAuteurField = document.querySelector("#id_valid_auteur")?.closest('.form-row');

        if (roleField) {
            if (roleField.value === "lecteur") {
                if (experienceField) experienceField.style.display = "none";
                if (bioField) bioField.style.display = "none";
                if (validAuteurField) validAuteurField.style.display = "none";
            } else {
                if (experienceField) experienceField.style.display = "";
                if (bioField) bioField.style.display = "";
                if (validAuteurField) validAuteurField.style.display = "";
            }
        }
    }

    // Exécuter au chargement
    toggleFields();

    // Exécuter à chaque changement du champ rôle
    document.querySelector("#id_role").addEventListener("change", toggleFields);
});
