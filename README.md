# ADDT — Anderson–Darling Detection Tool

**A standalone Windows application for detecting changes in the distribution of sequential numerical data.**

ADDT is an open-source Python implementation of the Anderson–Darling Detection Tool originally developed in Excel/VBA and presented in the scientific publication by Marmor and Bashkansky.

The application examines a sequence of observations by comparing Anderson–Darling-based scores calculated on both sides of successive candidate change points. It visualizes the scores and identifies the point with the largest valid difference.

**Current version:** v0.2.0 — Research Preview

## Download for Windows

**[Download ADDT.exe — Windows application](https://github.com/YarivMarmor/ADDT-Anderson-Darling-Detection/releases/download/v0.2.0-preview/ADDT.exe)**

The application runs directly on Windows. **No installation of Python, Jupyter, or Microsoft Excel is required.**

To get started:

1. Download `ADDT.exe` using the link above.
2. Save the file to your computer.
3. Double-click the executable to launch the application.
4. Open a TXT data file and select the appropriate distribution.
5. Run the analysis and examine the graphical results.

### Windows security notice

The executable is not digitally signed. Windows may display an *Unknown publisher* or *Windows protected your PC* warning.

If you downloaded the software from this official GitHub repository, verified its origin, and your organization's security policy permits it, you may select **More info → Run anyway**, where available.

Do not disable Windows security protections.

## Main features

- Detection of potential distributional changes in sequential numerical data.
- Support for Normal, Uniform, and Exponential distributions.
- Automatic estimation of distribution parameters, with the option to modify them manually.
- Calculation of **AD Left**, **AD Right**, and **AD difference** at successive candidate change points.
- Identification and graphical marking of the point with the largest valid AD difference.
- Configurable minimum number of observations on each side of a candidate change point.
- Interactive plots with zooming and navigation.
- Export of numerical results to CSV.
- Export of graphs to image files.
- Standalone Windows executable and publicly available Python source code.

## How the method works

For a sequence of numerical observations, ADDT evaluates successive candidate change points.

At each candidate point, the observations are divided into two subsets:

- **Left:** observations before and including the candidate point.
- **Right:** observations after the candidate point.

An Anderson–Darling-based score is calculated for each subset.

The detection measure is defined as:

**AD difference = |AD Left − AD Right|**

A large difference indicates that the two subsets exhibit different values of the selected goodness-of-fit measure and may suggest a change in process behavior.

The application reports the candidate point with the maximum difference among points satisfying the selected minimum sample sizes.

**Important:** The maximum AD difference is a descriptive detection score, not a calibrated statistical p-value.

## Input data

ADDT accepts plain-text (`.txt`) files containing one numerical observation per line.

Blank lines are ignored.

Two example datasets are included in the repository under `examples/`:

**1. Change in measurement precision**

`data_mu=5_sd=.20 from normal. Acuracy change from 3 to 1 points in 400.txt`

A numerical sequence with a change in measurement precision around observation 400.

**2. Distributional change**

`data_mu=100_sd=10 to unif.txt`

A numerical sequence used to examine changes involving a Normal-to-Uniform distribution transition.

These datasets can be used to explore the application's behavior and compare results with the original Excel/VBA implementation.

## Example results

The following results were obtained using the supplied datasets and the application's legacy calculation mode, with a minimum of 20 observations on each side.

| Example | Detected checkpoint | Maximum AD difference |
|---|---:|---:|
| Measurement precision change | 395 | 6.1353 |
| Normal-to-Uniform example | 364 | 2.5913 |

For the precision-change example, the detected point is close to the known change at observation 400.

These results describe the behavior of the implemented algorithm; they do not constitute independent statistical validation.

## Run from Python

Developers and researchers may also run the application from its source code.

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Launch the graphical interface:

```bash
python app.py
```

The Python version and the Windows executable use the same underlying calculation approach.

## Scientific publication

The ADDT approach is described in:

**Marmor, Y. N., & Bashkansky, E. (2018).** Abrupt change of process behavior: The Anderson-Darling detection tool. *Quality Engineering, 30*(2), 283–292.

**DOI:** https://doi.org/10.1080/08982112.2017.1343480

The article was first published online in 2017 and appeared in the journal's 2018 volume.

Researchers using the methodology are encouraged to cite the original article. The repository also includes `CITATION.cff` for software citation.

## Scientific status and limitations

**Research Preview — version 0.2.0**

The current Python implementation deliberately preserves the original Excel/VBA calculation approach, including certain nonstandard formula conventions.

Known methodological and implementation considerations include:

- The original right-hand Normal score formula is not identical to the standard Anderson–Darling formulation.
- Extreme CDF values are treated according to the legacy VBA conventions.
- The original workbook may have Excel-specific rounding and numerical conversion effects that are not reproduced bit-for-bit in Python.
- The final checkpoint has an empty right-hand subset and is excluded from valid peak detection by default.
- Complete independent numerical validation of the Python implementation against the original Excel/VBA tool remains in progress.
- No statistical significance level or inferential p-value is provided for the detected change point.

The current version implements **Legacy VBA mode only**. A revised statistically validated mode may be introduced in a future release following methodological review.

## Testing and validation

The Python implementation has undergone initial functional and numerical checks using the supplied example datasets.

The graphical application has been tested on Windows, including its standalone executable, data loading, visualization, CSV export, and graph export.

Four automated software tests have passed.

To run the automated tests:

```bash
python -m pytest tests -q
```

The repository also contains archived Excel checkpoint data for further comparison. A complete checkpoint-by-checkpoint validation requires confirmation of the original workbook parameters and data provenance.

## Building the Windows executable

The Windows executable is built using PyInstaller and GitHub Actions.

The repository includes a GitHub Actions workflow that runs the automated tests, builds a standalone executable, and attaches `ADDT.exe` to a published GitHub Release.

The latest published versions and downloads are available at:

https://github.com/YarivMarmor/ADDT-Anderson-Darling-Detection/releases

## Feedback and contributions

Researchers and users are welcome to report issues, suggest improvements, and provide feedback.

**GitHub Issues:** https://github.com/YarivMarmor/ADDT-Anderson-Darling-Detection/issues

Particular interest is given to numerical reproducibility, detection performance, edge cases, and comparisons with the original research implementation.

## Author

**Dr. Yariv N. Marmor**

Department of Industrial Engineering and Management  
Braude College of Engineering, Israel

**ORCID:** https://orcid.org/0000-0001-9200-5041

**GitHub:** https://github.com/YarivMarmor

## License

This software is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.
