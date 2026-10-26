# BullMQ #5017 import follow-up

Candidate `772e94a781313b2d21f7ae751df5dac935d236c7` extends the maintainer-rebased `483f33fdd44c4ebd42061cb064eb48b9744a841f` with exactly one changed import: `events` to `node:events` in tests/child-processor.test.ts. All six remote PR blob OIDs were verified against the fetched source before editing. The old checkout and its evidence remain untouched.

Same-environment baseline lint exits 1 with one restricted-import error. Candidate lint passes with only the existing postgres-relay-backend.ts:395 prefer-const warning. Build, public types, all six PR-file formatting checks, smoke (86 pass / 2 existing skip), and normal Husky pre-commit/commit-msg hooks pass. Full primary coverage on exact candidate HEAD passes: 54 files, 1315 tests passed, 14 skipped. A separate runner invocation confirms six EventEmitter unit tests and four actual Redis child-process/worker-thread persistence/error regressions.

Environment: Node24.22.1, Yarn1.22.22, Redis7.4.11, ESLint10.13.0, Vitest4.1.12. Frozen-lockfile install; tracked package/yarn files unchanged. All1068 tracked source entries and symlink types match candidate bytes before/after gates and normal hooks. Task-owned Redis/validation containers only.

This follow-up does not rerun the old full platform/backend matrix. Those results belong to old 2e5ecf5 and the fixed historical proof at325d94d1. The current receipt claims only the new checks actually run on772e94a. No hosted-CI approval bypass, CLA signing, merge, release, paid service, push, or PR edit by the worker.
