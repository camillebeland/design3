website.controller('systemStatePanelController', ['$scope', '$rootScope', 'RobotService', function($scope, $rootScope, robotService) {

    $scope.robot_socket = io(ROBOT_HOST);
    $scope.timer.time = 0;

    $scope.$on('robotModelUpdated', function(event) {
        $scope.robot = robotService.getRobotModel();
        $scope.$apply($scope.robot)
    });

    setInterval(function() {
        robot_socket.emit('fetchTime');
    }, TIMER_REFRESH_TIME_IN_MS);

    $scope.robot_socket.on('timeUpdate', function(message) {
        $scope.timer.time = message.time;
        $scope.apply($scope.timer);
    });

}]);
