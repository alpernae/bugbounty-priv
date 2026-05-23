# Security Report Template

Use this structure for each validated finding.

## Markdown Template

````md
# [Vulnerability Title]

## Overview
- Severity: [CVSS score and rating]
- Category: [Vulnerability type]
- Affected Component: [Asset or system name]
- Discovery Date: [YYYY-MM-DD]

## Summary
[Technical root cause, trust boundary crossed, exploitability conditions, and impact.]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Proof of Concept
[Code or command examples demonstrating the vulnerability]


## References
- [Reference 1]
- [Reference 2]

## Impact
[Technical and business impact]
````

## Report File Path and Notes

Export reports by following structure. 

- security-reports/[vulnerability-class]/[report-title].md

Save same vulnerability class issues reports in the same directory.

For example:

|-- security-reports/
|    - /SSRF
|       - BlindSSRFonCallbackURL.md
|       - SSRFLeadingInternalAccess.md
|    - /SQLi
|       -/ ErrorBasedSqlionUserId.md
|