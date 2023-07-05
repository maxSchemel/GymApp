# GymApp
The code is for a simple website to track the gym sessions of a user. The user can create custom workout plans and track
his workout sessions. Later on pre-built workout plans will be available, as well as community interaction tools. The primary device to acess the site will be mobile devices, thus the first format is for mobile
devices, but a desktop version will also be developed.
The website is written using the Python Flask Framework and a sqlite Database. The code uses a domain model and repository pattern, following the book Architecture
patterns with Python by Percival and Gregory. Parts of the code are from the Introduction to Flask Tutorial https://flask.palletsprojects.com/en/2.3.x/tutorial/

## Source Code Structure
The source code is structured into a test, a src folder, a static and a templates folder. With test containing all the tests and src the actual source code. The src folder itself is structured into
4 subfolders. 
- views contains all the Flask Blueprints and Views.
- domain contains the domain model classes user and workout
- repository contains the repository pattern
- database contains the database scheme and the database helper functions

The templates folder contains all the html templates and static contains the styles.css files


## Installing and running the Project

```sh
# Creating the virtual environment(optional)
$ python -m venv .venv
$ .venv\Scripts\activate

# installing Flask and Pytest
$ pip install Flask pytest 

# Creating the database
$ flask --app flaskr init-db

# Running the application
$ flask --app flaskr run --debug

## Running the tests
$ pytest
```
## Pull Requests
Pull requests to the main branch are automatically checked using a CI Pipe. The .yml file is in .github/workflow/python-app.yml. The CI Pipe checks the coding style using flake 8 and tests the code using pytest. Furthermore the code is being scanned by CodeQl.
## Documentation
The code is documented using Pydoc. The documentation can be accessed with
```sh
$ python -m pydoc -p 1234
```
