def merge_expression_and_clinical(expression_df, clinical_df, gene_symbol, id_col="Sample ID"):
    """
    Merges clinical and expression data on sample ID, and appends the expression value for one gene.

    Parameters:
    - expression_df: DataFrame with genes as rows, sample IDs as columns
    - clinical_df: DataFrame with sample metadata (must include 'Sample ID')
    - gene_symbol: str, e.g., 'CD36'
    - id_col: column in clinical_df to match sample IDs (default = 'Sample ID')

    Returns:
    - merged_df: clinical_df with an extra column for gene expression
    - aligned_expression_df: expression_df subset to only shared sample IDs
    """

    expression_df.columns = expression_df.columns.str.strip().str.upper()
    clinical_df = clinical_df.copy()
    clinical_df[id_col] = clinical_df[id_col].str.strip().str.upper()

    # Find and subset to common samples
    common_samples = expression_df.columns.intersection(clinical_df[id_col])
    expression_sub = expression_df[common_samples]
    clinical_sub = (
        clinical_df.set_index(id_col)
        .loc[common_samples]
        .reset_index()
        .rename(columns={"index": id_col})
    )

    # Build expression DataFrame
    gene_expr = expression_sub.loc[gene_symbol]
    gene_expr_df = pd.DataFrame({
        id_col: gene_expr.index,
        f"{gene_symbol} Expression": gene_expr.values
    })

    # Merge
    merged_df = pd.merge(clinical_sub, gene_expr_df, on=id_col)

    return merged_df, expression_sub
