const adminEditTeacherId = document.querySelector("#adminEditTeacherId");
const adminEditModuleSubmit = document.querySelector("#adminEditModuleSubmit");

adminEditTeacherId.addEventListener("blur", checkTeacherId);
adminEditModuleSubmit.addEventListener("submit", function (e) {
    if (!checkTeacherId()){
        e.preventDefault();
    }
});


function checkTeacherId() {
    // Verify id format
    const idFormat = /^[0-9]+$/;
    const id = adminEditTeacherId.value;
    if (idFormat.test(id)) {
        document.querySelector("#errorAdminEditTeacherId").innerHTML = "";
        adminEditTeacherId.parentNode.classList.remove("error");

        return true;
    } else {
        document.querySelector("#errorAdminEditTeacherId").innerHTML = "Please input id format";
        adminEditTeacherId.parentNode.classList.add("error");

        return false;
    }
}
