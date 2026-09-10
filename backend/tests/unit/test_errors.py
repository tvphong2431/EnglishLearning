import pytest

from app.errors import AppError


@pytest.mark.unit
def test_app_error():
    error = AppError(
        code="YOUTUBE_ACCESS_BLOCKED",
        message="Unable to access YouTube.",
        status_code=503,
    )

    assert error.code == "YOUTUBE_ACCESS_BLOCKED"
    assert error.message == "Unable to access YouTube."
    assert error.status_code == 503