function includeAuthToken() {
    const access_token = localStorage.getItem("access_token");
    if (access_token) {
        return {
            'Authorization': 'JWT ' + access_token
        };
    }
    return {};
}

fetch('/api' + window.location.pathname, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        ...includeAuthToken(),
    }
})
    .then(response => response.json())
    .then(data => {
        const productList = document.getElementById('comment-list');
        productList.innerHTML = '';

        data.comment.forEach(function (product) {
            const commentContainer = document.createElement('div');
            commentContainer.classList.add('be-comment');

            commentContainer.innerHTML = `
        <div class="be-comment-content">
            <div class="be-img-comment">    
                <img src="${product.user.image}" alt="" class="be-ava-comment">
            </div>    
            <span class="be-comment-name">
                <p>${product.user.first_name}</p>
                </span>
            <span class="be-comment-time">
                <i class="fa fa-clock-o"></i>
                ${product.created_at}
            </span>
            <p class="be-comment-text">
                ${product.text}
            </p>
            <button class="btn btn-sm btn-outline-primary like-button">Like</button>
            <span class="like-count">${product.likes}</span>
        </div>
        
        `;

            productList.appendChild(commentContainer);
        });
    })
    .catch(error => console.error('Error:', error));

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function () {
            const likeCount = this.parentElement.querySelector('.like-count');
            likeCount.textContent = parseInt(likeCount.textContent) + 1;
        });
    });

    const submitButton = document.querySelector('.btn-primary');

    submitButton.addEventListener('click', function () {
        const nameInput = document.querySelector('input[placeholder="Your name"]');
        const emailInput = document.querySelector('input[placeholder="Your email"]');
        const commentInput = document.querySelector('textarea[placeholder="Your text"]');

        const newComment = {
            name: nameInput.value,
            email: emailInput.value,
            text: commentInput.value
        };

        fetch('/api' + window.location.pathname, {
            method: "POST",
            headers: {
                ...includeAuthToken(),
                "Content-Type": "application/json",
            },
            body: JSON.stringify(newComment)
        })
            .then(response => response.json())
            .then(data => {
                console.log('New comment added:', data);
                window.location.reload();
            })
            .catch(error => console.error('Error:', error));
        window.location.reload();
    });
});