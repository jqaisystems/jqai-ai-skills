# Local package contract, version 1

Python 3.11+, standard library only. No network, automatic dependency installation, build execution, or remote operations.

## Commands

- prepare requires --build-dir, --package-dir, and --state-dir.
- verify requires --package-dir.
- confirm requires --package-dir, --state-dir, --package-id, and --acknowledge-upload.
- Every command supports --json. Exit 0 means the requested local operation passed; exit 1 means refusal/failure, not permission to retry an upload.

Package output must be absent, its parent must exist, and build/package/state paths must not overlap. Local directory links, reparse points, network paths, special files, nonportable names, and case-insensitive collisions are refused. A locked state is not automatically unlocked after a crash; first verify that no operation is active.

The filename guard refuses environment files, common access/configuration files, repository metadata, dependency trees, source maps, and selected sensitive extensions. A legitimate configuration asset may require a separately reviewed packaging approach. Do not bypass the guard by renaming a private file. Inline secrets or private copy in ordinary HTML/JavaScript still require a separate content review.

## Package and state

Each package contains only:

- upload/: changed/new files, retaining relative paths.
- manifest.json: schema_version, created_at, baseline_id, complete snapshot, upload subset, removed paths, and package_id.

Each file record has a nonnegative byte size and SHA-256. Package identity is SHA-256 of canonical JSON for all manifest fields except package_id, using sorted keys, compact separators, and ASCII escapes. JSON object order is irrelevant; paths and file contents are not.

The state directory contains state.json and, while an operation is active, a lock directory. State version 1 records the confirmed baseline, latest pending package, and acknowledgement history. JSON records are limited to 16 MiB. Do not edit them to force acceptance.

The initial package contains the complete nonempty export. Subsequent packages compare bytes against the last confirmed snapshot, not timestamps or the last local preparation. Unconfirmed changes remain eligible. Preparing a newer package makes older pending IDs stale.

Preparation checks copied payloads and re-snapshots the source before registration. A crash after package creation but before state registration can leave an orphan package; it cannot be confirmed. Preserve it for inspection and prepare a fresh package in a new directory. Failed operations never advance the confirmed baseline.

Confirmation verifies package identity and contents, latest pending identity, baseline identity, and exact change/removal sets. One atomic state replacement records both the new baseline and acknowledgement history. Only complete uploads may be acknowledged.

## Meaning and limits

The baseline represents the build the user says was uploaded, not an independently observed server inventory. Removed paths are reports only: they may still exist remotely. Keep earlier manifests for unresolved removal history. Files present remotely before the first baseline remain unknown.

Hashes detect accidental alteration against the recorded manifest; they are not signatures against an attacker who can replace both package and state. Use controlled local folders and preserve private review evidence. Do not modify these directories concurrently with the helper.

Never upload state, manifests, source directories, review reports, or backups.
