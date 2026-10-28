"""
Automated Selenium Python Specification Verification Test Suite
Target: NexBank ATM-X700 Core Terminal
Covers: Core Functional and Security Specifications (REQ-01 through REQ-08)
"""
import unittest
import time
from tests.driver_factory import create_driver, get_atm_app_url
from tests.pages.atm_page import ATMPage

class TestATMSystemSpecifications(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = create_driver(headless=True)
        cls.url = get_atm_app_url()

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def setUp(self):
        self.atm = ATMPage(self.driver, self.url)
        self.atm.open()
        # Ensure fresh state
        self.driver.refresh()
        time.sleep(0.3)

    def test_tc_spec_001_card_format_acceptance(self):
        """REQ-01.1: Verify valid 16-digit card transitions to PIN entry state"""
        self.atm.insert_card("4532109843218765")
        status = self.atm.get_session_status()
        self.assertEqual(status, "AUTHENTICATING", "Terminal must transition to AUTHENTICATING upon valid card insertion.")

    def test_tc_spec_002_invalid_card_rejection(self):
        """REQ-01.2: Verify non-numeric or non-16-digit card is rejected"""
        self.atm.insert_card("INVALID123")
        msg = self.atm.get_message_text()
        self.assertIn("Invalid Card", msg, "Error message must indicate invalid card format.")
        status = self.atm.get_session_status()
        self.assertEqual(status, "IDLE", "Session status must remain IDLE when card is invalid.")

    def test_tc_spec_003_valid_pin_authentication(self):
        """REQ-02.1: Verify valid 4-digit PIN authorizes user and opens Main Menu"""
        self.atm.insert_card("4532109843218765")
        self.atm.enter_pin("1234")
        self.assertTrue(self.atm.is_main_menu_visible(), "Main menu must be visible upon valid PIN entry.")
        self.assertEqual(self.atm.get_user_display_name(), "Alex Morgan")
        self.assertEqual(self.atm.get_session_status(), "AUTHORIZED")

    def test_tc_spec_004_single_withdrawal_limit_enforced(self):
        """REQ-03.2: Verify single withdrawal exceeding $500 is rejected"""
        self.atm.login("4532109843218765", "1234")
        self.atm.withdraw_cash(600)
        msg = self.atm.get_message_text()
        self.assertIn("exceeds single transaction limit", msg, "System must reject withdrawal exceeding $500.00.")

    def test_tc_spec_005_negative_withdrawal_rejected(self):
        """REQ-03.4: Verify negative withdrawal amount is rejected"""
        self.atm.login("4532109843218765", "1234")
        self.atm.withdraw_cash(-50)
        msg = self.atm.get_message_text()
        self.assertIn("Enter a valid positive", msg, "System must reject negative withdrawal amounts.")

    def test_tc_spec_006_max_deposit_limit(self):
        """REQ-04.1: Verify deposit exceeding $2,000 is rejected"""
        self.atm.login("4532109843218765", "1234")
        self.atm.deposit_cash(2500)
        msg = self.atm.get_message_text()
        self.assertIn("Maximum deposit per transaction is $2,000.00", msg)

    def test_tc_spec_007_pin_change_incorrect_old_pin(self):
        """REQ-06.1: Verify PIN change fails if current PIN is incorrect"""
        self.atm.login("4532109843218765", "1234")
        self.atm.change_pin("0000", "5678", "5678")
        msg = self.atm.get_message_text()
        self.assertIn("Current PIN is incorrect", msg)

    def test_tc_spec_008_balance_inquiry_and_receipt(self):
        """REQ-08.1: Verify balance inquiry returns correct balance and prints masked receipt"""
        self.atm.login("4532109843218765", "1234")
        balance = self.atm.get_current_balance()
        self.assertEqual(balance, 1000.00, "Initial available balance must be $1000.00.")
        self.atm.print_receipt()
        receipt_text = self.atm.get_receipt_text()
        self.assertIn("Masked Card: ****8765", receipt_text, "Receipt must mask account number.")


if __name__ == "__main__":
    unittest.main()
