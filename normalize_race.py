import pandas as pd

def normalize_race(race):
    if pd.isna(race):
        return 'Unknown'
    
    race = str(race).strip().lower().replace('_', ' ')
    
    # Map to consistent forms
    mapping = {
        'white': 'White',
        'asian': 'Asian',
        'black or african american': 'Black or African American',
        'native hawaiian or other pacific islander': 'Native Hawaiian or Other Pacific Islander'
    }
    
    return mapping.get(race, race.title())