# MOSETY OPERATIONAL & TECHNICAL RISK REGISTER (AG002)

**Audit Date**: 28 September 2026  
**Auditor**: Antigravity Autonomous Coding Agent  
**Release Gate**: Risk identification, impact rating, and mitigation controls.

---

## Risk Assessment Matrix

| Risk ID | Category | Risk Description | Severity | Probability | Mitigation Strategy & Operational Controls |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R01** | **Brand Decontamination** | Unintended data corruption or deletion during automated database string replacement of legacy tokens. | High | Low | Create encrypted SQLite backup (`db.sqlite3.backup_decon`) before script execution; run test replacements in memory; verify record counts before and after. |
| **R02** | **Crescent Island Fee Volatility** | Crescent Island Sanctuary adjusts its official gate fees without advance notice, creating price discrepancy for travelers. | Medium | Medium | Display clear disclaimer distinguishing third-party gate fees from boat fees; link directly to official URL (`crescentisland.co/entry-fees`); timestamp last verification date. |
| **R03** | **SSL Hostname Mismatch** | PythonAnywhere SSL certificate is issued exclusively for `www.mosetyboatridesnaivasha.co.ke`. Submissions to GSC without `www` fail crawler validation. | Medium | High | Enforce canonical `https://www.mosetyboatridesnaivasha.co.ke` across all sitemaps, robots.txt, and canonical tags; instruct owner to register www prefix in GSC. |
| **R04** | **Review Integrity & Legal Compliance** | Displaying fabricated reviews or "Verified" badges without provenance violates consumer protection rules. | High | Low | Audit all displayed testimonials; remove placeholder reviews; only display reviews with documented permission and authentic guest feedback; remove arbitrary "4.9 (480+)" badge. |
| **R05** | **Maritime Safety & Weather** | Sudden lake squalls or high winds make afternoon departures hazardous; customer disappointment if trips are rescheduled. | High | Medium | Explicitly state on all ride pages and quotes that departures are weather-contingent and captain safety decisions are final; offer flexible reschedule or full refund. |
| **R06** | **Search Engine Keyword Stuffing Penalty** | Repeated unnatural keyword phrases ("the best boat ride Naivasha has to offer") degrade user trust and trigger search quality downgrades. | Medium | Low | Rewrite headings and body copy in natural Kenyan English, using the primary keyword once in title, H1, and first paragraph, and natural phrasing elsewhere. |
