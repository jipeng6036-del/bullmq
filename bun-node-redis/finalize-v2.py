import pathlib,json,re,hashlib,datetime
r=pathlib.Path(__file__).parent
names=['candidate-build','candidate-bun-smoke','candidate-bun-full','candidate-adapter-conformance','candidate-node-redis','candidate-source-final']
results={n:json.loads((r/(n+'-result.json')).read_text()) for n in names}
assert all(x['exitCode']==0 for x in results.values()),results
mapping=json.loads((r/'final-head-tree-mapping.json').read_text())
assert mapping['allTreeGitBlobsModesAndSymlinksMatch']

def clean(n):
    s=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',(r/(n+'.log')).read_text(encoding='utf-8'))
    (r/(n+'-clean.log')).write_text(s,encoding='utf-8',newline='\n')
    return s

def tally(n):
    s=clean(n)
    files=re.findall(r'Test Files\s+([^\n]+)',s)[-1].strip()
    tests=re.findall(r'(?m)^\s*Tests\s+([^\n]+)',s)[-1].strip()
    return {'fileSummary':files,'testSummary':tests,'duration':re.findall(r'(?m)^\s*Duration\s+([^\n]+)',s)[-1].strip(),'skippedCases':[x.strip()[2:] for x in s.splitlines() if '\u2193' in x]}

smoke=clean('candidate-bun-smoke');assert '19 pass' in smoke and '0 fail' in smoke
stats={'smoke':{'passed':19,'failed':0,'files':2},'bunFull':tally('candidate-bun-full'),'adapterConformance':tally('candidate-adapter-conformance'),'nodeRedis':tally('candidate-node-redis')}
review=json.loads((r/'independent-source-review.json').read_text())
summary={
 'status':'FINAL_HEAD_V2_OFFICIAL_BUN_AND_NODE_REDIS_GATES_PASSED_LOCALLY',
 'createdAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'finalHead':mapping['finalHead'],'finalTree':'0503ca913f5b3b71b081f7912a497fe635317d67','base':'09b7bfeb8653e74074542ca48e70477540742a7e',
 'archiveSha256':mapping['archiveSha256'],'treeMapping':mapping,
 'runtime':{k:v for k,v in json.loads((r.parent/'runtime-summary.json').read_text()).items() if k in ['owner','node','yarn','bun','redis','redisHostPort','testRedisEndpoint','containers']},
 'dependencyReuse':{'source':'v1 exact frozen install; package.json and yarn.lock unchanged in v2','lockSha256':'352db92214415193667c493636408682bb3fb612775c70df81e5522f6b76cb4f'},
 'gates':results,'stats':stats,
 'unitVsRuntimeBoundary':'Six tests/child-processor.test.ts cases are EventEmitter/wrapJob message protocol unit cases; these are not described as real IPC/Redis tests.',
 'sourceFinalVerifiedEntries':1068,
 'reviewStatus':review['status'],'astEquivalenceVerified':True,
 'executionIsolation':'Bun and Node Redis ran sequentially on owned Redis7 only; owned Redis was reset between runtime lanes; no shared/default host Redis used.',
 'baselineControl':{'executed':False,'reason':'All candidate gates exited 0; no failing assertion to attribute'},
 'v1Evidence':'All v1 records retained as historical, not relabeled final HEAD.',
 'environmentRetained':True,
 'productEdited':False,'githubStateWritten':False
}
(r/'final-head-gate-summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
text=f'''# Final HEAD BullMQ Bun and Node Redis verification

Final HEAD `{summary['finalHead']}`, tree `{summary['finalTree']}`, base `{summary['base']}`. Source archive SHA256 `{summary['archiveSha256']}`. All 1068 Git tree blobs/modes/symlinks match the frozen v2 archive; source verified again unchanged after all tests.

| Official gate | Exit | Actual result |
| --- | --- | --- |
| `yarn build` | 0 | Build completed |
| `yarn test:bun:smoke` | 0 | 19 passed, 0 failed, 2 files |
| `yarn test:bun` | 0 | {stats['bunFull']['fileSummary']}; {stats['bunFull']['testSummary'].replace('|', ',')} |
| `yarn test:adapter-conformance` | 0 | {stats['adapterConformance']['fileSummary']}; {stats['adapterConformance']['testSummary'].replace('|', ',')} |
| `yarn test:node-redis` | 0 | {stats['nodeRedis']['fileSummary']}; {stats['nodeRedis']['testSummary'].replace('|', ',')} |

These are actual local runtime results for final HEAD, not GitHub Actions status. Existing official exclusions/skips remain explicit and are not passing assertions. Six ChildProcessor cases are EventEmitter/wrapJob protocol unit tests, not real IPC/Redis evidence. Existing v1 installed-package lifecycle observations retain their original revision labels.

Node 24.22.1 / Yarn 1.22.22 / Bun 1.4.4 / Redis 7.4.11. Dependency installation was reused from the exact frozen v1 install after package.json and yarn.lock byte equality was proved; lock SHA256 `352db92214415193667c493636408682bb3fb612775c70df81e5522f6b76cb4f`. Bun and Node Redis used the same final frozen source and the same independently owned Redis network namespace sequentially; no runtime lanes overlapped Redis. Redis reset targeted only owner-verified ID `87c43361f57b318fbe168cab1f1b9a7279b5bc57a5b7a3fed6ed0f9b8fb6bfa0`.

Redis `ghpr-0902-bullmq-bun-root-redis7`, host-only mapping `127.0.0.1:45261`; runner `ghpr-0902-bullmq-bun-root-runner`; owner label `bullmq-bun-root`. Full image digests, IDs and configuration are retained in prior runtime-summary.json and this directory's final-identities.log. Both containers remain available for root verification/cleanup.

Semantic review was carried forward only after two-file formatter byte delta, syntax-equivalence proof, four other unchanged file hashes and entire final HEAD tree mapping were verified. No evidence-backed blocking findings. The first HEAD precheck safely stopped before root finished host import; no build/tests ran in that attempt. Its exact boundary is retained in mapping-first-attempt.json. Bun test-reported duration and Docker CLI completion differed due to output/client closeout latency. A bounded Docker event-history query returned no historical rows; it was not used as proof of success. Completed gate output plus actual exit code 0 establish the result. Owned runner OOMKilled was false and memory.events OOM counters were 0. No tests were duplicated or containers terminated during diagnosis. No product edits, source formatting, commits, pushes or GitHub state writes were performed by this lane.

Raw command output, full argv, timestamps and exit codes are retained per gate. `final-head-gate-summary.json` is the machine-readable result; `independent-source-review.json` carries review provenance and boundaries. `evidence-sha256.json` covers this v2 evidence set; all v1 records remain historical and unchanged.
'''
(r/'REPORT.md').write_text(text,encoding='utf-8',newline='\n')
manifest=[{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(r.iterdir()) if p.is_file() and p.name!='evidence-sha256.json']
(r/'evidence-sha256.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':summary['status'],'finalHead':summary['finalHead'],'stats':stats,'evidenceFiles':len(manifest)},indent=2,ensure_ascii=True))


