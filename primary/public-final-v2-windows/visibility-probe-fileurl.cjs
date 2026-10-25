const { Queue, Worker } = require('bullmq');
const path = require('node:path');
const fs = require('node:fs');
const probe = require('./probe-core.cjs');
const port = Number(process.env.REDIS_PORT);
const connection = { host: '127.0.0.1', port };
(async () => {
  const all = [];
  for (const mode of ['in-process', 'child-process', 'worker-thread']) {
    const name = 'heartbeat0902-4168-' + mode + '-' + process.pid;
    const queue = new Queue(name, { connection });
    const observer = new Queue(name, { connection });
    await Promise.all([queue.waitUntilReady(), observer.waitUntilReady()]);
    const results = [];
    const errors = [];
    const worker = new Worker(name, mode === 'in-process' ? job => probe(job, observer) : require('node:url').pathToFileURL(path.join(__dirname, 'processor.cjs')), { connection, useWorkerThreads: mode === 'worker-thread', concurrency: 1 });
    worker.on('error', e => errors.push(e.message));
    const done = new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('public probe timeout')), 60000);
      worker.on('completed', (job, result) => { results.push(result); if (results.length === 10) { clearTimeout(timer); resolve(); } });
      worker.on('failed', (job, e) => { clearTimeout(timer); reject(e); });
    });
    for (let i = 0; i < 10; i++) await queue.add('probe', { queueName: name, port, n: 0 });
    try { await done; }
    finally { await worker.close(); await observer.close(); await queue.obliterate({ force: true }); await queue.close(); }
    const row = { mode, jobs: results.length, observations: results.reduce((n,x) => n+x.observations,0), mismatches: results.flatMap(x => x.mismatches), errors };
    all.push(row); console.log(JSON.stringify(row));
  }
  fs.writeFileSync(path.join(__dirname,'visibility-fileurl-results.json'), JSON.stringify({ node: process.version, bullmq: require('bullmq/package.json').version, port, all }, null, 2));
})().catch(e => { console.error(e); process.exitCode = 1; });
