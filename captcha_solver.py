import time
import requests

def solve_recaptcha(site_key, url, api_key):
    req_url = "http://2captcha.com/in.php"
    params = {
        "key": api_key,
        "method": "userrecaptcha",
        "googlekey": site_key,
        "pageurl": url,
        "json": 1
    }
    res = requests.post(req_url, data=params).json()
    if res["status"] != 1:
        raise Exception("Captcha submission failed")

    request_id = res["request"]
    fetch_url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1"

    for _ in range(20):
        time.sleep(5)
        result = requests.get(fetch_url).json()
        if result["status"] == 1:
            return result["request"]
    raise Exception("Captcha solving timed out")
