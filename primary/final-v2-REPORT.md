# BullMQ #4168 final local validation

Final commit `2e5ecf53615fd799d0c660d3b8bb8a5af579ccf7`, tree `0503ca913f5b3b71b081f7912a497fe635317d67`, base `09b7bfeb8653e74074542ca48e70477540742a7e`. Six changed files and all 1068 source entries are verified. Product code is frozen.

Status: **ALL_APPLICABLE_FINAL_V2_LOCAL_GATES_PASSED**. No GitHub CI or publication claim is made.

| Gate | Actual final result |
| --- | --- |
| `final-v2-primary-quality-coverage` | exit0; Test Files  6 passed (6); Tests  86 passed \| 2 skipped (88); Test Files  54 passed (54); Tests  1315 passed \| 14 skipped (1329); All files          \|   89.52 \|    80.71 \|   87.88 \|   89.76 \| |
| `final-v2-node24-redis6` | exit0; Test Files  49 passed (49); Tests  1114 passed \| 3 skipped (1117); Test Files  6 passed (6); Tests  206 passed \| 11 skipped (217) |
| `final-v2-valkey8` | exit0; Test Files  49 passed (49); Tests  1114 passed \| 3 skipped (1117) |
| `final-v2-dragonfly` | exit0; Test Files  49 passed (49); Tests  1114 passed \| 3 skipped (1117) |
| `final-v2-postgres-pack` | exit0; Test Files  8 passed (8); Tests  154 passed (154) |
| `final-v2-installed-byte-verification` | exit0;  |
| `final-v2-public-install` | exit0;  |
| `final-v2-public-retry-slow` | exit0;  |
| `final-v2-strong-requested-at` | exit0;  |
| `node20-redis7` | exit0; default: 49 files / 1114 passed / 3 upstream skipped; ioredis: 6 files / 206 passed / 11 upstream skipped |
| `node22-redis7` | exit0; default: 49 files / 1114 passed / 3 upstream skipped; ioredis: 6 files / 206 passed / 11 upstream skipped |
| Bun 1.4.4 / NodeRedis | build0; Bun smoke19; full1092 passed/2 upstream skips; adapter66; NodeRedis1114/3 upstream skips |
| ValkeyGLIDE 2.5.0 | passed; Test Files  48 passed (48); Tests  1093 passed \| 3 skipped (1096) |

Node LTS versions: 24.22.1, 22.23.4, 20.20.2; Yarn1.22.22. Primary Redis7.4.11; Redis6.2.24; Valkey8.0.1; PostgreSQL16.15; Dragonfly df-v2.0.2-8ce4bbb106586057fbd85f71ed353c60d0d5bf87. Exact Docker identities, image versions/digests, commands, timestamps and exit codes are in the indexed records.

The primary coverage run passed 1315 tests/54 files, with14 upstream skips. Coverage statements89.52%, branches80.71%, functions87.88%, lines89.76%; all configured thresholds passed. Smoke86 passed/2 upstream skips. Default49files+six ioredis files overlap one file; do not add raw suite counts as distinct tests.

## Genuine before/after and installed runtime

Exact baseline `09b7bfeb8653e74074542ca48e70477540742a7e` built successfully. The four new real Redis fork/thread regressions fail on baseline (`runtime/baseline-new-regressions-v2.log`), and pass in the final full Redis suites. The99 filtered-out tests in that baseline focused run are not new skips.

The final clean installed package has805 files, all SHA256-matched on Linux and Windows. Artifact SHA256 `d14b6b2ce3a64dccd7950860eb2b757e093bbf74735ea3ec7790bb43bf9b9f8e`. Inventory: `runtime/artifact-final-v2-manifest.json`.

Linux Node24.22.1/Redis7.4.11 and Windows Node24.14.0/npm11.16.0/Redis8.10.0 each passed750 actual Queue.getJob visibility observations with0 stale reads. Actual backend BigInt serialization errors are catchable in fork/thread; uncloneable send failures preserve local data and clean listeners. Actual5500ms WRITE pauses complete without a new5s timeout; retry history is[0,1,2]. Same real child is reused after cancellation/error/sendfailure; listeners remain1 and AbortSignal resets.

Four actual Update-pending cases per platform observe child ParentCommand.Update, parent Job data already new, independent Redis stored data still old and no child completion. PAUSE request timestamps are captured before sending the command and establish a conservative remaining-time lower bound before force-close/cancel. Subsequent workers/jobs complete; no worker error or hanging listener is seen. Windows result and full commands: `public-final-v2-windows/FINAL-RESULT.json`; Linux strong observation: `runtime/final-v2-strong-requested-at.json`.

## Scope and limitations

- Six child-processor EventEmitter/wrapJob tests are protocol unit tests, not actual IPC E2E.
- Four real Redis sandbox regressions execute via test:ioredis/coverage on Redis6/7; default Valkey/Dragonfly test config excludes sandboxed_process.
- No new skip, relaxed assertion, new public option, enum renumbering or hard updateData timeout.
- Original retry final-state permanent loss is not claimed reproduced.
- Windows supported file-URL Worker entry was used; unrelated Windows absolute import-path bug is out of scope.
- Initial v1 Windows/package/matrix records are historical; final package SHA d14b6b... and v2 logs establish finalHEAD.
- Force close can leave a running job active; subsequent-worker control is bounded to current shutdown semantics, not PR4991 redesign.
- Latest issue/policy/default HEAD/open PR prepublication refresh is root responsibility; local test success is not GitHub CI success.

## Retained failures and corrections

- v1 direct Prettier check failed two files; corrected only formatting, AST equivalent; every final gate rerun against v2.
- Dragonfly with custom proactor_threads=2 exposed an existing worker failure on candidate and baseline; official default Dragonfly configuration baseline control and final full suite pass.
- GLIDE first v2 runtime tests passed but npm no-save lock drift was detected; canonical-lock restore, version assertion, build, full suite1093 passed/3 upstream skips and1068-source postcheck subsequently passed. The initial drift run remains superseded evidence.

Official frozen Yarn installation completed0 and ran the real Husky prepare hook (`runtime/baseline-bootstrap-results.json`, `baseline-install.log`). Candidate dependencies were physically copied from that installation; package.json/yarn.lock are unchanged through finalHEAD. Final build/tests reran on final source. Consumer npm installs use ignore-scripts only after the real source build; they do not substitute for project installation or normal commit hooks.

Normal commit hooks ran without bypass and preserved final frozen bytes: `runtime/root-v2-normal-commit.json`. No paid/model calls, external coding tools, global configuration changes or shared production Redis were used. All Redis writes targeted identified task-owned services.

The public evidence allowlist contains only this task’s selected logs/results/source-hash manifests and reproducible consumer harnesses. It excludes Git metadata/bundles, source archives, node_modules, caches and account audits. Independent worker summaries are referenced separately and owned by those workers.
