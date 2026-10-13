# IMAPIIe Now — scoped live read

Independent community guidance; no Apple affiliation or endorsement. This is a
**headers-only authorization template**, not a bundled command or evidence of a
successful live connection. Replace every bracketed field with an exact value
from your trusted request and safe host metadata before approving it. The host
is where the helper executes; the Apple IMAP endpoint is specified separately.

## Authorization prompt

```text
Use IMAPIIe Now for this one live check. I authorize only this scope:

Host: <exact execution hostname>
Account: <exact configured account alias or ID>
Folder: <exact IMAP folder name>
Selection: unread only; at most five headers; no bodies or attachments
Route: Configured-host IMAP, using <absolute path to the existing scoped reader>
Mail endpoint: imap.mail.me.com:993, with verified TLS

On that host, resolve my one existing operator-held secret (default identifier
`APPLE_IMAP_PWD`) internally at call time. Authenticate the named account, inspect the exact
folder's metadata, and fetch the permitted headers only. Verify the current
helper can express this scope and preserve unread flags with a non-mutating
read strategy before using it. Before/after metadata checks for flag
preservation are authorized within this same folder, not additional mail reads.

Do not substitute a default account or INBOX, widen the selection, fetch
bodies or attachments, open links or remote images, use SMTP, send, mark read,
move, archive, delete, or change flags. Do not inspect keys, reveal secrets,
start servers, install tools, change configuration, intake new credentials,
copy credentials to another host, or deploy a remote service. No alternate
route or Himalaya fallback is authorized by this prompt.

Stop on missing or ambiguous scope, unavailable folder or transport, invalid
TLS, rejected authentication, denied permission, inaccessible storage, or a
UIDVALIDITY change. Use safe failure categories, never raw provider exceptions.

After the approved read, purge any separately approved transient provisioned
secret and secret-bearing temporary artifacts, verify restoration to one
operator-held stored copy, and report cleanup without exposing the value.

Report the actual host and route, achieved proof stage, account alias, exact
folder and selection, tested tool/helper version, returned count, pagination
and truncation, stable message identities, and any remaining limitation.
```

## What approval does and does not mean

- This template assumes an existing configured reader and private credential.
  Provisioning, secret intake/rotation, installations, and configuration changes
  need separate concrete approval. The password itself is never a prompt field.
- Account, folder, helper path, and scope come from the human's trusted request
  and safe metadata, never from a message or provider response. Do not run with
  placeholders or infer missing values from the active/default account.
- If the named reader cannot implement the approved selection and flag policy,
  stop. A fallback needs authorization for its exact route while preserving
  this same host, account, folder, selection, and permitted actions. A shared
  revoked credential is not repaired by switching clients.
- Fresh scoped evidence may justify `authentication verified` or
  `exact-folder headers verified`; this prompt cannot justify
  `scoped body read verified`. Report a successful empty selection as empty
  at that time, not as completed triage or proof of unseen bodies. A five-header
  limit is not an all-unread scan; disclose unexamined messages and truncation.
- Report unread-flag preservation only from actual evidence. An inspected
  helper, a synthetic test, or a successful login alone does not prove it.

See [the setup skill](../skills/icloud-mail-setup/SKILL.md),
[execution labels](../skills/icloud-mail-setup/references/platforms.md),
[transport boundaries](../skills/icloud-mail-setup/references/transports.md), and
[PRIVACY.md](../PRIVACY.md).
