var ToolsModule = angular.module('ToolsModule', [])
  .service('UnitConvertingService', ['$http', function($http) {

    this.convertFrontEndPixelsToBackEndPixels = function(point) {
        var xScale = BACKEND_IMAGE_WIDTH/CANVAS_WIDTH;
        var yScale = BACKEND_IMAGE_HEIGHT/CANVAS_HEIGHT;

        point.x = point.x*xScale;
        point.y = point.y*yScale;
        return point;
    };

    this.calculateFrontEndImageWidthScale = function(){
        return CANVAS_WIDTH/BACKEND_IMAGE_WIDTH;
    }

    this.calculateFrontEndImageHeightScale = function(){
        return CANVAS_HEIGHT/BACKEND_IMAGE_HEIGHT;
    }

}]);
