# Workout assistant

This is a documentation file for the Working Assistant project (workass). 
The document is describing set up, usage and components of the application. 

## Requirements

- The project was developed using Python. In the development process [Python version 3.10](https://www.python.org/downloads/) was used. 
Make sure that you are using the same python version in order to avoid issues with usage of the application. This is also specified in Pipenv file. 

- In the project was put a strict emphasis on the versioning of dependencies. [Pipenv](https://pypi.org/project/pipenv/) is used for version control. Make sure that pipenv is [installed](https://pipenv.pypa.io/en/latest/) and configured on your machine. Pipenv comprises `Pipfile` that contains the list of dependencies and `Pipfile.lock` that contains the dependencies' version. This allows for easier tracking dependencies. if you are using PyCharm, consider reading [documentation](https://www.jetbrains.com/help/pycharm/using-pipfile.html) for Pipfile in PyCharm.  

- `sqlite` database is used in the application. Make sure you have [installed](https://sqlite.org/cli.html) `sqlite cli` for usage of the database. 

#### Make sure environment variables are [added](https://www.schrodinger.com/kb/1842) to the system settings. 

## Set up

- `Pipenv shell` command to enter a pipenv shell
- `pipenv install` installation command

### optional commands

- `pipenv install --deploy` enforce pipenv.lock and install
- `pipenv install --system` install dependencies to the system

## Usage

- In case if you are using PyCharm make sure you have added and configure Python interpreter by following [documentation](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#interpreter). 
- The starting point of the application is `main.py` file, that can be started using command `python main.py`. 
- Once the application start, a timer will go off and go for 1 minute. Once the time is up, count of reps and time of exercise are added to the database.   