# Duckvaulta Smoke Test Report

Generated: 2026-10-27T04:48:24.239+00:00
Timeout per target: 8.0 seconds

## Summary

| Metric | Value |
| --- | ---: |
| Targets tested | 23 |
| Passed | 23 |
| Failed | 0 |
| Pass rate | 100.0% |
| Latency p50 | 10.323 ms |
| Latency p95 | 16.595 ms |
| Latency p99 | 24.128 ms |
| Slowest | https://godeye.duckvaulta.ai.id/ (26.175 ms) |
| Fastest | http://127.0.0.1:80/ (0.295 ms) |

## Target Results

| Target | Status | Pass | DNS ms | TCP ms | TLS ms | TTFB ms | Total ms | Bytes | KB/s | SHA-256 |
| --- | ---: | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| https://duckvaulta.ai.id/ | 200 | yes | 1.731 | 0.354 | 10.236 | 0.967 | 14.116 | 90074 | 131370.248 | cfbf45b01444f1cd32e6801b2071e3e310dd6b927c620475798867f51ee05374 |
| https://duckvaulta.ai.id/api/health.json | 200 | yes | 0.507 | 0.233 | 8.166 | 0.658 | 9.7 | 154 | 11595.268 | a819dc248973ca7590bce0e95b1dce29d37c39127661c22a07a5f13b17dccf54 |
| https://duckvaulta.ai.id/api/services.json | 200 | yes | 0.483 | 0.224 | 8.132 | 0.667 | 9.629 | 1703 | 141780.557 | 00ec7ea7a927e610932414800355c3fa04c7fe8e8b440c54bf348b0dac3eeeb4 |
| https://duckvaulta.ai.id/api/telemetry.json | 200 | yes | 0.466 | 0.219 | 8.63 | 0.709 | 10.186 | 9996 | 316425.243 | bebf8cb02844e6b5bf476939069848fa85ef5e167adc9bc6feaa574ed46a2d81 |
| https://aicompany.duckvaulta.ai.id/ | 200 | yes | 0.537 | 0.24 | 8.176 | 1.528 | 10.611 | 1025 | 79632.185 | 365d9e684fbbf958ad1bc958373f0b4b72285c233e2a2dc18c8dd12ff7b74199 |
| https://godeye.duckvaulta.ai.id/ | 200 | yes | 0.497 | 0.219 | 8.061 | 16.642 | 26.175 | 85579 | 137632.559 | 56021e634824be0e6e00f4036d5738d6d97ce37583fa34d83773ff29c11b21a3 |
| https://edtech.duckvaulta.ai.id/ | 200 | yes | 0.568 | 0.268 | 8.447 | 1.04 | 11.017 | 105238 | 179432.021 | 9a6d63f93feb806274343a15bb831f1aec72ee383f79a3f70c8632260bb722a4 |
| https://duckvaulta.ai.id/assets/logo.png | 200 | yes | 0.49 | 0.25 | 9.816 | 0.947 | 11.97 | 110087 | 308838.943 | 91ac19ad23e8e40ac7daab4900dafaf3b8f4f85ac41ef4ca1a0ed523b0ef6a3b |
| https://duckvaulta.ai.id/assets/duck-lockup.png | 200 | yes | 0.511 | 0.241 | 8.45 | 0.991 | 10.7 | 88559 | 228013.917 | 195fc35289ca56e24e494c108385d682d2eae424250b262f1730c43355a8a2ee |
| https://duckvaulta.ai.id/assets/logo-transparent.png | 200 | yes | 0.476 | 0.244 | 8.13 | 0.929 | 10.323 | 128334 | 303732.664 | 29017cf0a180753719f64a2148d3830bb772831b3f9b71936f3a949d2a58cdbb |
| https://duckvaulta.ai.id/assets/anime.min.js | 200 | yes | 0.46 | 0.224 | 8.249 | 0.842 | 9.937 | 17384 | 442789.841 | bceef94f964481f7680d95e7fbbe5a8c20d3945a926a754874898a578db7c7ab |
| https://duckvaulta.ai.id/assets/duck-emblem.png | 200 | yes | 0.461 | 0.233 | 8.387 | 1.776 | 11.106 | 39618 | 446605.715 | 03f69ec4e37e6d4988fcd98e756c95803b69c729c6fd5d20795f992c21cc9a86 |
| https://duckvaulta.ai.id/ctf-challenges/66-dont-use-client-side/index.html | 200 | yes | 0.58 | 0.672 | 8.827 | 0.64 | 10.873 | 3806 | 229149.006 | fcffad789df4f1e230c0c7109a6a4a270e984e2c085e3affbd66582b886f3d41 |
| https://duckvaulta.ai.id/ctf-challenges/779-perceptron/index.html | 200 | yes | 0.494 | 0.243 | 8.179 | 0.878 | 9.939 | 15906 | 553571.031 | 18489343bf7592d8d7b037e30a488d6d45637c9999ae69af5a80593e1e2d6750 |
| https://duckvaulta.ai.id/ctf-challenges/405-blame-game.zip | 200 | yes | 0.481 | 0.255 | 8.209 | 0.904 | 11.143 | 296464 | 243384.523 | 56bea5dbbfda90bfc2b1ce28ff84d914eb9cf9b5e44c2ada3f59d05a63e4d227 |
| https://duckvaulta.ai.id/drawio/index.html | 200 | yes | 0.442 | 0.228 | 8.146 | 2.014 | 10.992 | 16759 | 405606.219 | 6c058ceca2127067f1c4859f3e153fc0962efb4448248bc6797dd844fd037a12 |
| http://127.0.0.1:80/ | 301 | yes | 0.014 | 0.062 | n/a | 0.139 | 0.295 | 162 | 15124.582 | 9e17cb15dd75bbbd5dbb984eda674863c3b10ab72613cf8a39a00c3e11a8492a |
| http://127.0.0.1:3001/ | 200 | yes | 0.01 | 0.042 | n/a | 0.887 | 1.016 | 1025 | 81446.425 | 365d9e684fbbf958ad1bc958373f0b4b72285c233e2a2dc18c8dd12ff7b74199 |
| http://127.0.0.1:4173/ | 200 | yes | 0.013 | 0.055 | n/a | 16.573 | 16.871 | 85579 | 665710.07 | 56021e634824be0e6e00f4036d5738d6d97ce37583fa34d83773ff29c11b21a3 |
| http://127.0.0.1:20128/ | 307 | yes | 0.023 | 0.062 | n/a | 1.644 | 1.846 | 10 | 399.086 | 89347bb23a645278522a8cfd5dd8001ca6b244aa6898972d5af26a6dbaf33f55 |
| http://127.0.0.1:20128/dashboard | 307 | yes | 0.011 | 0.044 | n/a | 0.842 | 0.979 | 6 | 410.608 | 7e93fba0bc7adda858a2500090e639e4f563a3965c7cf4c719fb56eb6b12c666 |
| http://127.0.0.1:3005/ | 200 | yes | 0.009 | 0.041 | n/a | 0.295 | 0.416 | 74 | 8654.566 | 8b5830ca3734a9e07f7d32ff39dab50c59e32405ebba91d4a73f3c8520a622af |
| http://127.0.0.1:11434/api/version | 200 | yes | 0.009 | 0.052 | n/a | 0.315 | 0.484 | 20 | 1350.709 | 576f54710b38affc33858b6ef1f2a35e9b38c6c49535143bdec153afad5d8830 |

## Security Header Audit

Presence is checked from the response headers. A missing header is recorded as `no`.

| Target | HSTS | CSP | X-Frame-Options | X-Content-Type-Options | Referrer-Policy | CORS |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| https://duckvaulta.ai.id/ | yes | yes | yes | yes | yes | no |
| https://duckvaulta.ai.id/api/health.json | yes | yes | yes | yes | yes | no |
| https://duckvaulta.ai.id/api/services.json | yes | yes | yes | yes | yes | no |
| https://duckvaulta.ai.id/api/telemetry.json | yes | yes | yes | yes | yes | no |
| https://aicompany.duckvaulta.ai.id/ | yes | no | yes | yes | yes | no |
| https://godeye.duckvaulta.ai.id/ | yes | yes | yes | yes | yes | no |
| https://edtech.duckvaulta.ai.id/ | yes | yes | yes | yes | yes | no |
| https://duckvaulta.ai.id/assets/logo.png | yes | no | yes | yes | yes | no |
| https://duckvaulta.ai.id/assets/duck-lockup.png | yes | no | yes | yes | yes | no |
| https://duckvaulta.ai.id/assets/logo-transparent.png | yes | no | yes | yes | yes | no |
| https://duckvaulta.ai.id/assets/anime.min.js | yes | yes | yes | yes | yes | no |
| https://duckvaulta.ai.id/assets/duck-emblem.png | yes | no | yes | yes | yes | no |
| https://duckvaulta.ai.id/ctf-challenges/66-dont-use-client-side/index.html | no | no | no | no | no | no |
| https://duckvaulta.ai.id/ctf-challenges/779-perceptron/index.html | no | no | no | no | no | no |
| https://duckvaulta.ai.id/ctf-challenges/405-blame-game.zip | no | no | no | no | no | no |
| https://duckvaulta.ai.id/drawio/index.html | yes | yes | yes | yes | yes | no |
| http://127.0.0.1:80/ | no | no | no | no | no | no |
| http://127.0.0.1:3001/ | no | no | no | no | no | no |
| http://127.0.0.1:4173/ | no | yes | yes | yes | no | no |
| http://127.0.0.1:20128/ | no | no | no | no | no | no |
| http://127.0.0.1:20128/dashboard | no | no | no | no | no | no |
| http://127.0.0.1:3005/ | no | no | no | no | no | no |
| http://127.0.0.1:11434/api/version | no | no | no | no | no | no |

## Errors

No probe errors.

## Crawl

Crawl source: remote_homepage
References discovered: 2
Unique discovered targets probed: 2

Telemetry file: `smoke_test_telemetry.json`
