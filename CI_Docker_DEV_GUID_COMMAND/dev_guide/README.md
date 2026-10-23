# Developer guide

A one-page dashboard that shows how to use every part of this project: setup, API keys, settings, Git scripts, uv, Docker, Ruff, tests, commit checks and GitHub Actions. Each feature has its own color, step-by-step instructions and an example.

## Open it

```bash
open CI_Docker_DEV_GUID_COMMAND/dev_guide/index.html        # macOS
xdg-open CI_Docker_DEV_GUID_COMMAND/dev_guide/index.html    # Linux
start CI_Docker_DEV_GUID_COMMAND/dev_guide/index.html       # Windows
```

Or right-click `index.html` in VS Code and choose **Reveal in Finder**, then double-click it.

## Files

| File | What it is |
| --- | --- |
| [index.html](index.html) | The guide |
| [styles.css](styles.css) | Layout and the feature colors (at the top, under `:root`) |
| [script.js](script.js) | Adds "Copy" buttons to the examples (optional) |
| [reference/dashboard-reference.png](reference/dashboard-reference.png) | The design the layout is based on |

## Add a feature

1. Add a color for it in `styles.css`, e.g. `--myfeature: #0ea5e9;`.
2. In `index.html`, copy an existing `<section class="guide">` and change its `id`, text and `style="--c: var(--myfeature)"`.
3. Add a link in the sidebar, the color legend and one of the tabs.
