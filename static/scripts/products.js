document.addEventListener('DOMContentLoaded', function () {
    let currentPage = 1;
    let totalPages = 1;

    function fetchProducts(page, searchQuery = '') {
        let url = '/api' + window.location.pathname + `?page=${page}`;

        if (searchQuery) {
            url = `/api/product/search/?search=${searchQuery}`;
        }

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const productsRow = document.getElementById('productsRow');
                productsRow.innerHTML = '';

                if (data.results) {
                    data.results.forEach(product => {
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
                        productNameLink.href = `/products/${product.slug}`;
                        productNameLink.classList.add('product_name');

                        productBox.appendChild(figure);
                        productBox.appendChild(productNameLink);

                        colDiv.appendChild(productBox);
                        productsRow.appendChild(colDiv);
                    });
                }
                else {
                    console.error('No results found');
                }
                currentPage = page;
                totalPages = Math.ceil(data.count / data.results.length);

                updatePaginationButtons();
            })
            .catch(err => {
                console.error('Error fetching products data:', err);
            });
    }

    function updatePaginationButtons() {
        const previousButton = document.getElementById('previousButton');
        const nextButton = document.getElementById('nextButton');

        previousButton.disabled = (currentPage === 1);
        nextButton.disabled = (currentPage === totalPages);

        previousButton.addEventListener('click', () => {
            fetchProducts(currentPage - 1);
        });

        nextButton.addEventListener('click', () => {
            fetchProducts(currentPage + 1);
        });
    }

    const searchForm = document.querySelector('#searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const searchInput = document.getElementById('gsearch');
            const query = searchInput.value.trim();
            if (query) {
                fetchProducts(1, query);
            }
        });
    }

    fetchProducts(currentPage);
});
