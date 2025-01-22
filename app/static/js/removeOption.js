const delReviews = document.querySelectorAll(".delReview");
const deleteUser = document.querySelector(".deleteUser");

for (let i = 0; i < delReviews.length; i++) {
    delReviews[i].addEventListener("click", function (e) {
        const id = e.target.getAttribute("data-id");

        fetch(`deleteReview/${id}`, {
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
    });
}

deleteUser.addEventListener("click", function (e) {
    if (confirm("Are you sure to do that?")) {
        fetch("deleteAccount", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({})
        }).then(function (res) {
            return res.json();
        }).then(function (data) {
            alert(data.message);
            window.location.pathname = "auth/login";
        });
    }
});
