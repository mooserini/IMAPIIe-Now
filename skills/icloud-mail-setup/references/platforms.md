# Execution labels

Assign one of these labels before planning an action. Portability of instructions does not imply availability of accounts, binaries, local files, or connected services.

| Label | What can run there | Evidence needed |
| --- | --- | --- |
| Remote-capable guidance | Read these instructions, review sanitized metadata, validate package files and synthetic fixtures | Package present; no live account needed |
| Configured-host IMAP | Existing GigaMail/scoped helper or Himalaya on a supported host, local or remote | Actual binaries/helpers, operator-approved host-side secret source, network reachability, user account, and scoped authorization on that host |
| Mac-required dependency | A bridge/store bound to the user's Mac; any later native Apple APIs/UI or Keychain-dependent route | That Mac available with the exact approved dependency/permissions; those native features are outside v1 |
| Remote live access: unproved | A cloud task wants to use a Mac-local bridge or credential store | A separately designed, secured, explicitly authorized connection and deployment; none is supplied by v1 |

An existing Mac-local stdio MCP server is not automatically reachable from a cloud task. Installing skills on the web does not deploy local helpers or credential stores. Do not copy secrets to make a remote task work, expose a local service, open ports/tunnels, or turn a stdio runtime into a hosted endpoint as part of setup review.

Direct iCloud IMAP is not inherently Mac-only. Remote use remains conditional on a supported runtime, an operator-approved host-side secret on that host, network access, and explicit account scope. Discover the approved secret source and identifier through safe metadata or ask; do not assume Hermes or a particular store. Follow the [credential-resolution rules](../SKILL.md#credential-resolution-no-second-key-no-symlink): exactly one stored copy, resolution only at call time, no standing symlink or broad store access, and no secret output. After any separately approved transient provisioning, the provisioned secret and all secret-bearing temporary artifacts must be purged after success, failure, or interruption, restoration to one stored copy verified without exposing the value, and cleanup or its failure reported. Retention requires a separate, documented operator-approved exception with purpose, access scope, and removal/rotation plan. This candidate has not tested a remote live route. Do not infer support from a portable folder or from cross-platform upstream claims.
