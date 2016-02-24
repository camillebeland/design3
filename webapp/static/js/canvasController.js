website.controller('canvasController', ['$scope', 'RobotService', 'MapService', function($scope, RobotService, MapService) {

  var canvas;
  var canvasContext;
  var robot_socket = io(ROBOT_HOST);
  var stage = new createjs.Stage("mapCanvas");
  var completeRobotRepresentation;
  var completeMesh;

  var updateRobot = function(robotData) {
    completeRobotRepresentation.x = robotData.robotPosition[0];
    completeRobotRepresentation.y = canvas.height - robotData.robotPosition[1]; //Because of y axis direction in computer graphics convention
    completeRobotRepresentation.rotation = robotData.robotAngle;
  };

  var initVideoStream = function() {
    var image = new Image();
    image.src = "http://" + VIDEO_STREAM;
    var bitmap = new createjs.Bitmap(image);
    stage.addChild(bitmap);
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
    var whenGetIsComplete = MapService.getMesh();

    whenGetIsComplete.then(function(response) {
      completeMesh = new createjs.Container();
      for (cell of response.cells) {
        var square = new createjs.Shape();
        var rectTopLeftX = cell.x - cell.width / 2;
        var rectTopLeftY = cell.y + cell.height / 2;
        square.graphics.beginStroke("black").drawRect(rectTopLeftX, canvas.height - rectTopLeftY, cell.width, cell.height);
        completeMesh.addChild(square);
      }
      stage.addChild(completeMesh);
    });
  };


  $scope.$on('meshToggleOn', function(event) {
    initMesh();
  });

  $scope.$on('meshToggleOff', function(event) {
    stage.removeChild(completeMesh);
  });

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
    initRobot();
      function getMousePos(canvas, evt) {
          var rect = canvas.getBoundingClientRect();
          return {
              x: evt.clientX - rect.left,
              y: CANVAS_HEIGHT - (evt.clientY - rect.top)
          };
      }

      canvas.addEventListener('mousedown', function(evt) {
          var mousePos = getMousePos(canvas, evt);
          RobotService.move_to(mousePos);
      }, false);

  }
    canvasController();
}]);
