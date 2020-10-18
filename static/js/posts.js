$(".detail-button").click((event) => {
    event.preventDefault();
    const id = event.target.id;
    $.ajax({
        type: "GET",
        url: `https://djangonltk.herokuapp.com/api/comments/${id}`,
        success: response => {
            $(".modal-body").empty();
            if (response.length >= 1) {
                response.map(comment => {
                    $(".modal-body").append(`
                        <div>
                            <p> ${comment.content} </p>
                            <hr/>
                        </div>
                    `);
                });
            } 
            else {
                $(".modal-body").html("The post has no comments!");
            }
        },
        error: error => {
            console.log(error);
        }
    })
});