





angular.module('rsquareApp').controller('lucyTalk', function($scope, $http, API_URL) {
    console.log("lucyTalk");




    $scope.word = '';
    $scope.thedata = {};
    $scope.thedata.aware = true;

    $scope.letsTalk = function(){
        console.log("letsTalk triggered");
        $http({
            method: 'GET',
            url: API_URL+'/get-answer/?text_has='+$scope.word,
        }).then(function successCallback(response) {
            console.log(response);
            $scope.thedata =  response.data;
        }, function errorCallback(response) {
            console.log(response);
        });

    }



});
