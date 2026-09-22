# Deployment

Target only GenLayer Studionet: chain 61999, RPC https://studio.genlayer.com/api, explorer https://explorer-studio.genlayer.com.

The canonical deployment is recorded in `verid-manifest.json` and `config.js`: contract `0x53a45b9483aF795648a607cA1C900a766863F076`, transaction `0xd084d38f607e52249dc303dea09e6db31009f54a8951e8ec62d8fb2a7e748930`.

The frozen contract source is commit `ab2bac6b7e2f8a7f832f8003dbccd6b57d65a42a`, 19,407 bytes, SHA-256 `a4fa64ac91404458c48f7159d71241938ea071eddfba156e7e0b5d05b2b109b9`. Deployed source is retrieved with `gen_getContractCode` and compared as UTF-8 contract text.

The frontend is deployed at https://verid-sigma.vercel.app and must always use the manifest address. Contract changes require a new frozen commit, source hash, deployment, parity comparison and frontend deployment.
