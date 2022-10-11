$(document).ready(function() {
    $("#hide-list").click(function() {
        $("#show-list").show();
        $(".list-connaissance-hide").hide();
        $("#list-connaissance").hide();
        $("#hide-list").hide();

    });
    $("#show-list").click(function() {
        $("#hide-list").show();
        $(".list-connaissance-hide").show();
        $("#list-connaissance").show();
        $("#show-list").hide();

    });
});