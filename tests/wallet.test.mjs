import test from'node:test';import assert from'node:assert/strict';import{walletButtonText,connectLocalWallet,clearLocalWallet,toggleWalletMenu,copyFullWalletAddress}from'../src/wallet-session.js';
const short=v=>v&&v.length>12?`${v.slice(0,6)}…${v.slice(-4)}`:v,ADDRESS='0x6EAE29000000000000000000000000000039C822';
test('disconnected state shows Connect wallet',()=>assert.equal(walletButtonText('',short),'Connect wallet'));
test('connected state shows shortened wallet',()=>assert.equal(walletButtonText(ADDRESS,short),'0x6EAE…C822'));
test('wallet menu toggles for click and touch activation',()=>{assert.equal(toggleWalletMenu(false),true);assert.equal(toggleWalletMenu(true),false)});
test('copy uses the full connected wallet address',async()=>{let copied='';await copyFullWalletAddress(ADDRESS,{writeText:async value=>{copied=value}});assert.equal(copied,ADDRESS)});
test('local disconnect clears only the app wallet session',()=>{const s={wallet:ADDRESS,chain:61999,sessionActive:true};clearLocalWallet(s);assert.deepEqual(s,{wallet:'',chain:0,sessionActive:false})});
test('account can connect again after local disconnect',()=>{const s={wallet:ADDRESS,chain:61999,sessionActive:true};clearLocalWallet(s);connectLocalWallet(s,ADDRESS,61999);assert.deepEqual(s,{wallet:ADDRESS,chain:61999,sessionActive:true})});
