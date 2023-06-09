[![image](https://github.com/nsidnev/fastapi-realworld-example-app/workflows/Tests/badge.svg)](https://github.com/nsidnev/fastapi-realworld-example-app)

[![image](https://github.com/nsidnev/fastapi-realworld-example-app/workflows/Styles/badge.svg)](https://github.com/nsidnev/fastapi-realworld-example-app)

[![image](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/nsidnev/fastapi-realworld-example-app/blob/master/LICENSE)

[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

---

# Introduction

This is a Test E-commerce API created using Python and FASTAPI. The database used for the project is PostgresSQL.

# Main Dependencies

- Python 3.10.8
- Postgres:15.1-alpine
- Pytest
- FastAPI

# Routes

| Endpoint                                     | HTTP Method | CRUD Method | Result                        |
|----------------------------------------------|-------------|-------------|-------------------------------|
| /                                            | GET         | READ        | Check that the API is running |
| api/v1/auth/signup                           | POST        | CREATE      | Create new user               |
| api/v1/auth/login                            | POST        | CREATE      | Login user                    |
| api/v1/auth/me (protected)                   | GET         | READ        | Read current user details     |
| api/v1/maximum-power/create (protected)      | POST        | CREATE      | Set the maximum power         |
| api/v1/machines/create (protected)           | POST        | CREATE      | Create a machine              |
| api/v1/machines/create (protected)           | GET         | READ        | Get a specific machine        |
| api/v1/machines/update (protected)           | PUT         | UPDATE      | Update a specific machine     |
| api/v1/machines/delete (protected)           | DELETE      | DELETE      | Delete a specific machine     |

Most routes are protected by JWT authentication. To get a token, you need to register and login using the `/api/v1/auth/signup` and `/api/v1/auth/login` routes.

To login, you need to provide the email and password of the user you created using a form. The response will contain a token that you can use to access the protected routes.

# Documentation

Documentation related to the project is available on `/docs` or `/redoc` paths with Swagger or ReDoc.

# Running the project

To run the project, you need to have docker installed on your machine. You can download docker from [here](https://docs.docker.com/get-docker/).

You also need to have docker-compose installed on your machine. You can download docker-compose from [here](https://docs.docker.com/compose/install/).

After installing docker and docker compose, you can run the project by running the following command:

    docker-compose up --build

This will build the docker images and run the project. You can then access the project on `http://localhost:8000/`

# Running tests

Tests for this project are defined in the `tests/` folder.

This project uses [pytest](https://docs.pytest.org/) to define tests
because it allows you to use the `assert` keyword with good formatting
for failed assertations.

To run all the tests of a project, ensure that docker is running and simply run the command `docker-compose exec app pytest .` :

    $ docker-compose exec app pytest .
    ================================================= test session starts ==================================================
    platform linux -- Python 3.10.8, pytest-7.2.1, pluggy-1.0.0
    rootdir: /usr/src/fast_api
    plugins: anyio-3.6.2, asyncio-0.20.3
    asyncio: mode=strict
    collected 7 items
    
    tests/app/core/test_maximum_power.py .                                                                           [ 14%]
    tests/app/server/api_v1/test_api_is_running.py .                                                                 [ 28%]
    tests/app/server/api_v1/test_create_machine_endpoint.py .                                                        [ 42%]
    tests/app/server/api_v1/test_create_user_signup_endpoint.py ..                                                   [ 71%]
    tests/app/server/api_v1/test_me_endpoint.py .                                                                    [ 85%]
    tests/app/server/api_v1/test_user_login_endpoint.py .                                                            [100%]
    
    ==================================================================== 
                            7 passed in 11.14s 
    =====================================================================
