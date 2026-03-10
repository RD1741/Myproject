"""
Pytest configuration and shared fixtures for AdNabuTestStore automation.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pages.store_page import StorePage


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )


@pytest.fixture(scope="function")
def driver():
    """Set up and tear down a Chrome WebDriver instance per test."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    # Uncomment for headless CI environments:
    # chrome_options.add_argument("--headless=new")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service()  # Uses chromedriver from PATH
    _driver = webdriver.Chrome(service=service, options=chrome_options)
    _driver.implicitly_wait(2)

    yield _driver

    _driver.quit()


@pytest.fixture(scope="function")
def store(driver):
    """Return a StorePage instance with the store already open and unlocked."""
    page = StorePage(driver)
    page.open()
    return page
