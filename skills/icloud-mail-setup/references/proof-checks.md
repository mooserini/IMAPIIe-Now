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

For a minimal live proof, first prepare the exact account alias, host, folder, selection and route. Request authorization to use the existing stored credential internally and contact iCloud IMAP with verified TLS for authentication, folder metadata, and at most five unread headers in that exact folder. No bodies, attachments, SMTP, flags/moves/deletes, key inspection, secret output, server startup, configuration changes, or remote deployment. If flag verification needs a second metadata scan, include it in that proposal. Prove primary/fallback parity only if the fallback is also explicitly included. If no unread headers exist, report the empty selection and limited proof.

Provisioning, secret rotation/intake, server startup, native-Mac permissions, installation, and remote deployment are separate approval boundaries. A denied live check leaves offline validation useful; do not relax its scope to finish a proof.
