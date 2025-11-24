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
        # Select the typo class 'depedent-selector'
        checkbox_input = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.depedent-selector"))
        )

        # The label is always the sibling label right after input
        label = checkbox_input.find_element(By.XPATH, "./following-sibling::label")

        driver.execute_script("arguments[0].scrollIntoView(true);", label)
        driver.execute_script("arguments[0].click();", label)

        print("Clicked dependent checkbox (typo class).")
        return True

    except Exception as e:
        print("Dependent checkbox present but not clickable:", e)
        return False


# -----------------------------------------
# CLICK THE CUSTOM-CONTROL-LABEL::before THING
# (the waiver / confirmation checkbox)
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
    import time
    from datetime import datetime, timedelta

    # Target time: today at 7:15:05 AM
    target_time = datetime.now().replace(hour=7, minute=15, second=3, microsecond=0)
    driver = connect_to_browser()
    print("Connected to existing Chrome session.")
    # If the time has already passed today, schedule for tomorrow
    if datetime.now() > target_time:
        target_time += timedelta(days=1)
    print(f"Current Time: {datetime.now()}")
    print(f"Waiting until {target_time} to start...")

    # Sleep until target time
    while datetime.now() < target_time:
        time.sleep(0.5)  # check twice per second
        print(datetime.now())
        driver.refresh()

    print("Time reached! Starting the bot...")

    # === Start your Selenium bot here ===
    # driver.refresh()
    # ... rest of your script


    while True:
        print("\nRefreshing page...")
        driver.refresh()
        time.sleep(3)

        # --- STEP 1: offering-select-1 ---
        if not safe_click_id(driver, "offering-select-1"):
            time.sleep(60)
            continue

        time.sleep(1)

        # --- STEP 2: registerBtn ---
        if not safe_click_id(driver, "registerBtn"):
            time.sleep(60)
            continue

        time.sleep(1)
        # --- DEBUG: show all custom-control elements ---
        print("\n--- DEBUG: Looking for the dependent checkbox ---")
        elements = driver.find_elements(By.CSS_SELECTOR, "input.custom-control-input")
        for e in elements:
            print("ID:", e.get_attribute("id"),
                "NAME:", e.get_attribute("name"),
                "CLASS:", e.get_attribute("class"))
        print("--- END DEBUG ---\n")


        # --- STEP 3: dependent checkbox ---
        if not click_dependent_checkbox(driver):
            time.sleep(60)
            continue

        time.sleep(1)

        # --- STEP 4: btnNext ---
        if not safe_click_id(driver, "btnNext"):
            time.sleep(60)
            continue

        time.sleep(2)

        # --- STEP 5: Custom label for waiver ---
        if not click_custom_control_label(driver):
            time.sleep(60)
            continue

        time.sleep(1)

        # --- STEP 6: Proceed to Checkout Button ---
        if not click_proceed_checkout(driver):
            time.sleep(60)
            continue

        time.sleep(2)

        # --- STEP 7: STOP right before final checkout ---
        try:
            checkout_button = driver.find_element(By.XPATH, '//*[@id="checkoutButton"]')
            print("\n🎉 SUCCESS! All steps completed up to checkoutButton.")
            print("Stopped here so you can verify manually.")
        except:
            print("Checkout button not found — waiting and retrying.")
            time.sleep(60)
        # --- FINAL STEP: CLICK CHECKOUT BUTTON ---
        print("\n--- DEBUG: Attempting checkout button ---")

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


        # --- FINAL STEP 2: CLICK EXISTING CARD MODAL BUTTON (IF IT APPEARS) ---
        print("\n--- DEBUG: Checking for existing card modal ---")
        time.sleep(0.5)
        try:
            card_link = driver.find_element(By.XPATH, "//a[contains(@id,'aChargeCardSM_') and contains(@class,'card-item-1-large')]")
            card_link.click()
            print("Existing card modal button clicked.")
        except Exception as e:
            print("error")

        print("Automation completed.")


if __name__ == "__main__":
    main()
