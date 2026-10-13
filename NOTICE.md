# Attribution and dependency boundaries

IMAPlle Now (`apple-and-icloud-mail`) is Copyright (c) 2026 Thomas Kenny (mooserini), licensed under MIT. The setup and exact-folder guidance adapts the MIT-licensed `apple-imap` documentation from the `hermes-openwhispr` source inventory. [LICENSE](LICENSE) contains the package's MIT notice first, followed by the complete, unmodified third-party MIT notice (Copyright (c) 2026 hermes-openwhispr contributors) for that adapted documentation. The broader `agent-workflow-triage` skill was inspected for boundaries; its ledger/archive/report workflow is not bundled.

GigaMail and Himalaya are separately installed tools referenced by this guidance. No GigaMail or Himalaya runtime source, binary, credential store, configuration, or upstream manual is copied into the package. Installed GigaMail metadata was rechecked read-only on 2026-10-13 and identifies version 0.4.0 and license AGPL-3.0-or-later; any later runtime redistribution requires its own license review. Referenced third-party projects retain their own names, licenses and ownership.

Public documentation links are references rather than bundled manuals. Packaging follows [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins) and [skill authoring](https://developers.openai.com/plugins/build/skills), checked on 2026-10-05. A skills-only portable package does not require a bundled MCP server. The checked layout uses root `plugin.json`, not the legacy Cowork `.claude-plugin` layout.

Apple and iCloud are Apple names. This is an independent community candidate with no claim of Apple or OpenAI affiliation, endorsement, or full Apple-service coverage.
