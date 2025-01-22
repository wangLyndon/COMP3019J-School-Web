const userEditEmail = document.querySelector("#userEditEmail");
const userEditPhone = document.querySelector("#userEditPhone");
const userEditStudentId = document.querySelector("#userEditStudentId");
const userEditTeacherId = document.querySelector("#userEditTeacherId");
const userEditSubmit = document.querySelector("#userEditSubmit");

userEditEmail.addEventListener("blur", checkEmail);
userEditPhone.addEventListener("blur", checkPhone);

if (userEditStudentId) {
    userEditStudentId.addEventListener("blur", checkStudentId);
}

if (userEditTeacherId) {
    userEditTeacherId.addEventListener("blur", checkTeacherId);
}

userEditSubmit.addEventListener("submit", function (e) {
    if (!checkEmail() || !checkPhone()){
        e.preventDefault();
    }

    if (userEditStudentId){
        if (!checkStudentId()){
            e.preventDefault();
        }
    }

    if (userEditTeacherId){
        if (!checkTeacherId()){
            e.preventDefault();
        }
    }
});

function checkEmail() {
    // Verify email format
    const emailFormat = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const email = userEditEmail.value;
    if (emailFormat.test(email)) {
        document.querySelector("#errorEserEditEmail").innerHTML = "";
        userEditEmail.parentNode.classList.remove("error");

        return true;
    } else {
        document.querySelector("#errorEserEditEmail").innerHTML = "Please input email format";
        userEditEmail.parentNode.classList.add("error");

        return false;
    }
}

function checkPhone() {
    // Verify phone format
    const phoneFormat = /^[0-9]+$/;
    const phone = userEditPhone.value;
    if (phoneFormat.test(phone)) {
        document.querySelector("#errorEserEditPhone").innerHTML = "";
        userEditPhone.parentNode.classList.remove("error");

        return true;
    } else {
        document.querySelector("#errorEserEditPhone").innerHTML = "Please input phone format";
        userEditPhone.parentNode.classList.add("error");

        return false;
    }
}

function checkStudentId() {
    // Verify id format
    const idFormat = /^[0-9]+$/;
    const id = userEditStudentId.value;
    if (idFormat.test(id)) {
        document.querySelector("#errorUserEditStudentId").innerHTML = "";
        userEditStudentId.parentNode.classList.remove("error");

        return true;
    } else {
        document.querySelector("#errorUserEditStudentId").innerHTML = "Please input id format";
        userEditStudentId.parentNode.classList.add("error");

        return false;
    }
}

function checkTeacherId() {
    // Verify id format
    const idFormat = /^[0-9]+$/;
    const id = userEditTeacherId.value;
    if (idFormat.test(id)) {
        document.querySelector("#errorUserEditTeacherId").innerHTML = "";
        userEditTeacherId.parentNode.classList.remove("error");

        return true;
    } else {
        document.querySelector("#errorUserEditTeacherId").innerHTML = "Please input id format";
        userEditTeacherId.parentNode.classList.add("error");

        return false;
    }
}
