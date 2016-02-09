var website = angular.module('app', ['ui.router', 'RobotService']);

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

website.controller('homeController', ['$scope', '$http', 'Robot', function($scope, $http, Robot) {

  window.BASE_STATION_HOST = "http://localhost:5000";
  window.VIDEO_STREAM = BASE_STATION_HOST + "/video_feed";
  window.ROBOT_HOST = "localhost:3000";
  window.POSITION_REFRESH_TIME_IN_MS = 100
  window.IMAGE_REFRESH_TIME_IN_MS = 5000

  var robot_socket = io(ROBOT_HOST);

  this.initVideoStream = function() {
    document.getElementById("web-cam-stream").src = VIDEO_STREAM
  };

  this.drawCanvas = function() {
    window.canvas = document.getElementById("mapCanvas");
    window.ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
    ctx.fillStyle = "rgb(200,0,0)";
  };

  setInterval(function() {
    robot_socket.emit('fetchPosition')
  }, POSITION_REFRESH_TIME_IN_MS);
  robot_socket.on('position', function(msg) {
    ctx.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
    var width = 20;
    var height = 20;
    ctx.fillRect(msg.robotPosition[0], msg.robotPosition[1], width, height);
  });

  $scope.send = function(velocity) {
    robot_socket.emit('setVelocity', velocity);
  };


  $scope.robotUp = function() {
    Robot.up();
  };

  $scope.robotDown = function() {
    Robot.down();
  };

  $scope.robotLeft = function() {
    Robot.left();
  };

  $scope.robotRight = function() {
    Robot.right();
  };

  this.init = function() {
    $scope.activeTab = TabEnum.CONTROLS;
    this.drawCanvas();
    this.initVideoStream();
  };

  this.init();

}]);
