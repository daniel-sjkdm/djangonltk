// -- Render the fetched posts to the screen
let posts = [];                                // Temporal array that holds the posts       
let kind = "top";                              // Initial kind of reddit post to fetch
let limit = 10;                                // Initial post limit
const default_img = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.dailydot.com%2Fwp-content%2Fuploads%2F2018%2F05%2Freddit-redpill.jpg&f=1&nofb=1";


const render_post = (post) => {

    const post_card =  `
        <div class="col-lg-6 col-md-12" col-xs-12"> 
            <div class="card" style="height: 600px; margin-bottom: 30px;">
                <img src=${post.img} class="card-img-top" alt="" height="300">
                <div class="card-body post_body">
                    <h5 class="card-title post_title" id="post_title_${post.id}" style="overflow-y: scroll;"> ${post.title} </h5>
                    <h6 class="card-subtitle" style="text-align: center" id="post_username_${post.id}"> Author: ${post.username}  </h6>
                    <div class="d-flex flex-row justify-content-around">
                        <p id="post_subreddit_${post.id}"> r/${post.subreddit} </p>
                        <p id="post_created_${post.id}"> Created ${post.created} </p>
                    </div>
                    <div class="post_likes">
                        <span class="badge badge-success" id="post_ups_${post.id}"> ups: ${post.ups} </span>
                        <span class="badge badge-primary" id="post_sentiment_${post.id}"> sentiment: ${post.sentiment} </span>
                    </div>
                    <br/>
                    <div class="card-actions">
                        <button class="btn btn-success btn-sm store_button" id=${post.id}>
                            Save
                        </button>
                        <a class="btn btn-secondary btn-sm" href="${post.url}" id="post_url_${post.id}" target="_blank"> url </a>
                    </div>
                </div>
            </div>
        </div>
    `;
    return post_card;
};


// -- Get the information of the post with the given id
const parse_post_card = (post_id) => {
    const data = {
        post_id: post_id,
        title: $(`#post_title_${post_id}`).text().trim(),
        username: $(`#post_username_${post_id}`).text().trim().split(":").slice(1).join().trim(),
        created: $(`#post_created_${post_id}`).text().trim().split(" ").slice(1).join(" "),
        ups: $(`#post_ups_${post_id}`).text().trim().split(":").slice(1).join().trim(),
        url: $(`#post_url_${post_id}`).attr("href"),
        num_comments: $(`#post_num_comments_${post_id}`).text().trim(),
        subreddit: $(`#post_subreddit_${post_id}`).text().trim().split("/").slice(1).join(),
        sentiment: $(`#post_sentiment_${post_id}`).text().trim().split(":").slice(1).join()
    };
    return data;
};


const save_post = (data) => {
    console.log("Saving the post")
    $.ajax({
        url: "https://djangonltk.herokuapp.com/api/posts", 
        method: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(data),
        success: response => {
            console.log(response);
        },
        error: err => {
            alert("There was an error at the server");
        }
    });
};



// --- Paginator

let paginator_state = {
    current_page: 1,
    total_posts: posts.length,
    posts_per_page: 5,
    total_pages: 1,
    lower_bound: 0,
    higher_bound: 5
}


const updatePaginatorBounds = () => {
    paginator_state.lower_bound = (paginator_state.current_page - 1) * paginator_state.posts_per_page;
    paginator_state.higher_bound = paginator_state.lower_bound + paginator_state.posts_per_page;
}


const handlePaginator = (page) => {
    paginator_state.current_page = page;
    updatePaginatorBounds();
    showPosts();
};


const handleNextPage = () => {
    if ( paginator_state.current_page < paginator_state.total_pages ) {
        paginator_state.current_page ++;
        updatePaginatorBounds();
        showPosts();
        paginator();
    }
};


const handlePrevPage = () => {
    if ( paginator_state.current_page > 1 ) {
        paginator_state.current_page --;
        updatePaginatorBounds();
        showPosts();
        paginator();
    }
};


const paginator = () => {
    paginator_state.total_posts = posts.length;
    paginator_state.total_pages = Math.round(paginator_state.total_posts/paginator_state.posts_per_page);
    $(".post_paginator").html(`
        <nav aria-label="Post paginator">
            <ul class="pagination">
                <li class="page-item">
                    <a class="page-link" aria-label="Previous" onclick="handlePrevPage()">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                </li>
                <a class="btn btn-secondary" style="text-align: center; margin-right: 10px;" disabled> ${paginator_state.current_page} / ${paginator_state.total_pages} </a>
                <li class="page-item">
                    <a class="page-link" aria-label="Next" onclick="handleNextPage()">
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                </li>
            </ul>
        </nav>
    `);
    $(".post_paginator").attr("hidden", false);
};


// -- Display the posts 
const showPosts = () => {
    console.log(posts.slice(paginator_state.lower_bound, paginator_state.higher_bound));
    $(".post_container").empty();
    posts.slice(paginator_state.lower_bound, paginator_state.higher_bound).map(post => (
        $(".post_container").append(render_post(post))
    ));

    $(".comment_button").click((e) => {
        const post_id = e.target.id;
        render_post_comments(post_id);
    });

    $(".store_button").click((e) => {
        const post_id = e.target.id;
        const data = parse_post_card(post_id);
        save_post(data);
    });
};


const computeSentiments = (posts) => {
    console.log("Getting sentiment...")
    $.ajax({
        url: "https://djangonltk.herokuapp.com/api/posts",
        method: "POST",
        data: {tms: posts[0].title},
        success: response => {
            console.log(response);
        },
        error: err => {
            alert("Server error");
            console.log(err);
        }
    });
};


// -- Search a post, capture input and send a GET request
const search_posts = (query) => {
    $(".post_container").empty();
    $("#spinner").prop("hidden", false);
    $(".post_paginator").prop("hidden", true);
    posts = [];

    const params = {
        query: query.trim(),
        kind: kind.trim(),
        limit: Number(limit)
    };

    let url = `https://cors-anywhere.herokuapp.com/https://www.reddit.com/search.json?q=${params.query}&limit=${params.limit}&sort=${params.kind}`;

    $.ajax({
        url: url,
        method: "GET",
        success: response => {
            if (response.length === 0) {
                $("#spinner").prop("hidden", true);
                alert("No subreddit was found");
            }
            else {

                $("#spinner").prop("hidden", true);
                                
                response.data.children.map(item => {
                    const post = {
                        id: item.data.id,
                        title: item.data.title,
                        created: new Date(item.data.created_utc).toLocaleString(),
                        ups: item.data.ups,
                        username: item.data.author_fullname,
                        content: item.data.description,
                        subreddit: item.data.subreddit,
                    }

                    item.data.url.startsWith("/r/") ? post.url = "https://www.reddit.com" + item.data.url : post.url = item.data.url;
                    item.data.preview ? post.img = item.data.preview.images[0].source.url : post.img = default_img;

                    posts.push(post);
                });

                console.log(posts);

                computeSentiments(posts);
                paginator(); 
                showPosts();
            }
        },
        error: err => {
            $("#spinner").prop("hidden", true);
            alert("Server error");
            console.log(err);
        }
    });

};


$(document).ready( () => {
    $("#searchbar").keydown((e) => {
        const query = $("#searchbar").val().toLowerCase();
        if (e.keyCode === 13) {
            if (query !== "") {
                search_posts(query.trim());
            }
        }
    });

    $(".kind_dropdown").click((e) => {
        kind = e.target.text.trim();
    });

    $("#limit").change((e) => {
        const limit_value = Number(e.target.value);
        if ( limit_value >= 10 ) {
            limit = limit_value;
        }
    });
});