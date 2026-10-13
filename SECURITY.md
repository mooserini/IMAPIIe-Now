# Security — IMAPIIe Now

IMAPIIe Now (`apple-and-icloud-mail`) is an independent community project with
no Apple affiliation or endorsement. It ships MIT-licensed skills and
references, not a mail runtime, credential store, or enforced security sandbox.

## Report a problem

Report security concerns through this repository's
[GitHub issues](https://github.com/mooserini/IMAPlle-Now/issues). Issues are public;
submit a sanitized description, affected package/tool versions, expected
behavior, and a minimal reproduction using synthetic data. There is no security
contact email or private reporting service provided by this package.

**Never paste secrets.** Do not include an Apple Account password, app-specific
password, `.env` contents, keys, credential stores, authentication transcripts,
raw provider exceptions, or private mail. Do not attach unredacted screenshots
or logs. If a reproduction needs sensitive details, report only the safe failure
category and stop rather than publishing them.

## Credential exposure and rotation

If an app-specific password is exposed or suspected compromised:

1. Have the human revoke the matching app-specific password at
   [Apple Account](https://account.apple.com). Removing a plugin, deleting a
   local file, or changing a label does **not** revoke the password.
2. Have the human generate a replacement and enter it through unobserved,
   hidden local intake. Never send the old or new value through chat, agent
   tool arguments, screenshots, clipboard reads, or recorded terminal input.
3. Replace the one operator-held copy outside this repository. Remove any
   transient provisioned copies and secret-bearing temporary artifacts; verify
   cleanup using safe metadata, not by displaying the secret.
4. Treat previous authentication evidence as stale. Recheck only after fresh
   authorization names the exact host, account, folder, selection, and route.

Himalaya and GigaMail may share the same app-specific password. Revocation
therefore affects both; switching tools cannot repair an invalid credential.
An app-specific password label is a revocation aid, not a read-only or
folder-scoped credential restriction.

## Operational boundary

Installation and offline review do not authorize authentication, credential
intake, mail access, configuration changes, or server startup. Live mail checks
must use verified TLS to Apple IMAP (`imap.mail.me.com:993`), preserve the
approved account/folder/selection, and stop on invalid TLS or missing scope.
No SMTP or write operation is implied. Secrets must stay outside model context,
logs, reports, and analytics.

The policy is implemented by the operator's approval layer and separately
configured tools, not cryptographically enforced by these documents. Inspect
the actual helper/client before trusting its credential handling or flag
behavior. See [PRIVACY.md](PRIVACY.md), the
[setup skill](skills/icloud-mail-setup/SKILL.md), and
[account guidance](skills/icloud-mail-setup/references/accounts.md).
