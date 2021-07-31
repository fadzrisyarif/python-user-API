# python-user-REST-API

This API can be used to perform create read update and delete from database sqlite. this app is also hosted on http://felixstore.pythonanywhere.com/.

How to implements:
-Create user
send a json object to http://felixstore.pythonanywhere.com/api/v1/users/add with method post with value\ 
{
  "firstname":"user first name"\
  "lastname":"user last name"\
  "email":"user email"\
} 

-Read all user
send a get method to http://felixstore.pythonanywhere.com/api/v1/users

-Read single user
send a get method to http://felixstore.pythonanywhere.com/api/v1/users/{ user id } 

-Update user
send a json object to http://felixstore.pythonanywhere.com/api/v1/users/update with method post with value 
{
  "firstname":"user new first name"
  "lastname":"user new last name"
  "email":"user new email"
  "id":"{ user current id }"
} 

-Delete user
send a json object to http://felixstore.pythonanywhere.com/api/v1/users/delete with method post with value 
{
  "id":"{ user current id }"
} 
