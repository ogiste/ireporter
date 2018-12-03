ireporter
A web based system for reporting on corruption and public services needs and requests.

iReporter is a web based platform that enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and thegeneral public. Users can also report on things that need government intervention such as public works or repairs.

## Continuous Integration

### Travis-CI
[![Build Status](https://travis-ci.org/ogiste/ireporter.svg?branch=develop)](https://travis-ci.org/ogiste/ireporter)

## Test Coverage

### Codecov
[![codecov.io](https://codecov.io/github/ogiste/ireporter/coverage.svg?branch=develop)](https://codecov.io/github/ogiste/ireporter?branch=develop)

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

API endpoints :

        POST   /api/v1/incidents
        GET    /api//v1/incidents/<int:id>
        GET    /api/v1/incidents/
        PATCH  /api/v1/incidents/<int:id>/<property_name>
        DELETE /api/v1/incidents/<int:id>

  
