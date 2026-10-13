# Proof stages

For offline review, inspect only selected source files and nonsecret version/package metadata. Do not call account APIs or server initialization. Use isolated synthetic fixtures and mocked clients for success, empty result, errors, fallback, permission refusal, and secret-containing diagnostics.

| Stage | Passing evidence | Does not prove |
| --- | --- | --- |
| Package | Manifest schema validation, valid skill frontmatter, resolved local links, no personal paths/accounts or credential payloads | Host import/install/discovery |
| Source inventory | Bounded source inspection with recorded version and file hashes | Current authentication or runtime health |
| Synthetic execution | Mock IMAP plus fake child process; no network/store access | Apple behavior, unchanged live flags, every possible secret leak |
| Tabletop skill review | Agent responses to realistic requests while using the skill | Runtime enforcement or universal instruction compliance |
| Live integration | Fresh scoped evidence from an approved account/host/folder | Other accounts, folders, hosts, future health |

Report `passed`, `failed`, or `not run` separately for each stage; include limitations and failures. Do not rename a manual field check a full schema validation, or a scenario oracle a live test. Never copy raw provider exception strings into reports. Prefer allowlisted categories: authentication rejected, store inaccessible, permission denied, folder unavailable, TLS invalid, scan incomplete, transport unavailable. Redact or suppress diagnostics before model-visible output.

For a minimal live proof, first prepare the exact account alias, host, folder, selection and route, plus the operator-approved host-side secret source and identifier. Discover these through safe metadata or ask for missing inputs; do not inspect or print the secret. Request authorization to resolve the selected credential internally at call time and contact iCloud IMAP with verified TLS for authentication, folder metadata, and at most five unread headers in that exact folder. Follow the [credential-resolution rules](../SKILL.md#credential-resolution-no-second-key-no-symlink): exactly one stored copy, no standing symlink or broad store access, and no duplicate retention without a separate documented operator-approved exception. No bodies, attachments, SMTP, flags/moves/deletes, key inspection, secret output, server startup, configuration changes, or remote deployment. If flag verification needs a second metadata scan, include it in that proposal. Prove primary/fallback parity only if the fallback is also explicitly included. If no unread headers exist, report the empty selection and limited proof.

If transient provisioning was separately approved, its proof is incomplete until the provisioned secret and secret-bearing temporary artifacts are purged, restoration to one stored copy is verified through safe metadata, and cleanup or its failure is reported. Apply cleanup after success, failure, or interruption; if it cannot be verified, report it as incomplete rather than claiming restoration. Any retention exception must document the retained copy, purpose, access scope, and removal/rotation plan.

Provisioning, secret rotation/intake, server startup, native-Mac permissions, installation, and remote deployment are separate approval boundaries. A denied live check leaves offline validation useful; do not relax its scope to finish a proof.
