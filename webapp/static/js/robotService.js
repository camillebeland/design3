var Robot = angular.module('Robot', [])
  .service('RobotService', ['$http', function($http) {

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
      this.move_to = function(destination){
          console.log(destination);
          $http({
              method: 'POST',
              url: 'http://' + ROBOT_HOST + '/robot/move_to',
              data: destination
          });
      };
  }])
  .service('Mesh', ['$http', function($http) {

    this.get= function(callbackFunction) {
        $http({
            method: 'GET',
            url: 'http://' + ROBOT_HOST + '/mesh'
        }).then(function successCallback(response) {
            callbackFunction(response.data);
        }, function errorCallback(response) {
            console.log("error getting mesh from base station");
        });
    };
}]);
