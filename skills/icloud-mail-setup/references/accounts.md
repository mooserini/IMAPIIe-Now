# Per-user accounts and credential intake

**Route: configured host; human secret intake.** A Mac is required only when the chosen storage or tools depend on that Mac. Never reuse a package author's profile or account.

Use the user's iCloud Mail address, which may differ from their Apple Account sign-in. The reviewed GigaMail CLI authenticates with its email field; use the full iCloud Mail address. Apple's documented incoming server is `imap.mail.me.com`, port `993`, with verified TLS. POP is unsupported. If a setup UI requires outgoing fields, the documented SMTP values are `smtp.mail.me.com`, port `587`, with TLS/STARTTLS and authentication. Supplying SMTP fields does not authorize sending. See [Apple server settings](https://support.apple.com/en-us/102525).

For this IMAP bridge, the human generates an app-specific password at [Apple Account](https://account.apple.com), under Sign-In and Security → App-Specific Passwords. Two-factor authentication is required. Supported apps may offer Apple Account authorization instead; do not claim that this bridge implements it. See [Apple password guidance](https://support.apple.com/en-us/102654).

Prepare the private runtime/store proposal first. Keep secrets outside the plugin, source repositories, shared/synced document locations, and deliverables. Use a per-user nonsymlink data directory with owner-only access; inspect ownership/mode only. Specify one explicit store root for CLI, bridge, and helpers. Check redacted path metadata for conflicting overrides without dumping environment values.

After authorized preparation, have the human run their resolved GigaMail executable with `accounts add-imap` in an unrecorded local terminal. For the reviewed Python CLI, `PYTHONWARNINGS=error::getpass.GetPassWarning` makes an unsafe echoed-password fallback fail. Do not pipe answers, automate secret entry, capture the screen, or read the clipboard. The human enters the mail address, app-specific password, and required server fields. If hidden input is unavailable, stop intake.

GigaMail 0.4.0 was inspected as a separate dependency. Its macOS account data is encrypted in `.accounts.db`; the key is stored beside it in `.accounts.key`, not in macOS Keychain. Internal account lookup decrypts credentials, and importing its account module initializes storage. Do not import it for offline inventory or dump internal account objects. Other versions/platforms can differ. Do not migrate storage, remove accounts, create credentials, or patch upstream behavior without a concrete approved change.

After human setup, metadata and storage success are preliminary stages. Test authentication only when authorized; mailbox headers or bodies need their own scoped permission. Handle missing account, rejected authentication, unavailable store, and denied permission distinctly. Do not use the active/default account as a substitute.

For revocation, the human selects the matching app-specific password at Apple Account. Revocation affects both clients if they share it; changing/resetting the primary password revokes all app-specific passwords. If a secret was exposed, do not repeat it: tell the user to revoke and replace it through hidden intake. A password label does not constrain the client, folder, protocol, or action.
