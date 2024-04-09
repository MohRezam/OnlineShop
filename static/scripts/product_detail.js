function fetchProductDetail() {
    fetch('/api' + window.location.pathname)
        .then(response => response.json())
        .then(product => {
            const productDetailContainer = document.getElementById('productDetailContainer');

            const colDiv = document.createElement('div');
            colDiv.classList.add('col-md-7');

            const laptopImg = document.createElement('div');
            laptopImg.classList.add('laptop1_img');
            laptopImg.innerHTML = `<figure><img src="${product.product.image}" alt="${product.product.name}"/></figure>`;
            colDiv.appendChild(laptopImg);

            const colDiv2 = document.createElement('div');
            colDiv2.classList.add('col-md-5');

            const titlePage = document.createElement('div');
            titlePage.classList.add('titlepage');
            titlePage.innerHTML = `
                <h2>${product.product.name}</h2>
                <h1>${product.product.brand}</h1>
                <div class="product-info">
                    <div><strong>Description:</strong> ${product.product.description}</div>
                    <div><strong>Price:</strong> ${product.product.price}</div>
                    <div><strong>Is Available: </strong>${product.product.is_available}</div>
                    <div><strong>Inventory quantity:</strong> ${product.product.inventory_quantity}</div>
                    <div><strong>Discount:</strong> ${product.product.discount ? product.product.discount : '-'}</div>
                </div>
                <div class="quantity-control">
                    <button type="button" class="quantity-btn decrease-btn" onclick="decreaseQuantity()">-</button>
                    <input type="number" id="quantity" value="1" min="1" readonly>
                    <button type="button" class="quantity-btn increase-btn" onclick="increaseQuantity()">+</button>
                
                <button class="read_more" onclick="addToCart('${product.product.slug}')">Add to Cart</button>
            </div><br>
                <a class="read_more" href="/comment/${product.product.slug}">Comments</a>
            `;
            colDiv2.appendChild(titlePage);

            productDetailContainer.appendChild(colDiv);
            productDetailContainer.appendChild(colDiv2);
        })
        .catch(error => console.error('Error fetching product detail:', error));
}

function increaseQuantity() {
    const quantityInput = document.getElementById('quantity');
    quantityInput.value = parseInt(quantityInput.value) + 1;
}

function decreaseQuantity() {
    const quantityInput = document.getElementById('quantity');
    if (parseInt(quantityInput.value) > 1) {
        quantityInput.value = parseInt(quantityInput.value) - 1;
    }
}

function addToCart(productSlug) {
    const quantity = document.getElementById('quantity').value;
    fetch(`/orders/api/cart/${productSlug}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product: productSlug,
            quantity: quantity
        })
    })
        .then(response => {
            if (response.ok) {
                window.location.href = window.location.pathname
            } else {
                console.error('Failed to update cart');
            }
        })
        .catch(error => console.error('Error updating cart:', error));
}

window.addEventListener('DOMContentLoaded', fetchProductDetail);