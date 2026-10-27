import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5000/"

@pytest.fixture
def setup_teardown():
    options = webdriver.ChromeOptions()
    # Uncomment the next two lines if running Chrome in a headless environment:
    # options.add_argument("--headless=new")
    # options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield driver
    driver.quit()

def read_alert(driver):
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    message = alert.text
    alert.accept()
    return message

def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()
    assert read_alert(driver) == "Username cannot be empty."

def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "username").send_keys("John Doe")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()
    assert read_alert(driver) == "Password cannot be empty."

def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "username").send_keys("Jane")
    driver.find_element(By.NAME, "pwd").send_keys("abc1")
    driver.find_element(By.NAME, "sb").click()
    assert read_alert(driver) == "Password must be at least 6 characters long."

def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "username").send_keys("Alice")
    driver.find_element(By.NAME, "pwd").send_keys("abc123")
    driver.find_element(By.NAME, "sb").click()
    WebDriverWait(driver, 5).until(EC.url_contains("/submit"))
    assert "Hello, Alice! Welcome to the website" in driver.find_element(
        By.TAG_NAME, "body"
    ).text
