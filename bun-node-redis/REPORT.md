# Final HEAD BullMQ Bun and Node Redis verification

Final HEAD `2e5ecf53615fd799d0c660d3b8bb8a5af579ccf7`, tree `0503ca913f5b3b71b081f7912a497fe635317d67`, base `09b7bfeb8653e74074542ca48e70477540742a7e`. Source archive SHA256 `7bc67762360cab5ec31cc6f42e95cbc9c8d2401364a40b5129cf5bf2e10193a3`. All 1068 Git tree blobs/modes/symlinks match the frozen v2 archive; source verified again unchanged after all tests.

| Official gate | Exit | Actual result |
| --- | --- | --- |
| `yarn build` | 0 | Build completed |
| `yarn test:bun:smoke` | 0 | 19 passed, 0 failed, 2 files |
| `yarn test:bun` | 0 | 47 passed (47); 1092 passed , 2 skipped (1094) |
| `yarn test:adapter-conformance` | 0 | 1 passed (1); 66 passed (66) |
| `yarn test:node-redis` | 0 | 49 passed (49); 1114 passed , 3 skipped (1117) |

These are actual local runtime results for final HEAD, not GitHub Actions status. Existing official exclusions/skips remain explicit and are not passing assertions. Six ChildProcessor cases are EventEmitter/wrapJob protocol unit tests, not real IPC/Redis evidence. Existing v1 installed-package lifecycle observations retain their original revision labels.

Node 24.22.1 / Yarn 1.22.22 / Bun 1.4.4 / Redis 7.4.11. Dependency installation was reused from the exact frozen v1 install after package.json and yarn.lock byte equality was proved; lock SHA256 `352db92214415193667c493636408682bb3fb612775c70df81e5522f6b76cb4f`. Bun and Node Redis used the same final frozen source and the same independently owned Redis network namespace sequentially; no runtime lanes overlapped Redis. Redis reset targeted only owner-verified ID `87c43361f57b318fbe168cab1f1b9a7279b5bc57a5b7a3fed6ed0f9b8fb6bfa0`.

Redis `ghpr-0902-bullmq-bun-root-redis7`, host-only mapping `127.0.0.1:45261`; runner `ghpr-0902-bullmq-bun-root-runner`; owner label `bullmq-bun-root`. Full image digests, IDs and configuration are retained in prior runtime-summary.json and this directory's final-identities.log. Both containers remain available for root verification/cleanup.

Semantic review was carried forward only after two-file formatter byte delta, syntax-equivalence proof, four other unchanged file hashes and entire final HEAD tree mapping were verified. No evidence-backed blocking findings. The first HEAD precheck safely stopped before root finished host import; no build/tests ran in that attempt. Its exact boundary is retained in mapping-first-attempt.json. Bun test-reported duration and Docker CLI completion differed due to output/client closeout latency. A bounded Docker event-history query returned no historical rows; it was not used as proof of success. Completed gate output plus actual exit code 0 establish the result. Owned runner OOMKilled was false and memory.events OOM counters were 0. No tests were duplicated or containers terminated during diagnosis. No product edits, source formatting, commits, pushes or GitHub state writes were performed by this lane.

Raw command output, full argv, timestamps and exit codes are retained per gate. `final-head-gate-summary.json` is the machine-readable result; `independent-source-review.json` carries review provenance and boundaries. `evidence-sha256.json` covers this v2 evidence set; all v1 records remain historical and unchanged.
