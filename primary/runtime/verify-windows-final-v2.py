import pathlib,json,hashlib,subprocess,os,datetime,shutil,tarfile,sys
base=pathlib.Path(r'F:/Github-PR/ci-evidence/heartbeat0902-js-bullmq-4168');rt=base/'runtime'; out=base/'public-final-v2-windows';out.mkdir(exist_ok=False)
manifest=json.loads((rt/'artifact-final-v2-manifest.json').read_text());artifact=pathlib.Path(manifest['artifact']);assert hashlib.sha256(artifact.read_bytes()).hexdigest()==manifest['artifactSha256']
identity=json.loads(subprocess.check_output(['docker','inspect','ghpr-heartbeat0902-js-bullmq4168-redis'],text=True))[0]
assert identity['Id']=='ec80b192650b25877b7573510ece6cc532c79736982d0e1a126010640872ad11'; assert identity['State']['Running'];assert identity['NetworkSettings']['Ports']['6379/tcp']==[{'HostIp':'127.0.0.1','HostPort':'46017'}]
redis_version=subprocess.check_output(['docker','exec',identity['Id'],'redis-server','--version'],text=True).strip()
node=shutil.which('node');npm=shutil.which('npm.cmd'); env=dict(os.environ,REDIS_PORT='46017')
commands=[]
def run(name,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (out/(name+'.log')).open('w',encoding='utf-8') as log:
  log.write(json.dumps({'argv':args,'started':start,'cwd':str(out)})+'\n');log.flush();p=subprocess.run(args,cwd=out,env=env,stdout=log,stderr=subprocess.STDOUT)
 result={'argv':args,'started':start,'ended':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exitCode':p.returncode};commands.append(result);(out/(name+'-result.json')).write_text(json.dumps(result,indent=2));assert p.returncode==0,(name,p.returncode)
(out/'package.json').write_text(json.dumps({'name':'bullmq-final-v2-windows-consumer','private':True,'version':'1.0.0'}))
for name in ['probe-core.cjs','processor.cjs','visibility-probe-fileurl.cjs']:shutil.copyfile(base/'fixture'/name,out/name)
for name in ['contracts-processor.cjs','reuse-probe.cjs','reuse-processor.cjs']:shutil.copyfile(base/'public-candidate'/name,out/name)
contracts=(base/'public-candidate/contracts-probe.cjs').read_text().replace("'close','force-close']","'close']")
(out/'contracts-probe.cjs').write_text(contracts)
processor=(rt/'strong-close-processor.cjs').read_text().replace('let pauseAt;','let pauseAt,pauseRequestedAt;').replace("{await connection.client('PAUSE',2000,'WRITE');pauseAt=Date.now();}","{pauseRequestedAt=Date.now();await connection.client('PAUSE',2000,'WRITE');pauseAt=Date.now();}").replace('updated:true,pauseAt}', 'updated:true,pauseAt,pauseRequestedAt}')
probe=(rt/'strong-close-probe.cjs').read_text().replace('pauseAt:message.value.pauseAt,observedAt','pauseAt:message.value.pauseAt,pauseRequestedAt:message.value.pauseRequestedAt,observedAt').replace('checkedAt-update.pauseAt','checkedAt-update.pauseRequestedAt').replace('pauseAt:update.pauseAt,observedAt','pauseAt:update.pauseAt,pauseRequestedAt:update.pauseRequestedAt,observedAt').replace('strong-pending-close-result.json','strong-requested-at-result.json')
assert 'pauseRequestedAt=Date.now();await' in processor;assert 'remainingPauseLowerBoundMs:2000-(checkedAt-update.pauseRequestedAt)' in probe
(out/'strong-close-processor.cjs').write_text(processor);(out/'strong-close-probe.cjs').write_text(probe)
assets=rt/'strong-requested-at-assets.tar'
with tarfile.open(assets,'w') as archive:
 for name in ['strong-close-processor.cjs','strong-close-probe.cjs']:archive.add(out/name,arcname=name)
run('versions',[node,'-p',"JSON.stringify({node:process.version,versions:process.versions})"])
run('npm-version',[os.environ.get('COMSPEC','cmd.exe'),'/d','/c',npm,'--version'])
run('install',[os.environ.get('COMSPEC','cmd.exe'),'/d','/c',npm,'install','--ignore-scripts','--no-audit','--no-fund','--cache',str(out/'npm-cache'),'--registry','https://registry.npmjs.org',str(artifact),'ioredis@5.11.1'])
for f in manifest['files']: assert hashlib.sha256((out/'node_modules/bullmq'/f['path']).read_bytes()).hexdigest()==f['sha256'],f['path']
(out/'installed-package-verification.json').write_text(json.dumps({'verified':True,'files':len(manifest['files']),'artifactSha256':manifest['artifactSha256'],'sourceCommit':manifest['sourceCommit']},indent=2))
for script in ['visibility-probe-fileurl.cjs','contracts-probe.cjs','reuse-probe.cjs','strong-close-probe.cjs']:run(script[:-4],[node,script])
visible=json.loads((out/'visibility-fileurl-results.json').read_text());assert len(visible['all'])==3
for row in visible['all']:assert row['jobs']==10 and row['observations']==250 and not row['mismatches'] and not row['errors']
contract=json.loads((out/'contracts-result.json').read_text());assert len(contract['all'])==14
for row in contract['all']:
 assert not row.get('harnessError') and not row.get('error') and not row['workerErrors'],row
 v=row['value'];op=row['operation']
 if op in ['reject','send-failure']:assert v['caught'] and v['localType']==('bigint' if op=='reject' else 'function') and v['listenersBefore']==v['listenersAfter']==1
 else:assert v['equal'] and v['listenersBefore']==v['listenersAfter']==1
 if op=='slow':assert row['elapsedMs']>=5500
 if op=='retry':assert v['seen']==[0,1,2]
reuse=json.loads((out/'reuse-result.json').read_text());assert len(reuse['all'])==2
for row in reuse['all']:
 assert not row['workerErrors'];identities=[]
 for v in row['values']:
  result=v['value'];identities.append(result['identity']);assert result['listenersAfter']==1
  if v['operation'] in ['reject','send-failure']:assert result['caught']
  if v['operation']=='persist':assert result['equal'] and not result['aborted']
 assert len(set(identities))==1
strong=json.loads((out/'strong-requested-at-result.json').read_text());assert len(strong['rows'])==4
for row in strong['rows']:assert row['precondition']['remainingPauseLowerBoundMs']>500 and not row['workerErrors']
result={'verified':True,'sourceCommit':manifest['sourceCommit'],'sourceTree':manifest['sourceTree'],'artifactSha256':manifest['artifactSha256'],'installedFiles':len(manifest['files']),'redisContainerId':identity['Id'],'redisVersion':redis_version,'redisPort':46017,'node':visible['node'],'commands':commands,'visibilityObservations':750,'contractCases':14,'sameChildReuseModes':2,'strongPendingCases':4,'completed':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(out/'FINAL-RESULT.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
