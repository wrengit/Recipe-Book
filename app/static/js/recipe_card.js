'use strict';

var RecipeCard = function RecipeCard() {
    return React.createElement(
        'div',
        null,
        'Does this work?'
    );
};

var domContainer = document.querySelector('#react-recipe-card');
ReactDOM.render(React.createElement(RecipeCard, null), domContainer);