$(document).ready(() => {
  //https://stackoverflow.com/questions/2155453/jquery-toggle-text
  $.fn.extend({
    toggleText: function(a, b) {
      return this.text(this.text() == b ? a : b);
    }
  });
  $("#toggle-profile").on("click", function() {
    $(this).toggleText("Show Liked", "Show Owned");
    $("#profile-jumbo-text").toggleText(
      "Take a look at your posted recipes below",
      "Here are the recipes that you have liked"
    );
    $("#liked-recipes").toggle();
    $("#owned-recipes").toggle();
  });
});
