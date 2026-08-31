# Retail Promotions Analysis

An end-to-end retail promotion analysis comparing Diwali and Sankranti
campaign performance across stores, products, categories, and promotion types.

The project demonstrates data cleaning, dimensional joins, business-metric
design, and decision-focused analysis using Python, pandas, and Jupyter.

> **Data privacy:** The source datasets are confidential and are intentionally
> excluded from this repository. The notebook retains only aggregate outputs
> needed to demonstrate the analysis.

## Business questions

The analysis covers:

1. Duplicate event detection using the store, campaign, and product business key.
2. Store coverage by city.
3. Median imputation of missing pre-promotion sales quantities.
4. Product-category price positioning.
5. Diwali BOGOF sales volume.
6. Top-performing Diwali store.
7. Incremental sales comparison between Diwali and Sankranti.
8. Sankranti product-level Incremental Revenue Percentage (IR%).
9. Diwali store-level Incremental Sold Units Percentage (ISU%) in Visakhapatnam.
10. Identification of promotion types with negative IR% and ISU%.

## Key findings

| Finding | Result |
|---|---:|
| Duplicate event rows removed | 10 |
| Missing pre-promotion quantities imputed | 20 |
| Median used for imputation | 78 units |
| Cities with more than five stores | 3 |
| Lowest-price product category | Personal Care |
| Diwali BOGOF post-promotion volume | 34,461 units |
| Highest-volume Diwali store | STCHE-4 - 5,013 units |
| Campaign with larger incremental volume | Sankranti - 154,175 units |
| Highest Sankranti product IR% | Atliq Suflower Oil (1L) - 91.83% |
| Lowest Diwali ISU% in Visakhapatnam | STVSK-3 - 49.21% |
| Sankranti promotion with negative IR% and ISU% | 25% OFF - IR: -39.33%, ISU: -19.60% |

## Metric definitions

Revenue is calculated as base price multiplied by quantity sold.

```text
IR% = (revenue after promotion - revenue before promotion)
      / revenue before promotion * 100

ISU% = (units after promotion - units before promotion)
       / units before promotion * 100
```

Metrics are calculated from aggregated totals rather than by averaging
row-level percentages.

## Repository structure

```text
retail-promotions-analysis/
|-- analysis.ipynb       # Executed, step-by-step analysis with aggregate outputs
|-- analysis.py          # Reproducible cleaning and analysis pipeline
|-- datasets/
|   `-- README.md        # Expected schemas; source CSVs are not committed
|-- outputs/
|   `-- .gitkeep         # Generated outputs remain local
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Run locally

1. Clone the repository and create a virtual environment.
2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Add the four authorized source files to `datasets/` using the filenames
   documented in [`datasets/README.md`](datasets/README.md).
4. Run the pipeline:

   ```bash
   python analysis.py
   ```

5. Open the notebook:

   ```bash
   jupyter notebook analysis.ipynb
   ```

Generated files are written to `outputs/` and are ignored by Git to prevent
accidental disclosure.

## Tools

- Python
- pandas
- Jupyter Notebook
- Excel for presentation-ready reporting (kept local because it embeds data)

