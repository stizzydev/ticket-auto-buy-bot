from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import config
from captcha_solver import solve_recaptcha

def init_driver():
    chrome_options = Options()
    if config.HEADLESS:
        chrome_options.add_argument("--headless")
    import random

def get_random_proxy():
    try:
        with open("proxy_list.txt", "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        return random.choice(proxies)
    except:
        return config.PROXY

if config.USE_PROXY:
    proxy = get_random_proxy()
    print(f"[+] Using Proxy: {proxy}")
    chrome_options.add_argument(f'--proxy-server={proxy}')
        chrome_options.add_argument(f'--proxy-server={config.PROXY}')
    return webdriver.Chrome(options=chrome_options)

def run_bot():
    driver = init_driver()
    driver.get(config.TICKET_URL)
    time.sleep(3)

    try:
        iframe = driver.find_element(By.XPATH, '//iframe[contains(@src, "recaptcha")]')
        driver.switch_to.frame(iframe)
        site_key = driver.find_element(By.CLASS_NAME, "g-recaptcha").get_attribute("data-sitekey")
        driver.switch_to.default_content()

        token = solve_recaptcha(site_key, config.TICKET_URL, config.CAPTCHA_API_KEY)

        driver.execute_script(
            f'document.getElementById("g-recaptcha-response").innerHTML="{token}";'
        )
        print("[+] CAPTCHA solved and injected")
        time.sleep(2)
    except Exception as e:
        print("[-] No CAPTCHA or error:", e)

    try:
        buy_button = driver.find_element(By.XPATH, '//button[contains(text(), "Find Tickets")]')
        buy_button.click()
        print("[+] Clicked Buy button")
    except:
        print("[-] Could not click Buy button")

    time.sleep(10)
    driver.quit()
