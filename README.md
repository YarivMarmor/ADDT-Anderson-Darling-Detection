# ADDT — Anderson-Darling Detection Tool (Python, v0.2 research preview)

Desktop migration of the provided `ADD Tool.xlsm` VBA code, including `AndersonDarlingForm.frm`, for Windows. **Not statistically validated and not yet tested as an EXE on Windows.**

## Run from Python

```bash
python -m pip install -r requirements.txt
python app.py
```

Open a `.txt` file with one numeric observation per line. Select Normal, Uniform or Exponential. Parameters are prefilled according to the original form (sample standard deviation using `n-1`, uniform bounds `mean +/- sqrt(3)*SD`). Click Run analysis, inspect the curves, export CSV or graph.

## Scientific status and fidelity

- **Legacy VBA score equations deliberately preserved**, including the nonstandard right-hand Normal formula and treatment of tail CDF values (0/1), *not* silently replaced by standard Anderson-Darling.
- Empty right-hand sample on the last checkpoint retains original legacy score of `0`, but excluded from peak detection by default.
- `Minimum observations on each side` defaults to 20 for interpreting the maximum difference; plotted raw series and CSV still include all checkpoints.
- Input parsing skips blank lines; the original form has a possible empty-line array indexing issue. This intentional robustness improvement is recorded here.
- Original Excel/VBA `BubbleSort` uses a `String` swap variable; numerical precision/Excel-specific conversion effects may prevent bit-for-bit output matching. Python uses stable numerical sorting.
- No inferential p-values are claimed. Peak is descriptive, not a calibrated change-point significance test.
- Only the **legacy formula mode** is included. A scientifically validated corrected AD mode requires a separate methodological review.
- Large datasets will be slow due to per-checkpoint sorting and summation. Prioritize validation over speed.

## Validation

```bash
python -m unittest discover -s tests -v
```

Two provided sample TXT files included under `examples/`. The 299 archived spreadsheet checkpoint rows are saved as `examples/excel_checkpoints.csv`. These are *reference-only* until their provenance (dataset, distribution, selected parameters and workbook state) is confirmed; don't report a PASS without that match.

## Windows EXE / GitHub

`build_exe.bat` builds a Windows `dist/ADDT_Research_Preview.exe` with PyInstaller. `.github/workflows/windows.yml` can build an EXE from the browser via Actions > Windows EXE > Run workflow, after uploading the repository. The EXE must be smoke-tested on Windows before publication.
