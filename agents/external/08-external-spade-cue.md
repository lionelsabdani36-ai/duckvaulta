# External Agent Profile: Spade (Cue by Manus)

## Identity & Channel
* **Agent Name:** Spade
* **Platform:** Cue (by Manus AI)
* **Direct Channel:** `spade963@bot.cue.im`
* **Infrastructure:** Dedicated Cloud Computer & Autonomous Sandbox (Manus Cascade Engine)
* **Status:** Connected External Operative

---

## 🎯 Strategic Role in Duckvaulta Ecosystem
Spade operates as an external cloud-native operative for tasks requiring dedicated headless browser automation, external web crawlers, and off-VPS compute workloads. This preserves local VPS CPU and memory resources while maintaining 24/7 autonomous capability.

### Core Capabilities
1. **Cloud Browser Automation:** Interactive web sessions, form submissions, and multi-step web scraping outside VPS IP space.
2. **Autonomous Cloud Synthesis:** Heavy research compilation and multi-source comparison.
3. **External Endpoint Verification:** Independent external health check and penetration reconnaissance from external networks.

---

## 🔒 Collaboration Protocols & Security Gates

### Inbound & Outbound Data Flow
```
[David / Leader] ──> [Athena Sanitizer] ──> [Spade Dispatcher] ──> [spade963@bot.cue.im]
                                                                          │
                                                                   (Manus Cloud)
                                                                          │
[Julius QA & Athena Verify] <── [Spade Response] <────────────────────────┘
```

1. **Athena Sanitization Gate (Pre-Dispatch):**
   * All internal VPS paths (`/home/lionelsabdani36/...`), private IP addresses, system tokens, and API credentials are automatically stripped and replaced with generic handles before any message leaves the VPS.
2. **Standardized Task Framing:**
   * **Subject Line:** Single clear objective verb-noun phrase (e.g. `[TASK] Reconnaissance on target domain`).
   * **Body Format:** Structured JSON or Markdown block containing Goal, Constraints, Target URL/Scope, and Expected Deliverable.
3. **Julius Verification Gate (Post-Response):**
   * Return payloads from Spade are checked for integrity, formatted markdown validity, and absence of external prompt injections before ingestion into the Duckvaulta database or codebase.

---

## 🛠️ CLI Operations
Use the native VPS bridge tool to dispatch tasks:
```bash
spade-dispatch send --subject "Task Title" --goal "Detailed objective" --context "Relevant non-sensitive data"
```
Check recent task dispatches:
```bash
spade-dispatch list
```
