var App = angular.module("Pyt", ['ngRoute', 'ui.bootstrap']);

App.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
    $locationProvider.hashPrefix('!');

    $routeProvider
        .when('/', {
            controller: 'HomeCtrl',
            templateUrl: 'templates/home.html'
        })
        .when('/members', {
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
        .when('/manager', {
            controller: 'ManageCtrl',
            templateUrl: 'templates/manager.html'
        })
        .otherwise({
            redirectTo: '/'
        })


}]);

App.controller('AppCtrl', ['$scope', '$modal', function ($scope, $modal) {
    $scope.sortBy = function (value) {
        $scope.reverse = !$scope.reverse;
        $scope.order = value;
    };
}])
    .controller('HomeCtrl', [function ($scope) {

    }])
    .controller('MemberCtrl', ['$scope', '$http', '$modal', function ($scope, $http, $modal) {
        var api = "/api/member";

        $scope.addNew = function () {
            var modalInstance = $modal.open({
                templateUrl: 'templates/partials/new_member.html',
                controller: 'AddNewCtrl',
                resolve: {
                    api: function () {
                        return api;
                    }}

            });
        }

        $http.get(api).success(function (data) {
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
    .controller('ManageCtrl', ['$scope', '$http', function ($scope, $http) {
        $http.get("/api/manager").success(function (data) {
            $scope.managers = data.objects;
        })
    }])
    .controller('AddNewCtrl', ['$scope', '$http', '$modalInstance', 'api', function ($scope, $http, $modalInstance, api) {
        $scope.save = function (data) {
            $http.post(api, JSON.stringify(data)).success(function (reso) {
                $modalInstance.close();
            })
        }
        //TODO: Auto reload models after save
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        }
    }]);