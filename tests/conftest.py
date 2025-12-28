"""Pytest configuration and fixtures for AnyUnit tests."""

import pytest
from app import create_app
from config import Config


class TestConfig(Config):
    """Test configuration."""
    TESTING = True
    DEBUG = False
    SECRET_KEY = 'test-secret-key'


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app(TestConfig)
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def app_context(app):
    """Create application context."""
    with app.app_context():
        yield


@pytest.fixture
def unit_manager(app_context):
    """Create UnitManager instance within app context."""
    from app.utils.unit_converter import UnitManager
    return UnitManager()
