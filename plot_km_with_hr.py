from lifelines import KaplanMeierFitter, CoxPHFitter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_km_with_hr(clinical_df, time_col, event_col, group_col,
                    group_high_label="High", output_prefix=None):
    """
    Plots Kaplan–Meier survival curves and fits Cox model for a binary group.

    Parameters:
    - clinical_df: DataFrame with survival and grouping data
    - time_col: column name for survival duration (numeric)
    - event_col: column name for event occurrence (1=event, 0=censored)
    - group_col: column name for binary group (e.g., "High"/"Low", "Female"/"Male")
    - group_high_label: which label is considered "high" (coded as 1 in Cox model)
    - output_prefix: filename prefix to save plots (omit or None to skip saving)

    Returns:
    - cph: fitted CoxPHFitter model
    """

    # Drop NA and ensure copy
    df = clinical_df[[time_col, event_col, group_col]].copy()
    df = df.dropna()

    # Check for exactly 2 unique group labels
    unique_groups = df[group_col].unique()
    if len(unique_groups) != 2:
        raise ValueError(f"{group_col} must have exactly 2 groups. Found: {unique_groups}")

    # Identify reference group
    other_group_label = [g for g in unique_groups if g != group_high_label][0]

    # Encode binary variable for Cox model
    df["Group_High"] = (df[group_col] == group_high_label).astype(int)

    # Fit Cox model
    cph = CoxPHFitter()
    cph.fit(df, duration_col=time_col, event_col=event_col, formula="Group_High")

    # Get hazard ratio, CI, and p-value
    hr = cph.hazard_ratios_["Group_High"]
    log_ci = cph.confidence_intervals_.loc["Group_High"]
    ci_lower = np.exp(log_ci["95% lower-bound"])
    ci_upper = np.exp(log_ci["95% upper-bound"])
    p_val = cph.summary.loc["Group_High", "p"]

    # Plot KM curves
    plt.figure(figsize=(5, 5))
    ax = plt.gca()
    group_colors = {group_high_label: "red", other_group_label: "blue"}
    median_dict = {}

    for group in [group_high_label, other_group_label]:
        mask = df[group_col] == group

        # Convert to numeric, drop any bad entries
        durations = pd.to_numeric(df.loc[mask, time_col], errors="coerce")
        events = pd.to_numeric(df.loc[mask, event_col], errors="coerce")
        valid = (~durations.isna()) & (~events.isna())
        durations = durations[valid]
        events = events[valid]

        if durations.empty:
            raise ValueError(f"No valid numeric survival data for group: '{group}'")

        kmf = KaplanMeierFitter()
        kmf.fit(durations=durations, event_observed=events, label=group)
        kmf.plot_survival_function(ci_show=True, linewidth=2.5,
                                   color=group_colors[group], ax=ax)
        median_dict[group] = kmf.median_survival_time_

    # Annotate HR and medians
    legend_text = (
        f"Median (95% CI)\n"
        f"{group_high_label}: {median_dict[group_high_label]:.1f} months\n"
        f"{other_group_label}: {median_dict[other_group_label]:.1f} months\n\n"
        f"HR = {hr:.2f} (95% CI: {ci_lower:.2f}–{ci_upper:.2f})\n"
        f"$p$ = {p_val:.3f}"
    )

    ax.text(0.98, 0.98, legend_text, transform=ax.transAxes,
            ha='right', va='top',
            fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    # Final plot formatting
    plt.title(f"Kaplan–Meier Survival Curve by {group_col}")
    plt.xlabel("Time (Months)")
    plt.ylabel("Overall Survival Probability")
    plt.tight_layout()

    if output_prefix:
        plt.savefig(f"{output_prefix}_survival_curve_with_HR.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{output_prefix}_survival_curve_with_HR.pdf", bbox_inches="tight")

    plt.show()
    return cph
