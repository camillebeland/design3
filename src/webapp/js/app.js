var website = angular.module('app', ['ui.router']);


website.config(function ($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    $stateProvider.state('home', {
        url: "/",
        templateUrl: "partials/home.html",
        controller: "homeController"
    })

});



website.controller('homeController', ['$scope', function ($scope) {

    var canvas = document.getElementById("mapCanvas");

    console.log("drawing");
    var ctx = canvas.getContext("2d");
    //clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "rgb(200,0,0)";
    ctx.fillRect(50, 50, 55, 50);


}]);