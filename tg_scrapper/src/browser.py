import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.expected_conditions import staleness_of


def login_successful():
    try:
        driver.find_element(By.CSS_SELECTOR, "div.auth-image")
        return False
    except NoSuchElementException:
        return True


def get_user_status(username):
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
    # try:
    #     status_element = wait.until(
    #         EC.presence_of_element_located(STATUS_LOCATION))
    #     print(status_element)
    # except TimeoutException:
    #     return None
    # try:
    #     WebDriverWait(driver, 2).until(EC.staleness_of(status_element))
    # except TimeoutException:
    #     pass
    # else:
    #     status_element = wait.until(
    #         EC.presence_of_element_located(STATUS_LOCATION))
    #     # status_element = driver.find_element(*STATUS_LOCATION)
    print('Full status', status)
    return "online" in status  # or 'just now' in status


# Constants in seconds
STATUS_RENDERING_TIMEOUT = 5
STATUSES_PARSING_DELAY = 10

# Initialization
driver = webdriver.Chrome()
wait = WebDriverWait(driver, STATUS_RENDERING_TIMEOUT)

# Other constants
API_URL = "http://localhost:8000"
TELEGRAM_URL = "https://web.telegram.org/k/"
STATUS_LOCATION = (By.CSS_SELECTOR, "div.info span.i18n")

driver.get(TELEGRAM_URL)
response = requests.get(f"{API_URL}/user/")
if response.status_code == 200:
    users = response.json()
else:
    print('Failed to fetch users', response)
print(users)

while True:
    if login_successful() and users:
        users_data = []
        start_time = time.time()
        status_element = None
        for user in users:
            user_status = get_user_status(user['username'])
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
        time.sleep(STATUSES_PARSING_DELAY)
