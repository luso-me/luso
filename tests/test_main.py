from app.main import _extract_cors

localhost = "http://localhost:10000"
another_host = "http://some-other-host:5000"


def test_extract_cors():
    from app.config import settings

    settings.cors_allowed_origins = localhost
    result = _extract_cors()
    assert len(result) == 1
    assert result[0] == localhost

    settings.cors_allowed_origins = f"{localhost},{another_host}"
    result = _extract_cors()
    assert len(result) == 2
    assert result[0] == localhost
    assert result[1] == another_host
