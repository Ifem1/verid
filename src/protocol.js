export const CHAIN_ID=61999;
export const CHAIN={chainId:'0xf22f',chainName:'GenLayer Studionet',nativeCurrency:{name:'GEN',symbol:'GEN',decimals:18},rpcUrls:['https://studio.genlayer.com/api'],blockExplorerUrls:['https://explorer-studio.genlayer.com']};
export const SURFACES=['GITHUB','WEBSITE','PROJECT','ORGANISATION'];
export const short=v=>v&&v.length>12?`${v.slice(0,6)}…${v.slice(-4)}`:v;
export const configured=v=>/^0x[a-fA-F0-9]{40}$/.test(String(v||''));
export const txTruth=r=>{const f=r?.statusName==='FINALIZED'||Number(r?.status)===7;if(!f)return'PENDING';if(r?.txExecutionResultName==='FINISHED_WITH_RETURN'||Number(r?.txExecutionResult)===1)return'SUCCESS';if(r?.txExecutionResultName)return'FAILED';return'UNKNOWN'};
