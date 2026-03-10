# AdNabuTestStore — QA Assignment

Automated test suite for [AdNabuTestStore](https://adnabuteststore.myshopify.com) (Store Password: `AdNabuQA`).

---

## Project Structure

```
adnabu-qa/
├── pages/
│   ├── __init__.py
│   └── store_page.py          # Page Object Model (all locators + actions)
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Fixtures: WebDriver setup/teardown
│   └── test_search_and_cart.py  # All test scenarios
├── reports/
│   └── test_report.html       # Auto-generated HTML report (after run)
├── TEST_CASES.md              # Task 1: 12 manually written test cases
├── requirements.txt
├── pytest.ini
└── README.md
```


## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.9 + |
| Google Chrome | Latest stable |
| ChromeDriver | Must match Chrome version |

---

## Setup

### 1 — Clone the repository

```bash
git clone https://github.com/<your-username>/adnabu-qa.git
cd adnabu-qa
```

### 2 — Create and activate a virtual environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Install ChromeDriver

**Option A — Automatic (recommended):**  
`webdriver-manager` handles this automatically when you run the tests.

**Option B — Manual:**  
1. Check your Chrome version: `chrome://settings/help`
2. Download the matching ChromeDriver from https://chromedriver.chromium.org/downloads
3. Add it to your system PATH.

---

## Running the Tests

### Run all tests (with HTML report)

```bash
pytest
```

Report is saved to: `reports/test_report.html`

### Run only the primary automated scenario (Task 2 — smoke test)

```bash
pytest -m smoke
```

### Run regression tests

```bash
pytest -m regression
```

### Run a single specific test

```bash
pytest tests/test_search_and_cart.py::TestSearchAndAddToCart::test_search_and_add_product_to_cart -v
```

### Run headless (no browser window — useful for CI)

In `tests/conftest.py`, uncomment these lines inside the `driver()` fixture:

```python
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
```

---

## Test Cases (Task 1)

All 12 manually written test cases (6 for Product Search, 6 for Add to Cart) are documented in [`TEST_CASES.md`](./TEST_CASES.md).

| Area | Positive | Negative | Edge |
|------|----------|----------|------|
| Search | 3 | 2 | 2 |
| Cart | 4 | 1 | 2 |

---

## Automated Scenario (Task 2)

**Scenario:** Search for a product and add it to the cart successfully.

**Flow:**
1. Open the store (password gate handled automatically).
2. Search for `"snowboard"`.
3. Assert results are returned.
4. Click the first product.
5. Assert product page loaded (title is non-empty).
6. Click **Add to Cart**.
7. Assert the cart badge count is no longer `0`.

**Test file:** `tests/test_search_and_cart.py` → `TestSearchAndAddToCart::test_search_and_add_product_to_cart`

---

## Design Decisions

- **Page Object Model (POM):** All locators and browser interactions are in `pages/store_page.py`, keeping tests readable and maintainable.
- **No `time.sleep()`:** All waits use `WebDriverWait` with `expected_conditions` for reliability.
- **Password Gate:** Handled automatically in `StorePage.open()` — tests don't need to know about it.
- **Modular fixtures:** `conftest.py` provides a clean `driver` and `store` fixture so each test starts fresh.
- **HTML Report:** `pytest-html` generates a self-contained report in `reports/test_report.html`.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `SessionNotCreatedException` | ChromeDriver version doesn't match Chrome. Update via `webdriver-manager` or download manually. |
| `NoSuchElementException` | Shopify may have updated the store theme. Re-inspect locators in `store_page.py`. |
| Tests timeout on CI | Enable headless mode in `conftest.py` (see above). |

---

