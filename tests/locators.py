"""
Centralized DOM Locators for NexBank ATM-X700 Web Terminal Application
"""
from selenium.webdriver.common.by import By

class ATMLocators:
    # Mode selector
    SYSTEM_MODE_DROPDOWN = (By.ID, "system-mode")
    MODE_BADGE = (By.ID, "mode-badge")
    SESSION_STATUS = (By.ID, "session-status")

    # Card insertion screen
    CARD_INPUT = (By.ID, "card-number-input")
    INSERT_CARD_BTN = (By.ID, "insert-card-btn")
    DEMO_CARD_1_BTN = (By.XPATH, "//button[contains(text(), 'Demo Card #1')]")
    DEMO_CARD_2_BTN = (By.XPATH, "//button[contains(text(), 'Demo Card #2')]")

    # PIN screen
    PIN_INPUT = (By.ID, "pin-input")
    SUBMIT_PIN_BTN = (By.ID, "submit-pin-btn")
    CANCEL_PIN_BTN = (By.ID, "cancel-pin-btn")
    FAILED_ATTEMPTS_COUNT = (By.ID, "failed-attempts-count")

    # Main Menu screen
    VIEW_MAIN_MENU = (By.ID, "view-main-menu")
    USER_DISPLAY_NAME = (By.ID, "user-display-name")
    MENU_BALANCE = (By.ID, "menu-balance")
    MENU_WITHDRAW = (By.ID, "menu-withdraw")
    MENU_DEPOSIT = (By.ID, "menu-deposit")
    MENU_TRANSFER = (By.ID, "menu-transfer")
    MENU_PIN_CHANGE = (By.ID, "menu-pin-change")
    MENU_MINI_STATEMENT = (By.ID, "menu-mini-statement")
    MENU_EXIT = (By.ID, "menu-exit")

    # Balance screen
    CURRENT_BALANCE_DISPLAY = (By.ID, "current-balance-display")
    PRINT_RECEIPT_BTN = (By.XPATH, "//button[contains(text(), 'Print Receipt')]")

    # Withdrawal screen
    WITHDRAW_INPUT = (By.ID, "withdraw-amount-input")
    CONFIRM_WITHDRAW_BTN = (By.ID, "confirm-withdraw-btn")
    QUICK_CASH_BTN_FORMAT = "//button[@class='quick-btn quick-cash-btn' and @data-amount='{amount}']"

    # Deposit screen
    DEPOSIT_INPUT = (By.ID, "deposit-amount-input")
    CONFIRM_DEPOSIT_BTN = (By.ID, "confirm-deposit-btn")

    # Transfer screen
    TRANSFER_TARGET_INPUT = (By.ID, "transfer-target-input")
    TRANSFER_AMOUNT_INPUT = (By.ID, "transfer-amount-input")
    CONFIRM_TRANSFER_BTN = (By.ID, "confirm-transfer-btn")

    # PIN Change screen
    OLD_PIN_INPUT = (By.ID, "old-pin-input")
    NEW_PIN_INPUT = (By.ID, "new-pin-input")
    CONFIRM_NEW_PIN_INPUT = (By.ID, "confirm-new-pin-input")
    CONFIRM_PIN_CHANGE_BTN = (By.ID, "confirm-change-pin-btn")

    # Mini Statement screen
    STATEMENT_ROWS = (By.CSS_SELECTOR, "#statement-rows tr")

    # Locked Screen
    VIEW_LOCKED = (By.ID, "view-locked")

    # Alerts & Messages
    SCREEN_MESSAGE = (By.ID, "screen-message")
    CASH_DISPENSER_OUTPUT = (By.ID, "cash-dispenser-output")
    RECEIPT_OUTPUT = (By.ID, "receipt-output")
    CARD_HW_STATUS = (By.ID, "card-hw-status")
    AUDIT_LOG_PANEL = (By.ID, "audit-log")

