const { Queue, Worker, QueueEvents } = require('bullmq');
const Redis = require('ioredis');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
const fs = require('node:fs');
const port = Number(process.env.REDIS_PORT);
const connection = { host: '127.0.0.1', port };
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
async function main() {
 const all = [];
 for (const mode of ['child-process', 'worker-thread']) {
  for (const operation of ['persist','reject','send-failure','retry','slow','cancel','close']) {
   const name = `hb0902-4168-${mode}-${operation}-${process.pid}`;
   const queue = new Queue(name,{connection});
   const events = new QueueEvents(name,{connection});
   const redis = new Redis(connection);
   await Promise.all([queue.waitUntilReady(),events.waitUntilReady()]);
   const worker = new Worker(name,pathToFileURL(path.join(__dirname,'contracts-processor.cjs')),{connection,useWorkerThreads:mode==='worker-thread',workerForkOptions:{serialization:'advanced'}});
   const errors=[];worker.on('error',e=>errors.push({name:e.name,message:e.message}));
   const readyKey = `${name}:ready`;
   const started=Date.now();
   const row={mode,operation};
   let closing;
   try {
    const job=await queue.add('contract',{operation,port,readyKey: ['cancel','close'].includes(operation)?readyKey:undefined},{attempts:operation==='retry'?3:1});
    const completion=job.waitUntilFinished(events,20000).then(value=>({value}),error=>({error:{name:error.name,message:error.message}}));
    if(['cancel','close'].includes(operation)) {
     while(!await redis.get(readyKey)) { if(Date.now()-started>10000)throw Error('processor ready timeout');await sleep(5); }
     if(operation==='cancel')row.cancelled=worker.cancelJob(job.id,'contract control');
     else closing=worker.close(operation==='force-close');
    }
    Object.assign(row,await completion);
    if(closing)await closing;
    row.persisted=(await queue.getJob(job.id))?.data;
   } catch(error) {row.harnessError={name:error.name,message:error.message};}
   finally {
    await worker.close();await events.close();await queue.obliterate({force:true});await queue.close();await redis.del(readyKey);await redis.quit();
   }
   row.elapsedMs=Date.now()-started;row.workerErrors=errors;all.push(row);console.log(JSON.stringify(row));
  }
 }
 fs.writeFileSync(path.join(__dirname,'contracts-result.json'),JSON.stringify({node:process.version,port,all},null,2));
}
main().catch(error=>{console.error(error);process.exitCode=1;});
