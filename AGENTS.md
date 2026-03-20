# AGENTS.md

Guidelines for AI agents and contributors working on this codebase.

This project is currently internal but designed to mature into public open-source (MIT).

---

# 1. Core Philosophy

> Lightweight, offline, general-purpose data inspector.

Must remain:

- 100% static
- Server-less
- Single HTML file (`index.html`)
- Modular in structure (even within one file)

---

# 2. Architectural Constraints

## Single File Rule

All logic must reside in:

```
index.html
```

Code must be structured modularly — organized as clearly labeled sections within the single file.
No strict ES6 module enforcement is required, but functions must remain small and focused.
No large monolithic functions.

## Module Sections (Required Labels)

Each section must use this exact comment header format:

```js
// ============================================================
// MODULE: <Name>
// Responsibility: <description>
// ============================================================
```

Defined modules and their responsibilities:

| Module | Responsibility |
|---|---|
| File Loader | Scans folder for CSV/XLSX files; populates dropdown; handles "File Upload..." option |
| CSV Parser | Reads raw CSV text; outputs `{ headers, data }` |
| XLSX Parser | Reads XLSX binary; auto-loads first sheet; modal for multi-sheet; outputs `{ headers, data }` |
| Data Normalizer | Receives parser output; enforces data contract before passing to DataTables |
| DataTable Initializer | Consumes only normalized data; configures and renders DataTables instance |
| Theme Manager | Detects OS preference; handles manual toggle; persists override to `localStorage` |
| Grouping Manager | Builds dynamic grouping controls from column headers; no hardcoded column indices |
| Export Manager | Exports filtered rows; prompts user for filename via native browser `prompt()` |

---

# 3. Data Contract (Strict)

All parsers must output:

```js
{
  headers: string[],
  data: string[][]
}
```

DataTables must **only** consume normalized data from `normalizeData()`.
Never pass raw parser output directly to DataTables.

---

# 4. Theme System Rules

- Detect OS theme on first load via `window.matchMedia('(prefers-color-scheme: dark)')`
- Allow manual toggle
- Manual override stored in `localStorage`
- Apply theme exclusively via `body.dark-mode` CSS class
- JS theming must only use `classList.add('dark-mode')` / `classList.remove('dark-mode')`
- **No inline styling allowed** — all visual theming must be CSS-based
- Dark mode must cover Bootstrap pagination elements (`.page-link`, `.page-item.active`, `.page-item.disabled`)

---

# 5. Performance Requirements

Target max dataset: **10,000 rows**

Must always set:

```js
deferRender: true
```

Must **NOT**:

- Auto-render QR or barcode on load
- Redraw unnecessarily
- Hardcode column indices

---

# 6. Export Rules

Export must:

- Export filtered rows only
- Respect column visibility
- Prompt user to rename via native browser `prompt()`, pre-filled with the original filename
- Never export the search header row

---

# 7. Grouping Rules

- Grouping must be dynamic — generated from actual column headers at runtime
- Hardcoded column references are **prohibited**
- Must allow grouping by any column index

---

# 8. File Handling Rules

## Allowed File Types

- `.csv`
- `.xlsx`

## File Access — Two Methods

### Method 1: Folder Scan (Primary)

On page load, the app scans the folder where `index.html` resides for all `.csv` and `.xlsx` files.
Files listed alphabetically. First file auto-loaded on startup.

### Method 2: File Upload (Secondary)

Dropdown must include a persistent **"File Upload..."** option at the bottom.
Selecting it opens a native OS file picker filtered to `.csv` and `.xlsx`.
Selected file is then loaded identically to a folder file.

## XLSX Behavior

- Auto-load the first sheet on file open
- If the file has multiple sheets, display a modal for sheet selection
- Only raw cell values supported (no formulas, no formatting)

---

# 9. DataTables Configuration Rules

## DOM Layout

```js
dom:
  "<'row mb-2 align-items-center'<'col-4'l><'col-8 text-end'B>>" +
  'rt' +
  "<'row'<'col-sm-6'p><'col-sm-6 text-end'i>>",
```

- `l` (length) — left, col-4
- `B` (buttons) — right, col-8
- `p` (pagination) — left, col-sm-6
- `i` (info) — right, col-sm-6

## Pagination

- Classic pagination only — 10 / 25 / 50 / 100 / 250
- `deferRender: true` always set
- **No virtual scrolling**
- Pagination `<ul>` right-alignment: `justify-content: flex-end` CSS rule

## Buttons

Buttons config must use the `dom.button.className` override to remove `btn-secondary`:

```js
buttons: {
  dom: { button: { className: 'btn btn-sm' } },
  buttons: [...]
}
```

Button order (left to right in toolbar):

| # | Button | Notes |
|---|---|---|
| 1 | QR | Lazy render — never auto on load |
| 2 | Bar | Lazy render — never auto on load |
| 3 | Show Selected | Filters table to selected rows |
| 4 | colvis | Column visibility |
| 5 | Export CSV | Filtered rows only |

---

# 10. Code Style

- ES6+ syntax
- `const` / `let` only — never `var`
- Minimize globals — pass data through function arguments
- Keep functions small and single-purpose
- jQuery only where required by DataTables API
- Named functions preferred over anonymous callbacks

---

# 11. Do Not

- Do not introduce backend dependencies
- Do not remove existing features
- Do not remove QR/Barcode capability
- Do not change versioning format
- Do not replace pagination with virtual scrolling
- Do not add inline styles — use `body.dark-mode` CSS class only
- Do not hardcode column indices
- Do not auto-render QR or barcodes on page load
- Do not implement Roadmap items — those are planning notes only

---

# 12. Versioning Rules

## Format

```
YYMM + MajorRevision (letter) + MinorRevision (number)
```

**Example:** `260320A` = March 2026, 1st major revision

- `A–Z`: Major revision — A = 1st, B = 2nd …
- `0–9`: Minor revision — starts at 0

## Agent Versioning Behavior

- **Agents must never modify the version string**
- All version increments are the sole responsibility of the programmer
- Leave the existing version number untouched on every commit

---

# 13. CDN Dependencies

All loaded via CDN — no local install:

| Library | Version |
|---|---|
| Bootstrap | 5.3.3 |
| jQuery | 3.7.1 |
| DataTables | 2.3.4 |
| DataTables Buttons | 3.2.5 |
| DataTables RowGroup | 1.6.0 |
| DataTables Responsive | 3.0.6 |
| DataTables Select | 3.1.3 |
| SheetJS | CDN latest |
| JsBarcode | 3.11.5 |
| QRCode.js | 1.0.0 |

---

# 14. File Inventory

| File | Purpose |
|---|---|
| `index.html` | Target application — entire app lives here |
| `README.md` | Project documentation |
| `AGENTS.md` | Agent & contributor rules (this file) |
| `CLAUDE.md` | Claude Code project instructions (mirrors AGENTS.md) |
| `PROJECT_CHECKLIST.md` | Phased implementation tracker (Phases 1–11) |
| `*.csv` | Sample data files for testing |
| `*.xlsx` | Sample data files for testing |
