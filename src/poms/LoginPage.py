import time

from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By

import SeleniumUtil
from pcap import Pcap
from poms.BasePage import BasePage


class LoginPage(BasePage):
    username_input = (By.ID, 'username')
    password_input = (By.ID, 'password')
    signIn_button = (By.ID, 'btnSubmit')
    user = (By.ID, 'aDropDown')

    def insert_user_name(self, user_name):
        user = SeleniumUtil.wait_for_element_presence(LoginPage.username_input)
        user.send_keys(user_name)

    def insert_password(self, password):
        pwd = SeleniumUtil.wait_for_element_presence(LoginPage.password_input)
        pwd.send_keys(password)

    def sign_in(self):
        submit = SeleniumUtil.wait_for_element_presence(LoginPage.signIn_button)
        submit.click()

        SeleniumUtil.wait_for_element_to_disapper(submit)
        SeleniumUtil.wait_for_element_presence(LoginPage.user)
        time.sleep(3)

        # BuiltIn().log_to_console(Pcap.QUEUE.get())
        return Pcap.QUEUE.get()

