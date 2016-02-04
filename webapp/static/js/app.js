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

    var robot_socket = io('http://localhost:3000');
    var map_socket = io('http://localhost:5000');
    ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas

    ctx.fillStyle = "rgb(200,0,0)";

    setInterval(function(){
        if(robot_socket.connected) {
            robot_socket.emit('fetchPosition')
        }
    }, 1000); //Refresh data every 1 second

    robot_socket.on('position', function(msg){
        ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
        ctx.fillRect(msg.robotPosition[0], msg.robotPosition[1], msg.robotPosition[0] + 20, msg.robotPosition[1] + 20);
    });

    setInterval(function(){
        if(map_socket.connected) {
            map_socket.emit('fetch-image')
        }
    }, 3000); //Refresh data every 1 second
    map_socket.on('image2', function(msg){
        ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
        ctx.fillRect(msg.image);
    });


    $scope.send = function(velocity){
        robot_socket.emit('aaa', {x_velocity:1, y_velocity:2});
    };
    



}]);
