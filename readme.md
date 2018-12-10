ireporter
A web based system for reporting on corruption and public services needs and requests.

iReporter is a web based platform that enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and thegeneral public. Users can also report on things that need government intervention such as public works or repairs.

[![Build Status](https://travis-ci.org/ogiste/ireporter.svg?branch=develop)](https://travis-ci.org/ogiste/ireporter) [![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/ogiste/ireporter) [![codecov.io](https://codecov.io/github/ogiste/ireporter/coverage.svg?branch=develop)](https://codecov.io/github/ogiste/ireporter?branch=develop)

## Running the API  ##
Clone this repo to your machine

 ``` git clone https://github.com/ogiste/ireporter.git ```

Then change the directory to the project by

``` cd ireporter ```

to make sure all the packages needed to run the project present in your machine,
we'll create a virtual enviroment and install the packages there

* to create a virtual enviroment run


    ``` virtualenv -p python2.7 venv```
* activating the enviroment

    ``` source venv/bin/activate```

The virtual enviroment is now ready, we can install all packages needed for project
ensure you have pip installed otherwise
then on your terminal run

``` pip install -r requirements.txt ```

# run
To test our project on your terminal run

``` export FLASK_APP=run.py```

then

``` flask run ```

on your browser open up [http://127.0.0.1:5000/api/v1/incidents](http://127.0.0.1:5000/api/v1/incidents)

# Testing using postman

Sample Indicent Record JSON:
  {
            "title":"Corruption",
            "type":"red-flag",
            "location":"-1.324343434, 23.32321323",
            "comment":"Corruption in procurement"
  }

Current API endpoints :

        | METHOD        | ENDPOINT                    | DESCRIPTION                                                           |
        | --------------|:---------------------------:| ----------------------------------------------------------------------|
        | POST          | /api/v1/incidents           | Used to create an incident record                                     |
        | GET           | /api/v1/incidents/          | Used to read all incident records                                     |
        | GET           | /api/v1/incidents/<int:id>  | Used to view a particular incident record                             |
        | PUT           | /api/v1/incidents/<int:id>  | Used to update the incident location and comment of a specific record |
        | DELETE        | /api/v1/incidents/<int:id>  | Allows user to delete a specific incident record                      |

View the [published collection](https://documenter.getpostman.com/view/764347/RzffJ9Y8
) for more details

# Run tests using nosetests

Install nosetest, codecov and coverage:

 ```pip install nose```
 ```pip install coverage```
 ```pip install codecov```

Within the root repository directory run the tests using nosetest with codecov for coverage:
 ```nosetests --with-coverage --cover-package=app/```

 # **Built with**
```
Python 3
Flask 1.0.2
nosetests
```
# **Versioning**

[Blueprints](https://sanic.readthedocs.io/en/latest/sanic/blueprints.html) was used for versioning

# **Authors**

Alfred Opon

# **Contributing**

Though this project is open to feedback and suggestions all contributions are restricted to the main author as the project is for learning purposes
