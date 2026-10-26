set -eu
cd /tmp/bullmq5017/source
test "$(git rev-parse HEAD)" = 772e94a781313b2d21f7ae751df5dac935d236c7
node /evidence/verify-source.cjs /evidence/candidate-source-manifest.json
./node_modules/.bin/vitest run --no-file-parallelism tests/child-processor.test.ts
./node_modules/.bin/vitest run --no-file-parallelism --config vitest.ioredis.config.ts tests/sandboxed_process.test.ts -t 'should await persisted data|should return persistence errors'
node /evidence/verify-source.cjs /evidence/candidate-source-manifest.json
git diff --check
test -z "$(git status --porcelain)"
