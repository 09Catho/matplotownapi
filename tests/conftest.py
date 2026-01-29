import pytest
import os

# Set environment variable before importing app to pass Config validation
os.environ['API_KEY'] = 'test-secret-key'

from src.app import app as flask_app

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "API_KEY": "test-secret-key"
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
