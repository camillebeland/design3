var website = angular.module('app', ['ui.router']);


website.config(function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise('/');

  $stateProvider.state('home', {
    url: "/",
    templateUrl: "static/partials/home.html",
    controller: "homeController"
  })

});

TabEnum = Object.freeze({
  CONTROLS: "CONTROLS",
  OTHER: "OTHER"
});

website.controller('homeController', ['$scope', '$http', function($scope, $http) {

  window.BASE_STATION_HOST = "localhost:5000";
  window.ROBOT_HOST = "localhost:3000";

  var base_station_socket = io(BASE_STATION_HOST);
  var robot_socket = io(ROBOT_HOST);

  this.drawCanvas = function() {
    var canvas = document.getElementById("mapCanvas");
    var ctx = canvas.getContext("2d");
    var base_station_socket = io('localhost:5000');
    ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
    ctx.fillStyle = "rgb(200,0,0)";

    setInterval(function() {
      robot_socket.emit('fetchPosition')
    }, 1000); //Refresh data every 1 second
    robot_socket.on('position', function(msg) {
      ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
      ctx.fillRect(msg.robotPosition[0], msg.robotPosition[1], msg.robotPosition[0] + 20, msg.robotPosition[1] + 20);
    });

    setInterval(function() {
      base_station_socket.emit('fetchImage')
    }, 2000); //Refresh data every 2 second
    base_station_socket.on('sentImage', function(msg) {
      var image = new Image();
      image.src = 'data:image/jpeg;base64,' + msg.image.substring(2, msg.image.length - 1);

      canvas.width = image.width;
      canvas.height = image.height;
      ctx.drawImage(image, 0, 0);
    });
  }

  this.init = function() {
    $scope.activeTab = TabEnum.CONTROLS;
    this.drawCanvas();
  };

  this.init();

}]);
