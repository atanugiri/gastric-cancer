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
    xtick_rotation=None
):
    """
    Plot grouped bar or box plot and return the figure and axis.

    Returns:
    - fig: matplotlib Figure object
    - ax: matplotlib Axes object
    """
    # Drop missing values
    plot_df = df.dropna(subset=[y_col, group_col]).copy()

    # Create fig and ax explicitly
    fig, ax = plt.subplots(figsize=figsize)

    # Turn off horizontal gridlines
    sns.set(style="whitegrid")
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
            legend=False,
            ax=ax
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
            legend=False,
            ax=ax
        )
    else:
        raise ValueError("plot_type must be 'box' or 'bar'")

    # Label formatting
    ax.set_xlabel(group_col.replace("_", " "))
    ax.set_ylabel(y_col.replace("_", " "))
    ax.set_title(f"{y_col} by {group_col}")

    # Optional xtick relabeling
    if order:
        ax.set_xticks(range(len(order)))
        ax.set_xticklabels([str(x) for x in order])

    if xtick_rotation is not None:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=xtick_rotation,
                           ha='right' if xtick_rotation > 45 else 'center')

    fig.tight_layout()

    if save_path:
        fig.savefig(f"{save_path}.png", dpi=300, bbox_inches="tight")
        fig.savefig(f"{save_path}.pdf", bbox_inches="tight")

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

    return fig, ax
