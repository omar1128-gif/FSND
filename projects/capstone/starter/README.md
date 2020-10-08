# Casting Agency - Capstone Project

## Motivation

This project is the last project in  Udacity's Full Stack Nano Degree. I am pleased to create a backend casting agency site that creates, deletes and modifies both actors and movies . I wish to keep moving further in my carrer and improve this site and create more and better sites.

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the main directory of the project

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the postgres database. You'll primarily work in app.py and can reference models.py. 

## Database Setup

With Postgres running,drop existing database and  create a database called "casting_agency" and then run migrate commands to create the tables

```
dropdb casting_agency
createdb casting_agency
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```

now the casting_agency database is created with 3 tables ( Actor,  Movies, helper) but are empty

-> To set a database with records

```
dropdb casting_agency
createdb casting_agency
psql casting_agency < casting_agency.psql
```



## Running the server

From within the main directory use the following commands

```
source setup.sh
flask run
```

environment variables are exported via setup.sh and flask application is started

## API Reference

### Getting Started

- **Local URL**: This app is hosted locally on `http://127.0.0.1:5000/`
- **Heroku URL**: This app is hosted on Heroku on https://omars-casting-agency.herokuapp.com/

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return four error types when requests fail:

- 400 : Bad request
- 404 : Resource not found
- 422 : Unprocessable
- 401: AuthError

### Endpoints

Postman collection is provided for both the local and Heroku site

##### Get /actors

- General: 

  - The endpoint is provided with the authorization header to check the permission (get:actors)
  - It returns a success value and a list of actors

- Sample:

  ```
  {
      "actors": [
          {
              "actor_age": 47,
              "actor_gender": "f",
              "actor_id": 1,
              "actor_name": "Julia Roberts"
          },
          {
              "actor_age": 55,
              "actor_gender": "m",
              "actor_id": 2,
              "actor_name": "John Travolta"
          },
          {
              "actor_age": 57,
              "actor_gender": "m",
              "actor_id": 3,
              "actor_name": "Nicolas Cage"
          },
          {
              "actor_age": 61,
              "actor_gender": "m",
              "actor_id": 4,
              "actor_name": "Denzel Washington"
          }
      ],
      "success": true
  }
  ```

  

##### Get /movies

- General:

  - The endpoint is provided with the authorization header to check the permission (get:movies)
  - It returns a success value and a list of movies

- Sample:

  ```
  {
      "movies": [
          {
              "movie_id": 1,
              "movie_release_date": "Thu, 02 May 2013 00:00:00 GMT",
              "movie_title": "The Hobbit"
          },
          {
              "movie_id": 2,
              "movie_release_date": "Wed, 16 Dec 2009 00:00:00 GMT",
              "movie_title": "Avatar"
          },
          {
              "movie_id": 3,
              "movie_release_date": "Wed, 16 Jan 2013 00:00:00 GMT",
              "movie_title": "Django Unchained"
          }
      ],
      "success": true
  }
  ```

  

##### Get /actors/<int:actor_id>

- General:

  - The endpoint is provided with actor id and the authorization header to check the permission (get:actor)
  - It returns a success value and actor details

- Sample:

  ```
  {
      "age": 47,
      "gender": "f",
      "name": "Julia Roberts",
      "success": true
  }
  ```



##### Get /movies/<int:movie_id>

- General:

  - The endpoint is provided with movie id and the authorization header to check the permission (get:movie)
  - It returns a success value and movie details

- Sample:

  ```
  {
      "release_date": "Thu, 02 May 2013 00:00:00 GMT",
      "success": true,
      "title": "The Hobbit"
  }
  ```



##### Post /actors

- General:

  - The endpoint is provided with the  actors' ( name , age, gender) and the authorization header to check the permission (post:actor)
  - It creates a new actor. Returns the id of the created actor , list of actors and a success value

- Sample:

  ```
  {
      "actors": [
          "Julia Roberts - 47 - f",
          "John Travolta - 55 - m",
          "Nicolas Cage - 57 - m",
          "Denzel Washington - 61 - m"
      ],
      "created_id": 5,
      "success": true
  }
  ```

  

##### Post /movies 

- General:
  - The endpoint is provided with the  movie's ( title , release date) and the authorization header to check the permission (post:movie)
  - It creates a new movie. Returns the id of the created movie , list of movies and a success value

- Sample:

  ```
  {
      "created_id": 5,
      "movies": [
          "The Hobbit - 2013-05-02",
          "Avatar - 2009-12-16",
          "Django Unchained - 2013-01-16",
          "The Walking Dead - 2014-03-27"
      ],
      "success": true
  }
  ```



##### Delete /actors

- General:

  - The endpoint is provided with the authorization header to check permission(delete:actor)
  - It returns the id of the deleted actor and a success value

- Sample:

  ```
  {
  	"deleted": 5,
  	"success": true
  }
  ```



##### Delete /movies

- General:

  - The endpoint is provided with the authorization header to check permission(delete:movie)
  - It returns the id of the deleted movie and a success value

- Sample:

  ```
  {
  	"deleted": 4,
  	"success": true
  }
  ```



##### Patch /actors/<int:actor_id>

- General:

  - The endpoint is provided with the  new actor details and the authorization header to check permission(patch:actor)
  - It returns a success value and list of actors

- Sample:

  ```
  {
      "actor": [
          "Julia Roberts - 47 - f",
          "John Travolta - 55 - m",
          "Nicolas Cage - 57 - m",
          "The edited - 61 - m"
      ],
      "success": true
  }
  ```

  

##### Patch /movies/<int:movie_id>

- General:
  - The endpoint is provided with the  new actor details and the authorization header to check permission(patch:actor)
  - It returns a success value and list of actors

- Sample:

  ```
  {
      "movies": [
          "The Hobbit - 2013-05-02",
          "Avatar - 2009-12-16",
          "The edited - 2013-01-16"
      ],
      "success": true
  }
  ```



##### Get /login

- General:
  - The endpoint redirects to a page with a login link, once clicked, it redirects the user to the login page of auth0 to generate jwt token

##### Get /logout

- General:
  - It logs the current user out of the session



### Testing

- To run the tests, run

  ```
  dropdb casting_agency_test
  createdb casting_agency_test
  psql casting_agency_test < casting_agency.psql
  source setup.sh  # to export jwt tokens
  python3 test_app.py
  ```

  

- Postman collection is provided for the local server but before starting it , do the following for synchronization

  ```
  dropdb casting_agency
  createdb casting_agency
  psql casting_agency < casting_agency.psql
  ```

  

## Auth0 Authentication Details

- There are 3 roles in this project ( casting assistant - casting director - executive producer)

- We can generate new jwt token using the /login endpoint

#### Casting Assistant

- Casting assistant has 4 permissions ( get:actors - get:actor - get:movies - get:movie)
- Credentials for login:
  - Email : casting_assistant@udacity.com
  - Password: Assistant11

#### Casting Director

- Casting director has all casting assistant permissions plus ( post:actor - delete:actor - patch:actor - patch:movie)
- Credentials for login:
  - Email: casting_director@udacity.com
  - Password: Director11

#### Executive Producer

- Executive producer has all previous permissions plus (post:movie - delete:movie)
- Credentials for login:
  - Email: executive_producer@udacity.com
  - Password: Producer11



## Heroku Site Testing

Postman collection is provided in the project files and is configured with 3 valid jwt tokens.