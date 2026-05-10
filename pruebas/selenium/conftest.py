# Configuracion compartida: ruta a fixtures y driver Chrome headless.
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """
    Provides the absolute path to the fixtures directory.
    
    Returns:
        Path: The Path object pointing to the 'fixtures' folder.
    """
    return Path(__file__).resolve().parent / "fixtures"


def file_uri(path: Path) -> str:
    """
    Converts a given file path to a file URI string.
    
    Args:
        path (Path): The file path to convert.
        
    Returns:
        str: The file URI.
    """
    return path.resolve().as_uri()


@pytest.fixture(scope="session")
def driver():
    """
    Initializes and yields a headless Chrome WebDriver for the test session.
    
    Yields:
        webdriver.Chrome: The configured Chrome WebDriver instance.
    """
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
    """
    Provides a callable to open a specific HTML fixture file in the browser.
    
    Args:
        driver (webdriver.Chrome): The active WebDriver instance.
        fixtures_dir (Path): The base directory for fixtures.
        
    Returns:
        Callable[[str], None]: A function that takes a filename and loads it in the driver.
    """
    def _open(name: str) -> None:
        driver.get(file_uri(fixtures_dir / name))

    return _open
