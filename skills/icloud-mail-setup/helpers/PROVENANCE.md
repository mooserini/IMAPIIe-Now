# Helpers provenance

Vendored 2026-10-15 from the working copies at
`hermes-openwhispr/skills/apple-imap/scripts/` (untracked there — this
plugin is their canonical published home).

SHA-256 at vendoring (must match the reviewed sources byte-for-byte):

- `scoped_read.py`:
  `a6fb18f3ecf083d7dd44d6948915abdfd7bf6fd4949bd605079ea86cb4b72b3c`
- `himalaya_read.py`:
  `1f0d207f555b96f2dfea543ee50f34901f2356b60304238fad292e9cb9e42dfd`

These are the files re-verified 2026-10-13 against the 2026-10-05 inspected
snapshots (see `references/transports.md`). Helper bytes are kept exact so
that claim stays checkable; adopt any upstream change deliberately and
re-record hashes here.

Runtime prerequisites (not bundled): GigaMail 0.4.0+ with a scoped-reader
account, Himalaya 2.x binary, `GIGAMAIL_ROOT` set, human-entered
app-specific password. See `references/accounts.md`.
