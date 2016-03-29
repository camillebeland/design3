website.controller('displayControlsController', ['$scope', '$rootScope', function($scope, $rootScope) {

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

  /*$scope.recalculateMesh = function(){
    $http({
        method: 'GET',
        url: 'http://' + BASE_STATION_HOST + '/vision/',
    });
  };*/

  $scope.recalculateMap = function(){
    $http({
        method: 'GET',
        url: 'http://' + ROBOT_HOST + '/robot/worldmap/recalculate',
        data: angle
    });
    $
  };

}]);
