$(document).ready(() => {
  let ing = 100;

  $("#add_ingredient").click(() => {
    let newLi = $(document.createElement("li"));

    newLi
      .after()
      .html(
        '<label for="ingredients-' +
          ing +
          '"></label>' +
          '<input type="text" name="ingredients-' +
          ing +
          '" id="ingredients-' +
          ing +
          '" value="" >'
      );

    newLi.appendTo("#ingredients");

    ing++;
  });
});
