# Tic-Tac-Toe



## Description
This project is a Tic-tac-toe development challenge. 
It consists on a complete API that allows you to play Tic-Tac-Toe game. Technologies implemented listed below. [Repository](https://gitlab.com/mercadogmatias/fligoo-tic-tac-toe/-/tree/main)

## Technologies

- Python3
- FastApi
- PostgreSQL

## Getting Started

1. Create a virtual environment and install requirements
    - Linux
    ```
    python3 -m venv venv
    source venv/bin/activate
    cd api
    pip install -r requirements.txt
    ```
    or
    ```
    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    cd api
    pip install -r requirements.txt
    ```
    - Windows
      - Replace "source venv/bin/activate" with:
    ```
    cd venv/Scripts
    activate
    ```
2. Run the project:
    - Pycharm: Uvicorn is included in app.py class. Running app.py should make it work
    - Uvicorn: In terminal by sending the command: `uvicorn api.app:app --reload`
    - Python: Replace every `api.src` with `src`. Then execute `python3 api/app.py
