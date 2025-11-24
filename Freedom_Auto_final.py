import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# -----------------------------------------
# CONNECT TO YOUR ALREADY-OPEN CHROME
# -----------------------------------------
def connect_to_browser():
    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=chrome_options)
    return driver


# -----------------------------------------
# CLICK THE FIRST ENABLED "SELECT" BUTTON
# -----------------------------------------
def click_first_enabled_offering(driver):
    try:
        buttons = driver.find_elements(By.CSS_SELECTOR, "button.program-select-btn")

        if not buttons:
            print("No offering buttons found.")
            return False

        for btn in buttons:
            disabled = btn.get_attribute("disabled")

            if not disabled:   # This is the first AVAILABLE offering
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", btn)
                print("Clicked first ENABLED offering.")
                return True

        print("Only disabled offerings found — retrying…")
        return False

    except Exception as e:
        print(f"Error clicking offering: {e}")
        return False


# -----------------------------------------
# CLICK A BUTTON SAFELY BY ID
# -----------------------------------------
def safe_click_id(driver, element_id, timeout=6):
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        el.click()
        print(f"Clicked {element_id}")
        return True
    except:
        print(f"{element_id} not clickable yet.")
        return False


# -----------------------------------------
# CLICK CHECKBOX BY NAME = dependentSelector
# -----------------------------------------
def click_dependent_checkbox(driver):
    try:
        checkbox_input = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.depedent-selector"))
        )

        label = checkbox_input.find_element(By.XPATH, "./following-sibling::label")
        driver.execute_script("arguments[0].scrollIntoView(true);", label)
        driver.execute_script("arguments[0].click();", label)

        print("Clicked dependent checkbox (typo class).")
        return True

    except Exception as e:
        print("Dependent checkbox present but not clickable:", e)
        return False


# -----------------------------------------
# CLICK CUSTOM CONTROL LABEL (waiver)
# -----------------------------------------
def click_custom_control_label(driver):
    try:
        label = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label.custom-control-label"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", label)
        driver.execute_script("arguments[0].click();", label)
        print("Clicked custom-control-label")
        return True
    except Exception as e:
        print("Custom control label not ready:", e)
        return False


# -----------------------------------------
# CLICK THE PROCEED TO CHECKOUT BUTTON
# -----------------------------------------
def click_proceed_checkout(driver):
    try:
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.btn-NextRegistrationStep.btn.btn-block.btn-lg.btn-primary")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        driver.execute_script("arguments[0].click();", btn)
        print("Clicked Proceed to Checkout button")
        return True
    except Exception as e:
        print("Proceed-to-checkout button not ready:", e)
        return False


# -----------------------------------------
# MAIN LOOP
# -----------------------------------------
def main():
    from datetime import datetime, timedelta

    target_time = datetime.now().replace(hour=8, minute=38, second=45, microsecond=0)

    driver = connect_to_browser()
    print("Connected to existing Chrome session.")

    # if datetime.now() > target_time:
    #     target_time += timedelta(days=1)

    # print(f"Current Time: {datetime.now()}")
    # print(f"Waiting until {target_time} to start...")

    # # Wait until start time
    # while datetime.now() < target_time:
    #     time.sleep(0.5)
    #     print(datetime.now())
    #     driver.refresh()

    print("Time reached! Starting the bot...")

    while True:
        print("\nRefreshing page...")
        driver.refresh()
        time.sleep(3)

        # --- STEP 1: NEW METHOD — Click first enabled offering ---
        if not click_first_enabled_offering(driver):
            time.sleep(1)
            continue

        time.sleep(1)

        # --- STEP 2: registerBtn ---
        if not safe_click_id(driver, "registerBtn"):
            time.sleep(1)
            continue

        time.sleep(1)

        # --- STEP 3: dependent checkbox ---
        if not click_dependent_checkbox(driver):
            time.sleep(1)
            continue

        time.sleep(1)

        # --- STEP 4: btnNext ---
        if not safe_click_id(driver, "btnNext"):
            time.sleep(1)
            continue

        time.sleep(2)

        # --- STEP 5: waiver checkbox ---
        if not click_custom_control_label(driver):
            time.sleep(1)
            continue

        time.sleep(1)

        # --- STEP 6: proceed to checkout ---
        if not click_proceed_checkout(driver):
            time.sleep(1)
            continue

        time.sleep(2)

        ### ----- STEP 7: CLICK EXISTING CARD (WITH CONTROLLED REFRESH) ----- ###
        MAX_RETRIES = 25   # how many reloads allowed in Step 7 → Final

        for attempt in range(MAX_RETRIES):

            checkout_clicked = False
        while not checkout_clicked:
            try:
                checkout_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="checkoutButton"]'))
                )
                driver.execute_script("arguments[0].click();", checkout_btn)
                print("Checkout button clicked.")
                checkout_clicked = True
            except Exception as e:
                print(f"Checkout button not ready yet: {e}")
                time.sleep(2)
                driver.refresh()
        ### ----- FINAL STEP: CLICK PAY BUTTON (WITH CONTROLLED REFRESH) ----- ###
            try:
                print(f"Attempt {attempt + 1}: Trying FINAL STEP…")

                # EXAMPLE — replace with your final pay button locator
                print("\n--- DEBUG: Checking for existing card modal ---")
                time.sleep(0.5)
                card_link = driver.find_element(By.XPATH, "//a[contains(@id,'aChargeCardSM_') and contains(@class,'card-item-1-large')]")
                card_link.click()
                print("Existing card modal button clicked.")

            except Exception as e:
                print(f"Final step failed: {e}. Refreshing…")
                driver.refresh()
                time.sleep(0.4)
        else:
            raise Exception("Final step never became clickable.")

        print("Automation completed.")


if __name__ == "__main__":
    main()


