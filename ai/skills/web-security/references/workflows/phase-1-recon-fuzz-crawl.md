# Phase 1: Recon, Fuzz & Crawl

Goal: Enumerate the attack surface, discover endpoints, extract client-side code, and identify hidden inputs/URLs.

## Step 1: Subdomain & Host Discovery

### Technique 1A: Passive DNS & Certificate Logs

```bash
# Using curl + public APIs (no auth needed)
curl -s "https://crt.sh/?q=%.domain.com&output=json" | jq .[].name_value
# or
curl -s "https://dns.google/resolve?name=domain.com" | jq .Answer[]

# Tool: httpx for mass validation
httpx -l hosts.txt -status-code -title -server
```

**Decision**: If <5 subdomains found → expand search (ASNs, reverse DNS, GitHub scanning). If >20 → prioritize by business relevance.

### Technique 1B: Port & Service Detection

```bash
# httpx with full port scanning
httpx -u "http://host.com:*" -ports 80,443,8000,8080,3000,5000,9000 -status-code

# Or focused on common API ports
for port in 3000 5000 8000 8080 9000; do
  timeout 2 curl -s http://target.com:$port | grep -oP '(title|href|<h1)' && echo "Found: $port"
done
```

**Decision**: Prioritize 443/80 first, then expand to dev ports (3000, 8080) if in scope.

---

## Step 2: Web App & API Surface Mapping

### Technique 2A: Crawl HTML & Extract Links

```bash
# Using Playwright (or Selenium) to crawl dynamically rendered apps
cat > crawl.py << 'EOF'
import asyncio
from playwright.async_api import async_playwright

async def crawl(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        
        # Extract all links
        links = await page.evaluate("""
            Array.from(document.querySelectorAll('a[href]'))
                .map(a => a.href)
                .filter(h => h && (h.startsWith('/') || h.includes(window.location.host)))
        """)
        
        # Extract form endpoints
        forms = await page.evaluate("""
            Array.from(document.querySelectorAll('form'))
                .map(f => ({
                    action: f.action,
                    method: f.method || 'GET',
                    inputs: Array.from(f.querySelectorAll('input')).map(i => ({name: i.name, type: i.type, value: i.value}))
                }))
        """)
        
        return {"links": links, "forms": forms}

asyncio.run(crawl("https://target.com"))
EOF

python crawl.py
```

**Output Example**:
```json
{
  "links": ["/dashboard", "/api/users", "/settings", "/docs"],
  "forms": [
    {"action": "/api/login", "method": "POST", "inputs": [{"name": "email", "type": "email"}, {"name": "password", "type": "password"}]}
  ]
}
```

### Technique 2B: Extract Routes from JS Bundles

```bash
# Download all JS files
curl -s https://target.com | grep -oP 'src="[^"]*\.js"' | cut -d'"' -f2 | sort -u > js_files.txt

# Or use Playwright
cat > extract_js.py << 'EOF'
import asyncio
from playwright.async_api import async_playwright

async def extract_js(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        
        resources = await page.context.request.get_all()
        js_urls = [r.url for r in resources if r.url.endswith('.js')]
        
        return js_urls

asyncio.run(extract_js("https://target.com"))
EOF

# Download and analyze JS
for js_url in $(python extract_js.py | head -10); do
    echo "=== $js_url ==="
    curl -s "$js_url" > bundle.js
    
    # Extract API endpoints (common patterns)
    grep -oP '(?:post|get|put|delete)\(["\x60]/api/[^"\x60]*' bundle.js | sort -u
    
    # Extract hidden URLs
    grep -oP '(?:["\x60]/[a-zA-Z0-9/_-]+)+["\x60]' bundle.js | sort -u | head -20
    
    # Extract fetch/axios patterns
    grep -oP '(?:fetch|axios)\(["\x60]([^"\x60]*)["\x60]' bundle.js | sort -u
done
```

**Decision**: If >50 unique endpoints found → prioritize by:
1. State-changing (POST/PUT/DELETE) first
2. Unauthenticated or low-auth first
3. Those with object IDs or user data

---

## Step 3: Parameter & Input Discovery

### Technique 3A: Fuzz Query & Path Parameters

```bash
# Common parameter names (expand as needed)
cat > fuzz_params.txt << 'EOF'
id
user_id
account_id
org_id
tenant_id
user
email
username
action
cmd
command
filter
sort
limit
offset
page
search
q
query
v
version
debug
admin
role
api_key
token
session
auth
redirect
callback
return_to
next
back
url
uri
target
host
domain
file
path
dir
include
require
load
exec
eval
code
EOF

# Fuzz with ffuf or wfuzz
ffuf -u "https://target.com/api/users?FUZZ=1" -w fuzz_params.txt -fc 400,404 -t 30

# Or curl loop for validation
while read param; do
    response=$(curl -s "https://target.com/api/users?$param=test" -w "\n%{http_code}")
    status=$(echo "$response" | tail -1)
    if [ "$status" != "400" ] && [ "$status" != "404" ]; then
        echo "$param: $status"
    fi
done < fuzz_params.txt
```

### Technique 3B: Extract Input Fields from Forms & JS

```bash
# From HTML forms
curl -s https://target.com/register | grep -oP '(?<=name=")[^"]*' | sort -u

# From JS code patterns
grep -roh 'document.querySelector.*\[name=["\x27]\([^"]*\)' . | sed 's/.*name=["'"'"']\([^"'"'"']*\).*/\1/' | sort -u

# Hidden fields in JS
grep -oP 'name:\s*["\x27]\K[^"\x27]*' bundle.js | sort -u
```

### Technique 3C: Common Injection Points

Build a matrix of all inputs and their potential injection vectors:

```markdown
| Endpoint | Method | Input | Type | Fuzz Pattern | Priority |
|----------|--------|-------|------|--------------|----------|
| /api/search | GET | q | query | sql,xss,nosql | HIGH |
| /api/users | POST | email | body | sql,email | MEDIUM |
| /upload | POST | file | file | rce,xxe | HIGH |
| /redirect | GET | url | query | ssrf,openredirect | HIGH |
```

---

## Step 4: JS Analysis for Hidden Vulnerabilities

### Technique 4A: DOM XSS Patterns

```bash
cat > analyze_dom_xss.py << 'EOF'
import re
import sys

source_patterns = [
    r'window\.location\.[a-zA-Z]+',
    r'document\.location',
    r'document\.URL',
    r'document\.referrer',
    r'location\.search',
    r'location\.hash',
]

sink_patterns = [
    r'innerHTML\s*=',
    r'outerHTML\s*=',
    r'eval\(',
    r'setTimeout\(',
    r'setInterval\(',
    r'document\.write\(',
    r'appendChild\(',
    r'insertAdjacentHTML\(',
]

def analyze_js(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    sources = []
    sinks = []
    
    for pattern in source_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            sources.append((line_num, match.group()))
    
    for pattern in sink_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            sinks.append((line_num, match.group()))
    
    print(f"=== {filepath} ===")
    print(f"Sources (user input): {len(sources)}")
    for line, source in sources[:5]:
        print(f"  Line {line}: {source}")
    print(f"Sinks (dangerous operations): {len(sinks)}")
    for line, sink in sinks[:5]:
        print(f"  Line {line}: {sink}")
    
    # Flag if source and sink exist (high priority for analysis)
    if sources and sinks:
        print("⚠️  POTENTIAL DOM XSS: User input + dangerous sinks detected")

if __name__ == "__main__":
    analyze_js(sys.argv[1])
EOF

# Run on all downloaded JS
for js in *.js; do
    python analyze_dom_xss.py "$js"
done
```

### Technique 4B: API Endpoint Patterns in JS

```bash
# Extract all fetch/axios/XMLHttpRequest calls
grep -oP '(?:fetch|axios|XMLHttpRequest)\s*\(\s*["\x60]([^"\x60]+)["\x60]' *.js | cut -d':' -f2 | sort -u

# Extract GraphQL endpoints
grep -oP 'graphql|mutation|query' *.js | head -5 # Then look for the endpoint URL

# Extract hidden admin/debug routes
grep -oP '(/admin|/debug|/_internal|/api/v\d+/internal|/metrics|/health|/actuator)' *.js | sort -u
```

### Technique 4C: SSRF & Unvalidated Redirects

```bash
cat > find_ssrf.py << 'EOF'
import re

redirect_patterns = [
    r'window\.location\s*=\s*["\x27]?([^"\x27;]+)',
    r'location\.href\s*=\s*["\x27]?([^"\x27;]+)',
    r'fetch\(["\x27]([^"\x27]+)["\x27]',
    r'$.get\(["\x27]([^"\x27]+)["\x27]',
]

dangerous_patterns = [
    r'return_to\s*=',
    r'redirect_to\s*=',
    r'callback\s*=',
    r'url\s*=',
    r'target\s*=',
]

with open("bundle.js", "r") as f:
    content = f.read()

for pattern in redirect_patterns:
    for match in re.finditer(pattern, content):
        context = content[max(0, match.start()-50):match.end()+50]
        if any(re.search(d, context) for d in dangerous_patterns):
            print(f"⚠️  POTENTIAL SSRF/REDIRECT: {match.group()}")
EOF

python find_ssrf.py
```

---

## Step 5: Unauthenticated & CORS Scanning

### Technique 5A: Identify Public Endpoints

```bash
# List all discovered endpoints
cat all_endpoints.txt | head -20

# Test each without auth
for endpoint in $(cat all_endpoints.txt); do
    status=$(curl -s -o /dev/null -w "%{http_code}" "https://target.com$endpoint")
    if [ "$status" != "401" ] && [ "$status" != "403" ]; then
        echo "$endpoint: $status (UNAUTHENTICATED!)"
    fi
done
```

### Technique 5B: CORS Misconfiguration Detection

```bash
curl -i -X OPTIONS "https://target.com/api/users" \
  -H "Origin: https://attacker.com" | grep -i "access-control"

# Check for wildcard CORS
curl -s "https://target.com/api/data" \
  -H "Origin: https://attacker.com" | grep -i "access-control-allow-origin"
```

---

## Phase 1 Output

At the end of Phase 1, generate:

```yaml
endpoint_inventory:
  total_endpoints: 42
  authenticated: 28
  unauthenticated: 14
  
parameter_matrix:
  query_params: 23
  body_params: 17
  path_params: 8
  
javascript_analysis:
  files_analyzed: 12
  potential_dom_xss: 3
  hidden_endpoints: 7
  suspicious_patterns: 5
  
priority_targets:
  high: ["/api/users/{id}", "/api/upload", "/redirect"]
  medium: ["/search", "/export", "/admin"]
  
decision_gate: "Ready for Phase 2?"
```

---

## Decision: Phase 1 → Phase 2

**Continue if**:
- ✓ >10 endpoints discovered
- ✓ Attack surface clearly mapped
- ✓ At least 5 test parameters identified
- ✓ Critical endpoints isolated

**Refine if**:
- ✗ <5 endpoints found (expand crawling, check for dynamic routes)
- ✗ No unauthenticated access (focus on auth bypass vectors)
- ✗ Limited parameters (check API docs, examine request logs)

**Next**: Move to `phase-2-passive-active-scanning.md`

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
