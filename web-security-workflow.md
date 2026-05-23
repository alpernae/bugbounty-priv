# BlackBox Automation

## Information Gathering Workflow

This workflow describes the methods and tools used to gather reconnaissance information during security assessments and penetration testing phases.

---

## 1. Asset Discovery & Fingerprinting

Identify and enumerate digital assets including subdomains, services, hosts, and infrastructure. Simultaneously fingerprint technology stack, security controls, frameworks, and authentication mechanisms.

### Search & Public Information Methods

- **Dorking**: Use advanced search operators (Google, Bing, etc.) to find exposed information and infrastructure
- **Certificate Transparency (crt.sh)**: Find subdomains through SSL/TLS certificate records
- **WHOIS & DNS Records**: Gather domain registration info, nameservers, DNS history, and mail servers
- **Shodan**: Discover exposed services, versions, banners, and infrastructure details (paid account available)
- **Censys**: Free alternative for service enumeration and certificate discovery
- **Wayback Machine**: Retrieve historical snapshots of target websites and previous configurations

### Fingerprinting Targets

**Technology Stack:**
- Identify web frameworks, libraries, and backend technologies
- Detect programming languages and version information
- Find CMS, server software, and dependent packages

**WAF/CDN Detection:**
- Identify Web Application Firewalls (WAF) presence and type
- Detect Content Delivery Networks (CDN) and cloud providers
- Understand traffic routing and filtering mechanisms

**Frameworks & Libraries:**
- Map out frontend frameworks (React, Vue, Angular, etc.)
- Identify backend frameworks and API versions
- Discover third-party libraries and dependencies

**Authentication Detection:**
- Identify authentication mechanisms (OAuth, SAML, custom, etc.)
- Detect MFA/2FA implementations
- Find login endpoints and authentication flows

### Passive Methods

**Subdomain Enumeration (in order of preference):**
1. **Chaos** (preferred) - Fast and comprehensive subdomain discovery
2. **Subfinder** - Multi-source subdomain enumeration with passive techniques
3. **AMASS** - In-depth asset enumeration and profiling with network mapping
4. **Gungir / Live Cert Tracker** - Real-time certificate monitoring and discovery

**Passive Tools:**
- **Shodan CLI** - Command-line interface for service discovery and technology signatures (leverage paid account)
- **Wappalyzer CLI** - Identify web technologies and frameworks installed
- **JARM** - TLS server fingerprinting for WAF and infrastructure identification
- **dig/nslookup** - DNS queries and zone transfer attempts

### Aggressive Methods

**Active Probing & Scanning Tools:**
- **dnsx** - DNS probing and validation of discovered subdomains
- **shuffledns** - DNS resolver with wildcard filtering and mass subdomain validation (use [Trickest resolvers](https://github.com/trickest/resolvers) for optimal results)
- **httpx** - HTTP/HTTPS probing, service validation, banner grabbing, and technology detection
- **Nmap** - Network scanning, service enumeration, version detection, and OS fingerprinting
- **Nuclei** - Technology fingerprinting and service identification via templates
- **Masscan** - High-speed internet port scanner for large-scale reconnaissance

---

## 2. Content Discovery

Identify hidden content, directories, endpoints, leaked data, and sensitive information.

### Passive Methods

- **GitHub/GitLab Searches**: Find exposed credentials, API keys, internal configurations, and source code leaks
- **Public Breach Databases**: HaveIBeenPwned, Breaches.io, LeakDB for compromised credentials and data leaks
- **Social Media Reconnaissance**: LinkedIn, Twitter, Facebook for employee info, tech stack clues, and organizational structure
- **Email Discovery**: Use Hunter.io, Clearbit, RocketReach to find employee emails and contact information
- **Wayback Machine**: Search for historical endpoints, directories, and leaked content
- **waybackurls** - Extract URLs from Wayback Machine for historical endpoint discovery
- **gau** - Get All URLs from Common Crawl, URLScan, and Otx
- **urlfinder** - Find URLs from JavaScript files and source code

### Aggressive Methods

**Active Crawling & Scanning Tools:**
- **httpx** - Probe discovered assets and validate HTTP endpoints for accessibility
- **Nuclei** - Template-based scanning for exposed content and misconfigurations
- **GitHub Search CLI**: Automated searching for credentials and sensitive data in repositories
- **katana** - Powerful crawling and spidering tool for web reconnaissance
- **hakrawler** - Simple web crawler for content and endpoint discovery
- **gospider** - Fast web spider for discovering endpoints and links
- **ParamSpider** - Discover parameters from crawled URLs

---

## 3. Monitoring & Notifications

Real-time monitoring and alerting for discovered vulnerabilities, new findings, and automation workflow status.

### Notification Methods

**Discord Integration:**
- Receive real-time alerts on new findings, vulnerabilities, and automation status
- Organize alerts by channel (assets, content, fingerprinting, etc.)
- Archive and track findings over time

**Monitoring Tools:**
- **Notify** - Unified notification tool for sending alerts to Discord, Slack, Telegram, and other platforms
  - Installation: `go install -v github.com/projectdiscovery/notify/cmd/notify@latest`
  - Configuration: Set Discord webhook URLs in notify configuration file
  - Usage: Pipe tool outputs to notify for real-time Discord alerts

**Recommended Setup:**
- Configure separate Discord channels for each reconnaissance phase
- Set up notification pipelines from tools (e.g., `subfinder | notify`, `nuclei | notify`)
- Monitor for critical findings in real-time
- Create automated backup/logging of all findings

---

## General Configuration

This section contains all configuration settings including tools.

### Alterx Configuration

**Alterx** - Subdomain permutation and alteration tool for discovering new subdomains through word mutations and pattern variations.

**Configuration File**: [`.config/alterx/alterx-large-practical-deep.yaml`](.config/alterx/alterx-large-practical-deep.yaml)

**Overview**:
- **Profile**: Large but practical AlterX configuration optimized for bug bounty and authorized reconnaissance
- **Design Goals**: High-signal permutations first, environment/service/cloud/region-aware naming, minimal brute-force noise
- **Use Case**: HackerOne/Bugcrowd style external attack-surface discovery

**Key Patterns**:
- Core dash and dot permutations with word, subdomain, environment, service, tech, and cloud variables
- No-separator permutations for alternative naming conventions
- Environment-aware patterns (dev, staging, prod, test, etc.)
- Service-aware patterns (api, mail, web, cdn, etc.)
- Cloud provider patterns (aws, azure, gcp, etc.)

**Usage**:
```bash
alterx -c .config/alterx/alterx-large-practical-deep.yaml -d target.com | dnsx
```

**Integration**: Pipe results to `dnsx` or `httpx` for validation and active probing in reconnaissance pipelines.