# DSC8307 — Assignment 2

**Name:** Tayebwa Yonah  
**Access number:** B28697

**Data Mining, Modeling and Analytics | Advent 2026 | Uganda Christian University**

Two complete executed Python notebooks, one per project, with embedded reports, figures, methodological justification, evaluation, limitations and references.

| File | Purpose |
|---|---|
| `01_wholesale_customers.ipynb` | Customer EDA, preparation, cluster tendency, K-means/Ward/DBSCAN comparisons, stability, segment profiles and service recommendations |
| `02_credit_card_fraud.ipynb` | Transaction EDA, statistical baseline, label-withheld cluster and one-class anomaly ranking, AP, queue-budget metrics, sensitivity and uncertainty |
| `requirements.txt` | Pinned direct dependencies verified with Python 3.12 |
| `download_data.py` | Downloads matching public benchmark copies and verifies their checksums |
| `run_notebooks.py` | Executes both notebooks in fresh kernels and generates HTML reports |
| `reports/` | Executed reports containing aggregate outputs and figures |
| `data/*-README.txt` | Original supplied dataset descriptions |

Raw datasets and individual customer/transaction exports are excluded from this public repository. Notebook execution downloads public copies; the verified downloaded numerical records match the supplied assignment data. Individual assignments and rankings are generated locally under ignored `results/`.

## Reproduce

Use **Python 3.12**. From the repository root:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run_notebooks.py
```

Windows activation: `.venv\Scripts\activate`.

The first execution needs internet access to download approximately 151 MB of public benchmark data. Later runs use the verified local cache and can run offline. Both notebooks can also be run from top to bottom in VS Code or Jupyter with the installed environment selected. They automatically call the data helper when needed; no manual data download is required. Allow several minutes depending on download speed and hardware. Full original macOS environment pins are recorded in `requirements-lock-macos.txt`; use the direct `requirements.txt` for cross-platform installation.

The data helper fails if a source changes or no longer matches the assignment. Alternatively, place the original `wholesale-customers.csv` and `creditcard.csv` (or `creditcard.csv.gz`) in `data/`; they are verified and remain excluded from Git.

## Findings and evaluation design

Wholesale spending is log-transformed and standardized. Channel and Region are external descriptors, not clustering inputs. The selected K-means partition has 188 grocery/detergents-oriented customers and 252 fresh/frozen-oriented customers (silhouette 0.290). Stability and alternative preprocessing show why these are broad planning profiles rather than definitive customer types. DBSCAN noise and coverage are explicitly reported.

Fraud labels are excluded from fitting, preprocessing and primary parameter selection. A chronological training/validation/test design compares robust-z, cluster-distance and one-class SVM scores. The classifier is a **one-class classifier**, not a supervised fraud classifier. At a 284-transaction test queue, clustering captures 26 of 74 frauds with 258 legitimate alerts; the SVM captures 13 and the robust-z ranking captures one. AP uncertainty and temporal variation limit claims of superiority. Sensitivity settings are reported on validation without replacing the prespecified test comparison. Anomaly scores are not fraud probabilities.

## Data provenance and attribution

- **Wholesale:** Cardoso, M. (2013), [Wholesale customers](https://archive.ics.uci.edu/dataset/292/wholesale+customers), UCI Machine Learning Repository, [DOI 10.24432/C5030X](https://doi.org/10.24432/C5030X), CC BY 4.0. The download helper normalizes the public `Delicassen` header to `Delicatessen` and verifies normalized CSV values and row order against the supplied data.
- **Credit cards:** Worldline/ULB Credit Card Fraud Detection benchmark, September 2013. The public CSV URL is documented by the [TensorFlow imbalanced-data tutorial](https://www.tensorflow.org/tutorials/structured_data/imbalanced_data). The helper verifies its SHA256 against the assignment file. This project uses its own scikit-learn anomaly analysis; it does not use the TensorFlow tutorial's supervised model or require TensorFlow.
- Original descriptions supplied with the assignment are retained in `data/`. Additional method references are in each notebook. Data ownership is not claimed by this repository.

## Submission

Submit **https://github.com/tayebwa12/dsc8307-assignment-2** to Moodle as required by the brief. The repository contains the complete notebooks and dependency file. Moodle submission is separate from GitHub publication.

**AI-assistance disclosure:** Analysis and code were prepared with AI assistance. The submitting student should review and understand the work and comply with institutional academic-integrity and disclosure rules.
