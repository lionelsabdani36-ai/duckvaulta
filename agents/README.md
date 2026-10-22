# Autonomous AI Engineering Team Architecture

The Duckvaulta platform is developed and maintained by a 5-agent autonomous team running on Hermes Agent multi-profile orchestration.

---

## 👥 Agent Roster

| Profile Slug | Role | Mission & Responsibilities | Workstation |
| :--- | :--- | :--- | :--- |
| **Leader** (`default`) | Chief Orchestrator | Technical coordination, prompt dispatch, and platform strategy. | Desk 1 (Command) |
| **trend-hunter** | Market Intelligence | Continuous internet recon for emerging tech, EdTech trends, and viral demand. | Lounge Seat 5 |
| **fullstack-dev** | Core Web Developer | Full-stack engineering, responsive UI/UX, and API integration. | Desk 2 (Engineering) |
| **qa-engineer** | Quality Assurance | Cross-viewport regression testing, interactive sandbox auditing, and accessibility checks. | Lounge Seat 3 |
| **security-engineer** | Cyber Defense | Hardening server configs, verifying TLS 1.3 compliance, and session protection. | Lounge Seat 4 |

---

## 🔄 Automated Workflows & Telemetry

* **Kanban Task Coordination:** Tasks are tracked in an SQLite-backed Kanban board (`hermes kanban`) with automated claim/execute/review lifecycles.
* **Daily Cron Jobs:**
  * `08:00 WIB (01:00 UTC)`: EdTech AI platform daily update (`edtech-ai-daily-update`).
  * `Every 12h`: Trend Hunter market signals digest (`trend-hunter-daily`).
  * `Every 6h`: QA smoke tests on live endpoints (`qa-web-smoke-test`).
  * `Every 4h`: VPS security audits and telemetry scan (`security-vps-audit`).
* **3D Spatial Telemetry:** Live agent status and task states are reflected in real-time on the 3D virtual office at `https://aicompany.duckvaulta.ai.id`.
