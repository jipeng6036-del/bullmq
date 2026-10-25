import pathlib,json,hashlib,tarfile,datetime,sys,importlib.util,subprocess
root=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('v2run',root/'run-v2.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
archive=pathlib.Path(sys.argv[1]); expected=sys.argv[2]
assert hashlib.sha256(archive.read_bytes()).hexdigest()==expected
v1=m.input_root/'candidate-frozen-v1.tar'
archives={}
for p in [archive,v1]:
    with tarfile.open(p) as t:
        entries=[]
        for x in t.getmembers():
            assert not x.name.startswith('/') and '..' not in pathlib.PurePosixPath(x.name).parts
            entries.append({'path':x.name,'mode':x.mode,'type':'symlink' if x.issym() else 'file' if x.isfile() else 'dir','link':x.linkname,'sha256':hashlib.sha256(t.extractfile(x).read()).hexdigest() if x.isfile() else None})
    archives[p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'count':len(entries),'entries':entries}
a={x['path']:x for x in archives[archive.name]['entries']}; b={x['path']:x for x in archives[v1.name]['entries']}
delta=[p for p in a.keys()|b.keys() if a.get(p)!=b.get(p)]
assert set(delta)=={'src/classes/child-processor.ts','tests/child-processor.test.ts'},delta
assert a['yarn.lock']==b['yarn.lock'] and a['package.json']==b['package.json']
(root/'source-archives-v2.json').write_text(json.dumps(archives,indent=2)+'\n',encoding='utf-8')
(root/'v1-v2-byte-delta.json').write_text(json.dumps({'v2ArchiveSha256':expected,'changed':delta,'packageAndLockUnchanged':True,'dependencyReuse':'Exact frozen v1 installation, no dependency mutation'},indent=2)+'\n',encoding='utf-8')
verify=(root.parent/'verify-source.cjs').read_text().replace('/evidence/source-archives.json','/evidence/v2/source-archives-v2.json')
(root/'verify-source-v2.cjs').write_text(verify,encoding='utf-8',newline='\n')
ident=json.loads(subprocess.check_output(['docker','inspect',m.redis],text=True))[0]
assert ident['Config']['Labels']['owner']==m.owner and ident['Id']=='87c43361f57b318fbe168cab1f1b9a7279b5bc57a5b7a3fed6ed0f9b8fb6bfa0'
assert m.run('redis-reset-before-v2-bun',['docker','exec',m.redis,'redis-cli','FLUSHALL'])==0
cmd='tar -xpf /input/'+archive.name+' -C /tmp/bunroot/candidate && node /evidence/v2/verify-source-v2.cjs /tmp/bunroot/candidate '+archive.name+' && node --version && yarn --version && bun --version'
assert m.step('v2-extract-verify',cmd)==0
if '--prepare-only' in sys.argv:
    print('Prepared/verified v2 source only; awaiting final HEAD for build and test gates.',flush=True)
    raise SystemExit(0)
steps={}
for name,cmd in [('candidate-build','yarn build'),('candidate-bun-smoke','yarn test:bun:smoke'),('candidate-bun-full','yarn test:bun'),('candidate-adapter-conformance','yarn test:adapter-conformance'),('candidate-node-redis','yarn test:node-redis')]:
    if name=='candidate-adapter-conformance':
        owned=json.loads(subprocess.check_output(['docker','inspect',m.redis],text=True))[0]
        assert owned['Id']==ident['Id'] and owned['Config']['Labels']['owner']==m.owner
        assert m.run('redis-reset-before-node-redis',['docker','exec',m.redis,'redis-cli','FLUSHALL'])==0
    steps[name]=m.step(name,'cd /tmp/bunroot/candidate && '+cmd)
    (root/'pipeline-results.json').write_text(json.dumps(steps,indent=2)+'\n',encoding='utf-8')
    if name=='candidate-build' and steps[name]:break
steps['candidate-source-final']=m.step('candidate-source-final','node /evidence/v2/verify-source-v2.cjs /tmp/bunroot/candidate '+archive.name)
m.run('final-identities',['docker','inspect',m.redis,m.runner])
(root/'pipeline-results.json').write_text(json.dumps(steps,indent=2)+'\n',encoding='utf-8')
print(json.dumps(steps),flush=True)

