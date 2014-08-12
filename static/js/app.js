var App = angular.module("Pyt", ['ngRoute', 'ui.bootstrap']);

App.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
    $locationProvider.hashPrefix('!');

    $routeProvider
        .when('/', {
            controller : 'Members',
            templateUrl : 'templates/members.html'
        })

}]);

App.controller('AppCtrl', [function () {
    
}]);

App.controller('Members', ['$scope', '$http', function ($scope, $http) {
    $http.get('/api/member').success(function (data) {
         $http.get("/api/member").success(function (data) {
           $scope.members = data.objects;
        });
    });
}]);

