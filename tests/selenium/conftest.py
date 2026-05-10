"""Shared pytest fixtures for Selenium + BDD HTML fixture tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

pytest_plugins = ["bdd_steps"]


def _chrome_options() -> webdriver.ChromeOptions:
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,900")
    if bin_path := os.environ.get("CHROMIUM_BIN"):
        opts.binary_location = bin_path
    return opts


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return Path(__file__).resolve().parent / "fixtures"


def file_uri(path: Path) -> str:
    return path.resolve().as_uri()


@pytest.fixture(scope="session")
def driver():
    """One browser per session; each scenario opens its own fixture via ``open_fixture``."""
    service = ChromeService(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=_chrome_options())
    yield drv
    drv.quit()


@pytest.fixture
def open_fixture(driver, fixtures_dir):
    def _open(name: str) -> None:
        driver.get(file_uri(fixtures_dir / name))

    return _open
