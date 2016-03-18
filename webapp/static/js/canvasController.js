website.controller('canvasController', ['$scope', 'RobotService', 'MapService', 'UnitConvertingService', function($scope, robotService, MapService, unitConvertingService) {

    var canvas;
    var canvasContext;
    var robot_socket = io(ROBOT_HOST);
    var stage = new createjs.Stage("mapCanvas");
    var completeRobotRepresentation;
    var completeMesh;
    var path;
    var allIslands;
    var xScale;
    var yScale;

    var updateRobotRepresentation = function(robotModel) {
        completeRobotRepresentation.x = (robotModel.position[0] * xScale);
        completeRobotRepresentation.y = canvas.height - (robotModel.position[1] * yScale); //Because of y axis direction in computer graphics convention
        completeRobotRepresentation.rotation = robotModel.angle;
    };

    var updatePath = function(pathData) {
        stage.removeChild(path);
        path = new createjs.Shape();
        path.graphics.setStrokeStyle(2).setStrokeDash([20, 10], 0).beginStroke("#000000");
        for (pathNode of pathData.robotPath) {
            var x = pathNode[0];
            var y = pathNode[1];
            var convertedX = x*xScale;
            var convertedY = y*yScale;
            path.graphics.lineTo(convertedX, CANVAS_HEIGHT - convertedY);
        }
        stage.addChild(path);
        path.graphics.endStroke();
    };

    var initVideoStream = function() {
        var image = new Image();
        image.src = "http://" + VIDEO_STREAM;
        var bitmap = new createjs.Bitmap(image);
        bitmap.scaleX = xScale;
        bitmap.scaleY = yScale;
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
        var circle_x = circleData.x * xScale;
        var circle_y = CANVAS_HEIGHT - circleData.y * yScale;
        var circle_radius = circleData.radius * xScale;
        var circle_color = circleData.color;
        island.graphics.beginFill(circle_color).drawCircle(circle_x, circle_y, circle_radius);
        allIslands.addChild(island);
    };

    var drawPolygon = function(polygonData, edges_number) {
        var island = new createjs.Shape();
        var polygon_x = polygonData.x * xScale;
        var polygon_y = canvas.height - polygonData.y * yScale;
        var polygon_side_length = 20;
        var polygon_color = polygonData.color;
        var polygon_angle = -90;
        island.graphics.beginFill(polygon_color).drawPolyStar(polygon_x, polygon_y, polygon_side_length, edges_number, 0, polygon_angle);
        allIslands.addChild(island);
    };

    var showIslands = function() {
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
    };

    var getRobotPosition = function(){
        MapService.getRobotPosition().then(function(response) {
            var robot_square = new createjs.Shape();
            robot_square.graphics.beginFill('purple').drawPolyStar((response.center[0]*xScale), CANVAS_HEIGHT - (response.center[1]*yScale), 100, 4, 0, response.angle);
            stage.addChild(robot_square);
        });
    };

    setInterval(getRobotPosition, ROBOT_POSITION_FROM_VISION_REFRESH_TIME_IN_MS);

    var initPath = function(){
        path = new createjs.Shape();
        path.graphics.moveTo(completeRobotRepresentation.x, completeRobotRepresentation.y);
    };

    var initMesh = function() {
        var whenGetIsComplete = MapService.getMesh();

        whenGetIsComplete.then(function(response) {
            completeMesh = new createjs.Container();
            for (cell of response.cells) {
                var square = new createjs.Shape();
                var rectTopLeftX = (cell.x * xScale) - (cell.width*xScale) / 2;
                var rectTopLeftY = (cell.y * yScale) + (cell.height*yScale) / 2;
                square.graphics.beginStroke("black").drawRect(rectTopLeftX, CANVAS_HEIGHT - rectTopLeftY, (cell.width*xScale), (cell.height*yScale));
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

    $scope.$on('robotModelUpdated', function(event) {
        var robot = robotService.getRobotModel();
        updateRobotRepresentation(robot);
    });

    $scope.$on('islandToggleOn', function(event) {
        showIslands();
    });

    $scope.$on('islandToggleOff', function(event) {
        stage.removeChild(allIslands);
    });

    setInterval(function() {
        robot_socket.emit('fetchPath');
    }, PATH_REFRESH_TIME_IN_MS);

    robot_socket.on('path', function(message) {
        var whenUpdateIsComplete = updatePath(message)
    });

    setInterval(function() {
        stage.update();
    }, CANVAS_REFRESH_TIME_IN_MS);

    function init() {
        canvas = document.getElementById("mapCanvas");
        canvasContext = canvas.getContext("2d");
        xScale = unitConvertingService.calculateFrontEndImageWidthScale();
        yScale = unitConvertingService.calculateFrontEndImageHeightScale();
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
            robotService.move_to(mousePos);
        }, false);

    }
    init();

}]);
