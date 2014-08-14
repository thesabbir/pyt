var App = angular.module("Pyt", ['ngRoute', 'ui.bootstrap']);

App.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
    $locationProvider.hashPrefix('!');

    $routeProvider
        .when('/', {
            controller: 'MemberCtrl',
            templateUrl: 'templates/members.html'
        })
        .when('/meals', {
            controller: 'MealCtrl',
            templateUrl: 'templates/meals.html'
        })
         .when('/balances', {
            controller: 'BalanceCtrl',
            templateUrl: 'templates/balances.html'
        })
        .otherwise({
            redirectTo: '/'
        })


}]);

App.controller('AppCtrl', ['$scope', function ($scope) {
    $scope.sortBy = function (value) {
        $scope.reverse = !$scope.reverse;
        $scope.order = value;
    };
}])
    .controller('MemberCtrl', ['$scope', '$http', function ($scope, $http) {
    $http.get("/api/member").success(function (data) {
        $scope.members = data.objects;
    });
}])
    .controller('MealCtrl', ['$scope', '$http', function ($scope, $http) {
    $http.get("/api/meal").success(function (data) {
        $scope.meals = data.objects;
    });
}])
    .controller('BalanceCtrl', ['$scope', '$http', function ($scope, $http) {
    $http.get("/api/balance").success(function (data) {
        $scope.balances = data.objects;
    });
}])