[![MyPy Check](https://github.com/Process-Mining-Group-9/backend/actions/workflows/mypy.yml/badge.svg)](https://github.com/Process-Mining-Group-9/backend/actions/workflows/mypy.yml)

# Installation and Running

1. Check that your Python version is relatively new (```python --version```). Version 3.8 is used in production.
2. Create a virtual environment using ```python -m venv venv``` and activate it:
   1. On Linux: ```source venv\bin\activate```
   2. On Windows: ```\venv\Scripts\activate```
3. Install the required packages using ```pip install -r requirements.txt```.
4. The environment variables in ```.env``` need to be available to the program when running it. These are the options:
   1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and run ```heroku local``` to start the application
   2. When using an IDE like PyCharm, create a run configuration and copy-paste the contents of ```.env``` into the environment variables section

## Type Checking

Use ```mypy src``` to type-check the code for type violations.
