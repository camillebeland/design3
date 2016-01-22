var website = angular.module('app', ['ui.router']);


website.config(function ($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    $stateProvider.state('home', {
        url: "/",
        templateUrl: "partials/home.html"
    })
});

var canvas = angular.element(document.getElementById("mapCanvas"));
//var stage = new createjs.Stage(canvas);

if (canvas.getContext) {
    var ctx = canvas.getContext("2d");

    ctx.fillStyle = "rgb(200,0,0)";
    ctx.fillRect(10, 10, 55, 50);

    ctx.fillStyle = "rgba(0, 0, 200, 0.5)";
    ctx.fillRect(30, 30, 55, 50);
}