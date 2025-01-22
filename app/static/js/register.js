const password = document.querySelector("#regPassword");
const passwordAgain = document.querySelector("#regPasswordAgain");
const regEmail = document.querySelector("#regEmail");
const regPhone = document.querySelector("#regPhone");
const regSubmit = document.querySelector("#regSubmit");

password.addEventListener("blur", checkPasswordSame);
passwordAgain.addEventListener("blur", checkPasswordSame);
regEmail.addEventListener("blur", checkEmailReg);
regPhone.addEventListener("blur", checkPhoneReg);

regSubmit.addEventListener("submit", function (e) {
    if ( !checkPasswordSame() || !checkPhoneReg() || !checkEmailReg()) {
        // Prevent submission if lack some information
        e.preventDefault();
    }
});

function checkPasswordSame() {
    // Verify that the passwords are the same
    if (password && passwordAgain) {
        if (password.value !== passwordAgain.value) {
            document.querySelector("#regErrorPasswordAgain").innerHTML = "Passwords must be the same";
            passwordAgain.parentNode.classList.add("error");

            return false;
        } else {
            document.querySelector("#regErrorPasswordAgain").innerHTML = "";
            passwordAgain.parentNode.classList.remove("error");

            return true;
        }
    }

    return false;
}

function checkEmailReg() {
    // Verify email format
    const emailFormat = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const email = regEmail.value;
    if (emailFormat.test(email)) {
        document.querySelector("#errorRegEmail").innerHTML = "";
        regEmail.parentNode.classList.remove("error");

        return true;
    } else {
        document.querySelector("#errorRegEmail").innerHTML = "Please input email format";
        regEmail.parentNode.classList.add("error");

        return false;
    }
}

function checkPhoneReg() {
    // Verify phone format
    const phoneFormat = /^[0-9]+$/;
    const phone = regPhone.value;
    if (phoneFormat.test(phone)) {
        document.querySelector("#errorRegPhone").innerHTML = "";
        regPhone.parentNode.classList.remove("error");
        return true;
    } else {
        document.querySelector("#errorRegPhone").innerHTML = "Please input phone format";
        regPhone.parentNode.classList.add("error");
        return false;
    }
}
