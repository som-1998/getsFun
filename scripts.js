// Simulated data
let posts = [
    { id: 1, user: "user1", content: "This is the first post!", likes: 10, comments: [] },
    { id: 2, user: "user2", content: "Hello World!", likes: 5, comments: [] }
];

function login() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    // Perform authentication logic here
}

function renderPosts() {
    let postsContainer = document.getElementById("posts-container");
    postsContainer.innerHTML = '';
    posts.forEach(post => {
        let postElement = document.createElement("div");
        postElement.classList.add("post");
        postElement.innerHTML = `
            <strong>${post.user}</strong>: ${post.content}
            <div class="actions">
                <button onclick="likePost(${post.id})">Like</button>
                <button onclick="showComments(${post.id})">Comments</button>
            </div>
        `;
        postsContainer.appendChild(postElement);
    });
}

function likePost(postId) {
    // Logic to increment likes for the post with postId
}

function showComments(postId) {
    let post = posts.find(p => p.id === postId);
    let comments = post.comments;
    let postElement = document.querySelector(`.post:nth-child(${postId})`);
    comments.forEach(comment => {
        let commentElement = document.createElement("div");
        commentElement.classList.add("comment");
        commentElement.innerText = comment;
        postElement.appendChild(commentElement);
    });
}

// Initial rendering
renderPosts();
