import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import random
import re
import os

# --- SETTINGS ---
URL = "https://www.cabelas.com/l/used-guns#sortCriteria=%40offerprice%20ascending&f-cartridge_or_gauge=9mm%20Luger,9mm%20Parabellum,9mm&f-brand=Glock&nf-offerpricefilter=100...400"
TARGET_MODEL = "19" 
CHROME_PATH = "/usr/bin/chromium-browser"

def extract_number(text):
    if not text: return None
    match = re.search(r'\d+', text)
    return match.group() if match else None

def get_total_count(driver):
    """Scans the header for the total count (e.g., '20 Results')."""
    for _ in range(15):
        try:
            element = driver.find_element(By.ID, "ResultsQueryTitle")
            val = element.text.strip()
            num = extract_number(val)
            if num: return num
        except:
            pass
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(1)
    return None

def count_specific_models(driver, model_name):
    """Loops through the listings and counts how many match the target model."""
    found_count = 0
    try:
        results_list = driver.find_element(By.CLASS_NAME, "styles_ResultsList__ImdmV")
        items = results_list.find_elements(By.CSS_SELECTOR, "div[class*='styles_ResultItem__ySOf_']")
        
        for item in items:
            try:
                title = item.find_element(By.TAG_NAME, "h2").text
                if model_name.lower() in title.lower():
                    found_count += 1
            except:
                continue
        return found_count
    except:
        return 0

def play_alert():
    """Triggers the Ubuntu alert sound 3 times."""
    for _ in range(3):
        os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga')
        time.sleep(0.4)

def run_monitor():
    options = uc.ChromeOptions()
    options.binary_location = CHROME_PATH
    options.add_argument("--no-sandbox")

    try:
        print("Starting Stealth Monitor...")
        # version_main matches your local Chromium 146
        driver = uc.Chrome(options=options, version_main=146)
        driver.get(URL)
        
        last_total = get_total_count(driver)
        if not last_total:
            print("\n[!] Data not loading. Solve captcha if visible...")
            input("Press Enter once guns appear in browser...")
            last_total = get_total_count(driver)

        print(f"\n" + "="*45)
        print(f" MONITORING ACTIVE")
        print(f" Initial Total Items: {last_total}")
        print(f" Tracking Model: Glock {TARGET_MODEL}")
        print("="*45 + "\n")

        while True:
            # Wait between 25 and 45 seconds
            time.sleep(random.uniform(25, 45))
            
            driver.refresh()
            
            current_total = get_total_count(driver)
            specific_num = count_specific_models(driver, TARGET_MODEL)
            timestamp = time.strftime('%H:%M:%S')
            
            if current_total:                
                # 1. ONLY BEEP IF THE TOTAL CHANGES
                if current_total != last_total:
                    print(f" !!! INVENTORY CHANGE DETECTED: {last_total} -> {current_total} !!!")
                    play_alert()
                    last_total = current_total

                # 2. ALWAYS PRINT THE COUNTS
                print(f"[{timestamp}] Total: {current_total} | Glock {TARGET_MODEL}s: {specific_num}")
            else:
                print(f"[{timestamp}] Waiting for data/captcha...")

    except Exception as e:
        print(f"Monitor Stopped: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_monitor()