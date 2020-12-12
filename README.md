# Full Stack Casting Agency API Backend

## Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Getting Started

### Installing Depedencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
createdb casting
createdb castingtest
psql -d casting -f database/casting.psql
psql -d castingtest -f database/castingtest.psql
```

## Running the server

From within the current directory first ensure you are working using your created virtual environment.

To run the server execute the following commands:

```bash
export FLASK_APP=app.py
. ./setup.sh
flask run
```

## API End Point Reference
### GET '/movies'
    - Requires the get:movies permission
    - Returns the list of movies in the server with status code 200
    - Example output: 
```bash
    {
    "movies": [
        {
            "id": 7,
            "release_date": "Mon, 11 Oct 2010 00:00:00 GMT",
            "title": "Avatar"
        },
        {
            "id": 8,
            "release_date": "Mon, 03 May 2010 00:00:00 GMT",
            "title": "Inception"
        },
        {
            "id": 9,
            "release_date": "Sun, 07 Jun 2020 00:00:00 GMT",
            "title": "Parasite"
        },
    ],
    "success": true
    }
```

### GET '/actors'
    - Requires the get:actors permission
    - Returns the list of actors in the server with status code 200
    - Example output
```bash
{
    "actors": [
        {
            "age": 64,
            "gender": "Male",
            "id": 6,
            "name": "Tom Hanks"
        },
        {
            "age": 71,
            "gender": "Female",
            "id": 7,
            "name": "Meryl Streep"
        },
    ],
    "success": true
}
```

### POST '/movies'
    - Requires post:movies permission
    - Payload should be json. The release date should be of iso format YYYY-MM-DD
      Example payload: {"title":"MovieTitle", "release_date": "2020-12-30"}
    - Returns json with id of the newly created movie and status code 200
    - Example output
```bash
{
    "id": 20,
    "success": true
}
```

### POST '/actors'
    - Requires post:actors permission
    - Payload should be json. 
      Example payload: {"name" : "ActorName", "age" : 23, "gender": "Female"} 
    - Returns json with id of the newly created actor and status code 200
    - Example output
```bash
{
    "id": 18,
    "success": true
}
```

### DELETE '/movies/<movie_id>'
    - Requires delete:movie permission
    - If <movie_id> not found, returns a 404 error
    - Deletes the corresponding row for <id>
    - Returns json with id of deleted movie and status code 200 
    - Example output
```bash
{
    "delete": "10",
    "success": true
}
```

### DELETE '/actors/<actor_id>'
    - Requires delete:actor permission
    - If <actor_id> not found, returns 404 error
    - Deletes the corresponding row for <id>
    - Returns json with id of deleted actor and status code 200
    - Example output
```bash
{
    "delete": "10",
    "success": true
}
```

### PATCH '/movies/<movie_id>'
    - Requires patch:movies permission
    - If <movie_id> not found, returns a 404 error
    - Payload should be json. The release date should be of iso format YYYY-MM-DD
      Example payload: {"title":"MovieTitle", "release_date": "2020-12-30"}
    - Returns json with details of the modified movie and status code 200
    - Example output

```bash
{
    "movie": {
        "id": 15,
        "release_date": "Tue, 02 Jan 2018 00:00:00 GMT",
        "title": "Spider-Man:Into The Spider-Verse"
    },
    "success": true
}
```
### PATCH '/actors/<actor_id>
    - Requires patch:actors permission
    - If <actor_id> not found, returns a 404 error
    - Payload should be json.
      Example paylod: {"name":"ActorName", "age": 56, "gender": "Male"}
    - Returns json with details of the modified actor and status code 200
    - Example output
```bash
{
    "actor": {
        "age": 24,
        "gender": "Male",
        "id": 13,
        "name": "actornew"
    },
    "success": true
}
```


## Testing the application

In order to test the application APIs, execute the following commands:

```bash
python test_app.py
```




