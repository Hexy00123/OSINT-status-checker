import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


API_URL = "https://api.example.com/"

# Constants in seconds
LOGIN_TIMEOUT = 60
STATUS_RENDERING_TIMEOUT = 5
STATUSES_PARSING_DELAY = 60

# Define driver
driver = webdriver.Chrome()


def login_successful():
    try:
        driver.find_element(By.CSS_SELECTOR, "div.auth-image")
        return False
    except NoSuchElementException:
        return True


driver.get(f"https://web.telegram.org/k/")


def get_user_status(username):
    driver.get(f"https://web.telegram.org/k/#@{username}")
    status_element = WebDriverWait(driver, STATUS_RENDERING_TIMEOUT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.info span.i18n")))
    status = status_element.text
    print(status)
    return "online" in status or 'just now' in status


response = requests.get(f"{API_URL}/users")
if response.status_code == 200:
    users = response.json()
else:
    print('Failed to fetch users', response)
print(users)

while True:
    if login_successful() and users:
        users_data = []
        for user in users:
            user_data = {
                'ts': str(datetime.now()),
                'user': {
                    'id': user.id,
                    'collection': 'User',
                },
                'is_online': get_user_status(user.username),
            }
            users_data.append(user_data)
            print(user_data)

        response = requests.post(f"{API_URL}/statuses", json=users_data)
        if response.status_code != 200:
            print(f"Failed to post user statuses", response)

        time.sleep(STATUSES_PARSING_DELAY)
