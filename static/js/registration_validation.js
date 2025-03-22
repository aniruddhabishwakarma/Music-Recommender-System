
document.addEventListener("DOMContentLoaded", function () {
    const usernameInput = document.querySelector("input[name='username']");
    const emailInput = document.querySelector("input[name='email']");
    const contactInput = document.querySelector("input[name='contact_number']");
    const password1 = document.querySelector("input[name='password1']");
    const password2 = document.querySelector("input[name='password2']");
    const registerBtn = document.querySelector("button[form='registration-form']");

    const usernameMsg = document.createElement("small");
    const emailMsg = document.createElement("small");
    const contactMsg = document.createElement("small");
    const passwordMsg = document.createElement("small");

    usernameInput.parentNode.appendChild(usernameMsg);
    emailInput.parentNode.appendChild(emailMsg);
    contactInput.parentNode.appendChild(contactMsg);
    password2.parentNode.appendChild(passwordMsg);

    usernameMsg.classList.add("text-sm", "block", "mt-1");
    emailMsg.classList.add("text-sm", "block", "mt-1");
    contactMsg.classList.add("text-sm", "block", "mt-1");
    passwordMsg.classList.add("text-sm", "block", "mt-1");

    const enableBtnIfValid = () => {
        const passwordsMatch = password1.value === password2.value && password1.value !== "";
        const contactValid = /^(98|97)\d{8}$/.test(contactInput.value);
        const emailFormatValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value);
        const usernameAvailable = !usernameMsg.textContent.includes("already taken");
        const emailAvailable = !emailMsg.textContent.includes("already in use");

        if (passwordsMatch && contactValid && emailFormatValid && usernameAvailable && emailAvailable) {
            registerBtn.disabled = false;
            registerBtn.classList.remove("opacity-50", "cursor-not-allowed");
        } else {
            registerBtn.disabled = true;
            registerBtn.classList.add("opacity-50", "cursor-not-allowed");
        }
    };

    const checkUsername = () => {
        const username = usernameInput.value.trim();
        if (!username) {
            usernameMsg.textContent = "";
            enableBtnIfValid();
            return;
        }

        fetch(`/ajax/check-username/?username=${encodeURIComponent(username)}`)
            .then(res => res.json())
            .then(data => {
                if (data.exists) {
                    usernameMsg.textContent = "❌ Username is already taken.";
                    usernameMsg.classList.add("text-red-500");
                    usernameMsg.classList.remove("text-green-500");
                } else {
                    usernameMsg.textContent = "✅ Username is available.";
                    usernameMsg.classList.remove("text-red-500");
                    usernameMsg.classList.add("text-green-500");
                }
                enableBtnIfValid();
            });
    };

    const checkEmail = () => {
        const email = emailInput.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            emailMsg.textContent = "";
            enableBtnIfValid();
            return;
        }

        fetch(`/ajax/check-email/?email=${encodeURIComponent(email)}`)
            .then(res => res.json())
            .then(data => {
                if (data.exists) {
                    emailMsg.textContent = "❌ Email is already in use.";
                    emailMsg.classList.add("text-red-500");
                    emailMsg.classList.remove("text-green-500");
                } else {
                    emailMsg.textContent = "✅ Email is available.";
                    emailMsg.classList.remove("text-red-500");
                    emailMsg.classList.add("text-green-500");
                }
                enableBtnIfValid();
            });
    };

    const checkContact = () => {
        const contact = contactInput.value.trim();
        if (contact.length < 10) {
            contactMsg.textContent = "";
            enableBtnIfValid();
            return;
        }

        if (/^(98|97)\d{8}$/.test(contact)) {
            contactMsg.textContent = "✅ Valid Nepali number.";
            contactMsg.classList.remove("text-red-500");
            contactMsg.classList.add("text-green-500");
        } else {
            contactMsg.textContent = "❌ Must start with 98 or 97 and be 10 digits.";
            contactMsg.classList.remove("text-green-500");
            contactMsg.classList.add("text-red-500");
        }
        enableBtnIfValid();
    };

    const checkPasswordMatch = () => {
        if (!password1.value || !password2.value) {
            passwordMsg.textContent = "";
            enableBtnIfValid();
            return;
        }

        if (password1.value === password2.value) {
            passwordMsg.textContent = "✅ Passwords match.";
            passwordMsg.classList.remove("text-red-500");
            passwordMsg.classList.add("text-green-500");
        } else {
            passwordMsg.textContent = "❌ Passwords do not match.";
            passwordMsg.classList.remove("text-green-500");
            passwordMsg.classList.add("text-red-500");
        }
        enableBtnIfValid();
    };

    usernameInput.addEventListener("blur", checkUsername);
    emailInput.addEventListener("blur", checkEmail);
    contactInput.addEventListener("input", checkContact);
    password1.addEventListener("input", checkPasswordMatch);
    password2.addEventListener("input", checkPasswordMatch);

    registerBtn.disabled = true;
    registerBtn.classList.add("opacity-50", "cursor-not-allowed");
});

