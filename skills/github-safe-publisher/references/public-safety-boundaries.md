# Public Safety Boundaries

Use this reference before turning private work into a public GitHub artifact.

## Never Publish

- API keys, tokens, cookies, session values, OAuth secrets, SMTP credentials, SSH keys, private certificates, or `.env` files.
- Databases, spreadsheets, CSV exports, logs, browser profiles, raw analytics exports, backups, and generated archives.
- Client names, client assets, private conversations, invoices, proposals, contracts, NDAs, account data, or support tickets unless already approved for public use.
- Raw prompts, memory files, system instructions, hidden reasoning notes, private strategy, or private operating procedures.
- Local machine paths, usernames, workspace paths, deployment URLs, admin URLs, internal dashboards, or source-control remotes that reveal private infrastructure.
- Screenshots showing account menus, browser tabs, emails, API dashboards, customer data, file paths, analytics, invoices, or private project names.
- Production source code, deployment scripts, migrations, schemas, or config unless the user explicitly confirms they are intended for open source.

## Usually Safe To Generalize

- A workflow shape, such as intake -> AI draft -> human review -> approval -> export.
- A sanitized case study describing problem, workflow, outcome, and safety boundary.
- A skill, checklist, template, or fake-data example that teaches a repeatable process.
- Mock screenshots or diagrams recreated with fictional data.
- README improvements, repo descriptions, badges, changelog notes, and documentation that do not expose private details.

## Redaction Patterns

Use neutral replacements:

- `Example Client`, `Example Studio`, `example.com`
- `person@example.com`, `+1-555-0100`
- `YOUR_API_KEY_HERE`, `YOUR_TOKEN_HERE`
- `sample_project`, `demo-workflow`, `public-candidate`

Do not replace a real secret with another secret-looking value. Keep placeholders obviously fake.

## Public Case Study Boundary

A public case study can include:

- The business problem.
- The non-sensitive workflow.
- Human approval points.
- General stack categories, such as Python, SQLite, browser automation, or an LLM API.
- Outcomes described qualitatively or with approved aggregate numbers.
- What a client could adapt.

Keep out:

- Private implementation files.
- Raw data and prompts.
- Exact credentials, endpoint secrets, account identifiers, or internal path names.
- Client-specific details not explicitly approved for public use.

## Decision Rule

If a detail could help someone access, identify, impersonate, embarrass, or reverse-engineer a private person, client, account, system, or business process, remove it or rewrite it at a higher level.
