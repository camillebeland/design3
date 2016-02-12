website.controller('robotControlsController', ['$scope', '$http', 'Robot', function ($scope, $http, Robot) {

  function robotControlsController() {
  }

  $scope.robotUp = function() {
    Robot.up();
  };

  $scope.robotDown = function() {
    Robot.down();
  };

  $scope.robotLeft = function() {
    Robot.left();
  };

  $scope.robotRight = function() {
    Robot.right();
  };

  $scope.robotTurnLeft = function(){
    Robot.turnLeft();
  };

  $scope.robotTurnRight = function(){
    Robot.turnRight();
  }
}])
