var website = angular.module('app', ['ui.router', 'Robot', 'MapModule']);

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

website.controller('homeController', ['$scope', '$http', 'RobotService', 'MapService', function($scope, $http, RobotService, MapService) {
  /*Webapp constants*/
  window.BASE_STATION_HOST = "localhost:5000";
  window.VIDEO_STREAM = BASE_STATION_HOST + "/video_feed";
  window.ROBOT_HOST = "localhost:3000";
  window.POSITION_REFRESH_TIME_IN_MS = 100;
  window.CANVAS_REFRESH_TIME_IN_MS = 100;
  window.CANVAS_HEIGHT = 500;
  window.CANVAS_WIDTH = 900;

  var init = function() {
    $scope.activeTab = TabEnum.CONTROLS;
  };

  init();

}]);
