const pwShowHide = document.querySelectorAll(".eye-icon");


pwShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener("click", () => {
        let pwFields = eyeIcon.parentElement.parentElement.querySelectorAll(".password");

        pwFields.forEach(password => {
            if (password.type === "password") {
                password.type = "text";
                eyeIcon.classList.replace("fa-eye-slash", "fa-eye");
                return;
            }
            password.type = "password";
            eyeIcon.classList.replace("fa-eye", "fa-eye-slash");
        })

    })
})