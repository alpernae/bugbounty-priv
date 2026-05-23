# Phase 4: Reporting Issues

Goal: Consolidate validated findings into structured, actionable reports for stakeholders.

---

## Report Templates

### Quick Report (1-Page Summary)

```markdown
# Security Assessment Summary

**Target**: example.com  
**Date**: 2025-05-15  
**Assessor**: Codex Security  
**Scope**: Web application (in-scope: /app, /api)

## Executive Summary

This assessment identified **2 HIGH-severity** findings and **1 MEDIUM-severity** finding requiring immediate remediation.

### Critical Findings

| # | Issue | Severity | Impact |
|---|-------|----------|--------|
| 1 | SQL Injection in /api/users | CRITICAL | Complete database exfiltration |
| 2 | Authorization Bypass | HIGH | Cross-user data disclosure |
| 3 | Reflected XSS in Search | MEDIUM | Session hijacking |

### Remediation Priorities

1. **Immediate** (within 48 hours): SQL Injection → Implement parameterized queries
2. **Urgent** (within 1 week): Authorization → Add resource ownership verification
3. **Important** (within 2 weeks): XSS → HTML-encode all user input

**Next Steps**: Refer to detailed findings section for proof-of-concept and remediation steps.
```

---

### Detailed Report Template

```markdown
# Security Assessment Report

**Target**: example.com  
**Assessment Date**: 2025-05-15 to 2025-05-17  
**Assessor**: Codex Security  
**Scope**: 
- Authenticated endpoints in /api/v1
- Public endpoints in /app
- Admin dashboard (if authorized)

---

## 1. SQL Injection in User Search

### Summary
The user search endpoint (`GET /api/users?id=`) is vulnerable to SQL injection, allowing attackers to exfiltrate the entire user database.

### Details

**Endpoint**: `GET https://target.com/api/users?id=`  
**Severity**: CRITICAL  
**CVSS Score**: 9.8  
**Status**: Verified

### Proof of Concept

#### Request

```
GET /api/users?id=1 AND 1=1 HTTP/1.1
Host: target.com
Authorization: Bearer <user_token>
```

#### Response (Boolean-based confirmation)

```
# Baseline: id=1
Response: 200 OK, 245 bytes (8 user records)

# True condition: id=1 AND 1=1
Response: 200 OK, 245 bytes (8 user records) - SAME

# False condition: id=1 AND 1=2
Response: 200 OK, 0 bytes (no records) - DIFFERENT
```

#### Exploitation

```
# Extract user emails via UNION injection
GET /api/users?id=1 UNION SELECT email FROM users--
```

### Root Cause

```python
# Vulnerable code in UserRepository.py
@app.get("/api/users")
def get_user(id: int):
    query = f"SELECT * FROM users WHERE id = {id}"  # UNSAFE!
    return db.execute(query)
```

### Impact

- **Data Affected**: All user records (emails, names, hashed passwords)
- **Impact Scope**: All users across the application
- **Attackers**: Any authenticated user (low privilege required)
- **Detectability**: Limited—queries blend with normal traffic

### Remediation

**Fix**: Use parameterized queries

```python
# Secure code using parameterized queries
@app.get("/api/users")
def get_user(id: int):
    query = "SELECT * FROM users WHERE id = ?"  # Parameterized
    return db.execute(query, (id,))
```

**Validation**: After fixing, test:
```
GET /api/users?id=1 AND 1=2  → Should return error or handle gracefully
```

### References
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)

---

## 2. Authorization Bypass - Cross-User Access

### Summary
Authenticated users can access other users' sensitive data (invoices, payment methods) by modifying object IDs in the request.

### Details

**Endpoint**: `GET /api/invoices/{invoice_id}`  
**Severity**: HIGH  
**CVSS Score**: 8.2  
**Status**: Verified

### Proof of Concept

#### Setup

```
User1: email@user1.com, token=token_user1
User2: email@user2.com, token=token_user2
```

#### Request (User1 accessing User2's invoice)

```
GET /api/invoices/5678 HTTP/1.1
Host: target.com
Authorization: Bearer token_user1

# Response: 200 OK
{
  "id": 5678,
  "owner": "user2@example.com",
  "amount": 5000,
  "items": [{"product": "Pro Plan", "cost": 5000}]
}
```

#### Expected Behavior

```
# Should return 403 Forbidden or filtered data
403 Forbidden
{
  "error": "You do not have permission to access this resource"
}
```

### Root Cause

```python
# Vulnerable: No ownership check
@app.get("/api/invoices/{invoice_id}")
def get_invoice(invoice_id: int, current_user: User):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    return invoice  # No check if current_user owns this invoice!
```

### Impact

- **Data Affected**: All user invoices, payment methods, billing history
- **Impact Scope**: Cross-user data disclosure (all users can see each other's data)
- **Risk**: PII exposure, financial information leakage
- **Exploitability**: Easy—just enumerate invoice IDs

### Remediation

**Fix**: Verify resource ownership

```python
@app.get("/api/invoices/{invoice_id}")
def get_invoice(invoice_id: int, current_user: User):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == current_user.id  # ← Add ownership check
    ).first()
    
    if not invoice:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return invoice
```

**Validation**: After fixing, verify that:
```
User1 accessing User1's invoice → 200 OK
User1 accessing User2's invoice → 403 Forbidden
```

---

## 3. Reflected XSS in Search

### Summary
The search endpoint reflects user input without proper HTML encoding, allowing attackers to inject malicious JavaScript.

### Details

**Endpoint**: `GET /app/search?q=`  
**Severity**: MEDIUM  
**CVSS Score**: 6.1  
**Status**: Verified (Reflected, not Stored)

### Proof of Concept

#### Payload

```
https://target.com/app/search?q=<img src=x onerror="alert('XSS')">
```

#### Response

```html
<h1>Search Results for: <img src=x onerror="alert('XSS')"></h1>
```

#### Execution

When a user visits the link above, the `onerror` event fires and JavaScript executes in the user's browser context.

### Root Cause

```html
<!-- Vulnerable: Unencoded reflection -->
<h1>Search Results for: {{ search_query }}</h1>

<!-- Should be: HTML-encoded -->
<h1>Search Results for: {{ search_query | htmlescape }}</h1>
```

### Impact

- **Attack Vector**: Phishing link in emails, social media
- **Victim Action**: User must click the malicious link
- **Impact**: Session hijacking, credential theft, malware distribution
- **Scope**: Low (requires victim interaction)

### Remediation

**Fix**: HTML-encode all user input in templates

```html
<!-- Jinja2 example (default is unsafe) -->
<h1>Search Results for: {{ search_query | e }}</h1>

<!-- Or use framework defaults -->
<!-- Most modern frameworks encode by default -->
```

**Validation**: After fixing, verify that:
```
https://target.com/app/search?q=<img src=x onerror="alert('XSS')">
# Should display: Search Results for: <img src=x onerror="alert('XSS')">
# (The < and > should be visible as &lt; and &gt;)
```

---

## Overall Assessment Summary

### Statistics

```yaml
assessment_scope:
  endpoints_tested: 42
  total_time_hours: 6
  
findings_breakdown:
  critical: 1
  high: 1
  medium: 1
  low: 0
  informational: 2
  total: 5

status:
  confirmed: 3
  suppressed: 2
  false_positives: 0

affected_areas:
  data_exposure: 2
  injection: 1
  authorization: 1
```

### Risk Profile

**Before Remediation**: CRITICAL RISK
- Complete database exfiltration possible
- Cross-user data disclosure active
- Account takeover vectors present

**After Remediation**: LOW RISK
- Implement all CRITICAL and HIGH fixes → Risk drops to MEDIUM
- Implement MEDIUM fixes → Risk drops to LOW

---

## Remediation Roadmap

### Week 1 (Immediate)
- [ ] SQL Injection: Deploy parameterized queries
- [ ] Authorization: Add resource ownership verification
- [ ] Test fixes in staging environment

### Week 2
- [ ] XSS: Enable HTML encoding in templates
- [ ] Deploy to production
- [ ] Run regression tests

### Week 3+
- [ ] Implement WAF rules to prevent similar issues
- [ ] Add automated security testing to CI/CD
- [ ] Schedule follow-up assessment

---

## Tools & Methods Used

- **Reconnaissance**: httpx, Playwright, custom crawlers
- **Active Testing**: Python requests, custom scanners
- **Validation**: Manual verification, Playwright for browser context
- **Reporting**: Markdown templates

---

## Disclaimer

This report is based on testing performed with explicit authorization to the target application. Findings are valid as of the test date. Recommendations should be validated in the target environment before deployment.
```

---

## Automated Report Generation

### Python Script for Consolidation

```python
cat > generate_report.py << 'EOF'
import json
import sys
from datetime import datetime

def generate_markdown_report(findings):
    """Generate a Markdown report from validated findings"""
    
    report = f"""# Security Assessment Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Total Findings**: {len(findings)}

## Finding Summary

"""
    
    for i, finding in enumerate(findings, 1):
        report += f"""
### {i}. {finding['title']}

**Severity**: {finding['severity']}  
**Status**: {finding['status']}

**Description**: {finding['description']}

**Proof**:
```
{finding['evidence']}
```

**Remediation**: {finding['remediation']}

---
"""
    
    return report

# Load validated findings
with open("findings.json") as f:
    findings = json.load(f)

# Generate report
report = generate_markdown_report(findings)

# Save
with open("REPORT.md", "w") as f:
    f.write(report)

print("✓ Report generated: REPORT.md")

EOF

python generate_report.py
```

---

## Output Formats

### Markdown Report
- Human-readable
- Suitable for stakeholders
- Easy to email or share
- Suitable for inclusion in documentation

### JSON Export
```json
{
  "metadata": {
    "target": "example.com",
    "date": "2025-05-15",
    "findings_count": 3
  },
  "findings": [
    {
      "id": "SQL_INJECTION_001",
      "title": "SQL Injection",
      "severity": "CRITICAL",
      "status": "reproduced",
      "endpoint": "/api/users",
      "evidence": {...},
      "remediation": "Use parameterized queries"
    }
  ]
}
```

### CSV Export (for tracking systems)
```
ID,Title,Severity,Endpoint,Status,Remediation
1,SQL Injection,CRITICAL,/api/users,reproduced,Parameterized queries
2,Authorization Bypass,HIGH,/api/invoices,reproduced,Add ownership checks
```

---

## Distribution & Communication

### For Developers
- Send detailed report with code examples
- Include root cause analysis
- Provide remediation steps with code snippets

### For Management
- Send executive summary (1 page)
- Include risk rating before/after remediation
- Provide remediation timeline

### For Security Team
- Send full JSON export for tracking
- Include false-positive analysis
- Provide guidance on similar patterns

---

## Follow-Up Actions

### Validation of Fixes
After developer deployment:

```bash
# Re-test all confirmed findings
./retest_findings.py

# Generate comparison report
./compare_reports.py REPORT.md REPORT_RETEST.md
```

### Post-Remediation Checklist
- [ ] All CRITICAL fixes deployed
- [ ] Regression tests passed
- [ ] Monitoring/alerting in place
- [ ] Documentation updated
- [ ] Team trained on fixes

---

## Phase 4 Output

Final deliverables:

```
security-reports/
├── REPORT.md (main report)
├── findings.json (structured data)
├── executive-summary.md
└── remediation-tracking.csv
```

---

## Decision: End of Workflow

Assessment is complete when:
- ✓ All findings documented and classified
- ✓ Reports generated and distributed
- ✓ Remediation timeline agreed
- ✓ Follow-up assessment scheduled (if needed)

## Reference Quality Addendum

## Purpose

Use this section to normalize reference quality for scoring and day-to-day security work. It explains how to apply this reference during discovery, validation, attack-path analysis, reporting, or remediation.

## Workflow

1. Identify the relevant asset, code path, endpoint, workflow, or configuration.
2. Map attacker-controlled input to the closest control and security-sensitive sink or decision.
3. Validate the claim with the safest bounded proof available.
4. Search for counterevidence before promoting the issue.
5. Record impact, confidence, remediation, and proof gaps.

## False-positive checks

Suppress or downgrade when the path is unreachable, the input is not attacker-controlled, the behavior is public or self-only, an effective control blocks the exact path, the issue is scanner-only, or impact is only a best-practice concern.

## Validation example

```markdown
- expected: lower-privileged actor cannot reach protected data or action
- actual: request, test, fixture, or trace shows the protected behavior is reachable
- evidence: masked request/response, code trace, test output, callback, or parser fixture
- counterevidence: controls checked and why they do or do not apply
```

## Output fields

Include affected location, attacker input, closest control, sink or protected decision, validation evidence, impact, severity or confidence, remediation, and remaining proof gaps.
