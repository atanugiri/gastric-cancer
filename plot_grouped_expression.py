import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

def plot_grouped_expression(
    df,
    y_col,
    group_col,
    palette=None,
    order=None,
    save_path=None,
    figsize=(5, 5),
    show_pvalue=True,
    plot_type="box"
):
    """
    Plot grouped bar or box plot for any y-column in merged_df.

    Parameters:
    - df: DataFrame (e.g., merged_df) with y_col and group_col
    - y_col: column for y-axis (e.g., 'CD36 Expression')
    - group_col: column to group by (e.g., 'Race Category')
    - palette: dict mapping group -> color
    - order: list of group levels to control x-axis order
    - save_path: base path to save .png/.pdf (no extension)
    - figsize: (width, height) tuple
    - show_pvalue: show t-test p-value if only 2 groups
    - plot_type: 'box' or 'bar'
    """
    # Drop missing values
    plot_df = df.dropna(subset=[y_col, group_col]).copy()

    plt.figure(figsize=figsize)

    if plot_type == "box":
        sns.boxplot(
            x=group_col,
            y=y_col,
            hue=group_col,
            data=plot_df,
            palette=palette,
            order=order,
            dodge=False,
            legend=False
        )
    elif plot_type == "bar":
        sns.barplot(
            x=group_col,
            y=y_col,
            hue=group_col,
            data=plot_df,
            palette=palette,
            order=order,
            errorbar="se",
            dodge=False,
            legend=False
        )
    else:
        raise ValueError("plot_type must be 'box' or 'bar'")

    plt.xlabel(group_col.replace("_", " "))
    plt.ylabel(y_col.replace("_", " "))
    plt.title(f"{y_col} by {group_col}")

    if order:
        plt.xticks(ticks=range(len(order)), labels=[str(x) for x in order])

    # Optional statistical test
    if show_pvalue:
        unique_groups = plot_df[group_col].dropna().unique()

        if len(unique_groups) == 2:
            # Two groups → t-test
            g1, g2 = unique_groups
            y1 = plot_df[plot_df[group_col] == g1][y_col]
            y2 = plot_df[plot_df[group_col] == g2][y_col]
            stat, pval = ttest_ind(y1, y2, equal_var=False)
            test_label = f"t-test p = {pval:.3e}"
        elif len(unique_groups) > 2:
            # More than 2 groups → one-way ANOVA
            groups = [
                plot_df[plot_df[group_col] == grp][y_col].dropna()
                for grp in (order if order else unique_groups)
            ]
            stat, pval = f_oneway(*groups)
            test_label = f"ANOVA p = {pval:.3e}"
        else:
            test_label = None

        # Annotate plot if test was performed
        if test_label:
            max_y = plot_df[y_col].max()
            y_pos = max_y * 1.1
            plt.text(0.5, y_pos, test_label, ha='center', va='bottom', fontsize=10, transform=plt.gca().transAxes)

    plt.tight_layout()
    if save_path:
        plt.savefig(f"{save_path}.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{save_path}.pdf", bbox_inches="tight")
    plt.show()
