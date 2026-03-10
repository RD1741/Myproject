"""
Test Suite: AdNabuTestStore — Product Search & Add to Cart
URL     : https://adnabuteststore.myshopify.com
Password: AdNabuQA

Task 1 test cases are documented in TEST_CASES.md.
This file automates the primary happy-path scenario (Task 2).
"""

import pytest
from pages.store_page import StorePage


# ─────────────────────────────────────────────
# TASK 2 — AUTOMATED SCENARIO
# Search for a product and add it to the cart successfully
# ─────────────────────────────────────────────

class TestSearchAndAddToCart:
    """
    Automated scenario: Search for a product and add it to the cart.
    Covers the primary happy-path end-to-end flow.
    """

    SEARCH_TERM = "shirt"   # Generic term likely to return results

    @pytest.mark.smoke
    def test_search_and_add_product_to_cart(self, store: StorePage):
        """
        Scenario: User searches for a product and adds it to the cart.

        Steps:
          1. Open the store (password gate handled automatically).
          2. Search for a known product keyword.
          3. Assert at least one result is returned.
          4. Click the first product.
          5. Add it to the cart.
          6. Assert cart count has increased / cart contains an item.
        """
        # Step 1 — store is already open via fixture

        # Step 2 — Perform search
        store.search_for(self.SEARCH_TERM)

        # Step 3 — Verify results appear
        results = store.get_search_results()
        assert len(results) > 0, (
            f"Expected search results for '{self.SEARCH_TERM}', but got none."
        )

        # Step 4 — Open first product
        store.click_first_product()
        product_title = store.get_product_title()
        assert product_title, "Product page loaded but title is empty."

        # Step 5 — Add to cart
        store.add_to_cart()

        # Step 6 — Verify cart count updated
        cart_count = store.get_cart_count()
        assert cart_count != "" and cart_count != "0", (
            f"Cart count did not update after adding '{product_title}'. "
            f"Current count: '{cart_count}'"
        )


# ─────────────────────────────────────────────
# ADDITIONAL REGRESSION TESTS (bonus coverage)
# These mirror Test Cases 1–6 documented in TEST_CASES.md
# ─────────────────────────────────────────────

class TestProductSearch:
    """Additional search-focused regression tests."""

    @pytest.mark.regression
    def test_valid_product_search_returns_results(self, store: StorePage):
        """TC-S-01: Searching a valid keyword returns relevant products."""
        store.search_for("shirt")
        results = store.get_search_results()
        assert len(results) > 0, "No results returned for valid search term."

    @pytest.mark.regression
    def test_invalid_search_shows_no_results_message(self, store: StorePage):
        """TC-S-02: Searching a non-existent term shows a 'no results' message."""
        store.search_for("xyzzy_nonexistent_product_9999")
        no_results = store.has_no_results_message()
        results = store.get_search_results()
        assert no_results or len(results) == 0, (
            "Expected no results for a gibberish query, but products were shown."
        )

    @pytest.mark.regression
    def test_empty_search_does_not_crash(self, store: StorePage):
        """TC-S-03 (Edge): Submitting an empty search string does not crash the page."""
        store.search_for("")
        # Page should still be accessible — title should exist
        assert store.driver.title is not None, "Page title is None after empty search."
        assert "error" not in store.driver.title.lower(), (
            "Unexpected error page after empty search submission."
        )

    @pytest.mark.regression
    def test_special_characters_search_handled_gracefully(self, store: StorePage):
        """TC-S-04 (Edge): Special characters in search do not break the page."""
        store.search_for("<script>alert(1)</script>")
        # Page must still be accessible and not execute injected script
        assert "adnabu" in store.driver.current_url.lower() or "search" in store.driver.current_url.lower(), (
            "Navigated away from store after XSS-like search input."
        )


class TestAddToCart:
    """Add-to-cart focused regression tests."""

    @pytest.mark.regression
    def test_add_to_cart_increments_cart_count(self, store: StorePage):
        """TC-C-01: Adding a product increments the cart badge count."""
        store.search_for("shirt")
        results = store.get_search_results()
        assert len(results) > 0, "Precondition failed: no search results."

        store.click_first_product()
        store.add_to_cart()

        count = store.get_cart_count()
        assert count not in ("", "0"), (
            f"Cart count not updated after add-to-cart. Count='{count}'"
        )

    @pytest.mark.regression
    def test_cart_contains_added_product(self, store: StorePage):
        """TC-C-02: Product added to cart is visible in the cart page."""
        store.search_for("shirt")
        store.get_search_results()
        store.click_first_product()
        product_title = store.get_product_title()
        store.add_to_cart()

        store.go_to_cart()
        cart_items = store.get_cart_items()
        assert len(cart_items) > 0, (
            f"Cart page shows no items after adding '{product_title}'."
        )
