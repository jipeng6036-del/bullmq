const { Queue } = require('bullmq');
const Redis = require('ioredis');
const { getEventListeners } = require('node:events');
const { parentPort } = require('node:worker_threads');
module.exports = async function (job, token, signal) {
  const { operation, port, readyKey } = job.data;
  const receiver = parentPort || process;
  const listenersBefore = getEventListeners(receiver, 'message').length;
  if (operation === 'send-failure' || operation === 'reject') {
    try {
      await job.updateData({ value: operation === 'reject' ? BigInt(1) : () => {} });
      return { caught: false, localType: typeof job.data.value };
    } catch (error) {
      await new Promise(resolve => setImmediate(resolve));
      return { caught: true, name: error.name, message: error.message, localType: typeof job.data.value, listenersBefore, listenersAfter: getEventListeners(receiver, 'message').length };
    }
  }
  const redis = new Redis({ host: '127.0.0.1', port });
  const observer = new Queue(job.queueName, { connection: redis });
  try {
    await observer.waitUntilReady();
    if (readyKey) await redis.set(readyKey, 'ready');
    await redis.client('PAUSE', operation === 'slow' ? 5500 : 700, 'WRITE');
    const data = { ...job.data, seen: [...(job.data.seen || []), job.attemptsMade] };
    await job.updateData(data);
    const stored = await observer.getJob(job.id);
    const equal = JSON.stringify(stored.data) === JSON.stringify(data);
    if (operation === 'retry' && !equal) throw new Error('await returned before Redis persistence');
    if (operation === 'retry' && job.attemptsMade < 2) throw new Error('planned retry');
    return { equal, seen: stored.data.seen, aborted: !!signal?.aborted, listenersBefore, listenersAfter: getEventListeners(receiver, 'message').length };
  } finally {
    await observer.close();
    await redis.quit();
  }
};
