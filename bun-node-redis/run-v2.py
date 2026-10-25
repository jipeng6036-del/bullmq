import pathlib,json,hashlib,tarfile,subprocess,datetime,sys
root=pathlib.Path(__file__).parent
parent=root.parent
input_root=pathlib.Path(r'F:/Github-PR/ci-evidence/heartbeat0902-js-bullmq-4168/runtime')
runner='ghpr-0902-bullmq-bun-root-runner'; redis='ghpr-0902-bullmq-bun-root-redis7'
owner='bullmq-bun-root'
path='/tmp/bunroot/tools/node_modules/node/bin:/tmp/bunroot/tools/node_modules/.bin:/tmp/bunroot/bun/node_modules/@oven/bun-linux-x64/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
def run(name,args):
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (root/(name+'.log')).open('w',encoding='utf-8',newline='\n') as log:
        log.write(json.dumps({'argv':args,'started':started})+'\n');log.flush()
        done=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT)
    row={'name':name,'argv':args,'started':started,'ended':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exitCode':done.returncode}
    (root/(name+'-result.json')).write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(row),flush=True)
    if done.returncode:print((root/(name+'.log')).read_text()[-3000:],flush=True)
    return done.returncode

def step(name,cmd):
    return run(name,['docker','exec','--user','node','--env','HOME=/tmp/bunroot/home','--env','npm_config_cache=/tmp/bunroot/npm-cache','--env','YARN_CACHE_FOLDER=/tmp/bunroot/yarn-cache','--env','PATH='+path,'--env','REDIS_HOST=127.0.0.1','--env','REDIS_PORT=6379',runner,'sh','-c',cmd])

if __name__=='__main__':
    raise SystemExit('Prepared only. Await v2 archive manifest/hash and final HEAD mapping before running dependent gates.')
