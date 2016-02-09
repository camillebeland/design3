var RobotService = angular.module('RobotService', [])
.service('Robot', ['$http', function ($http) {

  this.up = function() {
    var velocity = {
      x: 0,
      y: -1
    }

    $http({
      method: 'POST',
      url: 'http://' + ROBOT_HOST + '/robot/move',
      data: velocity
    }).then(function successCallback(response) {}, function errorCallback(response) {});
  };

  this.down = function() {
    var velocity = {
      x: 0,
      y: 1
    }

    $http({
      method: 'POST',
      url: 'http://' + ROBOT_HOST + '/robot/move',
      data: velocity
    }).then(function successCallback(response) {

    }, function errorCallback(response) {

    });
  };


  this.left = function() {
    var velocity = {
      x: -1,
      y: 0
    }


    $http({
      method: 'POST',
      url: 'http://' + ROBOT_HOST + '/robot/move',
      data: velocity
    }).then(function successCallback(response) {}, function errorCallback(response) {

    });
  };

  this.right = function() {
    var velocity = {
      x: 1,
      y: 0
    }

    $http({
      method: 'POST',
      url: 'http://' + ROBOT_HOST + '/robot/move',
      data: velocity
    }).then(function successCallback(response) {

    }, function errorCallback(response) {

    });
  };

}]);
