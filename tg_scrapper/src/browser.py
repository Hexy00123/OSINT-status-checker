from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime


# Constants in seconds
LOGIN_TIMEOUT = 60
STATUS_RENDERING_TIMEOUT = 5
STATUSES_PARSING_DELAY = 60

# Define driver
driver = webdriver.Chrome()

# Login


def login_successful():
    try:
        driver.find_element(By.CSS_SELECTOR, "div.page-chats")
        return True
    except:
        return False


driver.get(f"https://web.telegram.org/k/")
WebDriverWait(driver, LOGIN_TIMEOUT).until(lambda driver: login_successful())


def get_user_status(username):
    driver.get(f"https://web.telegram.org/k/#@{username}")
    status_element = WebDriverWait(driver, STATUS_RENDERING_TIMEOUT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.info span.i18n")))
    status = status_element.text
    print(status)
    return "online" in status or 'just now' in status


# Parsing loop
usernames = []
with open("user_statuses.txt", "a") as file:
    while True:
        for username in usernames:
            status = get_user_status(username)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} {username} {status}\n")
            print(f"{timestamp} {username} {status}")
        time.sleep(STATUSES_PARSING_DELAY)
