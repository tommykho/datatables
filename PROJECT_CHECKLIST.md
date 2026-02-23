# 📋 Datatables Viewer Upgrade Checklist
Version Target: **2602A0**

------------------------------------------------------------------------

# 🧱 Phase 1 — Base Migration (CSV → Datatables)

## Core Structure

-   [ ] Create `datatables.html`
-   [ ] Copy working DataTables dependencies from `CSV_Viewer.html`
-   [ ] Remove legacy hardcoded grouping buttons (C2–C7)
-   [ ] Preserve:
    -   [ ] Column search row
    -   [ ] Row selection (multi)
    -   [ ] Column visibility (colVis)
    -   [ ] QR toggle
    -   [ ] Barcode toggle
    -   [ ] Excel serial date conversion
-   [ ] Enable `deferRender: true`
-   [ ] Keep classic pagination (10 / 25 / 50 / 100 / 250)

------------------------------------------------------------------------

# 📂 Phase 2 — File Loading System

## Dropdown Loader

-   [ ] Create dropdown UI
-   [ ] Populate dropdown dynamically from folder scan results (sorted alphabetically)
-   [ ] Any `.csv` or `.xlsx` file in the folder must appear automatically (no hardcoded filenames)
-   [ ] Add a divider below the file list
-   [ ] Add persistent **"File Upload..."** option at the bottom of the dropdown

## Auto-Load Logic

-   [ ] Auto-load first alphabetically sorted `.csv` file on page load
-   [ ] If no `.csv` found, auto-load first `.xlsx` file
-   [ ] Graceful fallback if no files found — load nothing, show neutral state

## File Upload

-   [ ] Accept `.csv`
-   [ ] Accept `.xlsx`
-   [ ] Validate file type on selection
-   [ ] Display friendly error message on invalid file type

------------------------------------------------------------------------

# 📄 Phase 3 — Parser Layer

## CSV Parser

-   [ ] Refactor `parseCSV()` into a modular, small-scope function
-   [ ] Handle quoted values
-   [ ] Handle missing or uneven columns safely
-   [ ] Output raw result only — do NOT pass directly to DataTables

## XLSX Parser (SheetJS)

-   [ ] Add SheetJS via CDN
-   [ ] Parse workbook on file load
-   [ ] Auto-load first sheet
-   [ ] Extract all sheet names for modal use
-   [ ] Ignore cell formatting (raw values only)
-   [ ] Output raw result only — do NOT pass directly to DataTables

------------------------------------------------------------------------

# 🔒 Phase 3.5 — Data Normalizer (Safeguard Layer)

> This is a mandatory gate between parsers and DataTables. No parser output may reach DataTables without passing through this layer.

-   [ ] Build a dedicated `normalizeData(raw)` function
-   [ ] Enforce strict output contract:

    ```js
    {
      headers: string[],
      data: string[][]
    }
    ```

-   [ ] Validate that `headers` is a non-empty array of strings
-   [ ] Validate that `data` is an array of arrays
-   [ ] Coerce all cell values to strings (no nulls, no undefined)
-   [ ] Pad short rows to match header length
-   [ ] Trim excess columns in rows that exceed header length
-   [ ] Throw a descriptive error (or display user-facing message) if normalization fails
-   [ ] Confirm: DataTable Initializer receives **only** the output of `normalizeData()`

------------------------------------------------------------------------

# 📑 Phase 4 — Sheet Selection Modal

-   [ ] Create Bootstrap modal for sheet selection
-   [ ] Populate modal with all sheet names from the workbook
-   [ ] Highlight the currently active sheet
-   [ ] Load selected sheet through the normalizer into DataTable
-   [ ] Skip modal entirely if the file has only one sheet

------------------------------------------------------------------------

# 📊 Phase 5 — Dynamic Grouping

-   [ ] Remove any remaining hardcoded grouping buttons
-   [ ] Create "Group By" dropdown populated from actual column headers at runtime
-   [ ] Include "None" as the default first option
-   [ ] Update `rowGroup().dataSrc()` dynamically on selection change
-   [ ] Maintain sort consistency when grouping changes

------------------------------------------------------------------------

# 🌙 Phase 6 — Dark Mode System

## Detection

-   [ ] Detect OS theme on first load via `window.matchMedia('(prefers-color-scheme: dark)')`
-   [ ] Apply correct theme class on load before first render

## Manual Override

-   [ ] Add theme toggle button
-   [ ] Apply toggle via `classList.add('dark-mode')` / `classList.remove('dark-mode')` only
-   [ ] Store override in `localStorage`
-   [ ] Ensure override persists across page reloads

## Styling

-   [ ] Define all dark mode styles under `body.dark-mode` CSS only — no inline styles
-   [ ] Style:
    -   [ ] Page background
    -   [ ] Table headers
    -   [ ] Hover rows
    -   [ ] Per-column search inputs
    -   [ ] Buttons
    -   [ ] Modal
-   [ ] Confirm DataTables integrates visually in both themes

------------------------------------------------------------------------

# 📤 Phase 7 — Export System

-   [ ] Add DataTables CSV export button
-   [ ] Configure export to:
    -   [ ] Export filtered rows only (respects global search + column search)
    -   [ ] Respect column visibility
-   [ ] Prompt user via **native browser `prompt()`**, pre-filled with the original filename
-   [ ] Allow user to freely edit filename before confirming
-   [ ] Verify the hidden search header row is **not** included in the export

------------------------------------------------------------------------

# 🔍 Phase 8 — Feature Validation

## QR / Barcode

-   [ ] Confirm QR/Barcode is not rendered on page load
-   [ ] Confirm rendering occurs only when toggled
-   [ ] Works correctly after filtering
-   [ ] Works correctly after pagination change

## Selection

-   [ ] Multi-row select works
-   [ ] Filtering does not break selection state
-   [ ] Grouping does not break selection state

## Column Search

-   [ ] Per-column search works independently
-   [ ] Per-column search works in combination with global search

------------------------------------------------------------------------

# ⚡ Phase 9 — Performance Validation (10k rows)

-   [ ] Load a 10,000-row CSV test file
-   [ ] No UI freeze during parse or normalization
-   [ ] Pagination is smooth
-   [ ] Grouping is smooth
-   [ ] Export completes successfully on full filtered dataset

------------------------------------------------------------------------

# 🧪 Phase 10 — Regression Testing

-   [ ] CSV loads correctly
-   [ ] XLSX loads correctly
-   [ ] First sheet auto-loads on XLSX open
-   [ ] Sheet selection modal works for multi-sheet files
-   [ ] Dark mode auto-detect works on first load
-   [ ] Manual theme override persists on reload
-   [ ] Export matches filtered data exactly
-   [ ] Grouping works dynamically on all columns
-   [ ] No console errors on any operation

------------------------------------------------------------------------

# 📦 Phase 11 — Finalization

-   [ ] Verify all module sections have required comment headers (see AGENTS.md Section 9)
-   [ ] Clean unused or dead code
-   [ ] Remove all commented legacy code
-   [ ] Add MIT license placeholder comment in file header
-   [ ] Update `README.md`
-   [ ] Update `AGENTS.md` if behavior has changed
-   [ ] **Programmer updates version string to `2602A0` before final commit**
-   [ ] Agents must not modify the version string — programmer owns this step
