document.addEventListener('DOMContentLoaded', function() {

    var order_id;

    // listen for clicks on all elements of class statusBtn and retrieve value

    document.querySelectorAll('.statusBtn').onclick = function() {

        order_id = document.querySelectorAll('.statusBtn').value;

    };

    document.getElementById('update_status').onclick = function() {

        status = document.getElementById('status_select').value;

        if (status !== 'unselected') {
            var status_update = new XMLHttpRequest();
            status_update.open('POST', '/update-status/{order_id}/{status}', true);
            status_update.send();
        }

    };

};