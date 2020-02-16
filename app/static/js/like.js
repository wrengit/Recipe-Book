$(document).ready(function() {
  //https://www.reddit.com/r/flask/comments/chm0qu/have_upvotedownvotes_buttons_that_dont_reload_the/
  //ajax request to access the 'like' route in views.py
  $(".like-btn").on("click", function(e) {
    recipe_id = $(this).data("id");
    $.ajax({
      url: `/like/${recipe_id}`,
      type: "post",
      success: function(response) {
        console.log(response);
      },
      error: function(xhr) {
        console.log(xhr);
      }
    });
    e.preventDefault();
    //checks to see if the like button has the class 'like-red', which shows that the users username
    //is in the db, and has therefor liked the recipe. Toggles 'like-red' and also adds +-1
    //to the like count.
    $(this).toggleClass("like-red");
    count = Number($(`#like-counter-${recipe_id}`).html());
    plus_count = count + 1;
    minus_count = count - 1;
    if ($(this).hasClass("like-red")) {
      $(`#like-counter-${recipe_id}`).html(`${plus_count}`);
    } else {
      $(`#like-counter-${recipe_id}`).html(`${minus_count}`);
    }
  });
});
