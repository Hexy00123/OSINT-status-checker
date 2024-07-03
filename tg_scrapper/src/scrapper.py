import base64
import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


API_URL = "http://backend:8000"
TELEGRAM_URL = "https://web.telegram.org/k/"
STATUS_LOCATION = (By.CSS_SELECTOR, "div.info span.i18n")

# Constants in seconds
STATUS_RENDERING_TIMEOUT = 5
STATUSES_PARSING_DELAY = 10


def scrapper_initialization():
    # Define driver
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # example
    driver = webdriver.Remote("http://chrome:4444/wd/hub", DesiredCapabilities.CHROME, options=options)
    wait = WebDriverWait(driver, STATUS_RENDERING_TIMEOUT)
    driver.get(f"https://web.telegram.org/k/")
    save_qr(driver)
    response = requests.get(f"{API_URL}/user")  
    if response.status_code == 200:
        users = response.json()
    else:
        raise RuntimeError(f'Failed to fetch users: {response.json()}')

    return driver, wait, users

def save_qr(driver):
    canvas = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas'))
    )

    canvas_base64 = driver.execute_script("""
        var canvas = arguments[0];
        return canvas.toDataURL('image/png').substring(22);  // Remove the data URL prefix
        """, canvas)

    canvas_png = base64.b64decode(canvas_base64)

    # Save the PNG data to a file
    with open('qr_image.png', 'wb') as f:
        f.write(canvas_png)

    print("QR saved successfully.")

def login_successful(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, "div.auth-image")
        return False
    except NoSuchElementException:
        return True


def get_user_status(driver, wait, username):
    driver.get(TELEGRAM_URL)
    driver.get(f"{TELEGRAM_URL}#@{username}")
    # time.sleep(1)
    status_element = wait.until(
        EC.visibility_of_element_located(STATUS_LOCATION))
    print(status_element)
    for i in range(5):
        try:
            status = WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located(STATUS_LOCATION)).text
            print(status)
            break
        except StaleElementReferenceException:
            print('exception')
            pass
    print('Full status', status)
    return "online" in status


def scrapper_run(driver, wait, users):
    if login_successful(driver) and users:
        users_data = []
        start_time = time.time()
        status_element = None
        for user in users:
            user_status = get_user_status(driver, wait, user['username'])
            if user_status is not None:
                user_data = {
                    'ts': str(datetime.now()),
                    'username': user['username'],
                    'is_online': user_status,
                }
                users_data.append(user_data)
                print(user_data)
            else:
                print('Unable to parse', user)
        if users_data:
            response = requests.post(
                f"{API_URL}/status/create-many", json=users_data)
            if response.status_code != 200:
                print(f"Failed to post user statuses", response)
        else:
            print('No users data')
        print(f"For {len(users_data)} it took {time.time() - start_time} seconds")
