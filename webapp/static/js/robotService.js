var Robot = angular.module('Robot', [])
    .service('RobotService', ['$http', '$rootScope', function($http, $rootScope) {

        var robot_socket = io(ROBOT_HOST);

        var RobotModel = function() {
            this.angle = 0;
            this.position = []
            this.batteryLevel = 0;
            this.batteryVoltage = 0;
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
            $http({
                method: 'POST',
                url: 'http://' + ROBOT_HOST + '/robot/move_to',
                data: destination
            });
        };

        setInterval(function() {
            robot_socket.emit('fetchRobotInfo');
        }, POSITION_REFRESH_TIME_IN_MS);

        robot_socket.on('robotUpdated', function(robotData) {
            robotModel.position = robotData.robotPosition;
            robotModel.angle = robotData.robotAngle;
            robotModel.batteryLevel = robotData.batteryLevel;
            robotModel.batteryVoltage = robotData.batteryVoltage;
            $rootScope.$broadcast('robotModelUpdated');
        });

    }]);
