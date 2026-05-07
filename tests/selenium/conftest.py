"""Shared Selenium fixtures and pytest-bdd step definitions for HTML fixtures."""

from pathlib import Path

import pytest
from pytest_bdd import then, when
from pytest_bdd.parsers import parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def _wait(driver, seconds: int = 10):
    return WebDriverWait(driver, seconds)


def file_uri(path: Path) -> str:
    return path.resolve().as_uri()


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="session")
def driver():
    """One browser per session; each scenario navigates to its own fixture."""
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


# --- BDD steps (must live in conftest so pytest-bdd binds them to scenarios) ---


@when(parse("I open the HTML fixture {name}"))
def open_html_fixture(open_fixture, name: str):
    open_fixture(name)


@then(parse('test id "{tid}" is displayed'))
def test_id_displayed(driver, tid: str):
    assert driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').is_displayed()


@then(parse('element id "{eid}" contains "{text}"'))
def element_id_contains(driver, eid: str, text: str):
    assert text in driver.find_element(By.ID, eid).text


@then(parse('test id "{tid}" contains "{text}"'))
def test_id_contains(driver, tid: str, text: str):
    assert text in driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').text


@then(parse('test id "{tid}" href ends with "{suffix}"'))
def test_id_href_suffix(driver, tid: str, suffix: str):
    href = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').get_attribute("href")
    assert href.endswith(suffix)


@when(parse('I click test id "{tid}"'))
def click_test_id(driver, tid: str):
    driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').click()


@then(parse('test id "{tid}" is present'))
def test_id_present(driver, tid: str):
    _wait(driver).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{tid}"]')))


@then(parse('test id "{tid}" becomes visible'))
def test_id_visible(driver, tid: str):
    _wait(driver).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="{tid}"]')))


@when(parse('I type "{value}" into test id "{tid}"'))
def type_into_test_id(driver, value: str, tid: str):
    driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').send_keys(value)


@when(parse('I clear test id "{tid}"'))
def clear_test_id(driver, tid: str):
    driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').clear()


@then(parse('test id "{tid}" has aria-required true'))
def aria_required(driver, tid: str):
    el = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]')
    assert el.get_attribute("aria-required") == "true"


@then(parse('test id "{tid}" has required attribute'))
def html_required(driver, tid: str):
    val = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').get_attribute("required")
    assert val is not None


@then(parse('test id "{tid}" is selected'))
def is_selected(driver, tid: str):
    assert driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').is_selected()


@then(parse('test id "{tid}" attribute "{attr}" equals "{value}"'))
def attr_equals(driver, tid: str, attr: str, value: str):
    actual = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').get_attribute(attr)
    assert actual == value


@then(parse('test id "{tid}" placeholder contains "{text}"'))
def placeholder_contains(driver, tid: str, text: str):
    ph = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').get_attribute("placeholder")
    assert text in ph


@then(parse('test id "{tid}" tag name is "{tag}"'))
def tag_name_is(driver, tid: str, tag: str):
    assert driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').tag_name.lower() == tag.lower()


@then(parse('test id "{tid}" contains substring "{text}" case-insensitive'))
def test_id_contains_ci(driver, tid: str, text: str):
    body = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').text.lower()
    assert text.lower() in body


@when("I submit train form")
def submit_train(driver):
    driver.find_element(By.CSS_SELECTOR, '[data-testid="btn-submit-train"]').click()


@when("I submit predict form")
def submit_predict(driver):
    driver.find_element(By.CSS_SELECTOR, '[data-testid="btn-predict-run"]').click()
