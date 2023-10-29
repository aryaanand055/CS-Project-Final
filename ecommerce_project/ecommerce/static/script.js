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
// document.addEventListener("DOMContentLoaded", function () {
//     var productListContainer = document.getElementById("product-list-container");
//     productListContainer.addEventListener("click", function (event) {
//         if (event.target.tagName == "I") {
//             if (event.target.parentElement.classList.contains("add-to-wishlist")) {
//                 var productID = event.target.parentElement.getAttribute("data-product-id");
//                 addToWishlist(productID, event.target.parentElement);
//             } else if (event.target.parentElement.classList.contains("remove-from-wishlist")) {
//                 var productID = event.target.parentElement.getAttribute("data-product-id");
//                 removeFromWishlist(productID, event.target.parentElement);
//             }
//         } else if (event.target.tagName == "BUTTON") {
//             if (event.target.classList.contains("add-to-wishlist")) {
//                 var productID = event.target.getAttribute("data-product-id");
//                 addToWishlist(productID, event.target);
//             } else if (event.target.classList.contains("remove-from-wishlist")) {
//                 var productID = event.target.getAttribute("data-product-id");
//                 removeFromWishlist(productID, event.target);
//             }
//         }
//     });
// });
document.addEventListener("DOMContentLoaded", function () {
    var productListContainer = document.getElementById("product-list-container");
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



// document.addEventListener("DOMContentLoaded", function () {
//     var addToWishlistButtons = document.querySelectorAll(".add-to-wishlist");

//     addToWishlistButtons.forEach(function (button) {
//         button.addEventListener("click", function () {
//             var productID = button.getAttribute("data-product-id");
//             addToWishlist(productID, button);
//         });
//     });
// });

function addToWishlist(productID, button) {
    fetch(`add_to_wishlist/${productID}/`, {
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
                button.classList = "remove-from-wishlist"
                var heartIcon = button.querySelector("i");
                heartIcon.classList.remove("fa-regular");
                heartIcon.classList.add("fa-solid");
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


// document.addEventListener("DOMContentLoaded", function () {
//     var removeFromWishlistButtons = document.querySelectorAll(".remove-from-wishlist");

//     removeFromWishlistButtons.forEach(function (button) {
//         button.addEventListener("click", function () {
//             var productID = button.getAttribute("data-product-id");
//             removeFromWishlist(productID, button);
//         });
//     });
// });

function removeFromWishlist(productID, button) {
    fetch(`remove_from_wishlist/${productID}/`, {
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
                button.classList = "add-to-wishlist"
                var heartIcon = button.querySelector("i");
                heartIcon.classList.remove("fa-solid");
                heartIcon.classList.add("fa-regular");
            } else {
                alert("Failed to remove product from wishlist.");
            }
        })
        .catch(function (error) {
            console.error("Fetch error:", error);
        });
}