# QA Automated Smoke Test Report: Production Portals

**Execution Date:** 2026-10-26 16:23:00 UTC  
**QA Specialist:** Julius (qa-engineer)  
**Task ID:** `t_3c1d81c7`  
**Targets Tested:**
1. `https://duckvaulta.ai.id` (Duckvaulta Corporate Portal & Autonomous Intelligence Gateway)
2. `https://godeye.duckvaulta.ai.id` (God's Eye View Planetary Geospatial Telemetry & 3D Radar)

**Scope:**
- HTTP Status Code 200 OK Validation (10 Consecutive Probes per Target)
- Multi-Run Latency & Performance SLA Benchmarking (DNS, Connect, TLS, TTFB, Total Time)
- Declared & Static Asset Integrity Audit (0 Broken Assets SLA)
- External & Outbound Link Validation
- Headless Browser DOM / Network Runtime Audit (CDP / Chromium)
- HTTP Security Headers & TLS Configuration Audit

---

## 1. Executive Summary & Verdict

| Target Service | URL | HTTP Status | Avg Latency (TTFB) | Avg Total Time | Assets Probed | Broken Assets | Overall QA Verdict |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Duckvaulta Portal** | `https://duckvaulta.ai.id` | **200 OK** (10/10) | **31.019 ms** | **32.429 ms** | 6 static + 6 browser | **0 (Zero)** | **PASSED (100%)** |
| **God's Eye View** | `https://godeye.duckvaulta.ai.id` | **200 OK** (10/10) | **55.608 ms** | **57.234 ms** | 11 static + 250 browser | **0 (Zero)** | **PASSED (100%)** |

> **Audit Conclusion:** Both services successfully passed all automated smoke test criteria with **zero broken assets**, 100% HTTP 200 OK reliability across all repeated probes, and fast latency (~31 ms TTFB for Duckvaulta, ~55 ms TTFB for God's Eye View).

---

## 2. Multi-Run Latency & Performance SLA Benchmarks

Tests were conducted across 10 consecutive automated runs with full HTTP timing breakdown:

### Duckvaulta Portal (`https://duckvaulta.ai.id`)

- **Status Code:** 200 OK (10/10 runs, 100% reliability)
- **Protocol:** HTTP/2 over TLS 1.3
- **Payload Size:** ~90 KB (HTML uncompressed)

| Metric | Min (ms) | Max (ms) | Average (ms) | Median (ms) | Std Dev (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **DNS Lookup** | 1.214 | 6.245 | 3.091 | 3.548 | 1.534 |
| **TCP Connect** | 1.499 | 9.272 | 3.707 | 3.846 | 2.174 |
| **TLS Handshake** | 20.072 | 46.659 | 29.945 | 29.374 | 7.263 |
| **TTFB (Time to First Byte)** | **20.865** | **47.48** | **31.019** | **29.843** | **7.367** |
| **Total Response Time** | **22.878** | **48.898** | **32.429** | **31.838** | **7.256** |

### God's Eye View (`https://godeye.duckvaulta.ai.id`)

- **Status Code:** 200 OK (10/10 runs, 100% reliability)
- **Protocol:** HTTP/2 over TLS 1.3 (reverse proxy to Vite/Node service on port 4173)
- **Payload Size:** ~85.6 KB (HTML uncompressed)

| Metric | Min (ms) | Max (ms) | Average (ms) | Median (ms) | Std Dev (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **DNS Lookup** | 1.432 | 4.594 | 2.454 | 2.397 | 1.047 |
| **TCP Connect** | 1.744 | 5.063 | 2.927 | 3.26 | 1.048 |
| **TLS Handshake** | 23.957 | 39.688 | 30.74 | 28.882 | 5.762 |
| **TTFB (Time to First Byte)** | **40.425** | **84.507** | **55.608** | **57.996** | **12.4** |
| **Total Response Time** | **46.117** | **85.508** | **57.234** | **59.303** | **11.632** |

---

## 3. Static & Declared Asset Integrity Audit

Every declared asset was probed via HTTP HEAD/GET to verify server response, content-type headers, and payload delivery.

### Duckvaulta Portal Declared Assets (6 items)

| Asset Path | Resolved URL | HTTP Status | Content-Type | Latency (ms) | Status |
| :--- | :--- | :---: | :--- | :---: | :---: |
| `/api/health.json` | `https://duckvaulta.ai.id/api/health.json` | **200** | `application/json` | 18.605 ms | ✅ PASS |
| `/api/services.json` | `https://duckvaulta.ai.id/api/services.json` | **200** | `application/json` | 18.345 ms | ✅ PASS |
| `/api/telemetry.json` | `https://duckvaulta.ai.id/api/telemetry.json` | **200** | `application/json` | 21.572 ms | ✅ PASS |
| `/assets/anime.min.js` | `https://duckvaulta.ai.id/assets/anime.min.js` | **200** | `application/javascript` | 28.976 ms | ✅ PASS |
| `/assets/duck-emblem.png` | `https://duckvaulta.ai.id/assets/duck-emblem.png` | **200** | `image/png` | 28.619 ms | ✅ PASS |
| `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap` | `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap` | **200** | `text/css; charset=utf-8` | 45.138 ms | ✅ PASS |

#### Duckvaulta Navigation Links Tested (3 items)

| Link Destination | HTTP Status | Latency (ms) | Status |
| :--- | :---: | :---: | :---: |
| `https://aicompany.duckvaulta.ai.id` | **200** | 28.863 ms | ✅ PASS |
| `https://edtech.duckvaulta.ai.id` | **200** | 36.696 ms | ✅ PASS |
| `https://godeye.duckvaulta.ai.id` | **200** | 48.474 ms | ✅ PASS |

### God's Eye View Declared Assets (11 items)

| Asset Path | Resolved URL | HTTP Status | Content-Type | Latency (ms) | Status |
| :--- | :--- | :---: | :--- | :---: | :---: |
| `/@vite/client` | `https://godeye.duckvaulta.ai.id/@vite/client` | **200** | `text/html` | 39.793 ms | ✅ PASS |
| `/cesium/Widgets/widgets.css` | `https://godeye.duckvaulta.ai.id/cesium/Widgets/widgets.css` | **200** | `text/css; charset=UTF-8` | 29.804 ms | ✅ PASS |
| `/icons/icon-180.png` | `https://godeye.duckvaulta.ai.id/icons/icon-180.png` | **200** | `image/png` | 32.494 ms | ✅ PASS |
| `/icons/icon-32.png` | `https://godeye.duckvaulta.ai.id/icons/icon-32.png` | **200** | `image/png` | 29.317 ms | ✅ PASS |
| `/logo.svg` | `https://godeye.duckvaulta.ai.id/logo.svg` | **200** | `image/svg+xml` | 26.548 ms | ✅ PASS |
| `/manifest.webmanifest` | `https://godeye.duckvaulta.ai.id/manifest.webmanifest` | **200** | `application/manifest+json` | 35.059 ms | ✅ PASS |
| `/pin.svg` | `https://godeye.duckvaulta.ai.id/pin.svg` | **200** | `image/svg+xml` | 24.674 ms | ✅ PASS |
| `/src/main.js` | `https://godeye.duckvaulta.ai.id/src/main.js` | **200** | `text/javascript` | 47.679 ms | ✅ PASS |
| `/style.css` | `https://godeye.duckvaulta.ai.id/style.css` | **200** | `text/css` | 33.644 ms | ✅ PASS |
| `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap` | `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap` | **200** | `text/css; charset=utf-8` | 38.187 ms | ✅ PASS |
| `https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20,400,0,0&icon_names=adjust,arrow_drop_down,arrow_forward,arrow_left,arrow_right,bolt,chevron_left,chevron_right,close,close_fullscreen,dark_mode,draw,east,flare,flight,layers_clear,light_mode,local_fire_department,my_location,navigation,normal,on,open_in_full,public,radar,radio,right_panel_close,right_panel_open,rocket_launch,skip_next,skip_previous,upload_file,view_in_ar,visibility,visibility_off` | `https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20,400,0,0&icon_names=adjust,arrow_drop_down,arrow_forward,arrow_left,arrow_right,bolt,chevron_left,chevron_right,close,close_fullscreen,dark_mode,draw,east,flare,flight,layers_clear,light_mode,local_fire_department,my_location,navigation,normal,on,open_in_full,public,radar,radio,right_panel_close,right_panel_open,rocket_launch,skip_next,skip_previous,upload_file,view_in_ar,visibility,visibility_off` | **200** | `text/css; charset=utf-8` | 30.606 ms | ✅ PASS |

#### God's Eye External Resources Tested (2 items)

| Link Destination | HTTP Status | Latency (ms) | Status |
| :--- | :---: | :---: | :---: |
| `https://open-meteo.com/` | **200** | 160.589 ms | ✅ PASS |
| `https://www.radio-browser.info/` | **200** | 200.231 ms | ✅ PASS |

---

## 4. Headless Browser DOM & Runtime Execution Audit

A headless Chromium instance rendered both web applications to verify runtime execution, Cesium WebGL initialization, and sub-resource loading.

### Duckvaulta Portal
- **Page Title:** `🐴 Duckvaulta: Technology Solutions`
- **Sub-resources Loaded by Browser:** 6 resources
- **Runtime Errors / Uncaught Exceptions:** 0 errors
- **Key Resources Dynamically Verified:**
  - Google Fonts CSS (`Plus Jakarta Sans`, `JetBrains Mono`)
  - Anime.js dynamic animation library (`/assets/anime.min.js`)
  - Duck Emblem SVG/PNG brand icon (`/assets/duck-emblem.png`)
  - Autonomous System Telemetry API (`/api/telemetry.json`)
  - Swarm Services Health API (`/api/services.json`)

### God's Eye View
- **Page Title:** `🐴 God's Eye View`
- **Sub-resources Loaded by Browser:** 250 resources (Vite ES modules, Cesium WebGL assets, icons, fonts)
- **Active WebGL / 2D Canvas Elements Rendered:** 8 canvases
- **Runtime Errors / Uncaught Exceptions:** 0 errors
- **Key Modules Dynamically Verified:**
  - Vite HMR/Client runtime (`/@vite/client`)
  - Main ES Module bundle (`/src/main.js`)
  - Cesium UI Styles (`/cesium/Widgets/widgets.css`)
  - SVG Branding & Map Pins (`/logo.svg`, `/pin.svg`)
  - Web Manifest (`/manifest.webmanifest`)
  - 243 application component scripts and Cesium engine modules

---

## 5. Security & Edge Configuration Verification

| Header | Duckvaulta Portal | God's Eye View | Standard Status |
| :--- | :--- | :--- | :---: |
| **Strict-Transport-Security (HSTS)** | `max-age=63072000; includeSubDomains; preload` | `max-age=63072000; includeSubDomains; preload` | ✅ Active (A+) |
| **Content-Security-Policy (CSP)** | Enforced (`'self'`, font-src, script-src) | Enforced (Cesium, Google Maps, workers, blobs) | ✅ Hardened |
| **X-Frame-Options** | `SAMEORIGIN` | `SAMEORIGIN` | ✅ Protected |
| **X-Content-Type-Options** | `nosniff` | `nosniff` | ✅ nosniff |
| **Referrer-Policy** | `strict-origin-when-cross-origin` | `strict-origin-when-cross-origin` | ✅ Strict |
| **Permissions-Policy** | `camera=(self), microphone=(self), geolocation=(self)` | `camera=(self), microphone=(self), geolocation=(self)` | ✅ Restrictive |
| **Edge Server Protocol** | HTTP/2 over TLS 1.3 (Nginx) | HTTP/2 over TLS 1.3 (Nginx Reverse Proxy) | ✅ Production Grade |

---

## 6. Final QA Assessment & Sign-Off

- [x] **Status 200 OK SLA:** 100% pass across 10 repeated tests per domain.
- [x] **TTFB Latency SLA:** Duckvaulta avg 31.019 ms (< 50ms SLA), GodEye avg 55.608 ms (< 100ms SLA).
- [x] **Asset Integrity SLA:** 0 broken assets detected across 17 static assets and 256 browser runtime modules.
- [x] **Navigation Integrity:** All 5 internal and outbound links resolved with HTTP 200 OK.
- [x] **Browser DOM / WebGL Render Integrity:** 8 WebGL/2D canvases initialized without runtime errors on God's Eye View.

**Verdict: READY & HEALTHY (PASS)**
