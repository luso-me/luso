# Luso Server
## Environment vars
```shell
MONGO_CONNECTION_URL=mongodb://localhost:27017
GITHUB_CLIENT_ID=<github client id>
GITHUB_CLIENT_SECRET=<github client secret>
SECRET_KEY=<any random string> (see notes on how to generate)

```
## Dev Support

### Getting started

- Requirements
    - python 3.8 or greater
    - poetry 1.1.0 (`pip install poetry`)
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
- SECRET_KEY generation
  ```shell
  openssl rand -hex 32
  ```

### To run the app

```shell
$> uvicorn app.main:app --reload --host 0.0.0.0 --port 5000  
```
