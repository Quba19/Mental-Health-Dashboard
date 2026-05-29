import pandas as pd
import numpy as np

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    """Load and clean the mental health survey dataset."""
    df = pd.read_csv(filepath)
    
    # Standardise column names
    df.columns = df.columns.str.strip()
    
    # Clean Age column - remove invalid ages
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df = df[(df['Age'] >= 18) & (df['Age'] <= 100)]
    
    # Clean Gender column
    df['Gender'] = df['Gender'].str.strip()
    # Map common variations
    gender_map = {
        'male': 'Male', 'm': 'Male', 'man': 'Male', 'cis male': 'Male',
        'female': 'Female', 'f': 'Female', 'woman': 'Female', 'cis female': 'Female',
        'trans female': 'Female', 'trans male': 'Male'
    }
    df['Gender'] = df['Gender'].str.lower().map(gender_map).fillna('Other')
    
    # Clean treatment column
    if 'treatment' in df.columns:
        df['treatment'] = df['treatment'].str.strip().map({'Yes': 'Yes', 'No': 'No'})
    
    # Clean remote_work column
    if 'remote_work' in df.columns:
        df['remote_work'] = df['remote_work'].str.strip().map({'Yes': 'Yes', 'No': 'No'})
    
    # Clean tech_company column
    if 'tech_company' in df.columns:
        df['tech_company'] = df['tech_company'].str.strip().map({'Yes': 'Yes', 'No': 'No'})
    
    # Clean family_history column
    if 'family_history' in df.columns:
        df['family_history'] = df['family_history'].str.strip().map({'Yes': 'Yes', 'No': 'No'})
    
    # Clean benefits column
    if 'benefits' in df.columns:
        df['benefits'] = df['benefits'].str.strip()
    
    # Clean work_interfere column
    if 'work_interfere' in df.columns:
        df['work_interfere'] = df['work_interfere'].str.strip()
    
    # Clean no_employees column
    if 'no_employees' in df.columns:
        df['no_employees'] = df['no_employees'].str.strip()
    
    # Remove rows with missing critical data
    df = df.dropna(subset=['Age', 'Gender', 'treatment'])
    
    return df

def apply_filters(df: pd.DataFrame,
                  gender_filter: list,
                  age_range: tuple,
                  country_filter: list,
                  treatment_filter: list,
                  remote_filter: list,
                  search_text: str) -> pd.DataFrame:
    """Apply all sidebar filters and return filtered dataframe."""
    filtered = df.copy()
    
    # Gender filter
    if gender_filter:
        filtered = filtered[filtered['Gender'].isin(gender_filter)]
    
    # Age range slider
    filtered = filtered[
        (filtered['Age'] >= age_range[0]) &
        (filtered['Age'] <= age_range[1])
    ]
    
    # Country filter
    if country_filter:
        filtered = filtered[filtered['Country'].isin(country_filter)]
    
    # Treatment filter
    if treatment_filter:
        filtered = filtered[filtered['treatment'].isin(treatment_filter)]
    
    # Remote work filter
    if remote_filter:
        filtered = filtered[filtered['remote_work'].isin(remote_filter)]
    
    # Search / text filter
    if search_text.strip():
        mask = (
            filtered['Country'].str.contains(search_text, case=False, na=False) |
            filtered['state'].str.contains(search_text, case=False, na=False) |
            filtered['Gender'].str.contains(search_text, case=False, na=False)
        )
        filtered = filtered[mask]
    
    return filtered

def get_kpi_metrics(df: pd.DataFrame) -> dict:
    """Return dictionary of KPI summary values."""
    treatment_yes = len(df[df['treatment'] == 'Yes'])
    family_history_yes = len(df[df['family_history'] == 'Yes']) if 'family_history' in df.columns else 0
    remote_yes = len(df[df['remote_work'] == 'Yes']) if 'remote_work' in df.columns else 0
    tech_yes = len(df[df['tech_company'] == 'Yes']) if 'tech_company' in df.columns else 0
    benefits_yes = len(df[df['benefits'] == 'Yes']) if 'benefits' in df.columns else 0
    
    return {
        'total_records': len(df),
        'avg_age': round(df['Age'].mean(), 1),
        'treatment_yes_pct': round(treatment_yes / len(df) * 100, 1) if len(df) > 0 else 0,
        'family_history_pct': round(family_history_yes / len(df) * 100, 1) if len(df) > 0 else 0,
        'remote_work_pct': round(remote_yes / len(df) * 100, 1) if len(df) > 0 else 0,
        'tech_company_pct': round(tech_yes / len(df) * 100, 1) if len(df) > 0 else 0,
        'benefits_pct': round(benefits_yes / len(df) * 100, 1) if len(df) > 0 else 0,
        'countries': df['Country'].nunique(),
    }