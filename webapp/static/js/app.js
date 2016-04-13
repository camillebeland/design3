var website = angular.module('app', ['ui.router', 'Robot', 'MapModule', 'ToolsModule']);

website.config(function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise('/');

  $stateProvider.state('home', {
    url: "/",
    templateUrl: "static/partials/home.html",
    controller: "homeController"
  })

});

TabEnum = Object.freeze({
  CONTROLS: "CONTROLS",
  OTHER: "OTHER"
});

website.controller('homeController', ['$scope', function($scope) {
  /*Webapp constants*/
  window.BASE_STATION_HOST = "localhost:5000";
  window.VIDEO_STREAM = BASE_STATION_HOST + "/video_feed";
  window.ROBOT_HOST = "localhost:3000";
  window.POSITION_REFRESH_TIME_IN_MS = 100;
  window.GRIPPER_VOLTAGE_REFRESH_RATE = 5000;
  window.ROBOT_POSITION_FROM_VISION_REFRESH_TIME_IN_MS = 100;
  window.MANCHESTER_CODE_REFRESH_RATE = 2000;
  window.ISLAND_CLUE_REFRESH_RATE = 2000;
  window.PATH_REFRESH_TIME_IN_MS = POSITION_REFRESH_TIME_IN_MS;
  window.CANVAS_REFRESH_TIME_IN_MS = 100;
  window.TIMER_REFRESH_TIME_IN_MS = 10000;
  window.BACKEND_IMAGE_HEIGHT = 1200;
  window.BACKEND_IMAGE_WIDTH = 1600;
  window.CANVAS_HEIGHT = 600;
  window.CANVAS_WIDTH = 800;
  window.actionsEnum = Object.freeze({
    READ_MANCHESTER: "read_manchester",
    DROPDOWN_TREASURE: "drop_down_treasure",
    FIND_BEST_TREASURE: "",
    FIND_ISLAND: "find_island_clue",
    MOVE_TO_CHARGE_STATION: "start",
    MOVE_TO_TARGET_ISLAND: "",
    MOVE_TO_TREASURE: "",
    PICKUP_TREASURE: "pick_up_treasure",
    RECHARGE: "recharge",
    SCAN_TREASURES : "scan_treasures",
    ALIGN_WITH_CHARGING_STATION : "align_charging_station",
    ALIGN_WITH_TREASURE : "align_treasure"
  });

  var init = function() {
    $scope.activeTab = TabEnum.CONTROLS;
  };

  init();

}]);
