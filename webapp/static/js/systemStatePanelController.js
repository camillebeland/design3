website.controller('systemStatePanelController', ['$scope', '$rootScope', 'RobotService', function($scope, $rootScope, robotService) {

    var robot_socket = io(ROBOT_HOST);
    $scope.timer = {
      "minutes" : 0,
      "seconds" : 0
    };

    $scope.$on('robotModelUpdated', function(event) {
        $scope.robot = robotService.getRobotModel();
        $scope.$apply($scope.robot);
    });

    setInterval(function() {
        robot_socket.emit('fetchTime');
    }, TIMER_REFRESH_TIME_IN_MS);

    robot_socket.on('timeUpdate', function(message) {
        $scope.timer.minutes = message.minutes;
        $scope.timer.seconds = message.seconds;
        $scope.$apply($scope.timer);
    });

}]);
