website.controller('gamePanelController', ['$scope', '$rootScope', 'RobotService', function($scope, $rootScope, robotService) {

    $scope.actionReadManchester = function() {
        $scope.sequenceToStart = window.actionsEnum.READ_MANCHESTER
    };

    $scope.actionDropdownTreasure = function() {
        $scope.sequenceToStart = window.actionsEnum.DROPDOWN_TREASURE
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

    $scope.actionScanTreasures = function(){
        $scope.sequenceToStart = window.actionsEnum.SCAN_TREASURES
    };

    $scope.actionsAlignWithChargingStation = function(){
        $scope.sequenceToStart = window.actionsEnum.ALIGN_WITH_CHARGING_STATION
    };

    $scope.actionAlignWithTreasure = function(){
        $scope.sequenceToStart = window.actionsEnum.ALIGN_WITH_TREASURE
    };

    $scope.startSequence = function() {
        robotService.sendAction($scope.sequenceToStart);
    };

    $scope.startFromBeginning = function() {
        var actionCompleted = function(){$rootScope.$broadcast('backendMapHasRefreshed')};
        robotService.sendAction(window.actionsEnum.START_TIMER, actionCompleted);
        robotModel = robotService.getRobotModel();
        robotModel.hasStartedSequence = true
    }
}]);
