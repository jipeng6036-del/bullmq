const { Queue } = require('bullmq');
const probe = require('./probe-core.cjs');
let observer;
module.exports = async function(job) {
  if (!observer) {
    observer = new Queue(job.data.queueName, { connection: { host: '127.0.0.1', port: job.data.port } });
    await observer.waitUntilReady();
  }
  return probe(job, observer);
};
