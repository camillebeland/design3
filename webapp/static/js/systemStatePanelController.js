website.controller('systemStatePanelController', ['$scope', '$rootScope', 'RobotService', function($scope, $rootScope, robotService) {

    $scope.$on('robotModelUpdated', function(event) {
        $scope.robot = robotService.getRobotModel();
        $scope.$apply($scope.robot)
    });

}]);
