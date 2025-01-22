const announcementDelBtns = document.querySelectorAll(".viewDel .announcement");
const menuDelBtns = document.querySelectorAll(".viewDel .menu");
const moduleDelBtns = document.querySelectorAll(".viewDel .module");
const userBanBtns = document.querySelectorAll(".viewDel .user");

for (let i = 0; i < announcementDelBtns.length; i++) {
    announcementDelBtns[i].addEventListener("click", function (e) {
        const announcementId = e.target.getAttribute("data-id");
        // use promise format
        fetch(`deleteAnnouncement/${announcementId}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({})
        }).then(function (res) {
            return res.json();
        }).then(function (data) {
            alert(data.message);
            e.target.parentNode.parentNode.remove();
        })
    })
}

for (let i = 0; i < menuDelBtns.length; i++) {
    menuDelBtns[i].addEventListener("click", function (e) {
        const menuId = e.target.getAttribute("data-id");
        // use promise format
        fetch(`deleteMenu/${menuId}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({})
        }).then(function (res) {
            return res.json();
        }).then(function (data) {
            alert(data.message);
            e.target.parentNode.parentNode.remove();
        })
    })
}

for (let i = 0; i < moduleDelBtns.length; i++) {
    moduleDelBtns[i].addEventListener("click", function (e) {
        const moduleId = e.target.getAttribute("data-id");
        // use promise format
        fetch(`deleteModule/${moduleId}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({})
        }).then(function (res) {
            return res.json();
        }).then(function (data) {
            alert(data.message);
            e.target.parentNode.parentNode.remove();
        })
    })
}

for (let i = 0; i < userBanBtns.length; i++) {
    userBanBtns[i].addEventListener("click", function (e) {
        const userId = e.target.getAttribute("data-id");
        // use promise format
        fetch(`ban/${userId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({})
        }).then(function (res) {
            return res.json();
        }).then(function (data) {
            alert(data.message);
            if (data.message === "Successful ban!"){
                e.target.textContent = "unBan"
            }else{
                e.target.textContent = "Ban"
            }
        })
    })
}
