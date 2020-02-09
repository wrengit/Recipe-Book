//Popup confirm box to ensure user actually wnts to delete recipe
//redirects to the deleterecipe api using the recipes _id
$(document).ready(() => {
  $("#recipe-delete-confirm").on("click", e => {
    recipeId = $(e.target).data("id");
    if (confirm("Are you sure you want to delete this recipe?")) {
      location.href = `/deleterecipe/${recipeId}`;
    }
  });
});
