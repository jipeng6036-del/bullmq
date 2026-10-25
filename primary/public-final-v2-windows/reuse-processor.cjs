const processor=require('./contracts-processor.cjs');const {threadId}=require('node:worker_threads');
module.exports=async function(...args){return {...await processor(...args),identity:`${process.pid}/${threadId}`};};
