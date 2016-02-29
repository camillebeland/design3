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
    robotSquare.graphics.beginFill("blue").drawRect(0, 0, robotSquareWidth, robotSquareHeight);
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

    var initMap = function() {
        MapService.getMap().then(function(response) {
            for (circle of response.circles) {
                var island = new createjs.Shape();
                var circle_x = circle.x;
                var circle_y = circle.y;
                var circle_radius = circle.radius;
                var circle_color = circle.color;
                island.graphics.beginFill(circle_color).drawCircle(circle_x,circle_y,circle_radius);
                stage.addChild(island);
            }
            for (triangle of response.triangles) {
                var island = new createjs.Shape();
                var triangle_x = triangle.x;
                var triangle_y = triangle.y;
                var triangle_side_length = 30;
                var triangle_color = triangle.color;
                var triangle_angle = -90;
                island.graphics.beginFill(triangle_color).drawPolyStar(triangle_x, triangle_y, triangle_side_length, 3, 0, triangle_angle);
                stage.addChild(island);
            }
            for (pentagon of response.pentagons) {
                var island = new createjs.Shape();
                var pentagon_x = pentagon.x;
                var pentagon_y = pentagon.y;
                var pentagon_side_length = 30;
                var pentagon_color = pentagon.color;
                var pentagon_angle = -90;
                island.graphics.beginFill(pentagon_color).drawPolyStar(pentagon_x, pentagon_y, pentagon_side_length, 5, 0, pentagon_angle);
                stage.addChild(island);
            }
            for (square of response.squares) {
                var island = new createjs.Shape();
                var square_x = square.x;
                var square_y = square.y;
                var square_side_length = 30;
                var square_color = square.color;
                var square_angle = -90;
                island.graphics.beginFill(square_color).drawPolyStar(square_x, square_y, square_side_length, 4, 0, square_angle);
                stage.addChild(island);
            }
        });
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
      initMap();
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
