/**
 * Created by cashc on 11/28/16.
 */
var request = require('request');

function user(first, last, email, role, schoolid, addressid){
    this.first = first;
    this.last = last;
    this.email = email;
    this.role = role;
    this.schoolid = schoolid;
    this.addressid = addressid;
}

var john = new user("John", "Smith", "cs.cmptn@gmail.com", "S", 1, 1);
var url = "http://ec2-54-160-178-89.compute-1.amazonaws.com/user/new";
var j = JSON.stringify(john);
console.log(j);

request.post(
    {headers: {'content-type' : 'application/json'},
    url:    url,
    body:   j,
    }, function(error, response, body){
        console.log(body);
    });