"""
Page Object Model for AdNabuTestStore
URL: https://adnabu-store-assignment1.myshopify.com/
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StorePage:
    """Handles interactions with the main store pages."""

    BASE_URL = "https://adnabu-store-assignment1.myshopify.com/"
    PASSWORD = "AdNabuQA"

    # Locators
    PASSWORD_INPUT = (By.ID, "password")
    PASSWORD_SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    SEARCH_ICON = (By.CSS_SELECTOR, "a[href='/search'], button[aria-label*='Search'], .header__icon--search")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search'], input[name='q'], #Search-In-Modal")
    SEARCH_SUBMIT = (By.CSS_SELECTOR, "button[type='submit'][aria-label*='Search'], .search__button")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".product-item, .grid__item, .product-card-wrapper")
    FIRST_PRODUCT = (By.CSS_SELECTOR, ".product-item:first-child a, .grid__item:first-child a.full-unstyled-link, .product-card-wrapper:first-child a")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "button[name='add'], .product-form__submit, button[id*='AddToCart']")
    CART_COUNT = (By.CSS_SELECTOR, ".cart-count-bubble, .header__cart-count, span[aria-label*='cart']")
    CART_ICON = (By.CSS_SELECTOR, "a[href='/cart'], .header__icon--cart")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item, .cart__item")
    NO_RESULTS_MSG = (By.CSS_SELECTOR, ".search__no-results, .empty-page-content, p.search-status__summary")
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product__title, .product-meta__title, h1[itemprop='name']")

    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        """Navigate to the store base URL."""
        self.driver.get(self.BASE_URL)
        self._handle_password_gate()

    def _handle_password_gate(self):
        """Handle Shopify password-protected store gate if present."""
        try:
            pwd_input = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.PASSWORD_INPUT)
            )
            pwd_input.clear()
            pwd_input.send_keys(self.PASSWORD)
            self.driver.find_element(*self.PASSWORD_SUBMIT).click()
            # Wait for the homepage to load after password
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except Exception:
            # No password gate — already on the store
            pass

    def search_for(self, query: str):
        """Open search and submit a query."""
        # Try clicking search icon first
        try:
            search_icon = self.wait.until(EC.element_to_be_clickable(self.SEARCH_ICON))
            search_icon.click()
        except Exception:
            pass  # Search bar may already be visible

        search_box = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

    def get_search_results(self):
        """Return list of product result elements."""
        try:
            self.wait.until(EC.presence_of_all_elements_located(self.SEARCH_RESULTS))
            return self.driver.find_elements(*self.SEARCH_RESULTS)
        except Exception:
            return []

    def has_no_results_message(self):
        """Check if a 'no results' message is displayed."""
        try:
            msg = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.NO_RESULTS_MSG)
            )
            return msg.is_displayed()
        except Exception:
            return False

    def click_first_product(self):
        """Click the first product in the search results."""
        first = self.wait.until(EC.element_to_be_clickable(self.FIRST_PRODUCT))
        first.click()

    def add_to_cart(self):
        """Click the Add to Cart button on a product page."""
        btn = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN))
        btn.click()

    def get_cart_count(self) -> str:
        """Return the cart item count from the header badge."""
        badge = self.wait.until(EC.presence_of_element_located(self.CART_COUNT))
        return badge.text.strip()

    def go_to_cart(self):
        """Navigate to the cart page."""
        cart = self.wait.until(EC.element_to_be_clickable(self.CART_ICON))
        cart.click()

    def get_cart_items(self) -> list:
        """Return list of cart item elements."""
        self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEMS))
        return self.driver.find_elements(*self.CART_ITEMS)

    def get_product_title(self) -> str:
        """Return the product page title text."""
        title = self.wait.until(EC.presence_of_element_located(self.PRODUCT_TITLE))
        return title.text.strip()
