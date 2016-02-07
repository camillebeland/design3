var website = angular.module('app', ['ui.router']);


website.config(function ($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    $stateProvider.state('home', {
        url: "/",
        templateUrl: "static/partials/home.html",
        controller: "homeController"
    })

});


website.controller('homeController', ['$scope', '$http', function ($scope, $http) {

    window.BASE_STATION_HOST = "http://localhost:5000";
    window.VIDEO_STREAM = BASE_STATION_HOST + "/video_feed";
    window.ROBOT_HOST = "localhost:3000";

    var robot_socket = io(ROBOT_HOST);

    this.initVideoStream = function(){
      document.getElementById("web-cam-stream").src = VIDEO_STREAM
    };

    this.drawCanvas = function() {
        window.canvas = document.getElementById("mapCanvas");
        window.ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
        ctx.fillStyle = "rgb(200,0,0)";
    };

    setInterval(function(){ robot_socket.emit('fetchPosition') }, 1000); //Refresh data every 1 second
    robot_socket.on('position', function(msg){
        ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
        ctx.fillRect(msg.robotPosition[0], msg.robotPosition[1], msg.robotPosition[0] + 20, msg.robotPosition[1] + 20);
    });

    this.drawCanvas();
    this.initVideoStream();
}]);



