$(document).ready(() => {
    $(".wyo-processing").hide();
});

$("#submit-btn").click(event => {
    event.preventDefault();
    const text = $("#tms").val();
    const encoded_form = $("#wyoform").serialize();
    if ( text !== "" ) {
        $.ajax({
            type: "post",
            url: "https://djangonltk.herokuapp.com/api/posts/parse",
            data: encoded_form,
            success: response => {
                console.log(response);
                const sentence_no_stop_words = response["sentence_no_stop_words"].join(" ");
                const sentence_tokens = response["sentence_tokens"].map(token => (
                    `< ${token} >`
                ));
                const sentence_stems = response["sentence_stems"].map(item => (
                    `< ${item} >`
                ));
                const sentence_pos_tags = response["sentence_pos"].map(item => (
                    `< ${item} >`
                ));
                const sentence_lemma = response["sentence_lemma"].map(item => Object.values(item)).join(", ");
                let sentence_sentiment = "";
                if (response["sentence_sentiment"] === 1) {
                    sentence_sentiment = "positive";
                }
                else if (response["sentence_sentiment"] === -1) {
                    sentence_sentiment = "negative";
                }
                else {
                    sentence_sentiment = "neutral";
                }
                $(".wyo-processing").show();
                $("#wyo-body").html("");
                $("#wyo-body").append(`
                    <tr>
                        <td> No stop words  </td>
                        <td> ${ sentence_no_stop_words }  </td>
                    </tr>
                    <tr>
                        <td> Word tokens  </td>
                        <td> ${ sentence_tokens } </td>
                    </tr>
                    <tr>
                        <td> Word stems  </td>
                        <td> ${ sentence_stems } </td>
                    </tr>
                    <tr>
                        <td> POS tags </td>
                        <td> ${ sentence_pos_tags } </td>
                    </tr>
                    <tr>
                        <td> Words Lemma </td>
                        <td> ${ sentence_lemma } </td>
                    </tr>
                    <tr>
                        <td> Sentiment </td>
                        <td> ${ sentence_sentiment } </td>
                    </tr>
                `);
            },
            error: err => {
                console.log(err)
            }
        });
    }
});

$("#random_tweet").click(() => {
    $.ajax({
        url: "https://djangonltk.herokuapp.com/api/tweet/random",
        method: "GET",
        success: response => {
            const tweet = response.tweet;
            $("#tms").html(tweet);
        },
        error: err => {
            alert("There was an error at server");
        }
    });
});