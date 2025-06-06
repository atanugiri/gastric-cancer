import pandas as pd

# Function to clean gene names
def clean_gene_name(name):
    if pd.isnull(name):
        return None
    return str(name).replace(' ', '')