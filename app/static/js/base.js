$(document).ready(function() {
  $("body").bootstrapMaterialDesign();
  //put a checkbox selection into an array on check, removes on uncheck,
  //then compares the data-tag attribute of each
  //recipe against this array. Only recipes that meet all checkbox requirements are shown.
  //If no checkboxes:checked, then all recipes show
  $("#filter-check input").on("click", () => {
    tags = [];

    if ($("#filter-check :checkbox:checked").length < 0) {
      $(".filter-div").show();
    }

    $("#filter-check :checkbox:checked").each(function() {
      tags.push($(this).val());
      tags.filter(tag => tag !== $(this).val());
    });

    function checkTags(div) {
      let tagsArray = $(div)
        .attr("data-tags")
        .trim()
        .split(" ");
      if (
        //(https://stackoverflow.com/questions/9204283/how-to-check-whether-multiple-values-
        //exist-within-an-javascript-array)
        tags.every(val => tagsArray.includes(val))
      ) {
        $(div).show();
      } else {
        $(div).hide();
      }
    }

    //@john_lynch_alumnus provided solution by suggesting a spread operator
    const divsList = $(".filter-div");
    [...divsList].forEach(div => {
      checkTags(div);
    });
  });
});
