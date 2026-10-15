# Existing bridge and Himalaya fallback

**Route: configured host.** Runtime code is not included; the two reviewed helpers ship under `helpers/` (pinned; see `helpers/PROVENANCE.md`). First locate the tools on the execution host and inspect current schemas or bounded source without loading credential modules.

Resolve the operator-approved host-side secret source and identifier through safe metadata, or ask if they are missing or ambiguous. Apply the [credential-resolution rules](../SKILL.md#credential-resolution-no-second-key-no-symlink) to every transport: exactly one stored copy, resolution only at call time inside the approved operation, no standing symlink or broad store access, and no secret output. `APPLE_IMAP_PWD` and Hermes `.env` are default variable/store examples, not transport requirements. Inspect whether the installed helper can use a narrowly scoped resolver; do not assume the reviewed GigaMail lookup already supports another store. If approved provisioning is needed, keep it transient, purge the provisioned secret and secret-bearing artifacts after success, failure, or interruption, verify restoration to one stored copy without exposing the value, and report cleanup or its failure. Retention requires a separate, documented operator-approved exception with purpose, access scope, and removal/rotation plan.

The 2026-10-05 source inventory reviewed GigaMail 0.4.0 and Himalaya 2.2.1. Read-only re-verification on 2026-10-13 confirmed those installed versions on macOS aarch64 and both helper files; their hashes still match the earlier inspected snapshots. This confirms presence and unchanged helper bytes, not authentication, live flags, or mailbox access. The cached GigaMail plugin was reported as a separate skill-only 0.3.3 package; that report is not proof of runtime parity. Do not silently install/upgrade either dependency. No Node runtime is needed for this candidate. If later tooling requires Node, use a per-repository fnm version and inspect transitive dependencies; do not use Homebrew Node.

The existing `apple-imap` bridge has two separately maintained helpers:

| Capability | Reviewed implementation | Important boundary |
| --- | --- | --- |
| Primary scoped reader | `scoped_read.py`: explicit account ID/store, verified iCloud TLS, readonly selection (EXAMINE), UID SEARCH, BODY.PEEK | One exact folder; paginate; no send/write; not an OS sandbox |
| Himalaya fallback | `himalaya_read.py`: explicit profile, GigaMail credential lookup, anonymous inherited pipe, temporary secret-free TOML, logging off | Same credential store; independent client, not independent credentials |

These filenames identify the helpers pinned under `helpers/` (see `helpers/PROVENANCE.md` for source and hashes). If a pinned helper is absent or hash-mismatched on the current host, report it unavailable and propose provisioning separately. Confirm current implementation before using it. The scoped helper bypasses the general MCP tool path; do not assume the server's approval layer applies. A human request authorizing the same scoped operation through available existing transports covers an equivalent configured fallback. Honor any restriction to a named route. If authorization permits only offline review, metadata, or one specific route, obtain the missing boundary before using a different live route; do not re-request permission already granted.

GigaMail 0.4.0 `list_unread` is inbox-focused and has a date window; general search can span more broadly. Neither proves an exact-folder, all-unread check. Choose a schema that expresses the requested scope or an inspected scoped helper. Avoid generic CLI body reads when their flag behavior is unverified.

Himalaya configuration/CLI changed between major versions. The reviewed v2 helper hands a decrypted password through an inherited anonymous pipe, with no password in child arguments, temporary TOML, or environment. The process still handles the secret internally. It selects a mailbox read-write internally, then uses STATUS, UID SEARCH, metadata FETCH and BODY.PEEK; no STORE, EXPUNGE, send, move, delete, or `--seen`. No native-Mac/API permission is implied by this route.

Before fallback, require the same account, exact folder, selection and approved actions, an available configured helper/client, accessible authorized store, and a failure category the fallback can plausibly address. Do not automatically fallback on invalid credentials, denied permission, invalid TLS, or missing scope. A missing folder stays blocked even if INBOX is accessible.

Use one successful transport per scan. Retain account/folder/UIDVALIDITY/UID and Message-ID identities, coverage, failures and pagination. Discard UID-based results if UIDVALIDITY changes. Report oversized/truncated bodies and unread attachments as incomplete evidence. A successful switch is not a second mailbox source.

Dependencies and upstream references: [GigaMail](https://github.com/adecubed/gigamail), [Himalaya](https://github.com/pimalaya/himalaya), [Himalaya 2.2.1 configuration](https://github.com/pimalaya/himalaya/blob/v2.2.1/config.sample.toml). No third-party runtime code is redistributed here.
