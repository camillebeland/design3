website.controller('canvasController', ['$scope', '$http', 'Robot', function($scope, $http, Robot) {

  var canvas;
  var canvasContext;
  var robot_socket = io(ROBOT_HOST);
  var stage;
  var robot;

  var drawCanvas = function() {
    canvasContext.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
    canvasContext.fillStyle = "rgb(200,0,0)";
  };

  var initVideoStream = function() {
    document.getElementById("web-cam-stream").src = VIDEO_STREAM
  };

  var initRobot = function(){
    //canvasContext.clearRect(0, 0, canvas.width, canvas.height); //clear the canvas
    var width = 20;
    var height = 20;
  //  canvasContext.fillRect(msg.robotPosition[0], msg.robotPosition[1], width, height);

    stage = new createjs.Stage("mapCanvas");
    robot = new createjs.Shape();
    robot.graphics.beginFill("blue").drawRect(0, 0, width, height);
    stage.addChild(robot);
  }

  setInterval(function() {
    robot_socket.emit('fetchPosition')
  }, POSITION_REFRESH_TIME_IN_MS);
  robot_socket.on('position', function(msg) {

    //Set position of Shape instance.
    robot.x = msg.robotPosition[0];
    robot.y = msg.robotPosition[1];
    //Add Shape instance to stage display list.
stage.addChild(robot);
    //Update stage will render next frame
    stage.update();
    console.log("Robot angle: " + msg.robotAngle);
  });

  function canvasController() {
    canvas = document.getElementById("mapCanvas");
    canvasContext = canvas.getContext("2d");
    drawCanvas();
    initVideoStream();
    initRobot();
  }

  canvasController();
}])
