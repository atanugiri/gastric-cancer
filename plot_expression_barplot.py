import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

def plot_expression_barplot(expression_df, clinical_df, gene_name, group_col,
                            palette=None, order=None, save_path=None, figsize=(5, 5),
                            show_pvalue=True, plot_type='bar'):
    """
    Plots gene expression grouped by a clinical variable using bar or box plot.
    
    Parameters:
    - expression_df: DataFrame with genes as rows and samples as columns.
    - clinical_df: DataFrame with clinical information.
    - gene_name: Name of the gene (e.g., 'CD36').
    - group_col: Column name to group by (e.g., 'Overall Survival Status').
    - palette: Dict of group level -> color.
    - order: List of group levels (controls x-axis order).
    - save_path: Base path (no extension) to save .png and .pdf.
    - figsize: Tuple of figure size in inches.
    - show_pvalue: If True, show t-test p-value on plot (only for 2 groups).
    - plot_type: 'bar' (default) or 'box' for plot style.
    """
    expr = expression_df.loc[gene_name]
    plot_df = clinical_df.copy()
    plot_df[f"{gene_name} Expression"] = expr.values

    # Drop missing values
    plot_df = plot_df.dropna(subset=[f"{gene_name} Expression", group_col])

    plt.figure(figsize=figsize)

    if plot_type == 'bar':
        sns.barplot(
            x=group_col,
            y=f"{gene_name} Expression",
            hue=group_col,
            data=plot_df,
            palette=palette,
            errorbar="se",
            dodge=False,
            legend=False,
            order=order
        )
    elif plot_type == 'box':
        sns.boxplot(
            x=group_col,
            y=f"{gene_name} Expression",
            hue=group_col,
            data=plot_df,
            palette=palette,
            order=order,
            dodge=False,
            legend=False
        )
    else:
        raise ValueError("plot_type must be 'bar' or 'box'")

    plt.xlabel(group_col.replace("_", " "))
    plt.ylabel(f"{gene_name} Expression")
    plt.title(f"{gene_name} Expression by {group_col}")

    if order:
        plt.xticks(ticks=range(len(order)), labels=[str(x) for x in order])

    # T-test for 2-group comparison
    if show_pvalue:
        unique_groups = plot_df[group_col].dropna().unique()
        if len(unique_groups) == 2:
            g1, g2 = unique_groups
            expr1 = plot_df[plot_df[group_col] == g1][f"{gene_name} Expression"]
            expr2 = plot_df[plot_df[group_col] == g2][f"{gene_name} Expression"]
            stat, pval = ttest_ind(expr1, expr2, equal_var=False)

            # Annotate plot
            max_height = plot_df[f"{gene_name} Expression"].max()
            y_pos = max_height * 1.1
            x1 = order.index(g1) if order else 0
            x2 = order.index(g2) if order else 1
            plt.plot([x1, x1, x2, x2], [y_pos, y_pos*1.05, y_pos*1.05, y_pos], color="black")
            plt.text((x1 + x2)/2, y_pos*1.08, f"p = {pval:.3e}", ha='center')

    plt.tight_layout()
    if save_path:
        plt.savefig(f"{save_path}.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{save_path}.pdf", bbox_inches="tight")
    plt.show()
