# Example Workflow Summary

Example Review Queue is a fictional workflow for checking public release copy before publication.

## Workflow

1. A draft release note is prepared from approved public facts.
2. A reviewer checks for unclear claims, sensitive wording, and missing context.
3. The release owner makes any edits requested by the reviewer.
4. A final human approval step confirms the copy is ready for public use.
5. Approved copy moves into the public release draft.

## Human Review Gate

No public release happens until a human approves the final diff.

The review should confirm:

- all names and examples are fictional or approved for public use;
- links point only to public pages;
- screenshots, logs, exports, account data, and private implementation notes are not included;
- the final staged diff matches the intended public artifact.

## Expected Output From The First Skill

When `github-safe-publisher` reviews this folder, the expected output should include:

- a safety verdict;
- inspected files;
- scanner summary;
- manual review checks;
- exact next commands for diff review;
- a reminder that publishing waits for human approval.
