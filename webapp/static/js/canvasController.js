website.controller('canvasController', ['$scope', '$http', 'Robot', function($scope, $http, Robot) {

  var canvas;
  var canvasContext;
  var robot_socket = io(ROBOT_HOST);
  var stage;
  var completeRobotRepresentation;

  var updateRobot = function(robotData) {
    completeRobotRepresentation.x = robotData.robotPosition[0];
    completeRobotRepresentation.y = robotData.robotPosition[1];
    completeRobotRepresentation.rotation = robotData.robotAngle;

    stage.update();
  };

  var initVideoStream = function() {
    document.getElementById("web-cam-stream").src = VIDEO_STREAM
  };

  var initRobot = function() {
    stage = new createjs.Stage("mapCanvas");

    var robotSquareWidth = 30;
    var robotSquareHeight = 30;
    var robotSquare = new createjs.Shape();
    robotSquare.graphics.beginFill("red").drawRect(0, 0, robotSquareWidth, robotSquareHeight);
    robotSquare.regX = robotSquareWidth / 2;
    robotSquare.regY = robotSquareHeight / 2;

    var circle = new createjs.Shape();
    var circleInitialPositionX = 0;
    var circleInitialPositionY = -robotSquareWidth/2;
    var circleRadius = 5;
    circle.graphics.beginFill("black").drawCircle(circleInitialPositionX, circleInitialPositionY, circleRadius);

    completeRobotRepresentation = new createjs.Container();
    var robotSquareMiddle = robotSquareWidth/2;
    completeRobotRepresentation.addChild(robotSquare, circle);

    stage.addChild(completeRobotRepresentation);
  }

  setInterval(function() {
    robot_socket.emit('fetchPosition')
  }, POSITION_REFRESH_TIME_IN_MS);
  robot_socket.on('position', function(msg) {

    updateRobot(msg);
  });

  function canvasController() {
    canvas = document.getElementById("mapCanvas");
    canvasContext = canvas.getContext("2d");
    initVideoStream();
    initRobot();
  }

  canvasController();
}])
