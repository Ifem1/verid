export const walletButtonText=(wallet,shortener)=>wallet?shortener(wallet):'Connect wallet';
export function connectLocalWallet(state,address,chain){state.wallet=address||'';state.chain=Number(chain)||0;state.sessionActive=Boolean(state.wallet);return state}
export async function restoreLocalWallet(state,provider){if(!provider)return state;try{const accounts=await provider.request({method:'eth_accounts'});const chain=Number.parseInt(await provider.request({method:'eth_chainId'}),16);if(accounts?.[0])connectLocalWallet(state,accounts[0],chain)}catch{}return state}
export function clearLocalWallet(state){state.wallet='';state.chain=0;state.sessionActive=false;return state}
export const toggleWalletMenu=open=>!Boolean(open);
export async function copyFullWalletAddress(wallet,clipboard){if(!wallet)throw Error('No connected wallet.');if(!clipboard?.writeText)throw Error('Clipboard access is unavailable.');await clipboard.writeText(wallet);return wallet}
