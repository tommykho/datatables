# Generic Datatables Viewer
Build: 2602A0 — Format: `YYMM` + `MajorRevision (letter)` + `MinorRevision (number)`

---

## Overview

This project upgrades the legacy `CSV_Viewer.html` into a more capable and extensible:

> `datatables.html`  
> A server-less, offline data inspection tool.

It supports:

- CSV loading
- XLSX loading (SheetJS)
- Sheet selection (auto-load first sheet + modal for multi-sheet files)
- Light / Dark mode (OS auto-detect + manual override)
- Dynamic grouping by any column
- Per-column search
- Row selection
- QR / Barcode rendering (on toggle only)
- Export filtered dataset to CSV
- Classic pagination (10 / 25 / 50 / 100 / 250)
- Optimized for datasets up to 10,000 rows

This is a **100% static project** — no backend required.

---

## Project Structure

```
/datatables.html   ← entire app lives here (single file)
/README.md
/AGENTS.md
/sample.csv
/sample.xlsx
```

---

## File Loading Behavior

### On Page Load

The app scans the folder where `datatables.html` resides for all `.csv` and `.xlsx` files. The files are listed in the dropdown, sorted alphabetically. The first file in the sorted list is auto-loaded on startup.

If no CSV or XLSX files are found in the folder, the app loads nothing until the user makes a selection.

### File Dropdown

The dropdown is dynamically populated at runtime from actual files in the folder. Example (will reflect real filenames):

```
sample.csv
sample.xlsx
──────────────
File Upload...
```

The **"File Upload..."** option is always present at the bottom of the list. Selecting it opens a native OS file picker filtered to `.csv` and `.xlsx`. The uploaded file is treated the same as a folder file.

---

## XLSX Behavior

- Uses **SheetJS** (loaded via CDN)
- Automatically loads the first sheet on file open
- If the file contains multiple sheets, a modal allows the user to select a different sheet
- Only raw cell values are imported — no formulas, no formatting

---

## DataTables Configuration

| Setting | Value |
|---|---|
| `deferRender` | `true` |
| Pagination lengths | 10, 25, 50, 100, 250 |
| Responsive | Enabled |
| Row selection | Multi-row |
| Row grouping | Dynamic (any column) |
| Column visibility | colVis button |
| Per-column search | Enabled (search header row) |
| QR / Barcode | On toggle only — never auto-rendered |

---

## Export Behavior

Export to CSV:

- Exports **only filtered rows** — respects global search, column search, and column visibility
- The search header row is **never** included in the export
- User is prompted via native browser `prompt()` to confirm or edit the filename
- Default filename is pre-filled with the original loaded filename

---

## Dark Mode System

| Behavior | Detail |
|---|---|
| Auto-detect | Reads OS theme on first load via `prefers-color-scheme` |
| Manual toggle | User can override at any time |
| Persistence | Manual override stored in `localStorage` |
| Implementation | Applied via `body.dark-mode` CSS class only — no inline styles |

---

## Dynamic Grouping

Grouping is generated at runtime from the actual column headers of the loaded file. There are no hardcoded column buttons.

Example dropdown (column names reflect the loaded file):

```
Group By:
  None
  Order Number
  Product Type
  Status
  ...
```

Grouping updates `rowGroup().dataSrc()` dynamically when the user changes the selection.

---

## Performance Profile

Optimized for:

- Up to **10,000 rows**
- `deferRender: true` for deferred DOM rendering
- Lazy QR / Barcode rendering (on toggle only)
- No unnecessary DOM redraws

Virtual scrolling and Web Workers are intentionally not implemented to maintain simplicity and offline compatibility.

---

## Data Flow

```
User selects file
       ↓
Detect file extension (.csv / .xlsx)
       ↓
Parse file → CSV Parser or XLSX Parser
       ↓
Normalize to: { headers: string[], data: string[][] }
       ↓
DataTable Initializer consumes normalized data
       ↓
Extensions applied (grouping, theme, export, QR/barcode)
```

---

## Browser Compatibility

| Browser | Support |
|---|---|
| Chrome | ✅ |
| Edge | ✅ |
| Firefox | ✅ |

Works via local file open or simple static hosting. No server required.

---

## Versioning Scheme

### Format

```
YYMM + MajorRevision (letter) + MinorRevision (number)
```

### Key

| Part | Meaning |
|---|---|
| `YYMM` | Year and month of the build |
| `A–Z` (letter) | Major revision — A = 1st, B = 2nd, C = 3rd ... |
| `0–9` (number) | Minor revision — starts at 0 |

### Example

```
2512G1
```

= December 2025 / 7th major revision / 1st minor revision

### Rules

- **Programmers control all version changes** — agents must never modify the version string
- Major revision is incremented by the programmer for significant changes
- Minor revision is incremented by the programmer for small fixes or adjustments

---

## Progress


---

## License

MIT (planned upon public release)

Currently an internal-use tool.
