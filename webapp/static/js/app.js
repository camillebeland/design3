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
    var socket = io('localhost:3000');
    ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas

    ctx.fillStyle = "rgb(200,0,0)";

    setInterval(function(){ socket.emit('fetchPosition') }, 1000); //Refresh data every 1 second
    socket.on('position', function(msg){
        ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
        ctx.fillRect(msg.robotPosition[0], msg.robotPosition[1], msg.robotPosition[0] + 20, msg.robotPosition[1] + 20);
    });

}]);
