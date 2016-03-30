website.controller('gamePanelController', ['$scope', '$rootScope', 'RobotService', function($scope, $rootScope, robotService) {

    $scope.continueSequence = false;

    $scope.actionReadManchester = function() {
        $scope.sequenceToStart = window.actionsEnum.READ_MANCHESTER
    };

    $scope.actionDropdownTreasure = function() {
        $scope.sequenceToStart = window.actionsEnum.MOVE_TO_CHARGE_STATION
    };

    $scope.actionFindBestTreasure = function() {
        $scope.sequenceToStart = window.actionsEnum.FIND_BEST_TREASURE
    };

    $scope.actionFindIsland = function() {
        $scope.sequenceToStart = window.actionsEnum.FIND_ISLAND
    };

    $scope.actionMoveToTargetIsland = function() {
        $scope.sequenceToStart = window.actionsEnum.MOVE_TO_TARGET_ISLAND
    };

    $scope.actionMoveToTreasure = function() {
        $scope.sequenceToStart = window.actionsEnum.MOVE_TO_TREASURE
    };

    $scope.actionPickUpTreasure = function() {
        $scope.sequenceToStart = window.actionsEnum.PICKUP_TREASURE
    };

    $scope.actionRecharge = function() {
        $scope.sequenceToStart = window.actionsEnum.RECHARGE
    };

    $scope.actionMoveToChargeStation = function(){
        $scope.sequenceToStart = window.actionsEnum.MOVE_TO_CHARGE_STATION
    };

    $scope.continueSequenceToggle = function(boolean) {
        this.continueSequence = boolean;
    };

    $scope.startSequence = function() {
        robotService.sendAction($scope.sequenceToStart);
    }

}]);
