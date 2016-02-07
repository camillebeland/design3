var website = angular.module('app', ['ui.router']);


website.config(function ($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    $stateProvider.state('home', {
        url: "/",
        templateUrl: "static/partials/home.html",
        controller: "homeController"
    })

});


website.controller('homeController', ['$scope', '$http', function ($scope) {

    window.BASE_STATION_HOST = "localhost:5000";
    window.ROBOT_HOST = "localhost:3000";
    window.POSITION_REFRESH_TIME_IN_MS = 100
    window.IMAGE_REFRESH_TIME_IN_MS = 5000


    var base_station_socket = io(BASE_STATION_HOST);
    var robot_socket = io(ROBOT_HOST);

    this.drawCanvas = function() {
        window.canvas = document.getElementById("mapCanvas");
        window.ctx = canvas.getContext("2d");
        var base_station_socket = io(BASE_STATION_HOST);
        ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
        ctx.fillStyle = "rgb(200,0,0)";
    };

    setInterval(function(){ robot_socket.emit('fetchPosition') }, POSITION_REFRESH_TIME_IN_MS); 
    robot_socket.on('position', function(msg){
        ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
        ctx.fillRect(msg.robotPosition[0], msg.robotPosition[1], msg.robotPosition[0] + 20, msg.robotPosition[1] + 20);
    });

    setInterval(function(){ base_station_socket.emit('fetchImage') }, IMAGE_REFRESH_TIME_IN_MS); 
    base_station_socket.on('sentImage', function(msg){
        var image = new Image();
        image.src = 'data:image/png;base64,' + msg.image.substring(2,  msg.image.length-1);

        canvas.width = image.width;
        canvas.height = image.height;
        ctx.drawImage(image, 0, 0);
    });
    this.drawCanvas();

    $scope.send = function(velocity) {
        robot_socket.emit('setVelocity', velocity);
    };


}]);




