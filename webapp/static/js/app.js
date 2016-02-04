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
    var image_socket = io('localhost:5000');
    var robot_socket = io('localhost:3000');
    ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas

    ctx.fillStyle = "rgb(200,0,0)";

   setInterval(function(){ robot_socket.emit('fetchPosition') }, 1000); //Refresh data every 1 second
    robot_socket.on('position', function(msg){
        ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
        ctx.fillRect(msg.robotPosition[0], msg.robotPosition[1], msg.robotPosition[0] + 20, msg.robotPosition[1] + 20);
    });

    setInterval(function(){ image_socket.emit('fetchImage') }, 2000); //Refresh data every 1 second
    image_socket.on('sentImage', function(msg){
        var image = new Image();
        image.src = 'data:image/jpeg;base64,' + msg.image.substring(2,  msg.image.length-1);
        document.body.appendChild(image);
    });

}]);
