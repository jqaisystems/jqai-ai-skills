# Utility Skill Proof Pack

Sample only. This fake-data pack shows the expected output shape for three lightweight utility skills:

- `web-scraper`
- `code-deduplicator`
- `em-dash-remover`

The examples use fictional pages, code, and copy. They do not include private source, account data, exports, browser profiles, raw logs, credentials, customer records, or local machine paths.

## Why This Exists

Some skills are intentionally small. They still need public proof, but the proof should match the job.

This pack gives visitors a quick way to inspect what the utility skills are supposed to produce before installing them.

## Example 1: `web-scraper`

### Fake Request

```text
Use $web-scraper to create a browser console scraper for this public demo catalog.

Goal:
- collect title, category, and public detail URL from each visible card
- keep results in localStorage while moving through pages
- return JSON that can be copied for review
```

### Public-Safe Assumptions

- The page is public or explicitly authorized for extraction.
- The user is collecting visible card text and public links only.
- No login-only areas, account menus, analytics panels, forms, or private records are included.
- The user will review site rules and avoid aggressive request patterns.

### Expected Output Shape

```js
const STORAGE_KEY = "example_catalog_items";

const existing = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");

const pageItems = [...document.querySelectorAll(".demo-card")].map((card) => ({
  title: card.querySelector(".demo-card-title")?.textContent.trim() || "",
  category: card.querySelector(".demo-card-category")?.textContent.trim() || "",
  url: new URL(card.querySelector("a")?.getAttribute("href") || "", location.href).href,
}));

localStorage.setItem(
  STORAGE_KEY,
  JSON.stringify([...existing, ...pageItems], null, 2)
);

console.table(pageItems);
```

### Example JSON Result

```json
[
  {
    "title": "Starter Workflow Notes",
    "category": "Documentation",
    "url": "https://example.com/catalog/starter-workflow-notes"
  },
  {
    "title": "Release Checklist Template",
    "category": "Templates",
    "url": "https://example.com/catalog/release-checklist-template"
  }
]
```

### Review Notes

- `READY` for a public demo page with visible text only.
- `REVIEW` if the selectors are unstable or the site has clear scraping restrictions.
- `BLOCK` if the page requires login, exposes private records, or contains account data.

## Example 2: `code-deduplicator`

### Fake Request

```text
Use $code-deduplicator to reduce repeated formatting helpers in this small sample.

Goal:
- keep behavior the same
- avoid a broad refactor
- explain what changed
```

### Before

```js
function formatStatusBadge(status) {
  const clean = String(status || "").trim().toLowerCase();
  if (!clean) return "unknown";
  return clean.replace(/\s+/g, "-");
}

function formatPriorityBadge(priority) {
  const clean = String(priority || "").trim().toLowerCase();
  if (!clean) return "unknown";
  return clean.replace(/\s+/g, "-");
}
```

### After

```js
function formatBadgeValue(value) {
  const clean = String(value || "").trim().toLowerCase();
  if (!clean) return "unknown";
  return clean.replace(/\s+/g, "-");
}

function formatStatusBadge(status) {
  return formatBadgeValue(status);
}

function formatPriorityBadge(priority) {
  return formatBadgeValue(priority);
}
```

### Expected Review

```text
READY

Changed:
- Extracted the shared cleanup behavior into formatBadgeValue.
- Kept the original function names so callers do not change.
- Avoided broader naming, rendering, or data-shape changes.

Verification:
- Empty values still return "unknown".
- Whitespace is still trimmed.
- Multi-word values still become hyphenated lowercase strings.
```

### Review Notes

- `READY` when the duplicate is exact or nearly exact and behavior is preserved.
- `REVIEW` when similar-looking code has different edge cases.
- `BLOCK` when the requested cleanup would change public behavior without tests or approval.

## Example 3: `em-dash-remover`

### Fake Request

```text
Use $em-dash-remover to clean this short product note without changing meaning.
```

### Before

The fake input labels the em dash placeholder so this repository can keep the example ASCII-safe.

```text
The toolkit helps teams package repeatable AI work [em dash] but the real value is review discipline. Each skill carries its own safety notes, examples, and output expectations.
```

### Expected Output

```text
The toolkit helps teams package repeatable AI work. The real value is review discipline. Each skill carries its own safety notes, examples, and output expectations.
```

### Edit Notes

```text
READY

Changed:
- Replaced the dash break with two shorter sentences.
- Preserved the original meaning.
- Kept the tone direct and public-safe.
```

### Review Notes

- `READY` when the edit removes the punctuation pattern without changing meaning.
- `REVIEW` when the sentence needs a tone decision.
- `BLOCK` if the copy includes sensitive or unpublished material that should not be edited in a public example.

## Combined Utility Workflow

These utility skills can work together after a larger public-safe workflow:

1. Use `web-scraper` only for public or authorized page extraction.
2. Use `research-brief-curator` if the extracted links need to become a reviewed brief.
3. Use `em-dash-remover` on final public copy if punctuation cleanup is needed.
4. Use `code-deduplicator` separately on code changes, with diff review before applying.

## Safety Boundary

Use this pack as an output-shape reference only. Before adapting it to real work:

- confirm extraction is allowed;
- remove private records, account data, exports, logs, credentials, and private source;
- use fake data for public examples;
- review diffs before committing code changes;
- review final copy before publishing.
