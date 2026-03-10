# Test Cases — AdNabuTestStore
**Application:** AdNabuTestStore (https://adnabuteststore.myshopify.com)  
**Password:** AdNabuQA  
**Tester:** QA Assignment  

---

## a) Product Search

---

### TC-S-01 — Valid Search Returns Relevant Results
**Type:** Positive  
**Priority:** High

**Steps:**
1. Open the store and enter store password.
2. Click the search icon in the header.
3. Type `shirt` in the search input.
4. Press Enter or click the search button.

**Expected Result:**
- A results page is displayed with one or more product cards.
- All visible products are relevant to the query (contain "shirt" in title or description).
- Product images, names, and prices are visible.

---

### TC-S-02 — Search with No Matching Products
**Type:** Negative  
**Priority:** High

**Steps:**
1. Open the store.
2. Search for `xyzzy_nonexistent_product_9999`.

**Expected Result:**
- Zero product cards are displayed.
- A user-friendly "No results found" (or equivalent) message is shown.
- No JavaScript errors or broken page layout.

---

### TC-S-03 — Search with Special Characters (XSS / Injection Attempt)
**Type:** Negative / Security Edge Case  
**Priority:** Medium

**Steps:**
1. Open the store.
2. Search for `<script>alert(1)</script>`.

**Expected Result:**
- The browser does **not** execute any script (no alert popup).
- The store remains on the search/results page without crashing.
- The input is either escaped in the URL or ignored gracefully.

---

### TC-S-04 — Empty Search Submission
**Type:** Negative / Edge Case  
**Priority:** Medium

**Steps:**
1. Open the store.
2. Click the search icon.
3. Leave the input field empty.
4. Press Enter or click the search button.

**Expected Result:**
- The page does **not** crash or show a server error.
- Either all products are returned OR a prompt/message asks the user to enter a search term.
- URL remains valid (no 500/404 response).

---

### TC-S-05 — Search is Case-Insensitive
**Type:** Positive  
**Priority:** Low

**Steps:**
1. Search for `SHIRT` (all caps).
2. Note the number/set of results.
3. Search again for `shirt` (all lowercase).

**Expected Result:**
- Both searches return the same (or equivalent) set of product results, confirming case-insensitive handling.

---

### TC-S-06 — Partial Keyword Search Returns Broader Results
**Type:** Positive / Edge Case  
**Priority:** Low

**Steps:**
1. Search for `sh` (partial prefix).

**Expected Result:**
- Results are returned that match any product whose name/description begins with or contains "sh".
- The store does not error out for a very short query.

---

## b) Add to Cart

---

### TC-C-01 — Add a Single Product to an Empty Cart
**Type:** Positive  
**Priority:** High

**Steps:**
1. Open the store with a fresh (empty) session.
2. Search for `shirt` and open the first result.
3. Click **Add to Cart**.

**Expected Result:**
- The cart icon badge updates from `0` (or empty) to `1`.
- A success confirmation is shown (drawer, toast, or redirect to cart).
- No error messages appear.

---

### TC-C-02 — Added Product Appears in Cart Page
**Type:** Positive  
**Priority:** High

**Steps:**
1. Search for a product and add it to the cart.
2. Navigate to `/cart` or click the cart icon.

**Expected Result:**
- The cart page lists exactly the product that was added.
- Product name, quantity (= 1), and price are correctly displayed.
- Subtotal matches the product price.

---

### TC-C-03 — Add Multiple Quantities of the Same Product
**Type:** Positive / Edge Case  
**Priority:** Medium

**Steps:**
1. Open a product page.
2. Change the quantity selector to `3`.
3. Click **Add to Cart**.

**Expected Result:**
- Cart badge shows `3` (or the total item count increases by 3).
- Cart page shows quantity `3` for that product and the subtotal is `unit price × 3`.

---

### TC-C-04 — Add to Cart Without Selecting Required Variant
**Type:** Negative  
**Priority:** High

**Steps:**
1. Open a product that has size/colour variants (if available).
2. Do **not** select any variant.
3. Click **Add to Cart**.

**Expected Result:**
- The item is **not** added to the cart.
- An inline validation message prompts the user to select a variant (e.g., "Please select a size").
- Cart count does not change.

---

### TC-C-05 — Cart Persists After Page Refresh
**Type:** Positive / Edge Case  
**Priority:** Medium

**Steps:**
1. Add a product to the cart.
2. Refresh the page (`F5` / `Ctrl+R`).
3. Check the cart icon count and navigate to the cart page.

**Expected Result:**
- Cart badge still shows the correct count after refresh.
- The cart page still contains the previously added item with correct details (Shopify uses cookies/session to persist the cart).

---

### TC-C-06 — Add to Cart from Search Results (Quick Add, if Available)
**Type:** Positive  
**Priority:** Low

**Steps:**
1. Search for `shirt`.
2. On the search results page, hover over the first product card.
3. If a **Quick Add** or **Add to Cart** button appears on the card, click it.

**Expected Result:**
- Product is added to cart without navigating to the product detail page.
- Cart badge increments by 1.
- A confirmation notification appears.

---

## Summary Table

| ID      | Area   | Type              | Priority |
|---------|--------|-------------------|----------|
| TC-S-01 | Search | Positive          | High     |
| TC-S-02 | Search | Negative          | High     |
| TC-S-03 | Search | Negative/Security | Medium   |
| TC-S-04 | Search | Negative/Edge     | Medium   |
| TC-S-05 | Search | Positive          | Low      |
| TC-S-06 | Search | Positive/Edge     | Low      |
| TC-C-01 | Cart   | Positive          | High     |
| TC-C-02 | Cart   | Positive          | High     |
| TC-C-03 | Cart   | Positive/Edge     | Medium   |
| TC-C-04 | Cart   | Negative          | High     |
| TC-C-05 | Cart   | Positive/Edge     | Medium   |
| TC-C-06 | Cart   | Positive          | Low      |
