# Deployment

Target only GenLayer Studionet: chain 61999, RPC https://studio.genlayer.com/api, explorer https://explorer-studio.genlayer.com.

Stage One does not fabricate deployment evidence. `config.js` and `verid-manifest.json` remain blank/null until a verified deployment exists.

Final pass: run GenVM/Direct Mode checks, complete adversarial review, hash exact source, deploy exact reviewed bytes, record address/tx/hash/commit, configure frontend with the real address, re-run checks and verify live reads/writes.
