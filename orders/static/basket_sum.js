document.addEventListener('DOMContentLoaded', function() {

    var basket_count = new XMLHttpRequest();
    basket_count.open('GET', '/basket-count', true);
    basket_count.send();

    basket_count.onload = function() {

        var count = JSON.parse(basket_count.responseText);

        if (count.count > 0) {
            document.getElementById('nav_basket_count').innerHTML = ' [' + count.count + ']';
        } else {
            document.getElementById('nav_basket_count').innerHTML = '';
        }

    };

});