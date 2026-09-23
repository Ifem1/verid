# Deployment

Target only GenLayer Studionet: chain 61999, RPC https://studio.genlayer.com/api, explorer https://explorer-studio.genlayer.com.

The currently configured deployment is `0xD4d621bBD288496cab9f7f5Ec23C579816D84EB3`, transaction `0x579901dc9706ec0d13c88b55224309ee191107b4bbfb7cb5140dbfae3bdb6f65`. The CLI receipt was `ACCEPTED` with majority agreement. Finality and exact source parity remain unverified, so it is not a canonical release deployment. The prior `0x4A430f7326DEdcd796df149Ce5d31223c5943d92` deployment is superseded historical evidence.

The previously verified source commit `5d0009502b7f39a05fc15a7b8b9f5577d3dbd895` belongs to the superseded deployment only. Current contract source has changed; the deployment above has not been read back and compared. A release must freeze the exact source commit, record its byte length, SHA-256, and Git blob, wait for `FINALIZED`, fetch deployed source, decode it, and prove exact byte parity.

The existing production site is https://verid-sigma.vercel.app; update it only after contract finality and source parity pass. Contract changes require a new frozen commit, source hash, deployment, parity comparison, and frontend deployment.

The previous live attempt on the superseded deployment returned `UNVERIFIED` with unresolved identity and authenticity. That is unsuccessful historical evidence. No complete live lifecycle is claimed for the current deployment.
