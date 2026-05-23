# Web Security Workflows - Complete Index

Welcome to the enhanced web-security skill workflows. This directory contains everything you need to run autonomous web application security testing with decision-making and command execution.

## Quick Navigation

### For New Users
1. Start here: [PHASES_OVERVIEW.md](PHASES_OVERVIEW.md) — Understand the 4-phase workflow
2. Then: [AUTONOMOUS_EXECUTION.md](AUTONOMOUS_EXECUTION.md) — See how Codex executes each phase
3. Finally: Pick the phase document relevant to your needs

### For Implementation
- **Building the executor**: Refer to `AUTONOMOUS_EXECUTION.md` for orchestration logic
- **Customizing phases**: Edit individual phase documents for tool configuration
- **Adding new patterns**: Update `phase-2-passive-active-scanning.md` with new vulnerability classes

---

## Document Map

### Workflow Phases

| Document | Purpose | Audience |
|----------|---------|----------|
| [PHASES_OVERVIEW.md](PHASES_OVERVIEW.md) | High-level workflow structure, decision gates, phase summaries | Everyone |
| [AUTONOMOUS_EXECUTION.md](AUTONOMOUS_EXECUTION.md) | Detailed orchestration logic, decision trees, automation flow | Developers, architects |
| [phase-1-recon-fuzz-crawl.md](phase-1-recon-fuzz-crawl.md) | Reconnaissance, fuzzing, endpoint discovery, JS analysis | Security testers, pentesters |
| [phase-2-passive-active-scanning.md](phase-2-passive-active-scanning.md) | Pattern scanning, hypothesis generation, candidate filtering | Security testers |
| [phase-3-validating-issues.md](phase-3-validating-issues.md) | Finding validation, evidence collection, root cause analysis | Security testers |
| [phase-4-reporting.md](phase-4-reporting.md) | Report generation, remediation guidance, stakeholder communication | Everyone |

### Reference Materials

| Document | Purpose |
|----------|---------|
| [recon-and-mapping.md](recon-and-mapping.md) | Traditional manual reconnaissance workflow |
| [scope-and-authorization.md](scope-and-authorization.md) | Scope verification and authorization checks |

---

## Workflow Decision Tree

```
START: New Assessment?
  │
  ├─ YES → Do you have scope defined?
  │  ├─ NO → Use scope-and-authorization.md first
  │  └─ YES → Run PHASES_OVERVIEW.md → Choose entry point:
  │     ├─ Full Assessment → Start Phase 1
  │     ├─ Resume from Phase 2 → Load Phase 1 output, start Phase 2
  │     ├─ Test Specific Hypothesis → Jump to Phase 3
  │     └─ Generate Report Only → Jump to Phase 4
  │
  └─ NO → Improving existing assessment?
     ├─ Expand testing → Re-run Phase 2 with new patterns
     ├─ Validate new candidates → Run Phase 3
     └─ Update report → Run Phase 4 with new findings
```

---

## Entry Points for Different Use Cases

### Use Case 1: Full Automated Assessment (No Prior Work)

**Best for**: Fresh targets, comprehensive audits, automated scanning

**Path**:
1. Review [PHASES_OVERVIEW.md](PHASES_OVERVIEW.md) for high-level view
2. Confirm scope in [scope-and-authorization.md](scope-and-authorization.md)
3. Run [phase-1-recon-fuzz-crawl.md](phase-1-recon-fuzz-crawl.md) → Phase 2 → Phase 3 → Phase 4
4. Follow [AUTONOMOUS_EXECUTION.md](AUTONOMOUS_EXECUTION.md) orchestration

**Time**: 15-45 minutes (depending on target size)

---

### Use Case 2: Hypothesis Validation (Known Findings)

**Best for**: Validating specific suspected vulnerabilities, quick proof-of-concept

**Path**:
1. Review [phase-3-validating-issues.md](phase-3-validating-issues.md)
2. Use the validation pattern matching your vulnerability class
3. Generate report in [phase-4-reporting.md](phase-4-reporting.md)

**Time**: 5-15 minutes per finding

---

### Use Case 3: Endpoint Testing (Have Endpoint Inventory)

**Best for**: Testing new endpoints, regression testing after fixes

**Path**:
1. Load endpoint inventory (from Phase 1 output or manual)
2. Jump to [phase-2-passive-active-scanning.md](phase-2-passive-active-scanning.md)
3. Run Phase 3 & 4 as needed

**Time**: 10-30 minutes

---

### Use Case 4: Deep Recon (Unmapped Target)

**Best for**: Complex applications, hidden endpoints, undocumented APIs

**Path**:
1. Focus on [phase-1-recon-fuzz-crawl.md](phase-1-recon-fuzz-crawl.md)
2. Use Technique 4A & 4B extensively (JS analysis, API endpoint extraction)
3. Consider extending Phase 1 beyond standard steps

**Time**: 30-60 minutes

---

### Use Case 5: Custom Scanning Pattern (New Vulnerability Class)

**Best for**: Testing emerging vulnerabilities, framework-specific issues

**Path**:
1. Add new scanning technique to [phase-2-passive-active-scanning.md](phase-2-passive-active-scanning.md)
2. Add new validation pattern to [phase-3-validating-issues.md](phase-3-validating-issues.md)
3. Update [AUTONOMOUS_EXECUTION.md](AUTONOMOUS_EXECUTION.md) decision logic

---

## Phase Outputs & Data Flow

```
Phase 1 Output:
├─ endpoints_inventory.json (all discovered endpoints)
├─ parameters_matrix.json (params per endpoint)
├─ js_analysis.json (DOM patterns, hidden endpoints)
├─ quick_checks.json (unauthenticated access, CORS)
└─ phase_1_summary.md

        ↓ (consumed by Phase 2)

Phase 2 Output:
├─ passive_findings.json (info disclosure matches)
├─ sqli_candidates.json (SQL injection hypotheses)
├─ xss_candidates.json (XSS hypotheses)
├─ authz_candidates.json (authorization bypass hypotheses)
├─ ssrf_candidates.json (SSRF hypotheses)
├─ logic_candidates.json (business logic hypotheses)
├─ findings_candidates.json (consolidated, prioritized)
└─ phase_2_summary.md

        ↓ (consumed by Phase 3)

Phase 3 Output:
├─ validated_findings.json (reproduced findings only)
├─ suppressed_findings.json (false positives)
├─ unverified_findings.json (inconclusive tests)
└─ phase_3_summary.md

        ↓ (consumed by Phase 4)

Phase 4 Output:
├─ EXECUTIVE_SUMMARY.md
├─ DETAILED_REPORT.md
├─ REMEDIATION_ROADMAP.md
├─ findings.json (structured export)
├─ findings.csv (spreadsheet export)
└─ index.md (report index)
```

---

## Customization Guide

### Adding New Scanning Technique

To add a new technique (e.g., JWT validation):

1. **Add to Phase 2**: `phase-2-passive-active-scanning.md`
   ```markdown
   ### Technique 2F: JWT Validation Bypass
   
   ```bash
   # Commands here
   ```
   ```

2. **Add to Phase 3**: `phase-3-validating-issues.md`
   ```markdown
   ### Pattern 6: JWT Bypass Validation
   
   #### Step 1: ...
   ```

3. **Update Autonomous Executor**: `AUTONOMOUS_EXECUTION.md`
   ```python
   # Add to Phase 2 execution flow
   ├─ STAGE: JWT Validation Scanning
   #  └─ [code here]
   ```

4. **Update Decision Logic**: `AUTONOMOUS_EXECUTION.md`
   ```python
   # Add to scoring function
   if test_results.get('jwt_tamper_successful'):
       confidence += 0.4
   ```

---

## Common Issues & Solutions

### Issue: "Not enough endpoints found in Phase 1"

**Solution**: Check `phase-1-recon-fuzz-crawl.md` Technique 1A & 2B
- Use multiple subdomain discovery methods
- Check for API versions (/api/v1, /api/v2, etc.)
- Look for mobile API endpoints (/m, /mobile, /app)

### Issue: "High false positive rate in Phase 2"

**Solution**: Review `phase-2-passive-active-scanning.md`
- Use refined confidence scoring
- Check false-positive reduction rules in parent SKILL.md
- Add framework-specific mitigations

### Issue: "Phase 3 validation too slow"

**Solution**: In `AUTONOMOUS_EXECUTION.md`, customize autonomy settings:
```yaml
max_parallel_requests: 20  # Increase parallelism
timeout_per_request: 3    # Reduce timeout
stop_on_first_finding: true  # Stop early?
```

### Issue: "Need custom report format"

**Solution**: Extend `phase-4-reporting.md`
- Add custom template section
- Create script to transform findings.json to desired format

---

## Integration with Parent SKILL.md

The workflow documents **supplement** but **don't replace** the parent SKILL.md rules:

```
SKILL.md: Operating principles (do's and don'ts)
   ↑
Workflows: Executable implementation (how to)
   ↑
Individual scripts: Tool-specific execution (what commands to run)
```

**Always refer back to SKILL.md for**:
- Hard operating rules (#4: no production data corruption)
- Scope validation (#1-3: confirm authorization)
- Safe proof standards (#5-7: evidence collection rules)
- Output style guidelines

---

## Performance Benchmarks

Expected execution times (varies by target complexity):

| Phase | Time | Parallelizable? |
|-------|------|-----------------|
| Phase 1: Recon | 5-15 min | 80% (DNS, crawling) |
| Phase 2: Scanning | 10-30 min | 90% (parallel requests) |
| Phase 3: Validation | 5-15 min | 50% (sequential) |
| Phase 4: Reporting | 2-5 min | 95% (report generation) |
| **Total** | **20-60 min** | - |

---

## Command Examples

### Run full assessment
```bash
codex audit https://target.com --phases all
```

### Resume from specific phase
```bash
codex audit https://target.com --phases 2,3,4 --phase1-output endpoints_inventory.json
```

### Validate single finding
```bash
codex validate --type sql-injection --endpoint "/api/users?id=" --payload-file sqli_payloads.txt
```

### Generate custom report
```bash
codex report --findings validated_findings.json --format html,pdf --template custom_template.md
```

---

## FAQ

**Q: Can I run phases in parallel?**  
A: No, phases must run sequentially (Phase 1 output feeds Phase 2, etc.). However, within each phase, many techniques run in parallel.

**Q: How often should I reassess?**  
A: Recommend quarterly for active targets, or after major code changes. Use `phase-2-passive-active-scanning.md` for faster re-scans.

**Q: Can I skip phases?**  
A: Yes, if you have prior outputs. E.g., if you have `endpoints_inventory.json` from Phase 1, you can start at Phase 2.

**Q: How do I handle rate limiting?**  
A: In `AUTONOMOUS_EXECUTION.md` autonomy settings, increase `rate_limit_delay`. Phase 2 will automatically backoff on 429 responses.

**Q: How do I report findings to developers?**  
A: Use outputs from `phase-4-reporting.md`. Executive summary goes to managers, detailed report to developers.

---

## Support & Updates

For issues or feature requests:
1. Review the relevant phase document
2. Check SKILL.md hard rules
3. Consult `AUTONOMOUS_EXECUTION.md` error handling section
4. Update document with new learnings

---

Last Updated: 2025-05-15  
Status: Production-Ready
