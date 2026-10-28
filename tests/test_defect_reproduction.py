"""
Automated Selenium Python Defect Reproduction & Remediation Verification Suite
Target: NexBank ATM-X700 Core Terminal
Defects: DEF-ATM-001 through DEF-ATM-008
"""
import unittest
import time
from tests.driver_factory import create_driver, get_atm_app_url
from tests.pages.atm_page import ATMPage

class TestATMDefectReproduction(unittest.TestCase):
    
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
        self.driver.refresh()
        time.sleep(0.3)

    # -------------------------------------------------------------
    # DEF-ATM-001: PIN Lockout Threshold Off-by-One Error
    # -------------------------------------------------------------
    def test_def01_pin_lockout_defect_reproduction(self):
        """
        DEF-ATM-001 Reproduction:
        In Production Build v1.0, 3 consecutive failed PIN attempts fail to lock the card.
        The card remains unblocked until the 4th attempt, violating REQ-02.2.
        """
        self.atm.set_system_mode("faulty")
        self.atm.insert_card("4532109843218765")
        
        # 1st failure
        self.atm.enter_pin("9999")
        self.assertEqual(self.atm.get_failed_attempts(), 1)
        self.assertFalse(self.atm.is_card_locked())

        # 2nd failure
        self.atm.enter_pin("8888")
        self.assertEqual(self.atm.get_failed_attempts(), 2)
        self.assertFalse(self.atm.is_card_locked())

        # 3rd failure (Defect Manifestation: Should lock here per REQ-02.2, but does NOT)
        self.atm.enter_pin("7777")
        self.assertEqual(self.atm.get_failed_attempts(), 3)
        defect_present = not self.atm.is_card_locked()
        self.assertTrue(
            defect_present,
            "DEFECT REPRODUCED: Card failed to lock on 3rd attempt in faulty build."
        )

        # In Compliant Mode: Card must lock immediately on 3rd attempt
        self.driver.refresh()
        self.atm.set_system_mode("compliant")
        self.atm.insert_card("4532109843218765")
        self.atm.enter_pin("9999")
        self.atm.enter_pin("8888")
        self.atm.enter_pin("7777")
        self.assertTrue(
            self.atm.is_card_locked(),
            "VERIFIED FIX: In compliant mode, card locks immediately on 3rd attempt."
        )

    # -------------------------------------------------------------
    # DEF-ATM-002: Minimum Maintaining Balance Violation
    # -------------------------------------------------------------
    def test_def02_minimum_maintaining_balance_defect(self):
        """
        DEF-ATM-002 Reproduction:
        In Production Build v1.0, customer can withdraw balance down to $20,
        violating the mandatory $50.00 minimum maintaining balance (REQ-03.5).
        """
        # Step 1: Reproduce Defect in Faulty Mode
        self.atm.set_system_mode("faulty")
        self.atm.login("4532109843218765", "1234")
        
        # Withdraw $500 (Balance becomes $500)
        self.atm.withdraw_cash(500)
        time.sleep(1.5)

        # Attempt to withdraw $480 (Leaving $20.00 - should be BLOCKED by REQ-03.5)
        self.atm.withdraw_cash(480)
        msg = self.atm.get_message_text()
        
        # In faulty mode, withdrawal succeeds, violating specification!
        self.assertIn("Please collect your cash", msg, "DEFECT REPRODUCED: Withdrawal breached $50 min balance.")

        # Step 2: Verify Compliant Mode enforces $50 minimum balance
        self.driver.refresh()
        self.atm.set_system_mode("compliant")
        self.atm.login("4532109843218765", "1234")
        self.atm.withdraw_cash(500)
        time.sleep(1.5)
        self.atm.withdraw_cash(480)
        compliant_msg = self.atm.get_message_text()
        self.assertIn("Balance cannot drop below required $50.00", compliant_msg, "VERIFIED FIX: Min balance enforced.")

    # -------------------------------------------------------------
    # DEF-ATM-003: Withdrawal Accepts Non-Standard Denomination
    # -------------------------------------------------------------
    def test_def03_non_standard_denomination_defect(self):
        """
        DEF-ATM-003 Reproduction:
        In Production Build v1.0, entering $37 is accepted even though dispenser only
        carries $20 and $50 notes (violating REQ-03.1).
        """
        self.atm.set_system_mode("faulty")
        self.atm.login("4532109843218765", "1234")
        self.atm.withdraw_cash(37)
        dispenser = self.atm.get_dispenser_status()
        self.assertIn("Dispensed: $37.00", dispenser, "DEFECT REPRODUCED: ATM dispensed non-stock denomination $37.")

        # In Compliant Mode:
        self.driver.refresh()
        self.atm.set_system_mode("compliant")
        self.atm.login("4532109843218765", "1234")
        self.atm.withdraw_cash(37)
        msg = self.atm.get_message_text()
        self.assertIn("Denomination invalid", msg, "VERIFIED FIX: Non-standard denomination rejected.")

    # -------------------------------------------------------------
    # DEF-ATM-004: Negative Deposit Accepted
    # -------------------------------------------------------------
    def test_def04_negative_deposit_defect(self):
        """
        DEF-ATM-004 Reproduction:
        In Production Build v1.0, depositing -$100 is accepted, debiting customer ledger (violating REQ-04.4).
        """
        self.atm.set_system_mode("faulty")
        self.atm.login("4532109843218765", "1234")
        self.atm.deposit_cash(-100)
        msg = self.atm.get_message_text()
        self.assertIn("Deposit of $-100.00 confirmed", msg, "DEFECT REPRODUCED: Negative deposit processed.")

        # In Compliant Mode:
        self.driver.refresh()
        self.atm.set_system_mode("compliant")
        self.atm.login("4532109843218765", "1234")
        self.atm.deposit_cash(-100)
        compliant_msg = self.atm.get_message_text()
        self.assertIn("Invalid deposit amount", compliant_msg, "VERIFIED FIX: Negative deposit rejected.")

    # -------------------------------------------------------------
    # DEF-ATM-005: Destination Account Validation Fails to Reject Self-Transfer
    # -------------------------------------------------------------
    def test_def05_self_transfer_defect(self):
        """
        DEF-ATM-005 Reproduction:
        In Production Build v1.0, transfer destination identical to source card is accepted (violating REQ-05.1).
        """
        self.atm.set_system_mode("faulty")
        self.atm.login("4532109843218765", "1234")
        self.atm.transfer_funds("4532109843218765", 100)
        msg = self.atm.get_message_text()
        self.assertIn("Transferred $100.00 to ****8765", msg, "DEFECT REPRODUCED: Self-transfer accepted.")

        # In Compliant Mode:
        self.driver.refresh()
        self.atm.set_system_mode("compliant")
        self.atm.login("4532109843218765", "1234")
        self.atm.transfer_funds("4532109843218765", 100)
        compliant_msg = self.atm.get_message_text()
        self.assertIn("Destination card cannot be identical", compliant_msg, "VERIFIED FIX: Self-transfer blocked.")

    # -------------------------------------------------------------
    # DEF-ATM-006: PIN Change Allows Identical PIN
    # -------------------------------------------------------------
    def test_def06_identical_pin_change_defect(self):
        """
        DEF-ATM-006 Reproduction:
        In Production Build v1.0, user can change PIN to existing PIN '1234' (violating REQ-06.3).
        """
        self.atm.set_system_mode("faulty")
        self.atm.login("4532109843218765", "1234")
        self.atm.change_pin("1234", "1234", "1234")
        msg = self.atm.get_message_text()
        self.assertIn("Security PIN successfully updated", msg, "DEFECT REPRODUCED: Identical PIN change accepted.")

        # In Compliant Mode:
        self.driver.refresh()
        self.atm.set_system_mode("compliant")
        self.atm.login("4532109843218765", "1234")
        self.atm.change_pin("1234", "1234", "1234")
        compliant_msg = self.atm.get_message_text()
        self.assertIn("New PIN cannot be the same as your current PIN", compliant_msg, "VERIFIED FIX: Identical PIN rejected.")

    # -------------------------------------------------------------
    # DEF-ATM-007: Sensitive PIN Exposure in DOM
    # -------------------------------------------------------------
    def test_def07_dom_pin_exposure_defect(self):
        """
        DEF-ATM-007 Reproduction:
        In Production Build v1.0, client DOM exposes customer PIN in data-debug-pin attribute (violating REQ-07.2).
        """
        self.atm.set_system_mode("faulty")
        self.atm.insert_card("4532109843218765")
        leaked_pin = self.atm.get_pin_debug_attribute()
        self.assertEqual(leaked_pin, "1234", "DEFECT REPRODUCED: Cleartext PIN exposed in DOM data-attribute.")

        # In Compliant Mode:
        self.driver.refresh()
        self.atm.set_system_mode("compliant")
        self.atm.insert_card("4532109843218765")
        sanitized_attr = self.atm.get_pin_debug_attribute()
        self.assertIsNone(sanitized_attr, "VERIFIED FIX: Sensitive data-attribute eliminated from DOM.")

    # -------------------------------------------------------------
    # DEF-ATM-008: Cumulative Daily Withdrawal Limit Bypass
    # -------------------------------------------------------------
    def test_def08_daily_limit_bypass_defect(self):
        """
        DEF-ATM-008 Reproduction:
        In Production Build v1.0, withdrawing $500, then $500, then $200 succeeds,
        bypassing the $1,000 daily limit (violating REQ-03.3).
        """
        # --- Part 1: Faulty Mode Reproduction ---
        self.atm.set_system_mode("faulty")
        self.atm.login("4532109843218765", "1234")
        
        # Boost balance by depositing $1000 so balance is $2000 (enough for $1200 withdrawals)
        self.atm.deposit_cash(1000)
        time.sleep(1.5)

        # 1st $500 withdrawal (Cumulative: $500, Remaining: $1500)
        self.atm.withdraw_cash(500)
        time.sleep(1.5)

        # 2nd $500 withdrawal (Cumulative: $1,000 [Daily Limit Reached!], Remaining: $1000)
        self.atm.withdraw_cash(500)
        time.sleep(1.5)

        # 3rd withdrawal of $200 (Total attempted today: $1,200)
        # In faulty mode, daily limit is NOT checked, so it succeeds:
        self.atm.withdraw_cash(200)
        msg = self.atm.get_message_text()
        self.assertIn("Please collect your cash", msg, "DEFECT REPRODUCED: Cumulative daily limit bypassed.")

        # --- Part 2: Compliant Mode Fix Verification ---
        self.driver.refresh()
        self.atm.set_system_mode("compliant")
        self.atm.login("4532109843218765", "1234")
        
        # Deposit $1000 so balance is $2000
        self.atm.deposit_cash(1000)
        time.sleep(1.5)

        # 1st $500 withdrawal
        self.atm.withdraw_cash(500)
        time.sleep(1.5)

        # 2nd $500 withdrawal (Reaches $1000 daily limit)
        self.atm.withdraw_cash(500)
        time.sleep(1.5)

        # 3rd withdrawal of $200 - Must be BLOCKED by REQ-03.3
        self.atm.withdraw_cash(200)
        compliant_msg = self.atm.get_message_text()
        self.assertIn("Daily limit exceeded", compliant_msg, "VERIFIED FIX: Daily cumulative limit enforced.")


if __name__ == "__main__":
    unittest.main()
