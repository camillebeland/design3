website.controller('robotControlsController', ['$scope', '$http', 'RobotService', function ($scope, $http, RobotService) {

  function robotControlsController() {
  }

  $scope.robotUp = function() {
    RobotService.up();
  };

  $scope.robotDown = function() {
    RobotService.down();
  };

  $scope.robotLeft = function() {
    RobotService.left();
  };

  $scope.robotRight = function() {
    RobotService.right();
  };

  $scope.robotTurnLeft = function(){
    RobotService.turnLeft();
  };

  $scope.robotTurnRight = function(){
    RobotService.turnRight();
  }

  $scope.robotStop = function(){
    RobotService.stop();
  }
}])
