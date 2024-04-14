fetch('/api' + window.location.pathname)
    .then(response => response.json())
    .then(data => {
        const productsRow = document.getElementById('productsRow');

        data.forEach(product => {
            const colDiv = document.createElement('div');
            colDiv.classList.add('col-md-4', 'margin_bottom1');

            const productBox = document.createElement('div');
            productBox.classList.add('product_box');

            const figure = document.createElement('figure');
            const img = document.createElement('img');
            img.src = product.image;
            img.alt = product.name;
            figure.appendChild(img);

            const productNameLink = document.createElement('a');
            productNameLink.textContent = product.name;
            productNameLink.href = `/product/${product.id}`;
            productNameLink.href = window.location.pathname + product.slug + '/products/'

            productNameLink.style.display = 'block';
            productNameLink.style.fontWeight = 'bold';
            productNameLink.style.width = '60%';
            productNameLink.style.borderRadius = '10px';
            productNameLink.style.margin = '0 auto';
            productNameLink.style.backgroundColor = '#f0f0f0';
            productNameLink.style.textAlign = 'center';

            productBox.appendChild(figure);
            productBox.appendChild(productNameLink);

            colDiv.appendChild(productBox);
            productsRow.appendChild(colDiv);
        });
    })
    .catch(err => {
        console.error('Error fetching products data:', err);
    });