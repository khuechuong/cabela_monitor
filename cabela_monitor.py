import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import random
import re
import os # Necessary for the sound command

options = uc.ChromeOptions()
options.binary_location = "/usr/bin/chromium-browser"
options.add_argument("--no-sandbox")

def extract_number(text):
    if not text: return None
    match = re.search(r'\d+', text)
    return match.group() if match else None

def get_count_robust(driver):
    # Try 30 times (30 seconds total) to get a non-empty number
    for _ in range(30):
        try:
            element = driver.find_element(By.ID, "ResultsQueryTitle")
            val = element.text.strip()
            num = extract_number(val)
            if num:
                return num
        except:
            pass
        
        # Scroll a little bit to "wake up" the dynamic loading
        driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(1)
    return None

try:
    print("Starting stealth browser...")
    driver = uc.Chrome(options=options, version_main=146)
    
    url = "https://www.cabelas.com/l/used-guns#sortCriteria=%40offerprice%20ascending&f-cartridge_or_gauge=9mm%20Luger,9mm%20Parabellum,9mm&f-brand=Glock&nf-offerpricefilter=100...400"
    
    print("Navigating to Cabela's...")
    driver.get(url)
    
    # Get the initial count
    last_num = get_count_robust(driver)
    
    if last_num:
        print(f"\n[SUCCESS] Monitoring started. Current results: {last_num}")
    else:
        print("\n[!] Could not see results. Check the browser window for a captcha!")
        # If it's stuck, it's usually a captcha. Wait for the user.
        input("Solve any captcha in the browser, then press Enter here...")
        last_num = get_count_robust(driver)

    while True:
        # Wait 15-25 seconds
        time.sleep(random.uniform(15, 25))
        
        driver.refresh()
        print(f"[{time.strftime('%H:%M:%S')}] Refreshing...")
        
        current_num = get_count_robust(driver)
        timestamp = time.strftime('%H:%M:%S')
        
        if current_num:
            if current_num != last_num:
                print(f"[{timestamp}] !!! ALERT: Count changed from {last_num} to {current_num} !!!")
                print('\a') # Beep
                last_num = current_num
            else:
                print(f"[{timestamp}] Results: {current_num}")
                # --- NOISE MAKER START ---
                # This plays the Ubuntu "Task Complete" sound 3 times
                for _ in range(3):
                    os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga')
                    time.sleep(0.5)
                # --- NOISE MAKER END ---
        else:
            print(f"[{timestamp}] Search timed out. Site might be blocking or loading slowly.")

except Exception as e:
    print(f"Error: {e}")
finally:
    input("Press Enter to close...")
    driver.quit()