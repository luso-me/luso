# Luso Server

## Environment vars

```shell
MONGO_CONNECTION_URL=mongodb://localhost:27017
GITHUB_CLIENT_ID=<github client id> (see notes on how to find it)
GITHUB_CLIENT_SECRET=<github client secret> (see notes on how to find it)
TOKEN_SECRET_KEY=<any random string> (see notes on how to generate)
```

## Dev Support

### Getting started

- Requirements
    - python 3.9 or greater
    - poetry 1.1.0 (`pip install poetry`).
    Install poetry globally if you are having issues running the `poetry` command below.
- Commands
    - `poetry install`

#### Notes

- A requirements.txt file can be generated using
  ```
  poetry export -f requirements.txt --output requirements.txt
  ```
- To ignore development requirements use
  ```
  poetry install --no-dev
  ```
- To activate the virtual env from your shell
  ```
  poetry shell
  ```
- To find GITHUB_CLIENT_ID do ...
- To find GITHUB_CLIENT_SECRET do ...
- TOKEN_SECRET_KEY generation
  ```shell
  openssl rand -hex 32
  ```

### To run the app

```shell
$> uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

#### Troubleshooting

Q: When I try to run `uvicorn` I get, `ModuleNotFoundError: No module named 'uvicorn'`

A: Make sure that you activated your virtual env with `poetry shell`


# Coding Standards

Code is automatically formatted with black before checkin
