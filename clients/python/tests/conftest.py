from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

DEFAULT_TEST_BASE_URL = "https://api.example.com"
DEFAULT_TEST_CLERK_API_TOKEN = "sk_test_dummy"


def _add_src_to_path() -> None:
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    sys.path.insert(0, str(src))


_add_src_to_path()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--base-url",
        action="store",
        default=os.getenv("CIEN_SDK_TEST_BASE_URL", DEFAULT_TEST_BASE_URL),
        help="Base URL used by SDK tests.",
    )
    parser.addoption(
        "--clerk-api-token",
        action="store",
        default=os.getenv("CIEN_SDK_TEST_CLERK_API_TOKEN", DEFAULT_TEST_CLERK_API_TOKEN),
        help="Clerk API token used by SDK tests.",
    )
    parser.addoption(
        "--run-live-api",
        action="store_true",
        default=False,
        help="Force live API integration tests.",
    )


@pytest.fixture
def base_url(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--base-url"))


@pytest.fixture
def clerk_api_token(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--clerk-api-token"))


@pytest.fixture
def run_live_api(request: pytest.FixtureRequest, base_url: str, clerk_api_token: str) -> bool:
    explicit_flag = bool(request.config.getoption("--run-live-api"))
    non_default_config = (
        base_url != DEFAULT_TEST_BASE_URL or clerk_api_token != DEFAULT_TEST_CLERK_API_TOKEN
    )
    return explicit_flag or non_default_config
