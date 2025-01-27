odoo.define('theme_sb.home_plans', [], function (require) {
    "use strict";

    $(document).ready(function () {
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: '/home_plans',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({'jsonrpc': "2.0", 'method': "home_plans", "params": {'limit': 1}}),
            success: function (action) {
                console.log(action.result)
            },
        });
    })
})
