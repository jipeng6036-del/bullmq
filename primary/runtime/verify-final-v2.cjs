const fs=require('fs');const crypto=require('crypto');
const root=process.argv[2];const base=JSON.parse(fs.readFileSync('/evidence/baseline-git-manifest.json'));const frozen=JSON.parse(fs.readFileSync('/evidence/candidate-frozen-v2-manifest.json'));
const files=new Map(base.files.map(f=>[f.path,f]));for(const f of frozen.files)files.set(f.path,f);
let links=0;
for(const f of files.values()) {const p=`${root}/${f.path}`;const st=fs.lstatSync(p);const bytes=st.isSymbolicLink()?Buffer.from(fs.readlinkSync(p)):fs.readFileSync(p);const sha=crypto.createHash('sha256').update(bytes).digest('hex');if(sha!==f.sha256)throw Error(`Source differs: ${f.path}`);const mode=st.isSymbolicLink()?'120000':st.mode&0o111?'100755':'100644';if(mode!==f.mode)throw Error(`Mode differs: ${f.path}`);if(st.isSymbolicLink())links++;}
console.log(JSON.stringify({verified:true,root,files:files.size,symlinks:links,node:process.version,base:base.base,candidateArchiveSha256:frozen.archiveSha256,checkedAt:new Date().toISOString()},null,2));
