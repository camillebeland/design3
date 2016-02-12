website.controller('canvasController', ['$scope', '$http', 'Robot', function($scope, $http, Robot) {

  var canvas;
  var canvasContext;
  var robot_socket = io(ROBOT_HOST);
  var stage;
  var completeRobotRepresentation;

  var updateRobot = function(robotData) {
    completeRobotRepresentation.x = robotData.robotPosition[0];
    completeRobotRepresentation.y = canvas.height - robotData.robotPosition[1]; //Because of y axis direction in computer graphics convention
    completeRobotRepresentation.rotation = robotData.robotAngle;

    stage.update();
  };

  var initVideoStream = function() {
    document.getElementById("web-cam-stream").src = VIDEO_STREAM;
  };

  var initRobot = function() {
    stage = new createjs.Stage("mapCanvas");

    var robotSquareLength = 30;
    var robotSquare = new createjs.Shape();
    robotSquare.graphics.beginFill("red").drawRect(0, 0, robotSquareLength, robotSquareLength);
    robotSquare.regX = robotSquareLength / 2;
    robotSquare.regY = robotSquareLength / 2;

    var circle = new createjs.Shape();
    var circleInitialPositionX = 0;
    var circleInitialPositionY = -robotSquareLength / 2;
    var circleRadius = 5;
    circle.graphics.beginFill("black").drawCircle(circleInitialPositionX, circleInitialPositionY, circleRadius);

    completeRobotRepresentation = new createjs.Container();
    var robotSquareMiddle = robotSquareLength / 2;
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
