module.exports = async function probe(job, observer) {
  const mismatches = [];
  for (let n = 1; n <= 25; n++) {
    await job.updateData({ ...job.data, n });
    const stored = await observer.getJob(job.id);
    if (stored.data.n !== n) mismatches.push({ expected: n, stored: stored.data.n });
  }
  return { observations: 25, mismatches };
};
