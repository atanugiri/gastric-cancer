# Gastric Cancer Gene Expression Analysis

This repository contains a reproducible pipeline for analyzing the expression of the **CD36** gene in gastric cancer patients, using TCGA gene expression and clinical datasets. Additional exploratory analyses include overlaps with hypercholesterolemia- and obesity-associated gene sets.

---

## Project Structure
.
├── data/ # Raw data files (expression, clinical, subtype)
│ └── expression profile(8863 genes).csv
│ └── tcga_gdc_clinical_data.tsv
│ └── tcga_pan_can_atlas_2018_clinical_data.tsv
├── notebooks/ # Jupyter notebooks for interactive analysis
│ └── 01_Data_Analysis.ipynb
├── python files/ # Custom functions (e.g. merge, plotting)
│ └── merge_expression_and_clinical.py
│ └── plot_grouped_expression.py
│ └── plot_km_with_hr.py
│ └── plot_volcano_with_fdr.py
├── results/ # Output figures and exported tables
│ └── CD36_merged_data.xlsx
│ └── CD36_by_Subtype.pdf
├── README.md # Project overview


---

## Datasets

- **Gene Expression**:  
  [Kaggle: Gene Expression in Gastric Cancer](https://www.kaggle.com/datasets/mahdiehhajian/gene-expression-in-gastric-cancer)  
  → Place the CSV in the `data/` folder.

- **Clinical & Subtype Data**:  
  - `tcga_gdc_clinical_data.tsv` from TCGA GDC  
  - `tcga_pan_can_atlas_2018_clinical_data.tsv` from TCGA Pan-Cancer Atlas  
  → Place both files in the `data/` folder.

---

## Getting Started

### 1. Clone the repo and open the environment:
```bash
git clone https://github.com/atanugiri/gastric-cancer.git
cd gastric-cancer
conda activate gastric
