var MapModule = angular.module('MapModule', [])
    .service('MapService', ['$http', function($http) {

        this.getMesh = function() {
            return $http({
                method: 'GET',
                url: 'http://' + ROBOT_HOST + '/mesh'
            }).then(function successCallback(response) {
                return response.data;
            }, function errorCallback(response) {
                console.log("error getting mesh from robot");
            });
        };

        this.getMap = function() {
            return $http({
                method: 'GET',
                url: 'http://' + BASE_STATION_HOST + '/worldmap'
            }).then(function successCallback(response) {
                return response.data;
            }, function erroCallback(response) {
                console.log("error getting map from base station");
            });
        };
    }]);
