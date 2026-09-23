# Deployment

Target only GenLayer Studionet: chain 61999, RPC https://studio.genlayer.com/api, explorer https://explorer-studio.genlayer.com.

The canonical deployment is recorded in `verid-manifest.json` and `config.js`: contract `0x4A430f7326DEdcd796df149Ce5d31223c5943d92`, transaction `0x3ea54a4abee79a9da8a3c973c04779ad5912572c72ec67ff6c2124e34d09d479`.

The frozen contract source is commit `5d0009502b7f39a05fc15a7b8b9f5577d3dbd895`, 20,134 bytes, Git blob `e13006fbd5b584726d4dbfb5b33a7b3f13d86ae3`, SHA-256 `caca027a0253142bee2f5793a508c76b645907b61815ca9c626345caf22184c4`. `gen_getContractCode` returned base64 source; decoding it produced 20,134 bytes with the same SHA-256 and Git blob: exact-byte parity.

The frontend is deployed at https://verid-sigma.vercel.app and must always use the manifest address. Contract changes require a new frozen commit, source hash, deployment, parity comparison and frontend deployment.

The production Vercel deployment for this source is `dpl_3vdPvUDVNGNtcuXLRjvNaUXixNHw`. The final live attempt used profile creation `0x0df6d45b59da1b774f533b6a0d12fa39032b55c6893de5c3c31bc5ea1d0192b7`, challenge issuance `0x8aba05d70dcf02ebbbc7a9c3a52a7862020daf5e24cf491ff2135a06f2e37aea`, surface registration `0xb87e77f5ffb562da08631a4189c6f22f4a6d7fa351c3c65b6de3cd53087e6a6a`, and verification `0xeb5a8d54133e05679cf29fab093eadcde41f6673f5161e311c6a940e3559fe68`. The final readback was `UNVERIFIED` with unresolved semantic identity/authenticity, so no proof/gate success is asserted.
