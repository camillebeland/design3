var Robot = angular.module('Robot', [])
    .service('RobotService', ['$http', '$rootScope', 'UnitConvertingService', function($http, $rootScope, unitConvertingService) {

        var robot_socket = io(ROBOT_HOST);

        var RobotModel = function() {
            this.angle = 0;
            this.position = [];
            this.capacitorLevel = 0;
            this.manchesterCode = '';
            this.island = '';
        };

        robotModel = new RobotModel();

        this.getRobotModel = function() {
            return robotModel;
        };

        this.up = function() {
            var delta = {
                delta_x: 0,
                delta_y: 100
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
                delta_y: -100
            };

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
                delta_x: -100,
                delta_y: 0
            };

            $http({
                method: 'POST',
                url: 'http://' + ROBOT_HOST + '/robot/move',
                data: delta
            }).then(function successCallback(response) {}, function errorCallback(response) {

            });
        };

        this.right = function() {
            var delta = {
                delta_x: 100,
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

        this.stop = function(){
            $http({
                method: 'POST',
                url: 'http://' + ROBOT_HOST + '/robot/stop'
            });
        };

        this.sendAction = function(action){
          $http({
              method: 'POST',
              url: 'http://' + ROBOT_HOST + '/actions/' + action
          });
        };

        setInterval(function() {
            robot_socket.emit('fetchRobotInfo');
        }, POSITION_REFRESH_TIME_IN_MS);

        setInterval(function(){
          robot_socket.emit("fetchGripperVoltage");
        }, GRIPPER_VOLTAGE_REFRESH_RATE);

        setInterval(function() {
            $http({
                method: 'GET',
                url: 'http://' + ROBOT_HOST + '/manchester' 
            }).then(function successCallback(response) {
                robotModel.manchesterCode = response.data.code;
            });
        }, MANCHESTER_CODE_REFRESH_RATE);

        setInterval(function() {
            $http({
                method: 'GET',
                url: 'http://' + ROBOT_HOST + '/island' 
            }).then(function successCallback(response) {
                robotModel.island = response.data.island;
            });
        }, ISLAND_CLUE_REFRESH_RATE);

        robot_socket.on('robotUpdated', function(robotData) {
            robotModel.position = {
              'x':robotData.robotPosition.x,
              'y':robotData.robotPosition.y
            };
            robotModel.angle = robotData.robotAngle;
            $rootScope.$broadcast('robotModelUpdated');
        });

        robot_socket.on('gripperUpdated', function(gripperData) {
            robotModel.capacitorLevel = convertIntoVoltage(gripperData.capacitorCharge);
            $rootScope.$broadcast('robotModelUpdated');
        });

        var convertIntoVoltage = function(percentageCharge){
          var totalCapacitorVoltage = 2.7;
          convertedVoltage = percentageCharge*totalCapacitorVoltage/100;
          return convertedVoltage;
        }

    }]);
