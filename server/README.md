# FAQ

### To run the app

```shell
$> uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

### Troubleshooting

Q: When I try to run `uvicorn` I get, `ModuleNotFoundError: No module named 'uvicorn'`

A: Make sure that you activated your virtual env with `poetry shell`
