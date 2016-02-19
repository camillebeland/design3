website.controller('canvasController', ['$scope', 'Mesh', function($scope, Mesh) {

  var canvas;
  var canvasContext;
  var robot_socket = io(ROBOT_HOST);
  var stage = new createjs.Stage("mapCanvas");
  var completeRobotRepresentation;

  var updateRobot = function(robotData) {
    completeRobotRepresentation.x = robotData.robotPosition[0];
    completeRobotRepresentation.y = canvas.height - robotData.robotPosition[1]; //Because of y axis direction in computer graphics convention
    completeRobotRepresentation.rotation = robotData.robotAngle;
  };

  var initVideoStream = function() {
    var image = new Image();
    image.src = "http://"+VIDEO_STREAM;
    var bitmap = new createjs.Bitmap(image);
    stage.addChildAt(bitmap);
  };

  var initRobot = function() {
    var robotSquareWidth = 30;
    var robotSquareHeight = 30;
    var robotSquare = new createjs.Shape();
    robotSquare.graphics.beginFill("red").drawRect(0, 0, robotSquareWidth, robotSquareHeight);
    robotSquare.regX = robotSquareWidth / 2;
    robotSquare.regY = robotSquareHeight / 2;

    var circle = new createjs.Shape();
    var circleInitialPositionX = 0;
    var circleInitialPositionY = -robotSquareWidth / 2;
    var circleRadius = 5;
    circle.graphics.beginFill("black").drawCircle(circleInitialPositionX, circleInitialPositionY, circleRadius);

    completeRobotRepresentation = new createjs.Container();
    completeRobotRepresentation.addChild(robotSquare, circle);

    stage.addChild(completeRobotRepresentation);
  };

  var initMesh = function() {
    Mesh.get(function(mesh){
      for (cell of mesh.cells) {
        var square = new createjs.Shape();
        square.graphics.beginStroke("black").drawRect(cell.x - cell.width / 2, cell.y - cell.height / 2, cell.width, cell.height);
        stage.addChildAt(square);
      }
    });
  };

  setInterval(function() {
     robot_socket.emit('fetchPosition');
  }, POSITION_REFRESH_TIME_IN_MS);

  robot_socket.on('position', function(msg) {
    updateRobot(msg);
  });

  setInterval(function() {
    stage.update();
  }, CANVAS_REFRESH_TIME_IN_MS);

  function canvasController() {
    canvas = document.getElementById("mapCanvas");
    canvasContext = canvas.getContext("2d");
    canvas.height = CANVAS_HEIGHT;
    canvas.width = CANVAS_WIDTH;
    initVideoStream();
    initMesh();
    initRobot();
  }
  canvasController();
}]);