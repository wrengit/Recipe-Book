$(document).ready(() => {
  let ing = 100;

  $("#add_ingredient").click(() => {
    let newLi = $(document.createElement("li"));
    // creates a new input with id and name to allow wtforms to
    // recognise the input for correct posting to db.
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

  // delegates the event handler to #ingredients, allowing dynamically
  // generated ingredient inputs to register event.
  // checks length of input, removing element if empty.
  $("#ingredients").on("keyup", "li", e => {
    if ($(e.target).val().length == 0) {
      $(e.target)
        .parent()
        .remove();
    }
  });
});
