var App = angular.module("Pyt", ['ngRoute', 'ui.bootstrap']);
App.filter('bdt', function () {
    return function (text) {
        var t = text + '.00 BDT';
        return t;
    };
});

App.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
    $locationProvider.hashPrefix('!');
//    TODO: Start Invoice Section
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
        .when('/journal', {
            controller: 'JournalCtrl',
            templateUrl: 'templates/journal.html'
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
    $scope.global_currency = "BDT ";
    $scope.order = 'id';
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
    .controller('JournalCtrl', ['$scope', '$http', function ($scope, $http) {
        $http.get("/api/journal").success(function (data) {
            $scope.journal = data.objects;
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