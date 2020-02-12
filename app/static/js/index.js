//Popup confirm box to ensure user actually wnts to delete recipe
//redirects to the deleterecipe api using the recipes _id
$(document).ready(() => {
  $(".recipe-delete-confirm").on("click", e => {
    recipeId = $(e.target).data("id");
    if (confirm("Are you sure you want to delete this recipe?")) {
      location.href = `/deleterecipe/${recipeId}`;
    }
  });

  $("#filter-check input").on("click", () => {
    tags = [];

    if ($("#filter-check :checkbox:checked").length < 0) {
      $(".filter-div").show();
    }

    $("#filter-check :checkbox:checked").each(function() {
      tags.push($(this).val());
    });
    $("#filter-check :checkbox:checked").each(function() {
      tags.filter(tag => tag !== $(this).val());
    });

    function checkTags(div) {
      let tagsArray = $(div)
        .attr("data-tags")
        .trim()
        .split(" ");
      if (
        //https://stackoverflow.com/questions/9204283/how-to-check-whether-multiple-values-exist-within-an-javascript-array
        tags.every(val => tagsArray.includes(val))
      ) {
        $(div).show();
      } else {
        $(div).hide();
      }
    }

    const divsList = $(".filter-div");
    [...divsList].forEach(div => {
      checkTags(div);
    });
  });
});
