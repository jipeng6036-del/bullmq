const Redis=require('ioredis');const {getEventListeners}=require('node:events');const {parentPort,threadId}=require('node:worker_threads');
module.exports=async function(job,token,signal){
 const identity=`${process.pid}/${threadId}`;if(job.data.operation==='warmup')return {warmup:true,identity};
 const connection=new Redis({host:'127.0.0.1',port:job.data.port});
 try{await connection.ping();let pauseAt,pauseRequestedAt;if(job.data.operation==='pending'){pauseRequestedAt=Date.now();await connection.client('PAUSE',2000,'WRITE');pauseAt=Date.now();}
 await job.updateData({...job.data,updated:true,pauseAt,pauseRequestedAt});return {control:job.data.control,updated:true,aborted:!!signal?.aborted,identity,listenersAfter:getEventListeners(parentPort||process,'message').length};
 }finally{await connection.quit();}
};
