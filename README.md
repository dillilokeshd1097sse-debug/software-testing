# Automated Software Testing & Defect Analysis Project: ATM System
### Target: NexBank ATM-X700 Core Terminal
### Test Automation Framework: Selenium WebDriver (Python 3.11)

---

## 1. Project Overview

This project provides an end-to-end, industry-grade software testing, defect identification, and automated verification implementation for an **Automated Teller Machine (ATM) System** (Model: **NexBank ATM-X700**).

The project includes:
1. **System Specifications (SRS):** Full formal specification defining functional, boundary, security, and hardware interface constraints (REQ-01 to REQ-08).
2. **Interactive ATM Web Application (`atm_app/index.html`):** Fully functional, responsive ATM terminal UI simulation with Card Reader, Screen, PIN Pad, Dispenser, and dual operating modes:
   - **Mode A (Production Build v1.0):** Contains intentional, realistic software defects violating specifications.
   - **Mode B (Hardened Patch v1.1):** Remediated build adhering strictly to all security and business rules.
3. **Software Defect Documentation (`docs/DEFECT_REPORT.md`):** Complete IEEE 829 / ISO/IEC/IEEE 29119-3 defect reports detailing root cause analyses (RCA), severity/priority ratings, reproduction steps, and remediation diffs.
4. **Requirements Traceability Matrix (`docs/TRACEABILITY_MATRIX.md`):** Cross-links specifications to test cases, defects, and fix verifications.
5. **Selenium Python Test Suite (`tests/`):**
   - Built on the **Page Object Model (POM)** architectural design pattern.
   - Headless Chrome browser automation verifying baseline specifications and reproducing/verifying all 8 defects.
6. **Master Automated Runner (`run_tests.py`):** Runs the test suites and generates execution summary reports.

---

## 2. Directory Structure

```
software-testing-1/
├── atm_app/
│   └── index.html                     # ATM web simulation UI & terminal logic
├── docs/
│   ├── SYSTEM_SPECIFICATIONS.md       # Complete SRS (Functional & Security Specs)
│   ├── DEFECT_REPORT.md               # IEEE 829 Compliant Defect Documentation
│   ├── TRACEABILITY_MATRIX.md         # Requirements Traceability Matrix (RTM)
│   └── TEST_EXECUTION_REPORT.md       # Generated automated test execution report
├── tests/
│   ├── __init__.py
│   ├── locators.py                    # Centralized DOM locators for UI elements
│   ├── driver_factory.py              # Headless Chrome WebDriver setup utility
│   ├── pages/
│   │   ├── __init__.py
│   │   └── atm_page.py                # Page Object Model (POM) encapsulation
│   ├── test_atm_system.py             # Specification verification test suite
│   └── test_defect_reproduction.py    # Defect reproduction & fix verification suite
├── run_tests.py                       # Unified test runner with report generation
└── README.md                          # Project documentation
```

---

## 3. Summary of Examined Specifications & Identified Defects

| Defect ID | Severity | Category | Specification Violated | Summary Description |
| :--- | :--- | :--- | :--- | :--- |
| **DEF-ATM-001** | **Critical** | Security / Brute-Force | `REQ-02.2` | PIN lockout allows 4 failed attempts instead of locking on 3rd attempt. |
| **DEF-ATM-002** | **Critical** | Financial Business Logic | `REQ-03.5` | System permits withdrawal below \$50.00 mandatory maintaining balance. |
| **DEF-ATM-003** | **Major** | Hardware Boundary Flaw | `REQ-03.1` | Dispenser accepts arbitrary non-stock amounts (\$37) instead of multiples of \$20/\$50. |
| **DEF-ATM-004** | **Major** | Input Validation Failure | `REQ-04.4` | Negative deposit amount (`-$100`) accepted and debits ledger balance. |
| **DEF-ATM-005** | **Major** | Business Logic | `REQ-05.1` | Fund transfer logic fails to prevent self-transfer to the source card. |
| **DEF-ATM-006** | **Moderate** | Security Policy | `REQ-06.3` | PIN change routine permits setting a New PIN identical to Old PIN. |
| **DEF-ATM-007** | **Critical** | Sensitive Data Leakage | `REQ-07.2` | Cleartext PIN exposed in client DOM `data-debug-pin` attribute. |
| **DEF-ATM-008** | **Major** | Limit Enforcement | `REQ-03.3` | Daily cumulative withdrawal limit (\$1,000) bypassed across multiple transactions. |

---

## 4. Test Automation Setup & Execution

### Prerequisites
* Python 3.8+ (Tested on Python 3.11.3)
* Google Chrome installed
* Selenium 4.x (`pip install selenium`)

### Running the Complete Test Suite
To execute all 16 automated tests (Specification verification + Defect reproduction):
```bash
python run_tests.py
```

### Running Specific Test Suites
* Run only Baseline Specification tests:
  ```bash
  python -m unittest tests/test_atm_system.py
  ```
* Run only Defect Reproduction & Fix Verification tests:
  ```bash
  python -m unittest tests/test_defect_reproduction.py
  ```

---

## 5. Manual UI Verification
To explore the ATM Terminal UI manually:
1. Open `atm_app/index.html` in any web browser (Chrome, Edge, Firefox).
2. Use the **Operational Mode** dropdown at the top to toggle between:
   - **Mode A: Production Build v1.0** (Inspect live defect manifestations in real time).
   - **Mode B: Hardened Patch v1.1** (Inspect compliant, secure behavior).
3. Test credentials:
   - Card: `4532109843218765` | PIN: `1234`
   - Card: `5412751234567890` | PIN: `4321`

