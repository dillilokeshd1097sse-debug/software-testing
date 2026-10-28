# Software Defect Documentation & Bug Report
## NexBank ATM-X700 Core Terminal System
**Standard:** IEEE 829 / ISO/IEC/IEEE 29119-3 Standard for Software Defect Reporting  
**Audit Target:** Production Build v1.0 vs System Specification v2.4.0  
**Test Automation Framework:** Selenium WebDriver with Python 3.11  

---

## 1. Executive Summary & Defect Overview

During a comprehensive specification-based audit and automated Selenium test run of the NexBank ATM-X700 Core Terminal System, **eight (8) critical to medium severity software defects** were identified. These defects span security vulnerabilities, business logic errors, input validation bypasses, and boundary constraint violations.

### Defect Severity & Priority Matrix

| Defect ID | Summary Title | Module / Area | Severity | Priority | Defect Type | Spec Ref |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEF-ATM-001** | PIN Lockout Threshold Off-by-One (Locks on 4th Attempt Instead of 3rd) | Authentication / Security | **Critical** | **P1 (High)** | Security / Logic | REQ-02.2 |
| **DEF-ATM-002** | Violation of Mandatory Minimum Maintaining Balance Constraint (\$50.00) | Cash Withdrawal | **Critical** | **P1 (High)** | Financial Logic | REQ-03.5 |
| **DEF-ATM-003** | Cash Withdrawal Accepts Non-Standard Banknote Denominations | Dispenser / Withdrawal | **Major** | **P2 (Med)** | Boundary / Format | REQ-03.1 |
| **DEF-ATM-004** | Negative Deposit Amount Accepted Resulting in Ledger Deduction | Cash Deposit | **Major** | **P1 (High)** | Input Validation | REQ-04.4 |
| **DEF-ATM-005** | Destination Account Validation Fails to Reject Self-Transfer | Fund Transfer | **Major** | **P2 (Med)** | Business Logic | REQ-05.1 |
| **DEF-ATM-006** | PIN Change Routine Permits Setting Identical Existing PIN | Credential Management | **Moderate** | **P3 (Low)** | Security Policy | REQ-06.3 |
| **DEF-ATM-007** | Sensitive Cleartext PIN Exposed in DOM `data-debug-pin` Attribute | Client / UI Security | **Critical** | **P1 (High)** | Sensitive Data Leak | REQ-07.2 |
| **DEF-ATM-008** | Cumulative Daily Withdrawal Limit Bypass Across Multiple Transactions | Cash Withdrawal | **Major** | **P1 (High)** | Limit Enforcement | REQ-03.3 |

---

## 2. Detailed Software Defect Reports

---

### Defect ID: DEF-ATM-001
* **Title:** Consecutive PIN Lockout Threshold Off-by-One Error (Locks on 4th Attempt Instead of 3rd)
* **Component:** `view-pin-entry` / Authentication Engine (`handlePinSubmit`)
* **Severity:** **Critical** (S1)
* **Priority:** **P1 - High**
* **Defect Classification:** Security Vulnerability / Brute-Force Protection Failure
* **SRS Requirement Ref:** `REQ-02.2` (Maximum 3 consecutive invalid attempts before hard lockout)

#### Preconditions
1. NexBank ATM application is running in default production build (Mode A).
2. Card number `4532109843218765` is inserted into the terminal.

#### Test Data
* Card: `4532109843218765`
* True PIN: `1234`
* Erroneous PINs: `9999`, `8888`, `7777`, `6666`

#### Steps to Reproduce
1. Navigate to ATM application: insert card `4532109843218765`.
2. Enter invalid PIN `9999` and submit (Attempt 1). Observe attempt counter = 1.
3. Enter invalid PIN `8888` and submit (Attempt 2). Observe attempt counter = 2.
4. Enter invalid PIN `7777` and submit (Attempt 3).
5. Inspect the terminal state.

#### Expected Result (Per SRS REQ-02.2)
On the **3rd consecutive failed attempt**, the system must immediately block the card (`isBlocked = true`), retain the card, and transition to the `view-locked` state with message `"SECURITY ALERT: CARD BLOCKED"`.

#### Actual Result (Observed Defect)
On the 3rd failed attempt, the system remains in the PIN entry state, displaying:
`"Invalid PIN. Consecutive attempts: 3. Remaining: 1"`.
The card is only blocked on the **4th** failed attempt. This gives attackers 33% more brute-force attempts than mandated by PCI-DSS security standards.

#### Root Cause Analysis (RCA)
In `atm_app/index.html`, the threshold conditional contains a strict inequality (`>`) instead of greater-than-or-equal-to (`>=`):
```javascript
// DEFECTIVE IMPLEMENTATION:
const lockoutThresholdReached = (acc.failedAttempts > 3); // Evaluates false on attempt 3!

// REMEDIATION:
const lockoutThresholdReached = (acc.failedAttempts >= 3);
```

---

### Defect ID: DEF-ATM-002
* **Title:** Violation of Mandatory Minimum Maintaining Balance Constraint (\$50.00)
* **Component:** `view-withdraw` / Balance Deductor (`executeWithdrawal`)
* **Severity:** **Critical** (S1)
* **Priority:** **P1 - High**
* **Defect Classification:** Core Banking Financial Logic Error
* **SRS Requirement Ref:** `REQ-03.5` (Minimum maintaining balance of \$50.00 required)

#### Preconditions
1. User authenticated with Card `4532109843218765`.
2. Available balance is \$1,000.00.

#### Test Data
* Withdrawal Amount: \$500.00 + \$480.00 = \$980.00 (or single test of account with \$100 attempting to withdraw \$90, leaving \$10).

#### Steps to Reproduce
1. Authenticate with valid card and PIN.
2. Select "Cash Withdrawal".
3. Enter withdrawal amount \$500.00 (Balance becomes \$500.00).
4. Perform second withdrawal of \$480.00.
5. Inspect remaining balance.

#### Expected Result (Per SRS REQ-03.5)
The transaction of \$480.00 must be rejected because leaving \$20.00 violates the mandatory minimum maintaining balance of \$50.00. The system should display:
`"ERROR: Insufficient funds. Balance cannot drop below required $50.00."`

#### Actual Result (Observed Defect)
The system approves the transaction and dispenses the cash. The customer balance drops to \$20.00 (or even \$0.00).

#### Root Cause Analysis (RCA)
The check in `executeWithdrawal()` only checks if the customer overdrafts below zero, ignoring `MIN_MAINTAINING_BALANCE`:
```javascript
// DEFECTIVE IMPLEMENTATION:
const insufficientFunds = (acc.balance - amount < 0);

// REMEDIATION:
const insufficientFunds = (acc.balance - amount < MIN_MAINTAINING_BALANCE);
```

---

### Defect ID: DEF-ATM-003
* **Title:** Cash Withdrawal Accepts Non-Standard Banknote Denominations
* **Component:** `view-withdraw` / Denomination Validator (`executeWithdrawal`)
* **Severity:** **Major** (S2)
* **Priority:** **P2 - Medium**
* **Defect Classification:** Hardware Interface / Input Boundary Flaw
* **SRS Requirement Ref:** `REQ-03.1` (Allowed Denominations: Multiples of \$20 or \$50)

#### Preconditions
1. User authenticated on ATM terminal.

#### Test Data
* Custom withdrawal amount: \$37.00 or \$13.00

#### Steps to Reproduce
1. Navigate to Cash Withdrawal screen.
2. In the "Custom Amount" field, enter `37`.
3. Click "Confirm Withdrawal".

#### Expected Result (Per SRS REQ-03.1)
The ATM hardware only carries \$20 and \$50 notes. Entering \$37 must be rejected immediately with:
`"ERROR: Denomination invalid. NexBank ATM dispenses multiples of $20 or $50 only."`

#### Actual Result (Observed Defect)
The terminal accepts \$37.00, subtracts \$37.00 from the user's account, and signals the cash dispenser to dispense `Dispensed: $37.00 [CASH READY]`, which is physically impossible for the currency cassettes and causes a physical hardware jam in field terminals.

#### Root Cause Analysis (RCA)
The input handler completely omitted modulus validation against the cassette bill denominations:
```javascript
// DEFECTIVE IMPLEMENTATION:
// No denomination check is performed! Accepts any arbitrary positive float.

// REMEDIATION:
if (amount % 20 !== 0 && amount % 50 !== 0) {
    showMessage("ERROR: Denomination invalid. NexBank ATM dispenses multiples of $20 or $50 only.");
    return;
}
```

---

### Defect ID: DEF-ATM-004
* **Title:** Negative Cash Deposit Amount Accepted Resulting in Account Debit
* **Component:** `view-deposit` / Deposit Processor (`executeDeposit`)
* **Severity:** **Major** (S2)
* **Priority:** **P1 - High**
* **Defect Classification:** Input Validation & Sanitization Failure
* **SRS Requirement Ref:** `REQ-04.4` (Deposit amount must be strictly positive $amount > 0$)

#### Preconditions
1. User authenticated with balance \$1,000.00.

#### Test Data
* Deposit amount: `-100`

#### Steps to Reproduce
1. Navigate to "Cash Deposit" screen.
2. Enter `-100` into the deposit amount input field.
3. Click "Confirm Deposit".

#### Expected Result (Per SRS REQ-04.4)
System must reject negative deposit with error:
`"ERROR: Invalid deposit amount. Amount must be strictly greater than $0."`

#### Actual Result (Observed Defect)
System accepts the transaction, displays `"SUCCESS: Deposit of $-100.00 confirmed"`, and adds $-100.00$ to the user's balance, effectively subtracting \$100.00 and creating a corrupt negative transaction record in the ledger.

#### Root Cause Analysis (RCA)
In `executeDeposit()`:
```javascript
// DEFECTIVE IMPLEMENTATION:
if (isNaN(amount)) { // Does not verify amount > 0 !
    showMessage("ERROR: Enter a valid number.");
    return;
}
acc.balance += amount; // 1000 + (-100) = 900!

// REMEDIATION:
if (isNaN(amount) || amount <= 0) {
    showMessage("ERROR: Invalid deposit amount. Amount must be strictly greater than $0.");
    return;
}
```

---

### Defect ID: DEF-ATM-005
* **Title:** Destination Account Validation Fails to Reject Self-Transfer
* **Component:** `view-transfer` / Inter-Account Engine (`executeTransfer`)
* **Severity:** **Major** (S2)
* **Priority:** **P2 - Medium**
* **Defect Classification:** Business Logic Error
* **SRS Requirement Ref:** `REQ-05.1` (Destination account cannot be identical to source account)

#### Preconditions
1. User authenticated with Card `4532109843218765`.

#### Test Data
* Destination Card: `4532109843218765` (Same as authenticated card)
* Transfer Amount: \$100.00

#### Steps to Reproduce
1. Select "Fund Transfer" from Main Menu.
2. In Destination Card field, enter the sender's own card number: `4532109843218765`.
3. Enter amount \$100.00.
4. Click "Confirm Transfer".

#### Expected Result (Per SRS REQ-05.1)
The terminal must detect self-transfer and reject the request with:
`"ERROR: Destination card cannot be identical to source card."`

#### Actual Result (Observed Defect)
The terminal processes the transfer. It creates redundant debit and credit entries in the user's transaction log and triggers duplicate inter-bank transfer messaging.

#### Root Cause Analysis (RCA)
Missing equality assertion between active source card and target card:
```javascript
// DEFECTIVE IMPLEMENTATION:
// Omits check if targetCard === activeCard

// REMEDIATION:
if (targetCard === activeCard) {
    showMessage("ERROR: Destination card cannot be identical to source card.", "error");
    return;
}
```

---

### Defect ID: DEF-ATM-006
* **Title:** PIN Change Routine Permits Setting Identical Existing PIN
* **Component:** `view-pin-change` / Security Routine (`executePinChange`)
* **Severity:** **Moderate** (S3)
* **Priority:** **P3 - Low**
* **Defect Classification:** Security Policy Violation
* **SRS Requirement Ref:** `REQ-06.3` (New PIN must not be identical to current PIN)

#### Preconditions
1. User authenticated with PIN `1234`.

#### Test Data
* Current PIN: `1234`
* New PIN: `1234`
* Confirm PIN: `1234`

#### Steps to Reproduce
1. Select "Change PIN" from Main Menu.
2. Enter Old PIN: `1234`.
3. Enter New PIN: `1234`.
4. Enter Confirm PIN: `1234`.
5. Click "Update PIN".

#### Expected Result (Per SRS REQ-06.3)
The terminal must reject the update with:
`"ERROR: New PIN cannot be the same as your current PIN."`

#### Actual Result (Observed Defect)
The terminal displays `"SUCCESS: Security PIN successfully updated"`, allowing the cardholder to recycle their existing PIN in direct contravention of the bank's password rotation and hygiene policies.

#### Root Cause Analysis (RCA)
```javascript
// DEFECTIVE IMPLEMENTATION:
// No check comparing newPin with oldPin

// REMEDIATION:
if (newPin === oldPin) {
    showMessage("ERROR: New PIN cannot be the same as your current PIN.", "error");
    return;
}
```

---

### Defect ID: DEF-ATM-007
* **Title:** Sensitive Cleartext PIN Exposed in DOM `data-debug-pin` Attribute
* **Component:** `view-pin-entry` / DOM Rendering (`handleCardInsertion`)
* **Severity:** **Critical** (S1)
* **Priority:** **P1 - High**
* **Defect Classification:** CWE-312 / Cleartext Storage of Sensitive Information
* **SRS Requirement Ref:** `REQ-07.2` & PCI-DSS 3.4 (Sensitive authentication data protection)

#### Preconditions
1. ATM Application loaded in browser.
2. Card `4532109843218765` inserted.

#### Steps to Reproduce
1. Insert valid card.
2. Inspect the DOM element `<input id="pin-input">` using browser DevTools or WebDriver query `element.get_attribute("data-debug-pin")`.

#### Expected Result (Per SRS REQ-07.2)
The DOM input element should never contain customer PINs in plaintext within any attribute or accessible property.

#### Actual Result (Observed Defect)
The element contains the unmasked PIN:
`<input type="password" id="pin-input" data-debug-pin="1234">`.
Any cross-site script, malicious browser extension, or terminal memory dumper can harvest customer PINs directly from the DOM tree.

#### Root Cause Analysis (RCA)
A development debugging attribute was accidentally left in the production release:
```javascript
// DEFECTIVE IMPLEMENTATION:
document.getElementById('pin-input').setAttribute('data-debug-pin', accounts[activeCard].pin);

// REMEDIATION:
// Completely eliminate the attribute from the DOM element.
```

---

### Defect ID: DEF-ATM-008
* **Title:** Cumulative Daily Withdrawal Limit Bypass Across Multiple Transactions
* **Component:** `view-withdraw` / Limit Aggregator (`executeWithdrawal`)
* **Severity:** **Major** (S2)
* **Priority:** **P1 - High**
* **Defect Classification:** Financial Security / Limit Enforcement Bypass
* **SRS Requirement Ref:** `REQ-03.3` (Cumulative daily withdrawal cap of \$1,000.00)

#### Preconditions
1. User authenticated with balance \$2,000.00.

#### Test Data
* Transaction 1: \$500.00
* Transaction 2: \$500.00 (Total withdrawn = \$1,000.00, daily limit reached)
* Transaction 3: \$200.00 (Total attempted = \$1,200.00)

#### Steps to Reproduce
1. Withdraw \$500.00 (Success).
2. Withdraw \$500.00 (Success, daily limit reached).
3. Withdraw another \$200.00.

#### Expected Result (Per SRS REQ-03.3)
Transaction 3 must be blocked with:
`"ERROR: Daily limit exceeded. Max daily limit is $1,000.00."`

#### Actual Result (Observed Defect)
The system only checks whether the single withdrawal is $\le \$500.00$. It permits Transaction 3, allowing cumulative daily withdrawals to reach \$1,200.00 or higher.

#### Root Cause Analysis (RCA)
```javascript
// DEFECTIVE IMPLEMENTATION:
if (amount > SINGLE_WITHDRAWAL_LIMIT) { // Checks single only!
    showMessage("ERROR: Amount exceeds single transaction limit.");
    return;
}
// Does not check: acc.dailyWithdrawn + amount > DAILY_WITHDRAWAL_LIMIT

// REMEDIATION:
if (acc.dailyWithdrawn + amount > DAILY_WITHDRAWAL_LIMIT) {
    showMessage("ERROR: Daily limit exceeded. Max daily limit is $1,000.00.");
    return;
}
```

---

## 3. Summary of Risk & Remediation Impact
All eight documented defects represent tangible real-world vulnerabilities and failures. In Section 4, we execute the automated **Selenium Python Test Suite** that tests these specifications and reproduces these defects.

