Capstone
---------
## introduction

this is the final project in my journey in becoming a fullstack developer, i have to use everything i learned so far in the FSND course to get a casting agancy an api that can create, read, update
and delete both movies and actors from a postgres database deployed on heroku with a postman collection to test the api 

### models and the database 

the api uses postgresql as its database of choice, the database contains 2 tables 

#### Movies
with columns for ID(Integer), title(String), and release date(String) (in years)

#### Actors
with columns for ID(Integer), name(String), age(Integer), and gender(String)

### roles

i have implemented 3 roles for the api, each having diffrent permissons 

# Casting Assistant

    Can view actors and movies

# Casting Director

    All permissions a Casting Assistant has and…
    Add or delete an actor from the database
    Modify actors or movies

# Executive Producer

    All permissions a Casting Director has and…
    Add or delete a movie from the database




### endpoints 

each model has it on CRUD endpoints while still complying with RESTful api architecture and requires a jwt with the proper permissons 

Endpoints:

    GET /actors 
    
    GET /movies

    DELETE /actors/<actor_id> 
    
    DELETE /movies/<movie_id>

    POST /actors
      you need to attach a json body containing name, age and gender
    
    POST /movies 
      you need to attach a json body containing title and release date

    PATCH /actors/<actor_id>
      you need to attach a json body containing the attributes you want to patch
    
    PATCH /movies/<movie_id>
      you need to attach a json body containing the attributes you want to patch

### testing

i have attached a postman collection of tests with valid JWTs for you to test the api with


### accessing the api

the api has been deployed on heroku and the url to access it is:
https://my-app-capstone.herokuapp.com

