# 🌋 VolcanoAPI 🌋
<br>

## 🐥 How do I start?
<br>

- ⏰ **Execute these commands**
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

## 🦕 References
- [How to create Docker environment for FastAPI](https://zenn.dev/sh0nk/books/537bb028709ab9/viewer/5d287c)

<br>

## 🌳 Folder Structure
```
└── 📁volcano
    └── __init__.py
    └── 📁__pycache__
        └── __init__.cpython-39.pyc
        └── main.cpython-39.pyc
    └── 📁api
        └── __init__.py
        └── 📁api_v1
            └── __init__.py
            └── api_v1_routers.py
            └── 📁endpoints
                └── __init__.py
    └── 📁core
        └── __init__.py
    └── 📁exceptions
        └── __init__.py
    └── main.py
    └── 📁models
        └── __init__.py
    └── 📁schemas
        └── __init__.py
```