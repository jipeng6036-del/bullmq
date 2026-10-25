import pathlib,json,hashlib,datetime
r=pathlib.Path(__file__).parent
old=r.parent/'independent-source-review.json'
prior=json.loads(old.read_text())
proof=json.loads((r/'format-v2-ast-equivalence.json').read_text())
mapping=json.loads((r/'final-head-tree-mapping.json').read_text())
manifest=json.loads((r/'candidate-frozen-v2-manifest.json').read_text())
assert proof['allAstEquivalent'] and mapping['allTreeGitBlobsModesAndSymlinksMatch']
assert {x['path'] for x in proof['files']}=={'src/classes/child-processor.ts','tests/child-processor.test.ts'}
old_hashes={x['path']:x['sha256'] for x in prior['sourceHashes']}
new_hashes={x['path']:x['sha256'] for x in manifest['files']}
for x in proof['files']:
    assert x['beforeSha256']==old_hashes[x['path']]
    assert x['afterSha256']==new_hashes[x['path']]
    assert x['astEquivalent'] and x['astBeforeSha256']==x['astAfterSha256']
for p in set(old_hashes)-{x['path'] for x in proof['files']}:assert old_hashes[p]==new_hashes[p]
review={
 'status':'NO_EVIDENCE_BACKED_BLOCKING_FINDINGS',
 'reviewedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'finalHead':mapping['finalHead'],
 'candidateArchiveSha256':mapping['archiveSha256'],
 'semanticReviewCarriedForwardFromV1':True,
 'carryForwardReason':'Full archive byte delta is limited to the two official formatter outputs; syntax-node kind/child/identifier/literal signatures are equivalent and other four changed files are byte-identical. Entire final Git tree exactly matches v2 archive.',
 'findings':prior['findings'],
 'originalIndependentReview':str(old),
 'originalIndependentReviewSha256':hashlib.sha256(old.read_bytes()).hexdigest(),
 'astProofSha256':hashlib.sha256((r/'format-v2-ast-equivalence.json').read_bytes()).hexdigest(),
 'finalHeadTreeMappingSha256':hashlib.sha256((r/'final-head-tree-mapping.json').read_bytes()).hexdigest(),
 'v2SourceFiles':manifest['files'],
 'checksCarriedForward':[x['topic'] for x in prior['checks']],
 'boundaries':['Original review line references and real lifecycle runtime observations remain explicitly v1 evidence; they are not relabeled as final HEAD runtime tests.','Current final HEAD Bun and Node Redis runtime gates are independently executed and recorded in this v2 directory.','Six ChildProcessor cases remain EventEmitter/wrapJob message protocol unit cases; no claim that they are real IPC/Redis tests.'],
 'productEdited':False,
 'additionalUnrelatedInvestigations':False
}
(r/'independent-source-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
print(json.dumps({'status':review['status'],'finalHead':review['finalHead'],'astProofVerified':True,'sourceFiles':len(manifest['files'])},indent=2))
