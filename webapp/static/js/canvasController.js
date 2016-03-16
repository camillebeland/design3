website.controller('canvasController', ['$scope', 'RobotService', 'MapService', function($scope, RobotService, MapService) {

    var canvas;
    var canvasContext;
    var robot_socket = io(ROBOT_HOST);
    var stage = new createjs.Stage("mapCanvas");
    var completeRobotRepresentation;
    var completeMesh;
    var path;
    var allIslands;

    var updateRobot = function(robotData) {
        completeRobotRepresentation.x = robotData.robotPosition[0];
        completeRobotRepresentation.y = canvas.height - robotData.robotPosition[1]; //Because of y axis direction in computer graphics convention
        completeRobotRepresentation.rotation = robotData.robotAngle;
    };

    var updatePath = function(pathData) {
        stage.removeChild(path);
        path = new createjs.Shape();
        path.graphics.setStrokeStyle(2).setStrokeDash([20, 10], 0).beginStroke("#000000");
        for (pathNode of pathData.robotPath) {
            var x = pathNode[0];
            var y = pathNode[1];
            path.graphics.lineTo(x, canvas.height - y);
        }
        stage.addChild(path);
        path.graphics.endStroke();
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

    var drawCircle = function(circleData){
        var island = new createjs.Shape();
        var circle_x = circleData.x;
        var circle_y = canvas.height - circleData.y;
        var circle_radius = circleData.radius;
        var circle_color = circleData.color;
        island.graphics.beginFill(circle_color).drawCircle(circle_x, circle_y, circle_radius);
        allIslands.addChild(island);
    };

    var drawPolygon = function(polygonData, edges_number){
        var island = new createjs.Shape();
        var polygon_x = polygonData.x;
        var polygon_y = canvas.height - polygonData.y;
        var polygon_side_length = 20;
        var polygon_color = polygonData.color;
        var polygon_angle = -90;
        island.graphics.beginFill(polygon_color).drawPolyStar(polygon_x, polygon_y, polygon_side_length, edges_number, 0, polygon_angle);
        allIslands.addChild(island);
    };

    var initIslands = function() {
        allIslands = new createjs.Container();
        var whenGetIsComplete = MapService.getMap();

        whenGetIsComplete.then(function(response) {
            for (circle of response.circles) {
                drawCircle(circle);
            }
            for (triangle of response.triangles) {
                drawPolygon(triangle, 3);
            }
            for (pentagon of response.pentagons) {
                drawPolygon(pentagon, 5);
            }
            for (square of response.squares) {
                drawPolygon(square, 4);
            }
            stage.addChild(allIslands);
        });

        MapService.getRobotPosition().then(function(response) {
            var robot_square1 = new createjs.Shape();
            var robot_square2 = new createjs.Shape();
            robot_square1.graphics.beginFill('purple').drawPolyStar(response.front[0].x, canvas.height - response.front[0].y, 10, 4, 0, response.angle);
            robot_square2.graphics.beginFill('purple').drawPolyStar(response.back[0].x, canvas.height - response.back[0].y, 10, 4, 0, response.angle);
            stage.addChild(robot_square1);
            stage.addChild(robot_square2);
        });

    };

    var initPath = function(){
        path = new createjs.Shape();
        path.graphics.moveTo(completeRobotRepresentation.x, completeRobotRepresentation.y);
    }

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

    robot_socket.on('position', function(message) {
        updateRobot(message);
    });

    setInterval(function() {
        robot_socket.emit('fetchPath');
    }, PATH_REFRESH_TIME_IN_MS);

    robot_socket.on('path', function(message) {
        var whenUpdateIsComplete = updatePath(message)
    });

    $scope.$on('islandToggleOn', function(event) {
        initIslands();
    });

    $scope.$on('islandToggleOff', function(event) {
        stage.removeChild(allIslands);
    });

    setInterval(function() {
        robot_socket.emit('fetchPosition');
    }, POSITION_REFRESH_TIME_IN_MS);

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
        initPath();

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
