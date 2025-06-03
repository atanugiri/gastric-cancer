import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests

def plot_volcano_with_fdr(expression_df, clinical_df, label_col, group1_label, group2_label,
                          log2fc_threshold=1, fdr_threshold=0.05,
                          use_fdr=True, output_prefix=None,
                          show_labels=True, label_fontsize=8):
    """
    Volcano plot with optional FDR correction.

    Parameters:
    - expression_df: genes x samples DataFrame
    - clinical_df: DataFrame with metadata, must contain label_col and "Sample ID"
    - label_col: column name to define groups
    - group1_label: value representing reference group
    - group2_label: value representing comparison group
    - log2fc_threshold: threshold for absolute log2 fold change
    - fdr_threshold: FDR threshold (or raw p if use_fdr=False)
    - use_fdr: whether to apply Benjamini-Hochberg correction
    - output_prefix: filename prefix for saving figures
    - show_labels: whether to label significant genes
    - label_fontsize: font size for labels

    Returns:
    - volcano_df: DataFrame with statistics and significance flag
    """

    # Identify sample IDs
    group1_ids = clinical_df[clinical_df[label_col] == group1_label]["Sample ID"]
    group2_ids = clinical_df[clinical_df[label_col] == group2_label]["Sample ID"]

    # Compute log2FC and p-values
    log2_fc = []
    pvals = []

    for gene in expression_df.index:
        g1 = expression_df.loc[gene, group1_ids]
        g2 = expression_df.loc[gene, group2_ids]
        fc = g2.mean() - g1.mean()
        log2_fc.append(fc)
        _, p = ttest_ind(g1, g2, equal_var=False, nan_policy='omit')
        pvals.append(p)

    # Build DataFrame
    volcano_df = pd.DataFrame({
        "Gene": expression_df.index,
        "log2FC": log2_fc,
        "pval": pvals
    })
    volcano_df["-log10pval"] = -np.log10(volcano_df["pval"])

    # FDR correction
    if use_fdr:
        volcano_df["FDR"], _, _, _ = multipletests(volcano_df["pval"], method="fdr_bh")
        volcano_df["Significant"] = (volcano_df["FDR"] < fdr_threshold) & (abs(volcano_df["log2FC"]) >= log2fc_threshold)
    else:
        volcano_df["FDR"] = volcano_df["pval"]  # fallback
        volcano_df["Significant"] = (volcano_df["pval"] < fdr_threshold) & (abs(volcano_df["log2FC"]) >= log2fc_threshold)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(volcano_df["log2FC"], volcano_df["-log10pval"],
                s=10, alpha=0.4, label='All genes')
    plt.scatter(volcano_df.loc[volcano_df["Significant"], "log2FC"],
                volcano_df.loc[volcano_df["Significant"], "-log10pval"],
                color='red', s=10, alpha=0.8, label='Significant')

    # Label
    if show_labels:
        for _, row in volcano_df[volcano_df["Significant"]].iterrows():
            plt.text(row["log2FC"], row["-log10pval"], row["Gene"],
                     fontsize=label_fontsize,
                     ha='right' if row["log2FC"] < 0 else 'left')

    # Threshold lines
    plt.axhline(-np.log10(fdr_threshold), linestyle='--', color='gray',
                label=f"{'FDR' if use_fdr else 'p'} = {fdr_threshold}")
    plt.axvline(log2fc_threshold, linestyle='--', color='red')
    plt.axvline(-log2fc_threshold, linestyle='--', color='blue')

    plt.xlabel("log2(Fold Change)")
    plt.ylabel("-log10(p-value)")
    plt.title(f"Volcano Plot: {group2_label} vs {group1_label}")
    plt.legend()
    plt.tight_layout()

    # Save
    if output_prefix:
        plt.savefig(f"{output_prefix}.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{output_prefix}.pdf", bbox_inches="tight")

    plt.show()
    return volcano_df
