# Gastric Cancer Gene Expression Analysis

This repository contains a reproducible pipeline for analyzing the expression of the **CD36** gene in gastric cancer patients, using TCGA gene expression and clinical datasets. Additional exploratory analyses include overlaps with hypercholesterolemia- and obesity-associated gene sets.

---

## Project Structure
```
.
├── data/                    # Raw data files (expression, clinical, subtype)
│   ├── expression profile(8863 genes).csv
│   ├── tcga_gdc_clinical_data.tsv
│   └── tcga_pan_can_atlas_2018_clinical_data.tsv
├── notebooks/               # Jupyter notebooks for interactive analysis
│   ├── 00_data_analysis.ipynb
│   └── 01_Data_Analysis.ipynb
├── python files/            # Custom functions (e.g. merge, plotting)
│   ├── clean_gene_name.py
│   ├── merge_expression_and_clinical.py
│   ├── plot_grouped_expression.py
│   ├── plot_km_with_hr.py
│   └── plot_volcano_with_fdr.py
├── results/                 # Output figures and exported tables
│   ├── CD36_merged_data.xlsx
│   ├── CD36_Expression_by_*.pdf
│   ├── CD36_KM.pdf
│   └── CD36_volcano_plot_with_fdr.pdf
├── environment.yml          # Conda environment specification
├── schematic_multi_database_integration_workflow.tex  # LaTeX schematic of workflow
└── README.md                # Project overview
```


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

### 1. Clone the repository:
```bash
git clone https://github.com/atanugiri/gastric-cancer.git
cd gastric-cancer
```

### 2. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate gastric
```

### 3. Download the required datasets:
- Download gene expression data from [Kaggle](https://www.kaggle.com/datasets/mahdiehhajian/gene-expression-in-gastric-cancer)
- Place all data files in the `data/` folder

### 4. Run the analysis:
Open and execute the Jupyter notebooks in the `notebooks/` folder:
```bash
jupyter notebook notebooks/01_Data_Analysis.ipynb
```

---

## Publication

If you use this code or data in your research, please cite:

**Int. J. Transl. Med. 2025, 5(3), 26**  
DOI: [https://doi.org/10.3390/ijtm5030026](https://doi.org/10.3390/ijtm5030026)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For questions or collaborations, please contact:
- **Author**: Atanu Giri
- **Email**: atanurkm11@gmail.com
- **GitHub**: https://github.com/atanugiri
