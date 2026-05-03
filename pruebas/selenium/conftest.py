# Configuracion compartida: ruta a fixtures y driver Chrome headless.
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return Path(__file__).resolve().parent / "fixtures"


def file_uri(path: Path) -> str:
    return path.resolve().as_uri()


@pytest.fixture(scope="session")
def driver():
    # Un solo navegador por sesion: cada prueba abre su fixture con open_fixture.
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,900")
    service = ChromeService(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=opts)
    yield drv
    drv.quit()


@pytest.fixture
def open_fixture(driver, fixtures_dir):
    def _open(name: str) -> None:
        driver.get(file_uri(fixtures_dir / name))

    return _open
