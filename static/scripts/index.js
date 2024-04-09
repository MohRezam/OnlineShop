fetch('/api/', {
    headers: {
        'Content-Type': 'application/json'
    }
})
    .then(response => response.json())
    .then(data => {
        const categories = data.categories;
        const newsData = data.news;
        const productsRow = document.getElementById('productsRow');
        const newsContainer = document.getElementById('newsContainer');

        categories.forEach(category => {
            const colDiv = document.createElement('div');
            colDiv.classList.add('col-md-4', 'margin_bottom1');

            const productBox = document.createElement('div');
            productBox.classList.add('product_box');

            const figure = document.createElement('figure');
            const img = document.createElement('img');
            img.src = category.image;
            img.alt = category.name;
            figure.appendChild(img);

            const productNameLink = document.createElement('a');
            productNameLink.classList.add('product_name');
            productNameLink.textContent = category.name;

            const categorySlug = category.slug;
            const categoryUrl = `/category/${categorySlug}/`;
            productNameLink.href = categoryUrl;
            productNameLink.style.display = 'block';
            productNameLink.style.textAlign = 'center';
            productNameLink.style.fontWeight = 'bold';
            productNameLink.style.width = '60%';
            productNameLink.style.borderRadius = '10px';
            productNameLink.style.margin = '0 auto';
            productNameLink.style.backgroundColor = '#f0f0f0';

            productBox.appendChild(figure);
            productBox.appendChild(productNameLink);

            colDiv.appendChild(productBox);

            productsRow.appendChild(colDiv);
        });

        newsData.forEach(newsItem => {
            const newsDiv = document.createElement('div');
            newsDiv.classList.add('col-md-6', 'margin_bottom1');

            const newsContent = document.createElement('div');
            newsContent.classList.add('titlepage');

            const newsTitle = document.createElement('p');
            newsTitle.textContent = newsItem.title;

            const newsDescription = document.createElement('h2');
            newsDescription.textContent = newsItem.body;

            const newsLink = document.createElement('a');
            newsLink.textContent = 'Read More';
            newsLink.href = '#';
            newsLink.classList.add('read_more');

            newsContent.appendChild(newsTitle);
            newsContent.appendChild(newsDescription);
            newsContent.appendChild(newsLink);

            const newsImage = document.createElement('figure');
            const img = document.createElement('img');
            img.src = newsItem.image;
            img.alt = newsItem.title;
            newsImage.appendChild(img);

            newsDiv.appendChild(newsContent);
            newsDiv.appendChild(newsImage);

            newsContainer.appendChild(newsDiv);
        });

    })
    .catch(err => {
        console.error('Error fetching data:', err);
    });