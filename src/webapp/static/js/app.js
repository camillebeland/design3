var website = angular.module('app', ['ui.router']);


website.config(function ($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    $stateProvider.state('home', {
        url: "/",
        templateUrl: "static/partials/home.html",
        controller: "homeController"
    })

});



website.controller('homeController', ['$scope', function ($scope) {

    var canvas = document.getElementById("mapCanvas");
    var ctx = canvas.getContext("2d");
    var socket = io();
    ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas

    ctx.fillStyle = "rgb(200,0,0)";

    setInterval(function(){ socket.emit('message') }, 3000); //Refresh data every 3 seconds
    socket.on('event', function(msg){
        ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
        ctx.fillRect(msg.data, msg.data, msg.data, msg.data);
    });

}]);