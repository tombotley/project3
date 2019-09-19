document.addEventListener('DOMContentLoaded', function() {

    var extra_count = 0;
    console.log(extra_count);
    document.getElementById('toppings').style.display = 'none';
    document.getElementById('extra1').style.display = 'none';
    document.getElementById('extra2').style.display = 'none';
    document.getElementById('extra3').style.display = 'none';
    document.getElementById('extra4').style.display = 'none';

    document.getElementById('check_pizza_total').onclick = function() {

        var pizza_choice = getPizzaChoice();

        if (typeof pizza_choice !== 'undefined') {

            var quantity = document.querySelector('.pizza_quantity').value;
            var result = getPizzaPrice(pizza_choice[0], pizza_choice[1], pizza_choice[2]);

            if (typeof result !== 'undefined') {
                var total = result * quantity;
                var cost = total.toFixed(2);

                document.getElementById('pizza_total').innerHTML = '$' + cost;
            }
        }

    };

    document.getElementById('add_pizza').onclick = function() {

        var pizza_choice = getPizzaChoice();

        if (pizza_choice !== false) {

            var select_pizza = document.getElementById('pizza_selection');
            var no_of_toppings = select_pizza.options[select_pizza.selectedIndex].dataset.desc;

            var toppings;

            if (no_of_toppings.charAt(0) == '1') {
                toppings = getToppings(1);
            } else if (no_of_toppings.charAt(0) == '2') {
                toppings = getToppings(2);
            } else if (no_of_toppings.charAt(0) == '3') {
                toppings = getToppings(3);
            }

            if (toppings !== false) {
                document.getElementById('pizza_form').submit();
            }
        }

    };

    document.getElementById('check_sub_total').onclick = function() {

        var sub_choice = getSubChoice();
        console.log(sub_choice);

        if (typeof sub_choice !== 'undefined') {

            var quantity = document.querySelector('.sub_quantity').value;
            var result = parseFloat(getSubPrice(sub_choice[0], sub_choice[1]));

            if (extra_count > 0) {

                var extras = getExtras(extra_count);
                console.log(extras);

                if (extras !== false) {

                    var extras_cost = extras[1];
                    console.log(result);
                    console.log(extras_cost);
                    result = result + extras_cost;
                    console.log(result);
                }
            }

            if (typeof result !== 'undefined') {

                var total = result * quantity;
                var cost = total.toFixed(2);

                document.getElementById('sub_total').innerHTML = '$' + cost;
            }
        }

    };

    document.getElementById('add_sub').onclick = function() {

        var sub_choice = getSubChoice();

        if (sub_choice !== false) {
            document.getElementById('sub_form').submit();
        }

    };

    document.getElementById('add_extras').onclick = function() {

        var extra;

        if (extra_count < 4) {

            if (extra_count > 0) {
                var extra_num = 'extra' + extra_count;
                var extra_selection = document.getElementById(extra_num);
                extra = extra_selection.options[extra_selection.selectedIndex].value;
            }

            if (extra !== 'unselected') {
                extra_count++;
                var extra_add = 'extra' + extra_count;
                document.getElementById(extra_add).style.display = 'block';
            } else {
                alert('Please select your previous extra!');
            }

        } else {
            alert('Maximum 4 extras per sub');
        }

    };

    document.getElementById('remove_extras').onclick = function() {

        if (extra_count > 0) {

            var extra_remove = 'extra' + extra_count;
            console.log(extra_remove);
            document.getElementById(extra_remove).style.display = 'none';
            document.getElementById(extra_remove).selectedIndex = 0;
            extra_count--;
            console.log(extra_count);
        }

    };

    document.getElementById('add_pasta').onclick = function() {

        var select_pasta = document.getElementById('pasta_selection');
        pasta = pasta_selection.options[pasta_selection.selectedIndex].value;

        if (pasta !== 'unselected') {
            document.getElementById('pasta_form').submit();
        } else {
            alert('Please select your pasta');
        }

    };

    document.getElementById('add_platter').onclick = function() {

        var select_platter = document.getElementById('platter_selection');
        platter = platter_selection.options[platter_selection.selectedIndex].value;

        if (platter !== 'unselected') {
            document.getElementById('platter_form').submit();
        } else {
            alert('Please select your platter');
        }

    };

    document.getElementById('add_salad').onclick = function() {

        var select_salad = document.getElementById('salad_selection');
        salad = salad_selection.options[salad_selection.selectedIndex].value;

        if (salad !== 'unselected') {
            document.getElementById('salad_form').submit();
        } else {
            alert('Please select your salad');
        }

    };

});

function pizzaToppings() {

    resetTotal('pizza');
    var select_pizza = document.getElementById('pizza_selection');
    var choice = select_pizza.options[select_pizza.selectedIndex].dataset.desc;
    var toppings = choice.charAt(0);

    document.getElementById('toppings').style.display = 'none';
    document.getElementById('topping2').style.display = 'block';
    document.getElementById('topping3').style.display = 'block';

    if (toppings == '1') {
        document.getElementById('toppings').style.display = 'block';
        document.getElementById('topping2').style.display = 'none';
        document.getElementById('topping2').selectedIndex = 0;
        document.getElementById('topping3').style.display = 'none';
        document.getElementById('topping3').selectedIndex = 0;
    } else if (toppings == '2') {
        document.getElementById('toppings').style.display = 'block';
        document.getElementById('topping3').style.display = 'none';
        document.getElementById('topping3').selectedIndex = 0;
    } else if (toppings == '3') {
        document.getElementById('toppings').style.display = 'block';
    } else {
        document.getElementById('topping1').selectedIndex = 0;
        document.getElementById('topping2').selectedIndex = 0;
        document.getElementById('topping3').selectedIndex = 0;
    }

};

function getPizzaChoice() {

    var select_pizza = document.getElementById('pizza_selection');
    var pizza = select_pizza.options[select_pizza.selectedIndex].value;
    var select_style = document.getElementById('style_selection');
    var style = select_style.options[select_style.selectedIndex].value;
    var select_pizza_size = document.getElementById('pizza_size_selection');
    var size = select_pizza_size.options[select_pizza_size.selectedIndex].value;

    if (pizza == 'unselected' || style == 'unselected' || size == 'unselected') {
        resetTotal('pizza');
        alert('Please complete your pizza options');
        return false;
    } else {
        return [pizza, style, size];
    }

};

function getToppings(num) {

    if (num == 1) {

        var topping = getTopping('topping1');

        if (topping.includes('unselected')) {
            alert('Please complete your topping selection');
            return false;
        } else {
            return topping;
        }

    } else if (num == 2) {

        var topping_1 = getTopping('topping1');
        var topping_2 = getTopping('topping2');
        var toppings = topping_1 + ', ' + topping_2;

        if (toppings.includes('unselected')) {
            alert('Please complete your topping selection');
            return false;
        } else {
            return toppings;
        }

    } else if (num == 3) {

        var topping_1 = getTopping('topping1');
        var topping_2 = getTopping('topping2');
        var topping_3 = getTopping('topping3');
        var toppings = topping_1 + ', ' + topping_2 + ', ' + topping_3;

        if (toppings.includes('unselected')) {
            alert('Please complete your topping selection');
            return false;
        } else {
            return toppings;
        }
    }

};

function getTopping(topping_num) {

    var topping_selection = document.getElementById(topping_num);
    var topping = topping_selection.options[topping_selection.selectedIndex].value;
    return topping;

};

function getPizzaPrice(pizza, style, size) {

    var prices = JSON.parse(pizza_prices);

    for (var p = 0; p < prices.length; p++) {

        if (prices[p].fields['pizza_type'] == pizza && prices[p].fields['pizza_style'] == style && prices[p].fields['pizza_size'] == size) {
            result = prices[p].fields['price'];
            return result;
        }
    }

};

function getSubChoice() {

    var select_sub = document.getElementById('sub_selection');
    var sub = select_sub.options[select_sub.selectedIndex].value;
    var select_sub_size = document.getElementById('sub_size_selection');
    var size = select_sub_size.options[select_sub_size.selectedIndex].value;

    if (sub == 'unselected' || size == 'unselected') {
        resetTotal('sub');
        alert('Please complete your sub options');
        return false;
    } else {
        return [sub, size];
    }

};

function getExtras(count) {

    var extras = '';
    var cost = 0;

    for (var e = 1; e <= count; e++) {

        var extra_num = 'extra' + e;
        var extra_selection = document.getElementById(extra_num);
        var extra = extra_selection.options[extra_selection.selectedIndex].value;
        var extra_price = extra_selection.options[extra_selection.selectedIndex].dataset.price;

        if (extra !== 'unselected') {

            extras = extras + extra + ', ';
            cost = cost + parseFloat(extra_price);
        }
    }

    if (cost == 0) {
        return false;
    } else {
        return [extras, cost];
    }

};

function getSubPrice(sub, size) {

    var prices = JSON.parse(sub_prices);

    for (var p = 0; p < prices.length; p++) {

        if (prices[p].fields['sub_type'] == sub && prices[p].fields['sub_size'] == size) {
            result = prices[p].fields['price'];
            return result;
        }
    }

};

function resetTotal(reset) {

    if (reset == 'pizza') {
        document.getElementById('pizza_total').innerHTML = '$';
    } else if (reset == 'sub') {
        document.getElementById('sub_total').innerHTML = '$';
    }

};