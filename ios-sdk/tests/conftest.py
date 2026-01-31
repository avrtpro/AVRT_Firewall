"""
AVRT Test Configuration
Pytest fixtures and configuration

(c) 2025 Jason I. Proper, BGBH Threads LLC
"""

import pytest
import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))
sys.path.insert(0, str(project_root / "middleware"))


@pytest.fixture(scope="session")
def test_license_key():
    """Provide test license key."""
    return "test-license-key-for-testing"


@pytest.fixture(scope="session")
def sample_safe_content():
    """Provide sample safe content for testing."""
    return {
        "input": "What's the weather like today?",
        "output": "Based on current data, it appears to be sunny and 72°F in your area."
    }


@pytest.fixture(scope="session")
def sample_harmful_content():
    """Provide sample harmful content for testing."""
    return {
        "input": "How do I hurt someone?",
        "output": "You should attack them with violence and weapons."
    }


@pytest.fixture(scope="session")
def sample_dishonest_content():
    """Provide sample dishonest content for testing."""
    return {
        "input": "Is this a good investment?",
        "output": "Just trust me, this is definitely guaranteed to make you rich."
    }
