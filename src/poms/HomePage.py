from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import SeleniumUtil
from poms.BasePage import BasePage


class HomePage(BasePage):

    login_link = (By.CSS_SELECTOR, "a[href*='Login']")


    def login_as_user(self):
        login_elem = SeleniumUtil.wait_for_element_presence(HomePage.login_link)
        login_elem.click()
        SeleniumUtil.wait_for_element_to_disapper(login_elem)