# IMAPIIe Now — offline inventory

Independent community guidance; no Apple affiliation or endorsement. This
example grants no live mail access.

```text
Use IMAPIIe Now for an offline inventory only. Review the package manifest,
skill frontmatter, reference files, and local links. Inspect only bounded
implementation files and nonsecret tool/version metadata on this host.

Do not authenticate, contact a mail server, read mail, call account APIs,
import modules that initialize account storage, or inspect keys or credential
payloads. Do not read .env, dump environments or account configuration, start
a server, install tools, change settings, or deploy anything remotely.

Report the execution route as Remote-capable guidance and the achieved stage
as offline inventory only. List package checks and separately installed
transport availability with passed, failed, or not run evidence. Distinguish
manual field checks from full schema validation; versions prove presence,
not authentication. Report unresolved prerequisites without exposing secrets.
```

Expected result: a bounded inventory and the next concrete approval needed,
not an authentication claim. Missing live authorization does not prevent
useful offline review. Nothing in this example authorizes credential intake.

See [the setup skill](../skills/icloud-mail-setup/SKILL.md) and
[proof stages](../skills/icloud-mail-setup/references/proof-checks.md).
