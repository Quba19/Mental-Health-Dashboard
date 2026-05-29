import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ── Consistent colour palette ─────────────────────────────────────
PRIMARY   = '#2E86AB'
SECONDARY = '#E84855'
ACCENT    = '#3BB273'
NEUTRAL   = '#A8DADC'
DARK      = '#1D3557'
PALETTE   = [PRIMARY, SECONDARY, ACCENT, NEUTRAL, DARK,
             '#F4A261', '#E76F51', '#264653', '#2A9D8F', '#E9C46A']

sns.set_theme(style='whitegrid', palette=PALETTE)
plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'figure.facecolor': 'white',
    'axes.facecolor': '#F8F9FA',
})

# 1 ── Pie Chart ───────────────────────────────────────────────────
def pie_chart_treatment(df: pd.DataFrame):
    """Pie chart — treatment vs no-treatment distribution."""
    counts = df['treatment'].value_counts()
    labels = ['Seeking Treatment', 'Not Seeking']
    colors = [PRIMARY, SECONDARY]
    explode = (0, 0.08)
    
    fig, ax = plt.subplots(figsize=(6, 5))
    wedges, texts, autotexts = ax.pie(
        counts.values, labels=labels, autopct='%1.1f%%',
        colors=colors, explode=explode, startangle=140,
        textprops={'fontsize': 12}
    )
    for at in autotexts:
        at.set_fontweight('bold')
    ax.set_title('Mental Health Treatment Distribution', fontsize=13,
                 fontweight='bold', pad=15)
    plt.tight_layout()
    return fig

# 2 ── Histogram ──────────────────────────────────────────────────
def histogram_age(df: pd.DataFrame):
    """Histogram — age frequency distribution."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df['Age'], bins=30, color=PRIMARY,
            edgecolor='white', linewidth=0.8)
    ax.axvline(df['Age'].mean(), color=SECONDARY, linestyle='--',
               linewidth=2, label=f"Mean: {df['Age'].mean():.1f}")
    ax.axvline(df['Age'].median(), color=ACCENT, linestyle='--',
               linewidth=2, label=f"Median: {df['Age'].median():.1f}")
    ax.set_title('Age Frequency Distribution', fontsize=13, fontweight='bold')
    ax.set_xlabel('Age (years)')
    ax.set_ylabel('Number of Respondents')
    ax.legend()
    plt.tight_layout()
    return fig

# 3 ── Line Chart ──────────────────────────────────────────────────
def line_chart_age_distribution(df: pd.DataFrame):
    """Line chart — age distribution by treatment status."""
    age_treatment = (
        df.groupby(['Age', 'treatment'], observed=True)
        .size()
        .reset_index(name='count')
    )
    
    fig, ax = plt.subplots(figsize=(9, 5))
    for treatment_val in df['treatment'].unique():
        subset = age_treatment[age_treatment['treatment'] == treatment_val]
        ax.plot(subset['Age'], subset['count'],
                marker='o', linewidth=2, markersize=4,
                label=f'Treatment: {treatment_val}')
    
    ax.set_title('Age Distribution by Treatment Status', fontsize=13, fontweight='bold')
    ax.set_xlabel('Age')
    ax.set_ylabel('Number of Respondents')
    ax.legend()
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    return fig

# 4 ── Bar Chart ───────────────────────────────────────────────────
def bar_chart_by_country(df: pd.DataFrame):
    """Bar chart — respondents by country."""
    country_counts = df['Country'].value_counts().head(10).reset_index()
    country_counts.columns = ['Country', 'Count']
    
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(country_counts['Country'], country_counts['Count'],
                  color=PALETTE[:len(country_counts)], edgecolor='white',
                  linewidth=0.8)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2,
                height + 1,
                f'{int(height)}', ha='center', va='bottom',
                fontsize=9, fontweight='bold')
    
    ax.set_title('Top 10 Countries by Respondents', fontsize=13, fontweight='bold')
    ax.set_xlabel('Country')
    ax.set_ylabel('Number of Respondents')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

# 5 ── Scatter Plot ────────────────────────────────────────────────
def scatter_age_work_interfere(df: pd.DataFrame):
    """Scatter plot — age vs work interference."""
    # Map work_interfere to numeric values
    work_map = {'Never': 1, 'Rarely': 2, 'Sometimes': 3, 'Often': 4}
    df_temp = df.copy()
    df_temp['work_interfere_num'] = df_temp['work_interfere'].map(work_map)
    
    fig, ax = plt.subplots(figsize=(9, 6))
    colors = df_temp['treatment'].map({'Yes': SECONDARY, 'No': PRIMARY})
    ax.scatter(df_temp['Age'], df_temp['work_interfere_num'],
               c=colors, alpha=0.5, s=20, edgecolors='none')
    
    legend_handles = [
        mpatches.Patch(color=PRIMARY, label='No Treatment'),
        mpatches.Patch(color=SECONDARY, label='Seeking Treatment'),
    ]
    ax.legend(handles=legend_handles, fontsize=11)
    ax.set_title('Age vs Work Interference (coloured by Treatment)',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('Age')
    ax.set_ylabel('Work Interference Frequency')
    ax.set_yticks([1, 2, 3, 4])
    ax.set_yticklabels(['Never', 'Rarely', 'Sometimes', 'Often'])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

# 6 ── Box Plot ────────────────────────────────────────────────────
def box_plot_age_by_treatment(df: pd.DataFrame):
    """Box plots — age by treatment status."""
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x='treatment', y='Age', data=df,
                palette=[PRIMARY, SECONDARY], ax=ax)
    ax.set_xticklabels(['No Treatment', 'Seeking Treatment'])
    ax.set_title('Age Distribution by Treatment Status',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('')
    ax.set_ylabel('Age (years)')
    plt.tight_layout()
    return fig

# 7 ── Heatmap ─────────────────────────────────────────────────────
def heatmap_correlation(df: pd.DataFrame):
    """Heatmap — correlation matrix of numeric features."""
    df_enc = df.copy()
    
    # Encode binary columns
    binary_cols = ['self_employed', 'family_history', 'treatment',
                   'remote_work', 'tech_company', 'benefits',
                   'care_options', 'wellness_program', 'seek_help',
                   'anonymity', 'leave']
    
    for col in binary_cols:
        if col in df_enc.columns:
            df_enc[col] = df_enc[col].map({'Yes': 1, 'No': 0, 'Maybe': 0.5, 'Don\'t know': 0.5})
    
    # Select numeric columns for correlation
    numeric_cols = ['Age'] + binary_cols
    numeric_cols = [col for col in numeric_cols if col in df_enc.columns]
    
    corr = df_enc[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(11, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
                cmap='coolwarm', linewidths=0.5,
                square=True, ax=ax,
                cbar_kws={'shrink': 0.8})
    ax.set_title('Correlation Heatmap — Mental Health Features',
                 fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    return fig

# 8 ── Area Chart ──────────────────────────────────────────────────
def area_chart_company_size(df: pd.DataFrame):
    """Area chart — cumulative count by company size."""
    company_size = df['no_employees'].value_counts().sort_index().reset_index()
    company_size.columns = ['Company Size', 'Count']
    
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.fill_between(company_size['Company Size'], company_size['Count'],
                    alpha=0.5, color=PRIMARY)
    ax.plot(company_size['Company Size'], company_size['Count'],
            marker='o', color=PRIMARY, linewidth=2)
    
    ax.set_title('Respondents by Company Size',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('Number of Employees')
    ax.set_ylabel('Number of Respondents')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

# 9 ── Count Plot ──────────────────────────────────────────────────
def count_plot_remote_work(df: pd.DataFrame):
    """Count plot — remote work by treatment status."""
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.countplot(x='remote_work', hue='treatment', data=df,
                  palette=[PRIMARY, SECONDARY], ax=ax)
    ax.set_title('Remote Work Status vs Treatment',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('Remote Work')
    ax.set_ylabel('Number of Respondents')
    handles = [
        mpatches.Patch(color=PRIMARY, label='No Treatment'),
        mpatches.Patch(color=SECONDARY, label='Seeking Treatment'),
    ]
    ax.legend(handles=handles)
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    return fig

# 10 ── Violin Plot ────────────────────────────────────────────────
def violin_plot_age_by_gender(df: pd.DataFrame):
    """Violin plot — age distribution by gender and treatment."""
    # Clean gender values for better visualization
    df_temp = df.copy()
    gender_map = {'Male': 'Male', 'Female': 'Female'}
    df_temp['Gender_clean'] = df_temp['Gender'].map(gender_map)
    df_temp = df_temp[df_temp['Gender_clean'].notna()]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(x='Gender_clean', y='Age', hue='treatment',
                   data=df_temp, split=True,
                   palette=[PRIMARY, SECONDARY], ax=ax,
                   inner='quartile')
    ax.set_title('Age Distribution by Gender & Treatment',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Age (years)')
    handles = [
        mpatches.Patch(color=PRIMARY, label='No Treatment'),
        mpatches.Patch(color=SECONDARY, label='Seeking Treatment'),
    ]
    ax.legend(handles=handles, title='Treatment Status')
    plt.tight_layout()
    return fig