Capstone
---------
## introduction

this is the final project in my journey in becoming a fullstack developer, i have to use everything i learned so far in the FSND course to get a casting agancy an api that can create, read, update and delete both movies and actors from a postgres database deployed using heroku with a postman collection to test the api

### dependancies

before starting the api you need to install all the needed python libraries and tools
but it is recommended to use a virtual environment before installing the libraries
run
```
 pip install virtualenv
 virtualenv venv
 source venv/bin/activate
``` 
whenever you want to exit out of the virtual environment run:
```
deactivate
```

after activating the environment run:
```
pip install -r requirments.txt
```
to install all the needed dependancies 

### running the API locally

after installing the needed dependancies if you wish to run the api locally cd into the capstone file and run the following command:
```
python3 app.py
```
or if you want to run the unit tests run:
```
python3 test_app.py
```

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
      will return all a paginated array of actors with a limit of 10 actors per page
    
    GET /movies
      will return all a paginated array of movies with a limit of 10 movies per page

    DELETE /actors/<actor_id> 
      will delete an actor assosiated with the given ID, will return 404 if not found
    
    DELETE /movies/<movie_id>
      will delete an movie assosiated with the given ID, will return 404 if not found

    POST /actors
      will create a new actor with the given info, if given info is not enough it will return 422.
      you need to attach a json body containing name, age and gender
    
    POST /movies 
      will create a new movie with the given info, if given info is not enough it will return 422.
      you need to attach a json body containing title and release date

    PATCH /actors/<actor_id>
      will update the info of the actor assosiated with the given ID, if no info is given it will return 400.
      you need to attach a json body containing the attributes you want to update
    
    PATCH /movies/<movie_id>
      will update the info of the actor assosiated with the given ID, if no info is given it will return 400.
      you need to attach a json body containing the attributes you want to update

### testing

i have attached a postman collection of tests with valid JWTs for you to test the deployed api, these tests have a valid JWT token and can run indefinatly since the tests feed into each other.


### accessing the api

the api has been deployed on heroku and the url to access it is:
https://my-app-capstone.herokuapp.com

