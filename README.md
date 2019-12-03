#### CUS Project Template

This repository serves as a starting point for your project. It is organized in a way that allows the monitoring of project deliverables.

#### Basic folder structure

- `app` : Folder that contains your Flask project
- `docs` : In this folder you are expected to store all project documentation, and project deliverables associated with the course
- `tests`: Here you need to include all unit and functional test for your project
- `.gitignore`: Contains files and folders to ignore when pushing with `git`
- `app.py`: In the main file that starts your sample project
- `Pipfile`: Contains basic information to set up a `pipenv` virtual environment
- `Pipfile.lock`: Generated automatically by `pipenv`, **DO NOT EDIT**
- `README.md`: This file, provides project overview and setup instructions

#### Basic Flask application

A basic flask application is provided for you. The project uses a `pipenv` virtual environment. Make sure you install `pipenv` on your machine.

First install and verify `pipenv` is up to date...
```shell
pip install pipenv
pip install --upgrade pipenv
```

Create the virtual environment by typing...
```shell
pipenv shell
```

Install the required dependencies for the project by typing...
```shell
pipenv install
```

Specify some virtual environment variables...
```shell  
export FLASK_APP=app.py             # May be required to run flask
export PYTHONDONTWRITEBYTECODE=1    # Prevents .pyc and __pycache__ creation
```

You can start the basic application using the command..
```shell
flask run
```
