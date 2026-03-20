```
 ██████╗  █████╗ ████████╗ █████╗ ████████╗ █████╗ ██████╗ ██╗     ███████╗███████╗
 ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔════╝██╔════╝
 ██║  ██║███████║   ██║   ███████║   ██║   ███████║██████╔╝██║     █████╗  ███████╗
 ██║  ██║██╔══██║   ██║   ██╔══██║   ██║   ██╔══██║██╔══██╗██║     ██╔══╝  ╚════██║
 ██████╔╝██║  ██║   ██║   ██║  ██║   ██║   ██║  ██║██████╔╝███████╗███████╗███████║
 ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚══════╝
                        V I E W E R   ·   v260320A
```

> **100% static · single-file · offline · no backend · no build**

---

```
╔══════════════════════════════════════════╗
║  [1]  OVERVIEW                           ║
╚══════════════════════════════════════════╝
```

`index.html` is a server-less, offline data inspection tool.
Drop it in any folder with CSV or XLSX files and open it in a browser.

**Feature set:**

| # | Feature |
|---|---|
| 1 | CSV & XLSX loading (SheetJS) |
| 2 | Multi-sheet XLSX — auto-loads first; modal for selection |
| 3 | Light / Dark mode — OS auto-detect + manual toggle |
| 4 | Dynamic row grouping by any column |
| 5 | Per-column search header row |
| 6 | Multi-row selection |
| 7 | QR code rendering (on toggle) |
| 8 | Barcode rendering (on toggle) |
| 9 | Export filtered dataset to CSV |
| 10 | Classic pagination — 10 / 25 / 50 / 100 / 250 |
| 11 | Column visibility toggle |
| 12 | Optimised for datasets up to 10,000 rows |

---

```
╔══════════════════════════════════════════╗
║  [2]  PROJECT STRUCTURE                  ║
╚══════════════════════════════════════════╝
```

```
/
├── index.html            ← entire application (single file)
├── README.md
├── AGENTS.md             ← agent & contributor rules
├── PROJECT_CHECKLIST.md  ← phased implementation tracker
├── *.csv                 ← sample data files
└── *.xlsx                ← sample data files
```

---

```
╔══════════════════════════════════════════╗
║  [3]  GETTING STARTED                    ║
╚══════════════════════════════════════════╝
```

```bash
python -m http.server 8000
```

Then open: `http://localhost:8000/index.html`

> **Note:** The folder-scan auto-load feature requires HTTP — it will not work via `file://` directly.

---

```
╔══════════════════════════════════════════╗
║  [4]  FILE LOADING                       ║
╚══════════════════════════════════════════╝
```

### On Page Load

The app scans the folder where `index.html` resides for all `.csv` and `.xlsx` files.
Files are listed alphabetically in the dropdown. The first file is auto-loaded on startup.

### File Dropdown

```
sample.csv
sample.xlsx
──────────────
File Upload...
```

**"File Upload..."** is always present at the bottom. Selecting it opens a native OS file picker
filtered to `.csv` and `.xlsx`. The uploaded file is treated identically to a folder file.

### XLSX Multi-Sheet

- Auto-loads the first sheet
- If multiple sheets exist, a modal allows selecting a different sheet
- Only raw cell values imported — no formulas, no formatting

---

```
╔══════════════════════════════════════════╗
║  [5]  TOOLBAR BUTTONS                    ║
╚══════════════════════════════════════════╝
```

Buttons appear in the `col-8 text-end` toolbar area, rendered left-to-right:

| Order | Button | Action |
|---|---|---|
| 1 | **QR** | Toggle QR code column (lazy render) |
| 2 | **Bar** | Toggle barcode column (lazy render) |
| 3 | **Show Selected** | Filter table to selected rows only |
| 4 | **Column Visibility** | Toggle individual column visibility |
| 5 | **Export CSV** | Export filtered rows to CSV |

> QR and Barcode are **never** auto-rendered on load — only on user toggle.

---

```
╔══════════════════════════════════════════╗
║  [6]  DATATABLES CONFIGURATION           ║
╚══════════════════════════════════════════╝
```

| Setting | Value |
|---|---|
| `deferRender` | `true` |
| Pagination lengths | 10, 25, 50, 100, 250 |
| Pagination position | Left-aligned |
| Row count info | Right-aligned |
| Responsive | Enabled |
| Row selection | Multi-row |
| Row grouping | Dynamic (any column) |
| Column visibility | colVis button |
| Per-column search | Enabled (second header row) |
| Button class | `btn btn-sm` (no `btn-secondary`) |

---

```
╔══════════════════════════════════════════╗
║  [7]  DARK MODE                          ║
╚══════════════════════════════════════════╝
```

| Behavior | Detail |
|---|---|
| Auto-detect | Reads OS `prefers-color-scheme` on first load |
| Manual toggle | User can override at any time |
| Persistence | Manual override stored in `localStorage` |
| Implementation | `body.dark-mode` CSS class only — no inline styles |
| Pagination | Bootstrap `.page-link` fully dark-themed |

---

```
╔══════════════════════════════════════════╗
║  [8]  DATA FLOW                          ║
╚══════════════════════════════════════════╝
```

```
User selects file
       │
       ▼
Detect extension (.csv / .xlsx)
       │
       ▼
CSV Parser ──or── XLSX Parser
       │
       ▼
normalizeData()  →  { headers: string[], data: string[][] }
       │
       ▼
DataTable Initializer
       │
       ▼
Extensions: GroupingManager · ThemeManager · ExportManager · QR/Barcode
```

---

```
╔══════════════════════════════════════════╗
║  [9]  EXPORT                             ║
╚══════════════════════════════════════════╝
```

- Exports **filtered rows only** — respects global search, column search, column visibility
- Search header row is **never** included
- User prompted via native `prompt()` to confirm or edit the filename
- Default filename pre-filled from the loaded file

---

```
╔══════════════════════════════════════════╗
║  [10] CDN DEPENDENCIES                   ║
╚══════════════════════════════════════════╝
```

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

All loaded via CDN. No local install required.

---

```
╔══════════════════════════════════════════╗
║  [11] VERSIONING SCHEME                  ║
╚══════════════════════════════════════════╝
```

```
YYMM + MajorRevision (letter) + MinorRevision (number)
```

| Part | Meaning |
|---|---|
| `YYMM` | Year + month of build |
| `A–Z` | Major revision — A = 1st, B = 2nd … |
| `0–9` | Minor revision — starts at 0 |

**Example:** `260320A` = March 2026, 20th day, 1st major revision

> **Agents must never modify the version string.**
> All version changes are the sole responsibility of the programmer.

---

```
╔══════════════════════════════════════════╗
║  [12] BROWSER SUPPORT                    ║
╚══════════════════════════════════════════╝
```

| Browser | Status |
|---|---|
| Chrome | ✅ |
| Edge | ✅ |
| Firefox | ✅ |

Works via static HTTP server. No backend required.

---

```
╔══════════════════════════════════════════╗
║  [13] LICENSE                            ║
╚══════════════════════════════════════════╝
```

MIT — planned upon public release.
Currently an internal-use tool.
