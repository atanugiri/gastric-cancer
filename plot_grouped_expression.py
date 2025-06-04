import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, f_oneway

def plot_grouped_expression(
    df,
    y_col,
    group_col,
    palette=None,
    order=None,
    save_path=None,
    figsize=(5, 5),
    show_pvalue=True,
    plot_type="box",
    xtick_rotation=None  # New argument
):
    """
    Plot grouped bar or box plot for any y-column in merged_df.

    Parameters:
    - df: DataFrame with y_col and group_col
    - y_col: column for y-axis (e.g., 'CD36 Expression')
    - group_col: column to group by (e.g., 'Biopsy Site')
    - palette: dict mapping group -> color
    - order: list of group levels to control x-axis order
    - save_path: base path to save .png/.pdf (no extension)
    - figsize: (width, height) tuple
    - show_pvalue: print t-test/ANOVA p-value in terminal
    - plot_type: 'box' or 'bar'
    - xtick_rotation: optional int/float to rotate x-axis labels (e.g., 90)
    """
    # Drop missing values
    plot_df = df.dropna(subset=[y_col, group_col]).copy()

    # Create figure
    plt.figure(figsize=figsize)

    # Turn off horizontal gridlines
    sns.set(style="whitegrid")
    ax = plt.gca()
    ax.yaxis.grid(False)

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

    # Label formatting
    plt.xlabel(group_col.replace("_", " "))
    plt.ylabel(y_col.replace("_", " "))
    plt.title(f"{y_col} by {group_col}")

    if order:
        plt.xticks(ticks=range(len(order)), labels=[str(x) for x in order])

    # Optional x-tick rotation
    if xtick_rotation is not None:
        plt.xticks(rotation=xtick_rotation, ha='right' if xtick_rotation > 45 else 'center')

    plt.tight_layout()
    if save_path:
        plt.savefig(f"{save_path}.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{save_path}.pdf", bbox_inches="tight")
    plt.show()

    # Print statistical test result instead of annotating
    if show_pvalue:
        unique_groups = plot_df[group_col].dropna().unique()

        if len(unique_groups) == 2:
            g1, g2 = unique_groups
            y1 = plot_df[plot_df[group_col] == g1][y_col]
            y2 = plot_df[plot_df[group_col] == g2][y_col]
            stat, pval = ttest_ind(y1, y2, equal_var=False)
            print(f"t-test: t = {stat:.3f}, p = {pval:.3e}")
        elif len(unique_groups) > 2:
            groups = [
                plot_df[plot_df[group_col] == grp][y_col].dropna()
                for grp in (order if order else unique_groups)
            ]
            stat, pval = f_oneway(*groups)
            print(f"ANOVA: F = {stat:.3f}, p = {pval:.3e}")
