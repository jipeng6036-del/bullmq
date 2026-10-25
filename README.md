# BullMQ sandbox `updateData` completion evidence

Source commit: `2e5ecf53615fd799d0c660d3b8bb8a5af579ccf7`  
Source tree: `0503ca913f5b3b71b081f7912a497fe635317d67`  
Upstream base: `09b7bfeb8653e74074542ca48e70477540742a7e`  
Issue: https://github.com/taskforcesh/bullmq/issues/4168

The six-file change makes a sandboxed `await job.updateData(data)` wait for the parent update and receive its failure. Local `job.data` keeps the native Job assignment timing. No new public option, response timeout, enum renumbering, backend change or unrelated shutdown behavior is introduced.

## Final source and actual gates

Every final lane is mapped to all 1068 final Git blobs and modes, including the tracked symlinks. Normal Husky commit hooks ran; the committed source did not change. Node LTS versions were resolved to 24.22.1, 22.23.4 and 20.20.2; Yarn is 1.22.22.

| Local final gate | Result |
| --- | --- |
| Lint, build, public types, direct Prettier check, normal commit hooks | Passed; one existing ESLint warning, zero errors |
| Node24 / Redis7.4.11 smoke | 86 passed, 2 existing skips |
| Node24 / Redis7 coverage (default + ioredis suites) | 1315 passed, 14 existing skips, 54 files; thresholds passed |
| Node20 and Node22 / Redis7, each | Default 1114 passed / 3 existing skips; ioredis 206 passed / 11 existing skips |
| Node24 / Redis6.2.24 | Default 1114 passed / 3 existing skips; ioredis 206 passed / 11 existing skips |
| NodeRedis / Redis7 | Adapter conformance 66 passed; full 1114 passed / 3 existing skips |
| Bun1.4.4 / Redis7 | Smoke 19 passed; full 1092 passed / 2 existing skips |
| Node24 / Valkey8.0.1 | 1114 passed / 3 existing skips |
| Node24 / Dragonfly df-v2.0.2, official CI configuration | 1114 passed / 3 existing skips |
| Node24 / PostgreSQL16.15 | 154 passed, 8 files |
| Node24 / Valkey GLIDE2.5.0 | 1093 passed / 3 existing skips, 48 files |

Coverage is statements 89.52%, branches 80.71%, functions 87.88%, lines 89.76%. Suite counts overlap; they are not a count of unique tests. Existing config exclusions and skips remain explicit in the raw logs. Other language ports are unaffected by this Node IPC change and were not tested. These local gates do not claim GitHub Actions, CodeQL or hosted uploads have passed.

## Reproduction and actual installed-package controls

The new four real child-process/worker-thread Redis regression cases fail on the exact baseline: two stale-data assertions and two failures to return a persistence error to the processor. The same cases pass in the final Redis ioredis/coverage runs. The baseline's 99 filtered-out cases are not newly introduced skips. Six additional EventEmitter/wrapJob tests are protocol unit tests, separate from actual IPC proof.

The final clean package has SHA256 `d14b6b2ce3a64dccd7950860eb2b757e093bbf74735ea3ec7790bb43bf9b9f8e`. All 805 installed files match the package inventory on Linux and Windows. Linux Node24.22.1/Redis7.4.11 and Windows Node24.14.0/npm11.16.0/Redis8.10.0 each exercise the public Worker/Queue API, with 750 visibility observations and zero stale reads. The Windows entry uses the supported file-URL form.

Real BigInt serialization failure, uncloneable IPC send failure, a 5500ms Redis WRITE pause, retries `[0,1,2]`, cancellation, child reuse and graceful close are recorded. Pending-write shutdown controls observe the real Update request, changed parent Job data, old independently fetched Redis data and no child completion before force-close/cancel. The pause request timestamp provides a conservative remaining-time bound. No helper replacement or fabricated IPC command substitutes for the runtime path.

The retry-accumulation control also succeeds on baseline; permanent retry-state loss is not claimed reproduced. Force-close retains its existing active-job semantics. No external model, paid service or production datastore was used.

## Evidence navigation

- `primary/final-v2-REPORT.md` and `primary/final-v2-gate-summary.json`: commands, versions, exact results and limitations.
- `primary/runtime/`: baseline failures, final primary/backend logs, normal hooks, package/source hashes, Linux runtime observations and consumer harnesses.
- `primary/public-final-v2-windows/`: exact installed artifact checks, raw commands/results and Windows consumer harnesses.
- `bun-node-redis/`: independent final Bun and NodeRedis logs, source mapping and review.
- `node-matrix/`: independent final Node20/22 and canonical-lock GLIDE logs and mapping.
- `SHA256SUMS.json`: exported bytes. Each lane also retains its explicit export list and source SHA provenance.

The per-gate result JSON records the actual command, timestamps and exit code. Rebuild the named commit with the recorded Yarn command, start disposable services matching the recorded versions/configuration, and use those commands and the retained consumer scripts. Sandbox regressions run via `yarn test:ioredis`; the primary coverage command includes that suite. The default Valkey/Dragonfly suite excludes sandboxed_process, so those lanes are backend regression gates rather than sandbox runtime proof.

Earlier attempts remain clearly identified: two v1 formatting failures were corrected before the normal commit and all final gates reran; a custom Dragonfly two-thread configuration failed an existing worker case on both baseline and candidate, while the official configuration passes; npm's initial GLIDE install altered the validation tree's lockfile, so the canonical lock was restored and the full final lane reran. Initial v1 results are not relabeled as final commit results.

Only explicit task evidence is exported. Dependencies, source archives, Git metadata, account audits, unrelated process inventories and credential files are excluded. Original local records are preserved.
