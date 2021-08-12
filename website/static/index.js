function like(postId) {
    // gets the total number of likes
    const likeCount = document.getElementById(`likes-count-${postId}`);
    // the like button
    const likeButton = document.getElementById(`like-button-${postId}`);

    // sends a `POST` request
    fetch(`/like-post/${postId}`, { method: "POST" })
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            // user liked the post
            if (data["liked"] === true) {
                likeButton.className = "fas fa-thumbs-up";
            // user didn't like the post
            } else {
                likeButton.className = "far fa-thumbs-up";
            }
        })
        // something went wrong
        .catch((e) => alert("Could not like post."));
}
