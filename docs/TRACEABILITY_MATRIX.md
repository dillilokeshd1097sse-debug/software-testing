# Requirements Traceability Matrix (RTM)
## NexBank ATM-X700 Core System Terminal

The Requirements Traceability Matrix (RTM) maps each System Specification requirement to its automated Selenium test case, the observed defect ID (if defective in Build v1.0), and the verification status in the hardened build.

| Requirement ID | Specification Summary | Selenium Test Case ID | Test Method Name | Associated Defect ID | Status in Build v1.0 | Status in Hardened v1.1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-01.1** | 16-Digit Card Format Acceptance | `TC_SPEC_001` | `test_card_format_acceptance` | None | PASS | PASS |
| **REQ-01.2** | Invalid Card Format Rejection | `TC_SPEC_002` | `test_invalid_card_rejection` | None | PASS | PASS |
| **REQ-02.1** | 4-Digit PIN Authentication | `TC_SPEC_003` | `test_valid_pin_authentication` | None | PASS | PASS |
| **REQ-02.2** | 3 Consecutive PIN Failures Locks Card | `TC_DEF_001` | `test_reproduce_def01_pin_lockout_off_by_one` | **DEF-ATM-001** | **FAIL (Defect)** | PASS |
| **REQ-03.1** | Allowed Denominations (\$20 / \$50) | `TC_DEF_003` | `test_reproduce_def03_denomination_check` | **DEF-ATM-003** | **FAIL (Defect)** | PASS |
| **REQ-03.2** | Single Withdrawal Limit (\$500) | `TC_SPEC_004` | `test_single_withdrawal_limit_enforced` | None | PASS | PASS |
| **REQ-03.3** | Cumulative Daily Limit (\$1,000) | `TC_DEF_008` | `test_reproduce_def08_daily_limit_bypass` | **DEF-ATM-008** | **FAIL (Defect)** | PASS |
| **REQ-03.4** | Positive Amount Withdrawal Validation | `TC_SPEC_005` | `test_negative_withdrawal_rejected` | None | PASS | PASS |
| **REQ-03.5** | Minimum Balance Retention (\$50.00) | `TC_DEF_002` | `test_reproduce_def02_minimum_balance_violation` | **DEF-ATM-002** | **FAIL (Defect)** | PASS |
| **REQ-04.1** | Max Single Deposit Limit (\$2,000) | `TC_SPEC_006` | `test_max_deposit_limit` | None | PASS | PASS |
| **REQ-04.4** | Strict Positive Deposit Validation | `TC_DEF_004` | `test_reproduce_def04_negative_deposit_accepted` | **DEF-ATM-004** | **FAIL (Defect)** | PASS |
| **REQ-05.1** | Prohibit Self-Account Transfer | `TC_DEF_005` | `test_reproduce_def05_self_transfer_allowed` | **DEF-ATM-005** | **FAIL (Defect)** | PASS |
| **REQ-06.1** | Require Correct Current PIN for Change | `TC_SPEC_007` | `test_pin_change_incorrect_old_pin` | None | PASS | PASS |
| **REQ-06.3** | New PIN Cannot Match Current PIN | `TC_DEF_006` | `test_reproduce_def06_identical_pin_change` | **DEF-ATM-006** | **FAIL (Defect)** | PASS |
| **REQ-07.2** | Sensitive Data Clearance in DOM Tree | `TC_DEF_007` | `test_reproduce_def07_cleartext_pin_leak_in_dom` | **DEF-ATM-007** | **FAIL (Defect)** | PASS |
| **REQ-08.1** | Account Masking on Receipts & Logs | `TC_SPEC_008` | `test_receipt_masking` | None | PASS | PASS |

