```md
# 🧪 Test Cases – News Scraper (Selenium + Manual)

---

## 🔍 1. Functional Test Cases

### TC01 – Valid Search Input
- **Input:** `technology`
- **Expected Result:** News articles should be displayed (cards visible)
- **Status:** Pass

---

### TC02 – Empty Input Validation
- **Input:** *(empty)*
- **Expected Result:** Error message displayed ("empty topic")
- **Locator:** `.error`
- **Status:** Pass

---

### TC03 – Invalid Input Characters
- **Input:** `@@@@@@`
- **Expected Result:** Error message displayed
- **Status:** Pass

---

### TC04 – API Failure / Exception Handling
- **Condition:** API key missing or invalid response
- **Expected Result:** Proper error message displayed
- **Status:** Pass

---

## 🧪 2. UI Test Cases

### TC05 – Page Load
- **Expected Result:** Homepage loads without error
- **Elements Present:**
  - Navbar
  - Search bar
- **Status:** Pass

---

### TC06 – Search Box Functionality
- **Action:** Enter topic and press Enter
- **Expected Result:** Results displayed dynamically
- **Status:** Pass

---

### TC07 – Article Card Rendering
- **Expected Result:** Each article shows:
  - Title
  - Description
  - Read More link
- **Status:** Pass

---

## 🔁 3. Pagination Test Cases

### TC08 – Next Button
- **Action:** Click "Next ➡"
- **Expected Result:** Next set of articles displayed
- **Status:** Pass

---

### TC09 – Prev Button
- **Action:** Click "⬅ Prev"
- **Expected Result:** Previous articles displayed
- **Status:** Pass

---

## 🧪 4. Selenium Automation Test Coverage

### Automated Scenarios:

- ✔ Valid search execution (`technology`)
- ✔ Empty input validation
- ✔ Invalid input validation (`@@@@@@`)
- ✔ Search history verification (localStorage UI buttons)
- ✔ Pagination Next button click
- ✔ Pagination Prev button click
- ✔ UI elements presence check (navbar, search box, cards)

---

## 🔁 5. Search History Test Case

### TC10 – Search History Storage
- **Action:** Search topic "ai"
- **Expected Result:** "ai" appears in history buttons
- **Storage:** localStorage
- **Status:** Pass

---

## ⚠️ 6. Edge Case Testing

- No API key provided
- API request timeout/failure
- No articles returned for query
- Special characters input
- Very long input strings

---

## 📊 Summary

| Category | Coverage |
|----------|----------|
| Functional | ✅ Complete |
| UI Testing | ✅ Complete |
| Pagination | ✅ Complete |
| Automation (Selenium) | ✅ Complete |
| Edge Cases | ✅ Covered |

---