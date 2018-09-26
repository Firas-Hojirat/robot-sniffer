import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

_options = Options()
_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=_options)
_waiter = WebDriverWait(driver, 10)

def open_browser(url):
    driver.get(url)
    driver.maximize_window()


def close_browser():
    driver.quit()


def wait_for_element_presence(locator):
    return _waiter.until(expected_conditions.presence_of_element_located(locator))

def wait_for_element_to_disapper(elem):
    _waiter.until(expected_conditions.invisibility_of_element(elem))
