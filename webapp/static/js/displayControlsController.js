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

}]);
