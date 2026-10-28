"""
Page Object Model (POM) implementation for the NexBank ATM-X700 Application
"""
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tests.locators import ATMLocators

class ATMPage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 5)

    def open(self):
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located(ATMLocators.CARD_INPUT))
        return self

    def set_system_mode(self, mode="faulty"):
        """
        mode: 'faulty' or 'compliant'
        """
        select_elem = self.wait.until(EC.presence_of_element_located(ATMLocators.SYSTEM_MODE_DROPDOWN))
        select = Select(select_elem)
        select.select_by_value(mode)
        time.sleep(0.3)

    def insert_card(self, card_number):
        card_box = self.wait.until(EC.element_to_be_clickable(ATMLocators.CARD_INPUT))
        card_box.clear()
        card_box.send_keys(card_number)
        insert_btn = self.wait.until(EC.element_to_be_clickable(ATMLocators.INSERT_CARD_BTN))
        insert_btn.click()
        time.sleep(0.3)

    def enter_pin(self, pin):
        pin_box = self.wait.until(EC.visibility_of_element_located(ATMLocators.PIN_INPUT))
        pin_box.clear()
        pin_box.send_keys(pin)
        submit_btn = self.wait.until(EC.element_to_be_clickable(ATMLocators.SUBMIT_PIN_BTN))
        submit_btn.click()
        time.sleep(0.3)

    def login(self, card_number, pin):
        self.insert_card(card_number)
        self.enter_pin(pin)

    def get_session_status(self):
        elem = self.wait.until(EC.presence_of_element_located(ATMLocators.SESSION_STATUS))
        return elem.text.strip()

    def get_user_display_name(self):
        elem = self.wait.until(EC.presence_of_element_located(ATMLocators.USER_DISPLAY_NAME))
        return elem.text.strip()

    def get_failed_attempts(self):
        elem = self.wait.until(EC.presence_of_element_located(ATMLocators.FAILED_ATTEMPTS_COUNT))
        return int(elem.text.strip())

    def is_card_locked(self):
        try:
            elem = self.driver.find_element(*ATMLocators.VIEW_LOCKED)
            return "active" in elem.get_attribute("class")
        except:
            return False

    def is_main_menu_visible(self):
        try:
            elem = self.driver.find_element(*ATMLocators.VIEW_MAIN_MENU)
            return "active" in elem.get_attribute("class")
        except:
            return False

    def get_message_text(self):
        try:
            elem = self.driver.find_element(*ATMLocators.SCREEN_MESSAGE)
            if "show" in elem.get_attribute("class"):
                return elem.text.strip()
            return elem.text.strip()
        except:
            return ""

    def get_current_balance(self):
        # Navigate to balance screen
        balance_btn = self.wait.until(EC.element_to_be_clickable(ATMLocators.MENU_BALANCE))
        balance_btn.click()
        time.sleep(0.2)
        disp = self.wait.until(EC.visibility_of_element_located(ATMLocators.CURRENT_BALANCE_DISPLAY))
        text = disp.text.replace("$", "").replace(",", "").strip()
        return float(text)

    def return_to_main_menu(self):
        back_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Back to Menu')]")
        back_btn.click()
        time.sleep(0.2)

    def withdraw_cash(self, amount):
        withdraw_btn = self.wait.until(EC.element_to_be_clickable(ATMLocators.MENU_WITHDRAW))
        withdraw_btn.click()
        time.sleep(0.2)
        inp = self.wait.until(EC.visibility_of_element_located(ATMLocators.WITHDRAW_INPUT))
        inp.clear()
        inp.send_keys(str(amount))
        confirm_btn = self.wait.until(EC.element_to_be_clickable(ATMLocators.CONFIRM_WITHDRAW_BTN))
        confirm_btn.click()
        time.sleep(0.4)

    def deposit_cash(self, amount):
        deposit_btn = self.wait.until(EC.element_to_be_clickable(ATMLocators.MENU_DEPOSIT))
        deposit_btn.click()
        time.sleep(0.2)
        inp = self.wait.until(EC.visibility_of_element_located(ATMLocators.DEPOSIT_INPUT))
        inp.clear()
        inp.send_keys(str(amount))
        confirm_btn = self.wait.until(EC.element_to_be_clickable(ATMLocators.CONFIRM_DEPOSIT_BTN))
        confirm_btn.click()
        time.sleep(0.4)

    def transfer_funds(self, target_card, amount):
        transfer_btn = self.wait.until(EC.element_to_be_clickable(ATMLocators.MENU_TRANSFER))
        transfer_btn.click()
        time.sleep(0.2)
        target_inp = self.wait.until(EC.visibility_of_element_located(ATMLocators.TRANSFER_TARGET_INPUT))
        target_inp.clear()
        target_inp.send_keys(str(target_card))
        amt_inp = self.wait.until(EC.visibility_of_element_located(ATMLocators.TRANSFER_AMOUNT_INPUT))
        amt_inp.clear()
        amt_inp.send_keys(str(amount))
        confirm_btn = self.wait.until(EC.element_to_be_clickable(ATMLocators.CONFIRM_TRANSFER_BTN))
        confirm_btn.click()
        time.sleep(0.4)

    def change_pin(self, old_pin, new_pin, confirm_pin):
        pin_btn = self.wait.until(EC.element_to_be_clickable(ATMLocators.MENU_PIN_CHANGE))
        pin_btn.click()
        time.sleep(0.2)
        old_inp = self.wait.until(EC.visibility_of_element_located(ATMLocators.OLD_PIN_INPUT))
        old_inp.clear()
        old_inp.send_keys(str(old_pin))
        new_inp = self.wait.until(EC.visibility_of_element_located(ATMLocators.NEW_PIN_INPUT))
        new_inp.clear()
        new_inp.send_keys(str(new_pin))
        conf_inp = self.wait.until(EC.visibility_of_element_located(ATMLocators.CONFIRM_NEW_PIN_INPUT))
        conf_inp.clear()
        conf_inp.send_keys(str(confirm_pin))
        confirm_btn = self.wait.until(EC.element_to_be_clickable(ATMLocators.CONFIRM_PIN_CHANGE_BTN))
        confirm_btn.click()
        time.sleep(0.4)

    def get_dispenser_status(self):
        elem = self.wait.until(EC.presence_of_element_located(ATMLocators.CASH_DISPENSER_OUTPUT))
        return elem.text.strip()

    def get_pin_debug_attribute(self):
        """Used to check security defect DEF-07 (sensitive PIN exposure in DOM)"""
        pin_box = self.wait.until(EC.presence_of_element_located(ATMLocators.PIN_INPUT))
        return pin_box.get_attribute("data-debug-pin")

    def print_receipt(self):
        btn = self.wait.until(EC.element_to_be_clickable(ATMLocators.PRINT_RECEIPT_BTN))
        btn.click()
        time.sleep(0.3)

    def get_receipt_text(self):
        elem = self.wait.until(EC.presence_of_element_located(ATMLocators.RECEIPT_OUTPUT))
        return elem.text.strip()

