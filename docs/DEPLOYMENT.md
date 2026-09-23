# Deployment

Target only GenLayer Studionet: chain 61999, RPC https://studio.genlayer.com/api, explorer https://explorer-studio.genlayer.com.

The canonical deployment is `0x5fDd2fC78Ddc1D904662B2D8A7174C17f85B5076`, transaction `0xc4ba82645f79eb0fe43641e15762671f3c54858c70ad666d079ce2f10c9fc333`. The receipt is `FINALIZED`, with unanimous agreement (5/5). RPC readback proves exact source parity: 24,520 bytes and SHA-256 `7ca2498af989b0cd0b332294f58538f3eecce2b9710cd554d342ac46593b513d` match local source. Frozen contract source is commit `df679a9aa1203e71a6e21c9678615d87dc7d5173` (Git blob `c35a17b2308a41d709947d07712ea297482388d5`).

The earlier deployments `0xD4d621bBD288496cab9f7f5Ec23C579816D84EB3` and `0x4A430f7326DEdcd796df149Ce5d31223c5943d92` are superseded historical evidence. The contract address in `config.js` now points to the finalized deployment above.

The existing production site is https://verid-sigma.vercel.app. Its Vercel deployment and live browser lifecycle walkthrough are still pending; do not claim full production readiness until those are verified.

The previous live attempt on the superseded deployment returned `UNVERIFIED` with unresolved identity and authenticity. That is unsuccessful historical evidence. No complete live lifecycle is claimed for the current deployment.
