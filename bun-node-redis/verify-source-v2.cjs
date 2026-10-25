const fs = require('fs'), crypto = require('crypto'), path = require('path');
const base=process.argv[2], archive=process.argv[3];
const manifest=JSON.parse(fs.readFileSync('/evidence/v2/source-archives-v2.json'))[archive];
let errors=[];
for (const entry of manifest.entries) {
  const name=path.join(base,entry.path);
  let st;try {st=fs.lstatSync(name);}catch(e){errors.push({path:entry.path,error:String(e)});continue;}
  if (entry.type!=='symlink' && (st.mode & 0o777)!==entry.mode) errors.push({path:entry.path,mode:st.mode&0o777,expected:entry.mode});
  if(entry.type==='symlink') {if(!st.isSymbolicLink()||fs.readlinkSync(name)!==entry.link)errors.push({path:entry.path,error:'symlink mismatch'});}
  else if(entry.type==='file') {const hash=crypto.createHash('sha256').update(fs.readFileSync(name)).digest('hex');if(!st.isFile()||hash!==entry.sha256)errors.push({path:entry.path,hash,expected:entry.sha256});}
}
console.log(JSON.stringify({base,archive,expectedEntries:manifest.count,errors,verified:errors.length===0},null,2));
process.exit(errors.length?1:0);

