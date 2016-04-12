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

  $scope.startGame = function() {
      $scope.recalculateMap().then(function () {
          $rootScope.$broadcast('startGame');
      }, function(){
          $rootScope.$broadcast('startGame');
      })
  };

  $scope.recalculateMap = function(){
    $http({
        method: 'POST',
        url: 'http://' + ROBOT_HOST + '/robot/vision/refresh'
    });
  };
}]);
