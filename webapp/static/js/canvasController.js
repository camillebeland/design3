website.controller('canvasController', ['$scope', '$http', 'Robot', function($scope, $http, Robot) {

  var canvas;
  var canvasContext;
  var robot_socket = io(ROBOT_HOST);

  var drawCanvas = function() {
    canvasContext.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
    canvasContext.fillStyle = "rgb(200,0,0)";
  };

  var initVideoStream = function() {
    document.getElementById("web-cam-stream").src = VIDEO_STREAM
  };

  setInterval(function() {
    robot_socket.emit('fetchPosition')
  }, POSITION_REFRESH_TIME_IN_MS);
  robot_socket.on('position', function(msg) {
    canvasContext.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
    var width = 20;
    var height = 20;
    canvasContext.fillRect(msg.robotPosition[0], msg.robotPosition[1], width, height);
    console.log("Robot angle: " + msg.robotAngle);
  });

  function canvasController() {
    canvas = document.getElementById("mapCanvas");
    canvasContext = canvas.getContext("2d");
    drawCanvas();
    initVideoStream();
  }

  canvasController();
}])
