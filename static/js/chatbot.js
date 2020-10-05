const add_human_message = (message) => {
    $("#chat-area").append(`
        <div class="row">
            <div class="col-lg-6 col-md-6 col-xs-12">
                <div class="card human-card">
                    <div class="card-body">
                        <i> human </i> : ${ message }
                    </div>
                </div>
            </div>
        </div>
    `);
};

const add_bot_message = (message, name) => {
    $("#chat-area").append(`
        <div class="row">
            <div class="col-lg-6 col-md-6 col-xs-12">
                <div class="card bot-card">
                    <div class="card-body">
                        <i> ${name} bot </i> : ${ message }
                    </div>
                </div>
            </div>
        </div>

    `);
}

$(".dropdown-item").click((event) => {
    event.preventDefault();
    const name = event.target.text;
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/api/chatbot",
        headers: {"Content-Type": "application/json"},
        data: {bot_name: name},
        success: response => {
        },
        error: error => {
            console.log(error)
        }
    });
});


$("#human-form").submit((event) => {
    event.preventDefault();
    const human_message = $("#human-message").val();
    const data = $("#human-form").serialize();
    $("#human-message").val("");
    $.ajax({
        method: "POST",
        url: "http://127.0.0.1:8000/api/chatbot",
        data: data,
        success: response => {
            add_human_message(human_message),
            add_bot_message(response.data, response.bot_name);
        },
        error: error => {
            console.log(error);
        } 
    })
});