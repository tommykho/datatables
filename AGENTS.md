# AGENTS.md

Guidelines for AI agents and contributors.

This project is currently internal but designed to mature into public open-source (MIT).

---

# 1. Core Philosophy

This is a:

> Lightweight, offline, general-purpose data inspector.

It must remain:

- 100% static
- Server-less
- Single HTML file
- Modular in structure (even within one file)

---

# 2. Architectural Constraints

## Single File Rule

All logic must reside in:

```
datatables.html
```

Code must be structured modularly — organized as clearly labeled, small-function sections within the single file. No strict ES6 module enforcement is required, but functions must remain small and focused. No large monolithic functions.

## Module Sections (Required Labels)

Each section must be clearly labeled with a comment block. Modules and their responsibilities are:

| Module | Responsibility |
|---|---|
| File Loader | Scans folder for CSV/XLSX files; populates dropdown; handles "File Upload..." option |
| CSV Parser | Reads raw CSV text; outputs normalized `{ headers, data }` |
| XLSX Parser | Reads XLSX binary; auto-loads first sheet; supports modal sheet selection; outputs normalized `{ headers, data }` |
| Data Normalizer | Receives parser output; enforces data contract before passing to DataTables |
| DataTable Initializer | Consumes only normalized data; configures and renders DataTables instance |
| Theme Manager | Detects OS preference; handles manual toggle; persists override to localStorage |
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

DataTables must **only** consume normalized data from the Data Normalizer.

Never pass raw parser output directly to DataTables.

---

# 4. Theme System Rules

- Detect OS theme on first load using `window.matchMedia('(prefers-color-scheme: dark)')`
- Allow manual toggle
- Manual override stored in `localStorage`
- Apply theme exclusively via:

```css
body.dark-mode
```

- JS theming must only use `classList.add('dark-mode')` / `classList.remove('dark-mode')`
- No inline styling allowed
- All visual theming must be CSS-based

---

# 5. Performance Requirements

Target max dataset: **10,000 rows**

Must include:

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
- Prompt user to rename file using **native browser `prompt()`**, pre-filled with the original filename
- Allow the user to edit the filename freely before confirming
- Default filename = original filename (without re-extension logic)
- Never export the search header row

---

# 7. Grouping Rules

- Grouping must be dynamic — generated from actual column headers at runtime
- Hardcoded column references (e.g., C2–C7 buttons) are **prohibited**
- Must allow grouping by any column index

---

# 8. File Handling Rules

## Allowed File Types

- `.csv`
- `.xlsx`

## File Access — Two Methods

### Method 1: Folder Scan (Primary)

On page load, the app scans the folder where `datatables.html` resides for all `.csv` and `.xlsx` files. These are listed in a dropdown selector, sorted alphabetically. The first file in the list is auto-loaded on startup.

> Implementation: Use the File System Access API or equivalent static folder parsing available in the deployment context. Document the chosen method in code comments.

### Method 2: File Upload (Secondary)

The dropdown must include a persistent **"File Upload..."** option at the bottom of the list. Selecting it opens a native OS file picker filtered to `.csv` and `.xlsx`. The selected file is then loaded as if it were a folder file.

## XLSX Behavior

- Auto-load the first sheet on file open
- If the file has multiple sheets, display a modal for sheet selection
- Only raw cell values are supported (no formulas, no formatting)

---

# 9. Code Style Expectations

- ES6+ syntax
- Use `const` / `let`; never `var`
- Minimize global variables — prefer passing data through function arguments
- Keep functions small and single-purpose
- Keep jQuery usage only where required by DataTables API
- Prefer named functions over anonymous callbacks for readability
- Label every module section with a clear comment header, e.g.:

```js
// ============================================================
// MODULE: Theme Manager
// Responsibility: OS detection, manual toggle, localStorage
// ============================================================
```

---

# 10. Do Not

- Do not introduce backend dependencies
- Do not remove existing features
- Do not remove QR/Barcode capability
- Do not change versioning format
- Do not replace pagination with virtual scrolling
- Do not implement any item listed under Section 12 (Roadmap) — those are planning notes only

---

# 11. Versioning Rules

## Format

```
YYMM + MajorRevision (letter) + MinorRevision (number)
```

**Example:** `2512G1` = December 2025, 7th major revision (G), 1st minor revision

Major revision uses letters: A = 1st, B = 2nd, C = 3rd ... G = 7th, and so on.  
Minor revision uses numbers starting from 0.

## Agent Versioning Behavior

- **Agents must never modify the version string**
- All version increments — major and minor — are the sole responsibility of the programmer
- Claude Code should leave the existing version number untouched on every commit

---

# 12. Roadmap (Do Not Implement)

> These are planning notes only. Claude Code must not scaffold, stub, or partially implement any of the following.

- `[ROADMAP]` JSON parser support
- `[ROADMAP]` Plugin-based parser architecture
- `[ROADMAP]` Additional