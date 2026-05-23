# BlackBox Automation

A comprehensive, authorized web application security testing framework combining reconnaissance, threat modeling, vulnerability discovery, safe validation, and structured reporting workflows for penetration testing and bug bounty programs.

## Overview

BlackBox Automation provides a structured methodology for conducting security assessments on web applications, APIs, GraphQL endpoints, and browser-based systems. The framework emphasizes evidence-driven vulnerability discovery, safe proof-of-concept validation, and impact-focused reporting while maintaining strict operational security controls.

### Key Principles

- **Evidence-First**: All findings backed by repeatable test cases and clear impact demonstration
- **Scoped & Authorized**: Strict enforcement of authorization boundaries and out-of-scope protections
- **Low-Impact Testing**: Reversible actions, owned accounts, and minimal noise
- **Security-Focused**: Built-in controls to prevent data exfiltration, malware deployment, or detection evasion

---

## Project Structure

```
blackbox-automation/
├── README.md                           # This file
├── web-security-workflow.md            # Information gathering and reconnaissance workflow
├── setup/
│   └── setup.sh                        # Initial environment setup script
├── .config/
│   └── alterx/                         # Alterx subdomain permutation configurations
│       └── alterx-large-practical-deep.yaml
├── ai/
│   └── skills/                         # AI-assisted testing skills and playbooks
│       ├── web-security/               # End-to-end web security testing orchestrator
│       ├── web-threat-model/           # Threat modeling for web applications
│       ├── web-finding-discovery/      # Vulnerability discovery workflows
│       ├── web-validation/             # Vulnerability validation and proof-of-concept
│       ├── web-reporting/              # Bug bounty and pentest report generation
│       ├── source-code-security/       # Source code security analysis
│       ├── source-threat-model/        # Application threat modeling
│       ├── source-validation/          # Code-based vulnerability validation
│       ├── ReportAI/                   # Structured vulnerability report generation
│       └── goal/                       # Goal-driven security assessment planning
└── nuclei-templates/                   # Custom Nuclei vulnerability scanning templates
```

---

## Core Components

### 1. AI Security Skills

The `ai/skills/` directory contains modular security testing workflows designed to integrate with AI-assisted vulnerability discovery and validation:

#### Web Application Testing

- **[web-security](ai/skills/web-security/SKILL.md)** - End-to-end authorized web application and API security testing. Orchestrates reconnaissance, threat modeling, discovery, validation, and reporting into a unified workflow.

- **[web-threat-model](ai/skills/web-threat-model/SKILL.md)** - Builds formal threat models for web applications by enumerating assets, trust boundaries, attacker-controlled inputs, roles, and security invariants. Outputs structured models for pentest planning and attack surface mapping.

- **[web-finding-discovery](ai/skills/web-finding-discovery/SKILL.md)** - Vulnerability discovery workflows for common web security issues (IDOR, auth bypass, injection, SSRF, XSS, etc.). Produces high-signal candidates with minimal false positives.

- **[web-validation](ai/skills/web-validation/SKILL.md)** - Safe validation of suspected vulnerabilities through repeatable HTTP request testing, baseline comparison, and impact confirmation. Includes false-positive suppression with exact counterevidence.

- **[web-reporting](ai/skills/web-reporting/SKILL.md)** - Structured vulnerability report generation for bug bounty platforms (HackerOne, Bugcrowd) and internal pentest deliverables. Includes severity triage and remediation guidance.

#### Source Code Security

- **[source-code-security](ai/skills/source-code-security/SKILL.md)** - Static analysis, secret detection, dependency scanning, and code-based vulnerability discovery.

- **[source-threat-model](ai/skills/source-threat-model/SKILL.md)** - Threat modeling for applications through source code review.

- **[source-validation](ai/skills/source-validation/SKILL.md)** - Validating suspected code-based vulnerabilities through taint analysis and execution flows.

#### Other Workflows

- **[ReportAI](ai/skills/ReportAI/SKILL.md)** - Security-focused vulnerability report generation with OWASP Top 10 guidance.

- **[goal](ai/skills/goal/SKILL.md)** - Goal-driven security assessment planning and orchestration.

---

### 2. Automation Scripts

#### Web Security Scripts

Located in `ai/skills/web-security/scripts/`:

- **`new_finding.py`** - Generates HackerOne finding drafts from vulnerability details. Automates initial report structuring for quick triage.

- **`check_skill_structure.py`** - Validates required files and structure for security skills. Ensures skill directories contain necessary documentation and references.

- **`api_key_exposure_triage.py`** - Automated triage for exposed API keys and credentials. Categorizes severity and suggested remediation.

#### Source Code Scripts

Located in `ai/skills/source-code-security/scripts/`:

- **`source_inventory.py`** - Catalogs source code assets, dependencies, and technology stack.

- **`source_candidate_triage.py`** - Triages code-based vulnerability candidates by severity and exploitability.

- **`secret_candidate_scanner.py`** - Detects and categorizes hardcoded secrets, credentials, and sensitive tokens.

---

### 3. Configuration Files

#### Alterx Subdomain Permutation

**File**: `.config/alterx/alterx-large-practical-deep.yaml`

Configuration for the Alterx tool, optimized for bug bounty and authorized reconnaissance:

- **Profile**: Large but practical permutation patterns for subdomain discovery
- **Design**: High-signal patterns first, environment/service/cloud-aware naming
- **Patterns Include**:
  - Core dash permutations: `{{word}}-{{sub}}.{{suffix}}`
  - Core dot permutations: `{{word}}.{{sub}}.{{suffix}}`
  - Environment patterns: dev, staging, prod, test
  - Service patterns: api, mail, web, cdn, ops
  - Cloud patterns: aws, azure, gcp, cloudflare

**Usage**:
```bash
alterx -c .config/alterx/alterx-large-practical-deep.yaml -d target.com | dnsx
```

---

## Information Gathering Workflow

See [web-security-workflow.md](web-security-workflow.md) for detailed reconnaissance methodology including:

### 1. Asset Discovery & Fingerprinting

- **Passive Methods**: Certificate transparency, WHOIS, DNS, subdomain enumeration (Chaos, Subfinder, AMASS)
- **Active Methods**: DNS probing (dnsx), HTTP validation (httpx), port scanning (Nmap, Masscan)
- **Technology Fingerprinting**: Web frameworks, WAF/CDN detection, authentication mechanisms

### 2. Content Discovery

- **Passive Methods**: GitHub/GitLab search, breach databases, social media reconnaissance, Wayback Machine
- **Active Methods**: Web crawling (katana, gospider, hakrawler), endpoint discovery, parameter mining (ParamSpider)

### 3. Monitoring & Notifications

- **Discord Integration**: Real-time alerts on new findings and vulnerability discoveries
- **Notify Tool**: Unified notification pipeline for tool output aggregation

---

## Quick Start

### Prerequisites

- Go 1.18+ (for reconnaissance tools)
- Python 3.8+ (for automation scripts)
- curl, dig, nslookup (DNS utilities)
- Sudo privileges (for setup script)

### Initial Setup

```bash
# Run setup script
sudo bash setup/setup.sh

# Install reconnaissance tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/dnsx@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/alterx/cmd/alterx@latest
go install -v github.com/projectdiscovery/notify/cmd/notify@latest

# Install Python dependencies (optional)
pip install -r requirements.txt  # Create based on script needs
```

### Running a Web Security Assessment

1. **Scope & Authorization** (Required):
   ```bash
   # Confirm target, environment, allowed accounts, rate limits, and out-of-scope actions
   # Document authorization before beginning
   ```

2. **Build Threat Model**:
   - Use `web-threat-model` skill to enumerate assets, roles, and security invariants
   - Map attack surface and trust boundaries
   - Identify priority failure modes

3. **Discover Vulnerabilities**:
   - Use `web-finding-discovery` skill for targeted vulnerability hunting
   - Reference issue-specific playbooks in `ai/skills/web-security/references/`

4. **Validate Findings**:
   - Use `web-validation` skill to confirm each finding
   - Capture baseline request, modify one variable, compare responses
   - Suppress false positives with exact counterevidence

5. **Report & Triage**:
   - Use `web-reporting` skill or `new_finding.py` script
   - Generate structured vulnerability reports
   - Include severity assessment and remediation guidance

---

## Operational Security

### Hard Rules

1. **Authorization**: Confirm scope and authorization before testing. Maintain evidence of written authorization.

2. **Low-Impact Operations**:
   - Use owned accounts and test tenants exclusively
   - Limit request volume and test frequency
   - Perform only reversible actions

3. **Data Protection**:
   - Never exfiltrate secrets, credentials, personal data, or customer information
   - Mask sensitive values in reports (tokens, cookies, emails, etc.)
   - Stop testing immediately upon demonstrating vulnerability and impact

4. **No Evasion or Malware**:
   - Do not deploy web shells, malware, or persistent access mechanisms
   - Do not evade detection systems or engage in anti-forensics
   - Do not phish users or attack third-party services

5. **Evidence Collection**:
   - Capture repeatable proof-of-concept for all findings
   - Document test methodology and impact clearly
   - Maintain audit trail of all assessment activities

---

## Testing Workflows by Phase

### Reconnaissance
- Asset discovery and enumeration
- Technology fingerprinting
- Service and endpoint mapping
- Credential harvesting (passive methods only)

### Threat Modeling
- Asset and workflow documentation
- Role and permission mapping
- Attack surface definition
- Security invariant identification

### Vulnerability Discovery
- Web application testing (IDOR, auth bypass, injection, XSS, SSRF, etc.)
- API endpoint fuzzing and parameter discovery
- Business logic flaws and race conditions
- Session and cookie manipulation
- Upload bypass and file handling

### Validation & Proof-of-Concept
- Safe payload testing with owned accounts
- Baseline-and-delta comparison methodology
- False-positive suppression
- Impact confirmation

### Reporting & Remediation
- Severity and CVSS assessment
- Bug bounty platform submission
- Pentest report generation
- Remediation guidance and fix verification

---

## References & Additional Resources

- **Threat Modeling**: See `ai/skills/web-threat-model/SKILL.md`
- **False Positive Reduction**: See `ai/skills/web-security/references/false-positive-reduction.md`
- **Issue Playbooks**: See `ai/skills/web-security/references/index.md` for issue-specific testing methodologies
- **Coverage Matrix**: See `ai/skills/web-security/references/coverage-matrix.md` for comprehensive testing checklist

---

## Contributing

To contribute new skills, tools, or workflows:

1. Create a new skill directory in `ai/skills/` with proper structure
2. Include SKILL.md with full documentation and workflow
3. Add supporting scripts and references as needed
4. Run `check_skill_structure.py` to validate structure
5. Update this README with the new skill description

---

## License & Authorization

This framework is designed for authorized security testing only. Users must:
- Obtain written authorization before conducting any security assessment
- Comply with all applicable laws and regulations
- Respect scope boundaries and out-of-scope systems
- Follow the hard rules outlined in the Operational Security section

Unauthorized access to computer systems is illegal. Use responsibly.

---

## Support & Documentation

- **Detailed Workflows**: See individual SKILL.md files in `ai/skills/*/`
- **Reconnaissance Guide**: See [web-security-workflow.md](web-security-workflow.md)
- **Script Documentation**: See individual `.py` file headers for usage and examples
- **Alterx Configuration**: See `.config/alterx/` for subdomain permutation options

---

**Last Updated**: May 2026  
**Version**: 1.0  
**Status**: Active Development
