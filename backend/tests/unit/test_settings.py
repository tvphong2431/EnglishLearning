from app.config.settings import Settings
import pytest

def test_settings_rejects_missing_deno_path(monkeypatch):
    monkeypatch.delenv("DENO_PATH", raising=False)
    monkeypatch.setenv(
        "POT_SERVER_URL",
        "http://127.0.0.1:4416",
    )

    with pytest.raises(KeyError):
        Settings()

def test_settings_rejects_missing_pot_server_url(monkeypatch):
    monkeypatch.setenv(
        "DENO_PATH",
        r"C:\Users\Nelsonn\.deno\bin\deno.exe",
    )
    monkeypatch.delenv("POT_SERVER_URL", raising=False)

    with pytest.raises(KeyError):
        Settings()

def test_settings_loads_environment_variables(monkeypatch):
    monkeypatch.setenv(
        "DENO_PATH",
        r"C:\Users\Nelsonn\.deno\bin\deno.exe",
    )
    monkeypatch.setenv(
        "POT_SERVER_URL",
        "http://127.0.0.1:4416",
    )

    settings = Settings()

    assert settings.deno_path == r"C:\Users\Nelsonn\.deno\bin\deno.exe"
    assert settings.pot_server_url == "http://127.0.0.1:4416"