$(document).ready(function() {

    $("#tache").hide();
    $("#activite").hide();
    $("#historique").hide();
    $("#phenomene").hide();
    $("#strategique").hide();
    $("#domaine").hide();
    $("#default").show();

    $("#tache-click").click(function() {


        $("#tache-click").css("background-color", "rgb(70, 180, 225)");
        $("#activte-click").css("background-color", "white");
        $("#historique-click").css("background-color", "white");
        $("#phenomene-click").css("background-color", "white");
        $("#strategique-click").css("background-color", "white");
        $("#domaine-click").css("background-color", "white");

        $("#default").hide();
        $("#tache").show();
        $("#activite").hide();
        $("#historique").hide();
        $("#phenomene").hide();
        $("#strategique").hide();
        $("#domaine").hide();
    });
    $("#activite-click").click(function() {

        $("#activite-click").css("background-color", "rgb(70, 180, 225)");
        $("#tache-click").css("background-color", "white");
        $("#historique-click").css("background-color", "white");
        $("#phenomene-click").css("background-color", "white");
        $("#strategique-click").css("background-color", "white");
        $("#domaine-click").css("background-color", "white");

        $("#default").hide();
        $("#activite").show();
        $("#tache").hide();
        $("#historique").hide();
        $("#phenomene").hide();
        $("#strategique").hide();
        $("#domaine").hide();
    });
    $("#historique-click").click(function() {

        $("#historique-click").css("background-color", "rgb(70, 180, 225)");
        $("#tache-click").css("background-color", "white");
        $("#activite-click").css("background-color", "white");
        $("#phenomene-click").css("background-color", "white");
        $("#strategique-click").css("background-color", "white");
        $("#domaine-click").css("background-color", "white");

        $("#default").hide();
        $("#historique").show();
        $("#tache").hide();
        $("#activite").hide();
        $("#phenomene").hide();
        $("#strategique").hide();
        $("#domaine").hide();
    });
    $("#phenomene-click").click(function() {

        $("#default").hide();
        $("#phenomene-click").css("background-color", "rgb(70, 180, 225)");
        $("#tache-click").css("background-color", "white");
        $("#activite-click").css("background-color", "white");
        $("#historique-click").css("background-color", "white");
        $("#strategique-click").css("background-color", "white");
        $("#domaine-click").css("background-color", "white");

        $("#tache").hide();
        $("#activite").hide();
        $("#historique").hide();
        $("#phenomene").show();
        $("#strategique").hide();
        $("#domaine").hide();
    });
    $("#strategique-click").click(function() {

        $("#default").hide();
        $("#strategique-click").css("background-color", "rgb(70, 180, 225)");
        $("#tache-click").css("background-color", "white");
        $("#activite-click").css("background-color", "white");
        $("#historique-click").css("background-color", "white");
        $("#phenomene-click").css("background-color", "white");
        $("#domaine-click").css("background-color", "white");

        $("#tache").hide();
        $("#activite").hide();
        $("#historique").hide();
        $("#phenomene").hide();
        $("#strategique").show();
        $("#domaine").hide();
    });
    $("#domaine-click").click(function() {

        $("#domaine-click").css("background-color", "rgb(70, 180, 225)");
        $("#tache-click").css("background-color", "white");
        $("#activite-click").css("background-color", "white");
        $("#historique-click").css("background-color", "white");
        $("#phenomene-click").css("background-color", "white");
        $("#strategique-click").css("background-color", "white");

        $("#default").hide();
        $("#domaine").show();
        $("#tache").hide();
        $("#activite").hide();
        $("#historique").hide();
        $("#phenomene").hide();
        $("#strategique").hide();

    });
});