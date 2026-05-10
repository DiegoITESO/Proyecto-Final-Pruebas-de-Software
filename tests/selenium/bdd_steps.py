"""Shared Gherkin step definitions for HTML documentation fixtures (pytest-bdd)."""

from __future__ import annotations

from pytest_bdd import given, parsers, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _wait(driver, timeout: float = 10.0):
    return WebDriverWait(driver, timeout)


@given(parsers.parse('I open the HTML fixture "{name}"'))
def step_open_fixture(open_fixture, name: str) -> None:
    open_fixture(name)


@then(parsers.parse('the element with data-testid "{tid}" should be visible'))
def step_tid_visible(driver, tid: str) -> None:
    el = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]')
    assert el.is_displayed()


@then(parsers.parse('the element with id "{eid}" should contain "{fragment}"'))
def step_id_contains(driver, eid: str, fragment: str) -> None:
    assert fragment in driver.find_element(By.ID, eid).text


@then(parsers.parse('the element with data-testid "{tid}" should contain "{fragment}"'))
def step_tid_contains(driver, tid: str, fragment: str) -> None:
    assert fragment in driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').text


@then(parsers.parse('the link with data-testid "{tid}" href should end with "{suffix}"'))
def step_href_ends(driver, tid: str, suffix: str) -> None:
    href = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').get_attribute("href")
    assert href is not None and href.endswith(suffix)


@when(parsers.parse('I click the element with data-testid "{tid}"'))
def step_click_tid(driver, tid: str) -> None:
    driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').click()


@then(parsers.parse('the element with data-testid "{tid}" should become visible within seconds'))
def step_wait_visible(driver, tid: str) -> None:
    _wait(driver).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="{tid}"]'))
    )


@then(
    parsers.parse(
        'the element with data-testid "{tid}" attribute "{attr}" should equal "{expected}"'
    )
)
def step_attr_equals(driver, tid: str, attr: str, expected: str) -> None:
    got = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').get_attribute(attr)
    assert got == expected


@then(parsers.parse('the input with data-testid "{tid}" should be required'))
def step_input_required(driver, tid: str) -> None:
    inp = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]')
    assert inp.get_attribute("required") is not None


@when(parsers.parse('I click the radio with data-testid "{tid}"'))
def step_click_radio(driver, tid: str) -> None:
    driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').click()


@then(parsers.parse('the radio with data-testid "{tid}" should be selected'))
def step_radio_selected(driver, tid: str) -> None:
    assert driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').is_selected()


@then(parsers.parse('the input with data-testid "{tid}" value should equal "{expected}"'))
def step_input_value(driver, tid: str, expected: str) -> None:
    got = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').get_attribute("value")
    assert got == expected


@then(parsers.parse('the input with data-testid "{tid}" placeholder should contain "{fragment}"'))
def step_placeholder_contains(driver, tid: str, fragment: str) -> None:
    ph = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').get_attribute("placeholder")
    assert ph is not None and fragment in ph


@then(parsers.parse('the element with data-testid "{tid}" tag name should be "{tag}"'))
def step_tag_name(driver, tid: str, tag: str) -> None:
    name = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').tag_name.lower()
    assert name == tag.lower()


@when(parsers.parse('I type "{text}" into data-testid "{tid}"'))
def step_type_tid(driver, text: str, tid: str) -> None:
    driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').send_keys(text)


@when(parsers.parse('I clear the input with data-testid "{tid}"'))
def step_clear_tid(driver, tid: str) -> None:
    driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').clear()


@when(parsers.parse('I click the button with data-testid "{tid}"'))
def step_click_button_tid(driver, tid: str) -> None:
    driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').click()


@then(
    parsers.parse('the element with data-testid "{tid}" should contain ignoring case "{fragment}"')
)
def step_tid_contains_icase(driver, tid: str, fragment: str) -> None:
    text = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{tid}"]').text.lower()
    assert fragment.lower() in text
