console.log("Hello World!!")

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

document.addEventListener("DOMContentLoaded", function () {
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
});

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
                // Update the UI to reflect the change in the wishlist
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
                alert("Failed to add product to wishlist.");
            }
        })
        .catch(function (error) {
            console.error("Fetch error:", error);
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
                // Update the UI to reflect the removal from the wishlist
                if (button.id == "productDetailWishlist") {
                    button.classList.add("add-to-wishlist")
                    button.classList.remove("remove-from-wishlist")
                    button.textContent = "Add To Wishlist"
                    // alert("F to wishlist")
                } else {
                    button.classList = "add-to-wishlist"
                    var heartIcon = button.querySelector("i");
                    heartIcon.classList.remove("fa-solid");
                    heartIcon.classList.add("fa-regular");
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

document.addEventListener("DOMContentLoaded", function () {
    showSlides(slideIndex)
})

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
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