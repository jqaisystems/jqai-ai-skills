# Framework Checks

Use only the section matching the detected project. Prefer the project's documented commands when they differ from these defaults.

## PHP

Detection markers:

- `.php` entrypoints or templates
- Composer configuration or a documented PHP router

Checks:

- Run `php -l` on every changed PHP file.
- Start the documented local router or server and request the target route directly.
- Verify shared includes, content registries, form handlers, metadata, and discovery files affected by the change.
- Test both success and error states for forms or dynamic routes.

## Static HTML

Detection markers:

- standalone `.html` pages
- shared CSS or JavaScript assets
- no required application build manifest

Checks:

- Serve the actual project root through a local HTTP server.
- Test direct page URLs, navigation links, asset paths, encoding, metadata, and responsive rendering.
- Confirm hidden content policy across navigation, direct access, sitemap, and search directives.

## Next.js or React

Detection markers:

- `package.json` with Next.js, React, Vite, or a related framework
- application folders such as `app`, `pages`, or `src`

Checks:

- Read the installed framework version and use its documented lint, type, test, and production-build commands.
- Verify generated and dynamic routes through direct navigation and refresh.
- Inspect metadata, structured data, client interactions, failed network requests, and any static export output.
- Test a narrow mobile viewport and a representative desktop viewport.

## Other frameworks or mixed sites

- Inspect manifests, entrypoints, server configuration, content registries, and hosting notes before choosing commands.
- Distinguish source folders, generated output, upload packages, and live document roots.
- Prefer existing project scripts over generic commands.
- Record any verification layer that cannot be completed safely.
