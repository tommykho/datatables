# Datatables Viewer — Implementation Checklist
Version: **260320A** | Status: **COMPLETE**

---

## Phase 1 — Base Migration ✅
- [x] Create `index.html` with DataTables dependencies from `CSV_Viewer.html`
- [x] Remove hardcoded grouping buttons (C2–C7)
- [x] Column search row, multi-row selection, colVis, QR/Barcode toggle, date conversion
- [x] `deferRender: true`; classic pagination (10 / 25 / 50 / 100 / 250)

## Phase 2 — File Loading ✅
- [x] Dropdown auto-populated from folder scan (alphabetical, `.csv` + `.xlsx`)
- [x] Persistent **"File Upload..."** option at bottom of dropdown
- [x] Auto-load first file on page load; graceful fallback if none found
- [x] Validate file type on upload; friendly error on invalid type

## Phase 3 — Parser Layer ✅
- [x] Modular `parseCSV()` — handles quoted values, uneven columns
- [x] SheetJS XLSX parser — first sheet auto-loaded, raw values only
- [x] Neither parser passes output directly to DataTables

## Phase 3.5 — Data Normalizer ✅
- [x] `normalizeData(raw)` as mandatory gate between all parsers and DataTables
- [x] Enforces `{ headers: string[], data: string[][] }` contract
- [x] Validates, coerces all values to strings, pads/trims rows; error on failure

## Phase 4 — Sheet Selection Modal ✅
- [x] Bootstrap modal listing all sheets; highlights active sheet
- [x] Skipped automatically for single-sheet files

## Phase 5 — Dynamic Grouping ✅
- [x] "Group By" dropdown populated from actual column headers at runtime
- [x] "None" as default; updates `rowGroup().dataSrc()` on change

## Phase 6 — Dark Mode ✅
- [x] OS detection via `prefers-color-scheme`; applied before first render
- [x] Toggle button; `localStorage` persistence; `body.dark-mode` class only — no inline styles
- [x] Full coverage: table, headers, inputs, buttons, modal, Bootstrap pagination

## Phase 7 — Export ✅
- [x] Exports filtered rows only; respects column visibility
- [x] Native `prompt()` pre-filled with original filename; search row excluded

## Phase 8 — Feature Validation ✅
- [x] QR/Barcode: lazy render on toggle only; correct after filter and pagination change
- [x] Multi-row selection: stable across filter and grouping changes
- [x] Per-column search: works independently and combined with global search

## Phase 9 — Performance ✅
- [x] 10,000-row CSV: no freeze during parse/normalize, smooth pagination/grouping/export

## Phase 10 — Regression Testing ✅
- [x] CSV and XLSX load correctly; first sheet auto-loads; multi-sheet modal works
- [x] Dark mode auto-detect and manual override persist on reload
- [x] Export matches filtered data exactly; grouping dynamic on all columns
- [x] No console errors on any operation

## Phase 11 — Finalization ✅
- [x] All module sections have required comment headers
- [x] Dead and legacy code removed; MIT license placeholder in file header
- [x] `README.md` and `AGENTS.md` updated
- [x] Version set to `260320A` (programmer-owned — agents must not modify)
