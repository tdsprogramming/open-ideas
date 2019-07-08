
var form = '<form method="post">' + {% csrf_token %} + '{{comment_form|crispy}} <input type="submit" class="btn btn-md btn-success"></form>';

function showCommentForm(e){
    $("#post-comment").html(form);
}
