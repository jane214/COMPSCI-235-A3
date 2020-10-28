# compsci-235-A2

## Description

A Web application that demonstrates use of Python's Flask framework. The application makes use of libraries such as the Jinja templating library and WTForms. Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. The application uses Flask Blueprints to maintain a separation of concerns between application functions. Testing includes unit and end-to-end testing using the pytest tool. 

## Installation

**Installation via requirements.txt**

```shell
$ cd COMPSCI-235-A2
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:COMPSCI-235' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *COMPSCI-235* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 


## Configuration

The *COMPSCI-235/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.


## Testing

Testing requires that file *COMPSCI-235/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *COMPSCI-235-A2/tests/data* directory. 

E.g. 

'''TEST_DATA_PATH = "C:/Users/zhong/Desktop/compsci-235-A2/test/data"'''

please make sure you use the full path
you can first into test file
then right click the data directory to get the full path.

You can then run tests from within PyCharm.
