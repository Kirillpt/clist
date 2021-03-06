function toggle_hide_contest(e) {
    e.preventDefault();
    var icon = $(this);
    $.ajax({
        type: 'GET',
        url: document.URL,
        data: {
            pk: icon.attr("data-contest-id"),
            action: "hide-contest-toggle",
        },
        success: function(data) {
            icons = $('.hide-contest[data-contest-id="' + icon.attr("data-contest-id") + '"]');
            if (icon.hasClass("fa-eye")) {
                icons.parent().find('.contest_title>a').css({textDecoration: 'line-through'});
                icons.parent().find('.fc-title').css({textDecoration: 'line-through'});
            } else {
                icons.parent().find('.contest_title>a').css({textDecoration: 'none'});
                icons.parent().find('.fc-title').css({textDecoration: 'none'});
            }
            icons.toggleClass("fa-eye");
            icons.toggleClass("fa-eye-slash");
        },
    })
}

$(function() {
    $(".toggle").click(function(e) {
        var cls = $(this).attr("data-group");
        $(cls).toggleClass("hidden");
        var icon = $(".badge[data-group='{0}']".format(cls)).find("i");
        icon.toggleClass("fa-caret-down");
        icon.toggleClass("fa-caret-up");
        e.preventDefault();
    })

    $("#toggle-all").click(function (e) {
        var icon = $(this).find("i");
        var cls = $(icon).attr("class").match(/fa-caret-[\w-]*/)[0];
        icon.toggleClass("fa-caret-down");
        icon.toggleClass("fa-caret-up");
        $(".toggle.badge>i[class~='{0}']".format(cls)).click();
        e.preventDefault();
    })

    $(".party-check[data-contest-id]").click(function (e) {
        var icon = $(this);
        $.ajax({
            type: 'GET',
            url: document.URL,
            data: {
                pk: icon.attr("data-contest-id"),
                action: "party-contest-toggle",
            },
            success: function(data) {
                icon.toggleClass("fa-check-square");
                icon.toggleClass("fa-square");
            },
        })
    })


    $(".hide-contest[data-contest-id]").click(toggle_hide_contest)
});
