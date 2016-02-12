var website = angular.module('app', ['ui.router', 'RobotService']);

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

website.controller('homeController', ['$scope', '$http', 'Robot', function($scope, $http, Robot) {
  /*Webapp constants*/
  window.BASE_STATION_HOST = "http://localhost:5000";
  window.VIDEO_STREAM = BASE_STATION_HOST + "/video_feed";
  window.ROBOT_HOST = "localhost:3000";
  window.POSITION_REFRESH_TIME_IN_MS = 100;
  window.IMAGE_REFRESH_TIME_IN_MS = 5000;

  var init = function() {
    $scope.activeTab = TabEnum.CONTROLS;
  };

  init();

}]);
