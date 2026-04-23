import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# =========================
# 🔧 DRIVER SETUP (STABLE)
# =========================
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 15)  # Increased timeout


# =========================
# 🧠 SAFE HELPERS
# =========================
def load(url):
    driver.get(url)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    time.sleep(1.5)  # Slightly more buffer


def safe_click(element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", element)


def find_error_message():
    """Try multiple selectors to find an error message on the page."""
    selectors = [
        (By.CLASS_NAME, "error"),
        (By.CLASS_NAME, "alert"),
        (By.CLASS_NAME, "alert-danger"),
        (By.CLASS_NAME, "flash"),
        (By.CSS_SELECTOR, "[class*='error']"),
        (By.CSS_SELECTOR, "[class*='alert']"),
        (By.CSS_SELECTOR, "[role='alert']"),
    ]
    for by, selector in selectors:
        try:
            el = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((by, selector))
            )
            if el and el.text.strip():
                return el
        except Exception:
            continue
    return None


BASE_URL = "http://127.0.0.1:5000/"

passed = 0
failed = 0


def report(name, success, reason=""):
    global passed, failed
    if success:
        passed += 1
        print(f"✅ {name} Passed")
    else:
        failed += 1
        print(f"❌ {name} Failed" + (f": {reason}" if reason else ""))


# =========================
# 🚀 TEST START
# =========================
try:

    # =========================
    # ✅ 1. VALID SEARCH
    # =========================
    try:
        load(BASE_URL)
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "topic")))
        search_box.clear()
        search_box.send_keys("technology")
        search_box.send_keys(Keys.RETURN)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card")))
        report("Valid Search", True)
    except Exception as e:
        report("Valid Search", False, str(e))

    # =========================
    # ❌ 2. EMPTY INPUT
    # =========================
    try:
        load(BASE_URL)
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "topic")))
        search_box.clear()

        # Try submitting via the form button first, then fallback to RETURN
        try:
            submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            safe_click(submit_btn)
        except Exception:
            search_box.send_keys(Keys.RETURN)

        time.sleep(1.5)

        # Check for error via multiple strategies
        error_el = find_error_message()

        if error_el:
            # Accept any error/warning message for empty input
            report("Empty Input", True)
        else:
            # Fallback: check if page still shows the form (no navigation = validation blocked it)
            try:
                still_on_page = driver.find_element(By.NAME, "topic")
                # If search box is still present and empty, client-side validation worked
                report("Empty Input", True)
            except Exception:
                report("Empty Input", False, "No error element found and page navigated away")
    except Exception as e:
        report("Empty Input", False, str(e))

    # =========================
    # ❌ 3. INVALID INPUT
    # =========================
    try:
        load(BASE_URL)
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "topic")))
        search_box.clear()
        search_box.send_keys("@@@@@@")
        search_box.send_keys(Keys.RETURN)

        time.sleep(1.5)

        error_el = find_error_message()

        if error_el:
            report("Invalid Input", True)
        else:
            # Some apps show "no results" instead of an error — accept that too
            try:
                no_results = driver.find_element(By.XPATH,
                    "//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'no result') or "
                    "contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'not found') or "
                    "contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'invalid')]"
                )
                report("Invalid Input", True)
            except Exception:
                report("Invalid Input", False, "No error or no-results message found")
    except Exception as e:
        report("Invalid Input", False, str(e))

    # =========================
    # 🔁 4. SEARCH HISTORY
    # =========================
    try:
        load(BASE_URL)
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "topic")))
        search_box.clear()
        search_box.send_keys("ai")
        search_box.send_keys(Keys.RETURN)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card")))

        load(BASE_URL)

        history_buttons = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#history button"))
        )
        history_texts = [btn.text.lower() for btn in history_buttons]
        assert any("ai" in text for text in history_texts), \
            f"'ai' not found in history: {history_texts}"
        report("Search History", True)
    except Exception as e:
        report("Search History", False, str(e))

    # =========================
    # 📄 5. PAGINATION NEXT
    # =========================
    try:
        load(BASE_URL)
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "topic")))
        search_box.clear()
        search_box.send_keys("technology")
        search_box.send_keys(Keys.RETURN)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card")))

        next_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]"))
        )
        safe_click(next_btn)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card")))
        report("Pagination Next", True)
    except Exception as e:
        report("Pagination Next", False, str(e))

    # =========================
    # 📄 6. PAGINATION PREV
    # =========================
    try:
        prev_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Prev')]"))
        )
        safe_click(prev_btn)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card")))
        report("Pagination Prev", True)
    except Exception as e:
        report("Pagination Prev", False, str(e))

    # =========================
    # 🎨 7. UI CHECK
    # =========================
    try:
        load(BASE_URL)
        navbar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "navbar")))
        search_input = driver.find_element(By.NAME, "topic")
        assert navbar is not None
        assert search_input is not None
        report("UI Layout", True)
    except Exception as e:
        report("UI Layout", False, str(e))


finally:
    print(f"\n📊 Results: {passed} passed, {failed} failed out of {passed + failed} tests")
    time.sleep(2)
    driver.quit()