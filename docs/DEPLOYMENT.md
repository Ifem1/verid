# Deployment

Target only GenLayer Studionet: chain 61999, RPC https://studio.genlayer.com/api, explorer https://explorer-studio.genlayer.com.

The canonical deployment is recorded in `verid-manifest.json` and `config.js`: contract `0xeE4Df291A9e8B4f5b2B90b3F6eeAe578818E0B0B`, transaction `0xf42e4c8876ed300b59cc96ca87e6822b7e622f90eab57564e323d4ce8b7427dd`.

The frozen contract source is commit `281ff29a2585adeb4d9294bb8b5c678053a9a7b0`, 20,018 bytes, SHA-256 `240abb1f32bb5e65196133792f1b7f9ac5f143912957895adf1b98ccae493246`. `gen_getContractCode` returns base64 source; decoding it produced 20,018 bytes with SHA-256 `240abb1f32bb5e65196133792f1b7f9ac5f143912957895adf1b98ccae493246`: exact-byte parity.

The frontend is deployed at https://verid-sigma.vercel.app and must always use the manifest address. Contract changes require a new frozen commit, source hash, deployment, parity comparison and frontend deployment.

The production Vercel deployment for this source is `dpl_3vdPvUDVNGNtcuXLRjvNaUXixNHw`. The final live attempt used profile creation `0x0df6d45b59da1b774f533b6a0d12fa39032b55c6893de5c3c31bc5ea1d0192b7`, challenge issuance `0x8aba05d70dcf02ebbbc7a9c3a52a7862020daf5e24cf491ff2135a06f2e37aea`, surface registration `0xb87e77f5ffb562da08631a4189c6f22f4a6d7fa351c3c65b6de3cd53087e6a6a`, and verification `0xeb5a8d54133e05679cf29fab093eadcde41f6673f5161e311c6a940e3559fe68`. The final readback was `UNVERIFIED` with unresolved semantic identity/authenticity, so no proof/gate success is asserted.
