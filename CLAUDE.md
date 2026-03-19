# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **100% static, single-file** offline data inspection tool. The entire application lives in `datatables.html` — no build system, no backend, no bundler. The legacy starting point is `index.html` (and `CSV_Viewer.html`).

## Running Locally

```
python -m http.server 8000
```

Then open `http://localhost:8000/datatables.html`. The folder-scan feature for auto-loading CSV/XLSX files requires HTTP (not `file://`).

No build, lint, or test commands exist — this is a static HTML/JS/CSS project.

## Architecture

All code lives inside `datatables.html` structured as labeled module sections:

| Module | Responsibility |
|---|---|
| File Loader | Scans served folder for `.csv`/`.xlsx`; populates dropdown; handles "File Upload..." |
| CSV Parser | Parses raw CSV text → `{ headers, data }` |
| XLSX Parser | Uses SheetJS CDN; auto-loads first sheet; modal for multi-sheet files → `{ headers, data }` |
| Data Normalizer | Mandatory gate between parsers and DataTables; enforces the data contract |
| DataTable Initializer | Consumes only normalized data; configures DataTables instance |
| Theme Manager | OS `prefers-color-scheme` detection; manual toggle; `localStorage` persistence |
| Grouping Manager | Builds dynamic grouping from column headers at runtime |
| Export Manager | Exports filtered rows only; prompts via native `prompt()` |

**Data contract** — all parsers must output exactly:
```js
{ headers: string[], data: string[][] }
```
DataTables must **only** receive output from `normalizeData()`, never raw parser output.

Each module section must use this comment header format:
```js
// ============================================================
// MODULE: <Name>
// Responsibility: <description>
// ============================================================
```

## Key Constraints

- **Single file rule**: all logic stays in `datatables.html`
- **No inline styles**: theming applied exclusively via `body.dark-mode` CSS class
- **No hardcoded column indices**: grouping and all column references must be dynamic
- **QR/Barcode**: never auto-rendered on load — only on toggle
- **`deferRender: true`** must always be set on the DataTables instance
- **No virtual scrolling** — classic pagination only (10/25/50/100/250)
- ES6+; use `const`/`let`, never `var`; keep jQuery only where DataTables API requires it

## Versioning

**Agents must never modify the version string.** Version format: `YYMM + MajorRevision (letter) + MinorRevision (number)` (e.g. `2602A0`). The programmer owns all version increments.

## CDN Dependencies (all loaded via CDN, no local install)

- Bootstrap 5.3.3
- jQuery 3.7.1
- DataTables 2.3.4 (+ Bootstrap5 integration, Buttons, RowGroup, Responsive, Select)
- SheetJS (for XLSX parsing)
- JsBarcode 3.11.5
- QRCode.js

## File Inventory

- `datatables.html` — the target application (being built per `PROJECT_CHECKLIST.md`)
- `index.html` / `CSV_Viewer.html` — legacy CSV-only viewers (reference/migration source)
- `PROJECT_CHECKLIST.md` — phased implementation checklist (Phases 1–11)
- `AGENTS.md` — full agent/contributor rules (authoritative source for constraints)
- `*.csv` — sample data files used for testing
