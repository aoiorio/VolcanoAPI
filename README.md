# 🌋 VolcanoAPI 🌋
<br>

## 🐥 How do I start?
<br>

- 🦋 **Execute these commands**
```shell
# Create image of volcano-api
$ docker-compose build

# Create pyproject.toml file that writes FastAPI and uvicorn[standard] by using poetry (poetry is like pip) And say yes at every time
$ docker-compose run \
  --entrypoint "poetry init \
    --name volcano-api \
    --dependency fastapi \
    --dependency uvicorn[standard]" \
  volcano-api

# Install dependencies that was written in pyproject.toml file
$ docker-compose run --entrypoint "poetry install --no-root" volcano-api

# Install all dependencies to Docker environment
$ docker-compose build --no-cache
```

<br>

## 🌳 Folder Structure
```
└── 📁volcano
    └── __init__.py
    └── 📁api
        └── __init__.py
        └── 📁v1
            └── __init__.py
            └── 📁endpoints
                └── __init__.py
                └── auth.py
                └── todo.py
                └── user.py
            └── routes.py
    └── 📁core
        └── __init__.py
        └── auth_exception.py
        └── config.py
    └── 📁domain
        └── __init__.py
        └── 📁entity
            └── __init__.py
            └── todo.py
            └── user.py
        └── 📁repository
            └── auth.py
            └── todo.py
            └── user.py
    └── 📁infrastructure
        └── __init__.py
        └── 📁postgresql
            └── __init__.py
            └── database.py
            └── 📁dto
                └── __init__.py
                └── todo.py
                └── volcano_user.py
        └── 📁repository
            └── auth.py
            └── todo.py
            └── user.py
    └── main.py
    └── 📁use_case
        └── __init__.py
        └── auth.py
        └── 📁model
            └── auth.py
            └── todo.py
        └── todo.py
        └── user.py
```

<br>

## 🦕 References

- Docker 👽
    - [How to create Docker environment for FastAPI](https://zenn.dev/sh0nk/books/537bb028709ab9/viewer/5d287c)

<br>

- FastAPI 👨🏼‍🔬
    - [Folder structure for FastAPI](https://zenn.dev/tk_resilie/books/bd5708c54a8a0a/viewer/01-endpoints)

<br>

- GitHub Actions 🐩
    - [How to create GitHub Actions to deploy zip file to AWS Lambda](https://dev.classmethod.jp/articles/lambda-github-actions/)

<br>

- AWS API Gateway and AWS Lambda 🤐
    - [How to connect Lambda function to API Gateway](https://www.deadbear.io/simple-serverless-fastapi-with-aws-lambda/#serverless-fastapi-with-aws-lambda)