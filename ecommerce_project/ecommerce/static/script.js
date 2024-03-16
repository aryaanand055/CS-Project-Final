document.addEventListener("DOMContentLoaded", function () {
    addtoWishlist1()
    showSlides1()
    deleteProfile()
});

function searchProducts(e) {
    let input = document.getElementById("navbar-search")
    let filter = input.value.toLowerCase()
    if (window.location.pathname.startsWith("/products") != true) {
        fetch("/get_top_products?filter=" + filter)
            .then(response => response.json())
            .then(data => {
                updateDropdown(data);
            })
            .catch(error => console.error("Error fetching top products:", error));
    } else {
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
}
document.addEventListener("click", function (event) {
    let dropdown = document.getElementById("search-dropdown");
    let searchBar = document.getElementById("navbar-search");
    if (!dropdown.contains(event.target) && !searchBar.contains(event.target)) {
        dropdown.style.display = "none";
    }
});

function updateDropdown(products) {
    let dropdown = document.getElementById("search-dropdown");
    if (!dropdown) {
        console.error("Dropdown element not found");
        return;
    }

    dropdown.innerHTML = "";
    dropdown.style.maxWidth = document.getElementById("navbar-search").offsetWidth + "px";

    if (products.length === 0) {
        let noProductsItem = document.createElement("div");
        noProductsItem.classList = "dropdown-item text-truncate w-100 text-muted";
        noProductsItem.innerText = "No products found";
        dropdown.appendChild(noProductsItem);
    } else {
        for (let i = 0; i < Math.min(5, products.length); i++) {
            let product = products[i];
            let dropdownItem = document.createElement("div");
            dropdownItem.classList = "dropdown-item text-truncate w-100 min-width-search-bar";
            let link = document.createElement("a");
            link.classList = "link-offset-2 link-underline link-underline-opacity-0 text-secondary";
            link.href = "/products/" + product["id"];
            link.innerText = product.name;
            dropdownItem.appendChild(link);
            dropdownItem.addEventListener("click", function () {
                window.location = "/products/" + product.id; // Adjust accordingly
            });
            dropdown.appendChild(dropdownItem);
        }
    }

    dropdown.style.display = "block";
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


document.addEventListener('DOMContentLoaded', function () {
    const wishlistBtns = document.querySelectorAll(".move-to-wishlist")
    wishlistBtns.forEach((item) => {
        item.addEventListener("click", (e) => {
            const productID = item.getAttribute('data-product-id');
            moveToWishlist(productID)
        })
    })
})

function moveToWishlist(productID) {
    fetch(`/add_to_wishlist/${productID}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            product_id: productID
        }),
    }).then(() => {
        fetch(`/remove_all_from_cart/${productID}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location = "wishlist";
                }
            }).catch(error => console.error("Error occured"))
    })

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
    }).then(function (response) {
        if (response.ok) {
            return response.json();
        }
        throw new Error("Network response was not ok.");
    }).then(function (data) {
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
                let heartAnimateIcon = button.querySelector(".heart-outline-animate")
                heartAnimateIcon.style.opacity = 0;
                heartAnimateIcon.style.transform = "scale(4)";

                setTimeout(function () {
                    heartAnimateIcon.style.transform = "scale(1)";
                    setTimeout(function () {
                        heartAnimateIcon.style.opacity = 1;
                    }, 500);
                }, 500);
            }
        } else {
            if (data.msg == "User not logged in") {
                if (confirm("You will have to login before that...")) {
                    open("/login", "_self")
                }
            }
        }
    }).catch(function (error) {
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
                        let heartAnimateIcon = button.querySelector(".heart-outline-animate")
                        heartAnimateIcon.style.opacity = 0;
                        heartAnimateIcon.style.transform = "scale(4)";

                        setTimeout(function () {
                            heartAnimateIcon.style.transform = "scale(1)";
                            setTimeout(() => {
                                heartAnimateIcon.style.opacity = 1;
                            }, 500);
                        }, 500)
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

document.addEventListener("DOMContentLoaded", function () {
    const btnContainer = document.getElementById("btn-cart-container");

    btnContainer.addEventListener("click", (e) => {
        const button = e.target.closest("button");
        if (!button) return;

        const productID = button.getAttribute('data-product-id');

        if (button.classList.contains("btn-addtocart")) {
            addToCart(productID);
        } else if (button.classList.contains("btn-removefromcart")) {
            removeFromCart(productID, 0);
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const cartItems = document.querySelectorAll(".remove-from-cart")
    cartItems.forEach((item) => {
        item.addEventListener("click", (e) => {
            const productID = item.getAttribute('data-product-id');
            removeFromCart(productID, 2)
        })
    })
})

function updateCartUI(cartQuantity, productID, msg) {
    const cntnr = document.getElementById("btn-cart-container");

    if (cartQuantity > 0) {

        cntnr.innerHTML = `
            <div class="btn-group w-100 rounded-4 p-4 m-2">
                <button type="button" class="btn btn-outline-dark p-2 btn-removefromcart" data-product-id="${productID}">
                    <span class="fa fa-minus minus"></span>
                </button>
                <a type="button" class="btn btn-outline-dark p-2">${cartQuantity}</a>
                <button type="button" class="btn btn-outline-dark p-2 btn-addtocart" data-product-id="${productID}" data-toggle="tooltip"
                                data-placement="auto right" title="${msg}" >
                    <span class="fa fa-plus plus"></span>
                </button>
            </div>`;
    } else {
        cntnr.innerHTML = `
            <button class="btn btn-dark rounded-5 p-3 m-2 w-100 btn-addtocart" data-product-id="${productID}">
                Add to Bag
            </button>`;
    }
}

function addToCart(productID) {
    const csrftoken = getCookie("csrftoken");
    if (!csrftoken) {
        // User is not logged in, redirect to login page
        window.location.href = "/login";
        return;
    }
    fetch(`/add_to_cart/${productID}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
            product_id: productID
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateCartUI(data.cart_quantity, productID, "");
            } else {
                updateCartUI(data.cart_quantity, productID, data.message);
                console.error(data.message);
            }
        })
        .catch(error => console.error("Fetch error:", error));
}

function removeFromCart(productID, mode) {
    if (mode == 2) {
        fetch(`/remove_all_from_cart/${productID}/`, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location = "cart";
                }
            }).catch(error => console.error("Error occured"))
    }
    else {
        fetch(`/remove_from_cart/${productID}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (mode === 0) {
                        updateCartUI(data.cartQuantity, productID, "");
                    }
                } else {
                    console.error(data.message);
                }
            })
            .catch(error => console.error("Fetch error:", error));
    }
}
document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('id_password');
    const ic = document.querySelector(".fa-eye")

    togglePassword.addEventListener('mouseenter', function () {
        passwordInput.type = 'text';
        ic.style.scale = 1.1
    });

    togglePassword.addEventListener('mouseleave', function () {
        passwordInput.type = 'password';
        ic.style.scale = 1

    });
});

