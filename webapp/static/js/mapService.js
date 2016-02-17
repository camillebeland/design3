var MapModule = angular.module('MapModule', [])
  .service('MapService', ['$http', function($http) {

    this.getMesh = function(callbackFunction) {
      
      $http({
        method: 'GET',
        url: 'http://' + BASE_STATION_HOST + '/mesh'
      }).then(function successCallback(response) {
        callbackFunction(response.data);
      }, function errorCallback(response) {
        console.log("error getting mesh from base station");
      });

    };

  }]);
