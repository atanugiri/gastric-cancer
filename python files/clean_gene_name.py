import pandas as pd

def clean_gene_name(name):
    if pd.isnull(name):
        return None
    return str(name).replace(' ', '').replace('-', '').upper()
