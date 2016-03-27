var Robot = angular.module('Robot', [])
    .service('RobotService', ['$http', '$rootScope', 'UnitConvertingService', function($http, $rootScope, unitConvertingService) {

        var robot_socket = io(ROBOT_HOST);

        var RobotModel = function() {
            this.angle = 0;
            this.position = [];
            this.capacitorLevel = 0;
        };

        robotModel = new RobotModel();

        this.getRobotModel = function() {
            return robotModel;
        };

        this.up = function() {
            var delta = {
                delta_x: 0,
                delta_y: 25
            };

            $http({
                method: 'POST',
                url: 'http://' + ROBOT_HOST + '/robot/move',
                data: delta
            }).then(function successCallback(response) {}, function errorCallback(response) {});
        };

        this.down = function() {
            var delta = {
                delta_x: 0,
                delta_y: -25
            }

            $http({
                method: 'POST',
                url: 'http://' + ROBOT_HOST + '/robot/move',
                data: delta
            }).then(function successCallback(response) {

            }, function errorCallback(response) {

            });
        };

        this.left = function() {
            var delta = {
                delta_x: -25,
                delta_y: 0
            }

            $http({
                method: 'POST',
                url: 'http://' + ROBOT_HOST + '/robot/move',
                data: delta
            }).then(function successCallback(response) {}, function errorCallback(response) {

            });
        };

        this.right = function() {
            var delta = {
                delta_x: 25,
                delta_y: 0
            };

            $http({
                method: 'POST',
                url: 'http://' + ROBOT_HOST + '/robot/move',
                data: delta
            }).then(function successCallback(response) {

            }, function errorCallback(response) {

            });
        };

        this.turnLeft = function() {
            var angle = {
                angle: -30
            };

            $http({
                method: 'POST',
                url: 'http://' + ROBOT_HOST + '/robot/rotate',
                data: angle
            });
        };

        this.turnRight = function() {
            var angle = {
                angle: 30
            };

            $http({
                method: 'POST',
                url: 'http://' + ROBOT_HOST + '/robot/rotate',
                data: angle
            });
        };

        this.move_to = function(destination) {
            destinationConverted = unitConvertingService.convertFrontEndPixelsToBackEndPixels(destination);
            $http({
                method: 'POST',
                url: 'http://' + ROBOT_HOST + '/robot/move_to',
                data: destinationConverted
            });
        };

        setInterval(function() {
            robot_socket.emit('fetchRobotInfo');
        }, POSITION_REFRESH_TIME_IN_MS);

        robot_socket.on('robotUpdated', function(robotData) {
            robotModel.position = {
              'x':robotData.robotPosition.x,
              'y':robotData.robotPosition.y
            }
            robotModel.angle = robotData.robotAngle;
            robotModel.capacitorLevel = robotData.capacitorCharge;
            $rootScope.$broadcast('robotModelUpdated');
        });

    }]);
