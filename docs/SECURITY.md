# Security

Verid proves public account/domain/profile control or association; it is not KYC.

Evidence is HTTPS-only, local/private hosts are rejected, fetched content is bounded and treated as untrusted data, and challenge presence without semantic first-party context is insufficient.

Profile mutation requires the profile wallet. Gate membership requires an eligible proof belonging to the sender. The protected room never trusts localStorage or frontend-derived state.

Writes are Studionet 61999 only. Wrong-network writes are blocked in UI and immediately before signature. Finalized transactions are success only on explicit authoritative success; an absent execution result is reported as unknown and state is re-read.
