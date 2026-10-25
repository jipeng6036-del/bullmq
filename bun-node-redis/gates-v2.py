import pathlib,json,hashlib,tarfile,subprocess,sys,importlib.util
root=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('v2run',root/'run-v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
head=sys.argv[1]; assert len(head)==40
repo=pathlib.Path(r'F:/Github-PR/inspection/heartbeat0902-js-bullmq-4168')
archive=m.input_root/'candidate-frozen-v2.tar'
expected='7bc67762360cab5ec31cc6f42e95cbc9c8d2401364a40b5129cf5bf2e10193a3'
assert hashlib.sha256(archive.read_bytes()).hexdigest()==expected
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==head
raw=subprocess.check_output(['git','-C',str(repo),'ls-tree','-r','-z','--full-tree',head])
tree={}
for row in raw.split(b'\0'):
    if not row:continue
    metadata,name=row.split(b'\t',1);mode,kind,oid=metadata.decode().split(' ')
    tree[name.decode()]={'mode':mode,'kind':kind,'gitblob':oid}
expected_tree={}
with tarfile.open(archive) as t:
    for x in t.getmembers():
        assert x.isfile() or x.issym()
        payload=x.linkname.encode() if x.issym() else t.extractfile(x).read()
        expected_tree[x.name]={'mode':'120000' if x.issym() else '100755' if x.mode&0o111 else '100644','kind':'blob','gitblob':hashlib.sha1(b'blob '+str(len(payload)).encode()+b'\0'+payload).hexdigest()}
errors=[{'path':p,'git':tree.get(p),'archive':expected_tree.get(p)} for p in tree.keys()|expected_tree.keys() if tree.get(p)!=expected_tree.get(p)]
mapping={'finalHead':head,'archiveSha256':expected,'treeEntries':len(tree),'archiveEntries':len(expected_tree),'errors':errors,'allTreeGitBlobsModesAndSymlinksMatch':not errors}
(root/'final-head-tree-mapping.json').write_text(json.dumps(mapping,indent=2)+'\n',encoding='utf-8');assert not errors,errors[:10]
assert m.step('final-head-source-precheck','node /evidence/v2/verify-source-v2.cjs /tmp/bunroot/candidate candidate-frozen-v2.tar && node --version && yarn --version && bun --version')==0
steps={}
for name,cmd in [('candidate-build','yarn build'),('candidate-bun-smoke','yarn test:bun:smoke'),('candidate-bun-full','yarn test:bun'),('candidate-adapter-conformance','yarn test:adapter-conformance'),('candidate-node-redis','yarn test:node-redis')]:
    if name=='candidate-adapter-conformance':
        owned=json.loads(subprocess.check_output(['docker','inspect',m.redis],text=True))[0]
        assert owned['Id']=='87c43361f57b318fbe168cab1f1b9a7279b5bc57a5b7a3fed6ed0f9b8fb6bfa0' and owned['Config']['Labels']['owner']==m.owner
        assert m.run('redis-reset-before-node-redis',['docker','exec',m.redis,'redis-cli','FLUSHALL'])==0
    steps[name]=m.step(name,'cd /tmp/bunroot/candidate && '+cmd)
    (root/'pipeline-results.json').write_text(json.dumps(steps,indent=2)+'\n',encoding='utf-8')
    if name=='candidate-build' and steps[name]:break
steps['candidate-source-final']=m.step('candidate-source-final','node /evidence/v2/verify-source-v2.cjs /tmp/bunroot/candidate candidate-frozen-v2.tar')
m.run('final-identities',['docker','inspect',m.redis,m.runner])
(root/'pipeline-results.json').write_text(json.dumps(steps,indent=2)+'\n',encoding='utf-8')
print(json.dumps(steps),flush=True)
