website.controller('displayControlsController', ['$scope', '$rootScope', '$http', function($scope, $rootScope, $http) {

  $scope.meshToggleOn = function() {
    $rootScope.$broadcast('meshToggleOn');
  };

  $scope.meshToggleOff = function() {
    $rootScope.$broadcast('meshToggleOff');
  };

  $scope.islandToggleOn = function() {
    $rootScope.$broadcast('islandToggleOn');
  };

  $scope.islandToggleOff = function() {
    $rootScope.$broadcast('islandToggleOff');
  };

  $scope.visionRobotToggleOn = function() {
    $rootScope.$broadcast('visionRobotToggleOn');
  };

  $scope.visionRobotToggleOff = function() {
    $rootScope.$broadcast('visionRobotToggleOff');
  };

  $scope.recalculateMap = function(){
    $http({
        method: 'POST',
        url: 'http://' + ROBOT_HOST + '/robot/vision/refresh',
    });
  };

}]);
