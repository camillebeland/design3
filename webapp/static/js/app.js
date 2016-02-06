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
    window.ROBOT_HOST = "localhost:3000";

    var robot_socket = io(ROBOT_HOST);

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


    var get_image = function(){
        $http({
            method: 'GET',
            url: BASE_STATION_HOST
        }).then(function successCallback(response) {
            var image = new Image();
            image.src = 'data:image/png;base64,' + response.data.image.substring(2,  response.data.image.length-1);
            image.onload = setTimeout(get_image());
            canvas.width = image.width;
            canvas.height = image.height;
            ctx.drawImage(image, 0, 0);
        });
    };
    get_image()

    this.drawCanvas();
}]);



