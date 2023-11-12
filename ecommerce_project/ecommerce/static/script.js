document.addEventListener("DOMContentLoaded", function () {
    addtoWishlist1() 
    showSlides1()
    deleteProfile()
});

function searchProducts(e) {
    let input = document.getElementById("navbar-search")
    let filter = input.value.toLowerCase()
    let products = document.querySelectorAll(".product-small")
    products.forEach(product => {
        let productName = product.querySelector(".card-title").textContent.toLowerCase();
        let productDesc = product.querySelector(".card-text").textContent.toLowerCase();
        if (productName.indexOf(filter) > -1 || productDesc.indexOf(filter) > -1) {
            product.style.display = "block"
        } else {
            product.style.display = "none"

        }
    });
}
function addtoWishlist1() {
    var productListContainer = document.getElementById("wishlist-container");
    productListContainer.addEventListener("click", function (event) {
        var target = event.target;
        var button = target;
        if (!target.classList.contains("add-to-wishlist") && !target.classList.contains("remove-from-wishlist")) {
            button = target.parentElement;
        }
        var productID = button.getAttribute("data-product-id");
        if (button.classList.contains("add-to-wishlist")) {
            addToWishlist(productID, button);
        } else if (button.classList.contains("remove-from-wishlist")) {
            removeFromWishlist(productID, button);
        }
    });    
}

function addToWishlist(productID, button) {
    fetch(`/add_to_wishlist/${productID}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({
                product_id: productID
            }),
        })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            }
            throw new Error("Network response was not ok.");
        })
        .then(function (data) {
            if (data.success) {
                if (button.id == "productDetailWishlist") {
                    button.classList.remove("add-to-wishlist")
                    button.classList.add("remove-from-wishlist")
                    button.textContent = "Remove From Wishlist"
                } else {

                    button.classList = "remove-from-wishlist"
                    var heartIcon = button.querySelector("i");
                    heartIcon.classList.remove("fa-regular");
                    heartIcon.classList.add("fa-solid");
                }
            } else {
                if (data.msg == "User not logged in") {
                    if (confirm("You will have to login before that...")){
                        open("/login", "_self")
                    }
                }
            }
        })
        .catch(function (error) {
            console.error("Fetch error:", error.msg);
        });
}

// Function to get the CSRF token from cookies (Django-specific)
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) {
        return parts.pop().split(";").shift();
    }
    return "";
}

function removeFromWishlist(productID, button) {
    fetch(`/remove_from_wishlist/${productID}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({
                product_id: productID
            }),
        })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            }
            throw new Error("Network response was not ok.");
        })
        .then(function (data) {
            if (data.success) {
                if (button.classList.contains("wishlistCard")) {
                    if (button.parentElement.parentElement.parentElement.parentElement.childElementCount == 1) {
                        para = document.createElement("p")
                        para.textContent = "Your wishlist is empty."
                        button.parentElement.parentElement.parentElement.parentElement.appendChild(para)
                        button.parentElement.parentElement.parentElement.remove()
                    } else {
                        button.parentElement.parentElement.parentElement.remove()
                    }
                } else {
                    if (button.id == "productDetailWishlist") {
                        button.classList.add("add-to-wishlist")
                        button.classList.remove("remove-from-wishlist")
                        button.textContent = "Add To Wishlist"
                    } else {
                        button.classList = "add-to-wishlist"
                        var heartIcon = button.querySelector("i");
                        heartIcon.classList.remove("fa-solid");
                        heartIcon.classList.add("fa-regular");
                    }
                }
            } else {
                alert("Failed to remove product from wishlist.");
            }
        })
        .catch(function (error) {
            console.error("Fetch error:", error);
        });
}
let slideIndex = 1;
function showSlides1() {
    showSlides(slideIndex)
}

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    if (window.location.pathname.search("/products/") != -1) {
        let i;
        let slides = document.getElementsByClassName("mySlides");
        let dots = document.getElementsByClassName("demo");
        if (n > slides.length) {
            slideIndex = 1
        }
        if (n < 1) {
            slideIndex = slides.length
        }
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }
        for (i = 0; i < dots.length; i++) {
            dots[i].className = dots[i].className.replace(" active", "");
        }
        slides[slideIndex - 1].style.display = "block";
        dots[slideIndex - 1].className += " active";
    }
}

function deleteProfile() {
    if (window.location.pathname.search("/profile/") != -1) {

    
        document.getElementById("deleteProfileBtn").addEventListener("click", () => {
            let psswd = prompt("Enter password to delete user");
            fetch('/deleteUser/', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: `password=${encodeURIComponent(psswd)}`,
            }).then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Password is incorrect");
                }
            }).then(data => {
                console.log(data);
                alert("User deleted successfully");
                window.location.href = "/login";
            }).catch(error => {
                console.error(error);
                alert("Cannot delete account. Password is incorrect");
            });
        });
    }
}
     