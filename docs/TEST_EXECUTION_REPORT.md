# Automated Test Execution Report
## NexBank ATM-X700 Core Terminal Testing
**Executed At:** 2026-10-28 09:57:23  
**Execution Engine:** Python 3.11 unittest + Selenium WebDriver (Headless Chrome)  
**Total Duration:** 67.95 seconds  

---

### Executive Metric Summary

| Metric | Count | Percentage |
| :--- | :--- | :--- |
| **Total Test Cases** | 16 | 100.0% |
| **Passed (Verified)** | 16 | 100.0% |
| **Failed** | 0 | 0.0% |
| **Errors** | 0 | 0.0% |

---

### Executed Test Breakdown

| Suite | Test Case Identifier | Requirement / Target Defect | Status |
| :--- | :--- | :--- | :--- |
| **Specs** | `test_tc_spec_001_card_format_acceptance` | REQ-01.1 (16-Digit Card Format Acceptance) | `PASS` |
| **Specs** | `test_tc_spec_002_invalid_card_rejection` | REQ-01.2 (Invalid Card Format Rejection) | `PASS` |
| **Specs** | `test_tc_spec_003_valid_pin_authentication` | REQ-02.1 (4-Digit PIN Authentication) | `PASS` |
| **Specs** | `test_tc_spec_004_single_withdrawal_limit_enforced` | REQ-03.2 (Single Withdrawal Limit $500) | `PASS` |
| **Specs** | `test_tc_spec_005_negative_withdrawal_rejected` | REQ-03.4 (Negative Withdrawal Rejection) | `PASS` |
| **Specs** | `test_tc_spec_006_max_deposit_limit` | REQ-04.1 (Max Deposit Limit $2,000) | `PASS` |
| **Specs** | `test_tc_spec_007_pin_change_incorrect_old_pin` | REQ-06.1 (PIN Change Requires Current PIN) | `PASS` |
| **Specs** | `test_tc_spec_008_balance_inquiry_and_receipt` | REQ-08.1 (Balance Inquiry & Masked Receipt) | `PASS` |
| **Defects** | `test_def01_pin_lockout_defect_reproduction` | DEF-ATM-001 (PIN Lockout Threshold Off-by-One) | `PASS (Repro + Fix)` |
| **Defects** | `test_def02_minimum_maintaining_balance_defect` | DEF-ATM-002 (Minimum Maintaining Balance $50) | `PASS (Repro + Fix)` |
| **Defects** | `test_def03_non_standard_denomination_defect` | DEF-ATM-003 (Withdrawal Denomination Check) | `PASS (Repro + Fix)` |
| **Defects** | `test_def04_negative_deposit_defect` | DEF-ATM-004 (Negative Deposit Validation) | `PASS (Repro + Fix)` |
| **Defects** | `test_def05_self_transfer_defect` | DEF-ATM-005 (Prohibit Self-Transfer) | `PASS (Repro + Fix)` |
| **Defects** | `test_def06_identical_pin_change_defect` | DEF-ATM-006 (Prohibit Identical PIN Change) | `PASS (Repro + Fix)` |
| **Defects** | `test_def07_dom_pin_exposure_defect` | DEF-ATM-007 (Sensitive PIN Leak in DOM) | `PASS (Repro + Fix)` |
| **Defects** | `test_def08_daily_limit_bypass_defect` | DEF-ATM-008 (Daily Withdrawal Limit Bypass) | `PASS (Repro + Fix)` |

---

### Conclusion & Audit Sign-Off
All 16 automated tests completed successfully. The test harness has conclusively confirmed:
1. Baseline adherence to standard ATM operations (Card reading, authorization, receipts).
2. Exact defect reproduction for all eight (8) documented defects in Production Build v1.0.
3. Successful remediation and compliance verification in Hardened Patch v1.1.
