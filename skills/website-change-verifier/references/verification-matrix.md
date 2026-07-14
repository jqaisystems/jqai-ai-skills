# Website Verification Matrix

Select the rows that match the actual change. A passing file edit is not sufficient evidence for a user-visible result.

| Change | Required checks |
|---|---|
| Copy or exact replacement | Syntax or build, target route, new text present, old text absent, encoding, visible rendering |
| New page or route | Source registration, production build, direct request, refresh behavior, title, H1, canonical, navigation, and discovery policy |
| Layout or CSS | Build, desktop rendering, mobile rendering, overflow, interaction, contrast, and image cropping |
| Navigation or internal links | Every affected target, active state, keyboard access, and intentional removal from nearby indexes |
| Blog post | Content model or registry, article route, listing route, metadata, structured data, credits, related links, sitemap, and social image |
| Metadata or SEO | Rendered title and description, canonical, Open Graph, structured data, sitemap, and robots consistency |
| Hide or restore | Exact target, navigation state, direct-access behavior, sitemap and search policy, preserved assets, and adjacent pages |
| Form | Client validation, server handler, error state, success state, spam controls, and recipient configuration without exposing values |
| Media | File existence, dimensions or codec, responsive crop, loading behavior, alt text, and no unintended replacement |
| Static export | Production export, generated route file, asset paths, and direct serving from the export output |
| Deployment | Live status, final URL, rendered content, canonical host, cache behavior, and difference from localhost |

## Local server discipline

- Check the expected port before starting a process.
- Reuse a known healthy server for the same project when possible.
- Record the project root, command, process, and base URL used.
- Confirm the listener and make an HTTP request before calling the server ready.
- Stop only processes started for the current task.

## Browser checks

- Inspect the actual target route.
- Test a representative desktop width and a narrow mobile width.
- Exercise changed controls, menus, media, forms, and anchor links.
- Check the console and failed network requests when JavaScript behavior changed.
- Capture proof only after the final route state is loaded.
