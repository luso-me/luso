# Luso Server

## Dev Support

### Getting started

- Requirements
    - python 3.8 or greater
    - poetry 1.1.0
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