import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, f_oneway

def plot_grouped_expression(
    df,
    y_col,
    group_col,
    palette=None,
    order=None,
    figsize=(5, 5),
    show_pvalue=True,
    plot_type="box"
):
    """
    Plot grouped bar or box plot for any y-column in df, grouped by group_col.

    Parameters:
    - df: DataFrame with data
    - y_col: column name for y-axis values
    - group_col: column name to group by on the x-axis
    - palette: optional color mapping
    - order: list of group values to control x-axis order
    - figsize: tuple for figure size
    - show_pvalue: whether to print t-test or ANOVA result
    - plot_type: 'box' or 'bar'

    Returns:
    - fig: matplotlib Figure object
    - ax: matplotlib Axes object
    """
    plot_df = df.dropna(subset=[y_col, group_col]).copy()

    fig, ax = plt.subplots(figsize=figsize)
    sns.set(style="whitegrid")
    ax.yaxis.grid(False)

    if plot_type == "box":
        sns.boxplot(
            x=group_col, y=y_col, hue=group_col, data=plot_df,
            palette=palette, order=order, dodge=False, legend=False, ax=ax
        )
    elif plot_type == "bar":
        sns.barplot(
            x=group_col, y=y_col, hue=group_col, data=plot_df,
            palette=palette, order=order, errorbar="se", dodge=False,
            legend=False, ax=ax
        )
    else:
        raise ValueError("plot_type must be 'box' or 'bar'")

    ax.set_xlabel(group_col.replace("_", " "))
    ax.set_ylabel(y_col.replace("_", " "))
    ax.set_title(f"{y_col} by {group_col}")

    if order:
        ax.set_xticks(range(len(order)))
        ax.set_xticklabels([str(x) for x in order])

    if show_pvalue:
        unique_groups = plot_df[group_col].dropna().unique()
        if len(unique_groups) == 2:
            y1 = plot_df[plot_df[group_col] == unique_groups[0]][y_col]
            y2 = plot_df[plot_df[group_col] == unique_groups[1]][y_col]
            stat, pval = ttest_ind(y1, y2, equal_var=False)
            print(f"t-test: t = {stat:.3f}, p = {pval:.3e}")
        elif len(unique_groups) > 2:
            groups = [plot_df[plot_df[group_col] == g][y_col].dropna()
                      for g in (order if order else unique_groups)]
            stat, pval = f_oneway(*groups)
            print(f"ANOVA: F = {stat:.3f}, p = {pval:.3e}")

    fig.tight_layout()
    return fig, ax
