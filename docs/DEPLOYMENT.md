# Deployment

Target only GenLayer Studionet: chain 61999, RPC https://studio.genlayer.com/api, explorer https://explorer-studio.genlayer.com.

The canonical deployment is recorded in `verid-manifest.json` and `config.js`: contract `0x12f2136e0d372038E72Beb54511c72fF372c694d`, transaction `0xd2d9c0b20927fb006cd2b2ad340220140cfaffa59d7dc16d6dee97372546e818`.

The frozen contract source is commit `281ff29a2585adeb4d9294bb8b5c678053a9a7b0`, 19,691 bytes, Git blob `e4986586e37a5c1c616a1da5a9a391dc263f13d0`, SHA-256 `7b1d2087745582eb15ac8acf844a2028d849d5100ef199bcbd6b8a9ad721c0de`. `gen_getContractCode` returned base64 source; decoding it produced 19,691 bytes with the same SHA-256 and Git blob: exact-byte parity.

The frontend is deployed at https://verid-sigma.vercel.app and must always use the manifest address. Contract changes require a new frozen commit, source hash, deployment, parity comparison and frontend deployment.

The production Vercel deployment for this source is `dpl_3vdPvUDVNGNtcuXLRjvNaUXixNHw`. The final live attempt used profile creation `0x0df6d45b59da1b774f533b6a0d12fa39032b55c6893de5c3c31bc5ea1d0192b7`, challenge issuance `0x8aba05d70dcf02ebbbc7a9c3a52a7862020daf5e24cf491ff2135a06f2e37aea`, surface registration `0xb87e77f5ffb562da08631a4189c6f22f4a6d7fa351c3c65b6de3cd53087e6a6a`, and verification `0xeb5a8d54133e05679cf29fab093eadcde41f6673f5161e311c6a940e3559fe68`. The final readback was `UNVERIFIED` with unresolved semantic identity/authenticity, so no proof/gate success is asserted.
