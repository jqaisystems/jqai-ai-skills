# Batch And Monitoring

Use this reference when optimizing multiple listings.

## Priority Signals

Prioritize listings with:

- Missing or weak tags.
- Poor title fit.
- High views but low conversion.
- Strong product fit but weak keyword coverage.
- Old listings that have not been refreshed recently.
- Missing images, attributes, or clarity.
- Seasonal urgency.

Avoid changing too many variables at once when the user wants to measure impact.

## Batch Size

Use small batches by default:

- 5-10 listings for a small shop.
- 10-20 listings for a larger shop when data quality is strong.
- Fewer listings when the changes are large or risky.

## Batch Output

Return:

```text
Batch name:
Goal:
Listings:
Data freshness:
Recommended order:
Risks:
Human review checklist:
Next review date:
```

Use fake listing names or approved identifiers in public docs.

## Monitoring Cadence

Recommend waiting long enough for marketplace behavior to settle before judging results. Use a 14-30 day review window by default unless the user has a different platform-specific cadence.

Track:

- Views.
- Visits.
- Favorites.
- Conversion signals.
- Ranking or keyword movement when available.
- Which fields changed.
- Date changed.

## Changelog

For each listing, maintain a simple changelog:

```text
date
fields_changed
reason
keywords_added
keywords_removed
next_review_date
notes
```

Do not publish changelogs containing private sales data, customer details, or raw export rows.
