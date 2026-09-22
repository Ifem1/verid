export const walletButtonText=(wallet,shortener)=>wallet?shortener(wallet):'Connect wallet';
export function connectLocalWallet(state,address,chain){state.wallet=address||'';state.chain=Number(chain)||0;state.sessionActive=Boolean(state.wallet);return state}
export function clearLocalWallet(state){state.wallet='';state.chain=0;state.sessionActive=false;return state}
export const toggleWalletMenu=open=>!Boolean(open);
export async function copyFullWalletAddress(wallet,clipboard){if(!wallet)throw Error('No connected wallet.');if(!clipboard?.writeText)throw Error('Clipboard access is unavailable.');await clipboard.writeText(wallet);return wallet}
