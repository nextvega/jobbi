import requests
import json
import os
import pandas as pd
from datetime import datetime

BASEDIR = os.path.dirname(os.path.abspath(__file__)) 

def extract_state(row):
    return row['address']['state']

def identify_os(user_agent):
    if 'Windows' in user_agent:
        return 'Windows'
    elif 'Linux' in user_agent:
        return 'Linux'
    elif 'Macintosh' in user_agent or 'Mac OS X' in user_agent:
        return 'macOS'
    else:
        return 'Otro'

def summary(data):
    df_summary = pd.DataFrame(data)

    # datos requeridos para el summary

    total_registros = len(df_summary)
    num_hombres = df_summary[df_summary['gender'] == 'male'].shape[0]
    num_mujeres = df_summary[df_summary['gender'] == 'female'].shape[0]

    bins = [0, 20, 40, 60, 80]
    labels = ['00-20', '21-40', '41-60', '61-80']

    df_summary['age_range'] = pd.cut(df_summary['age'], bins=bins, labels=labels, right=False)
    age_groups = df_summary.groupby(['gender', 'age_range'], observed=False).size().unstack(fill_value=0)

    summary_data = {
        'registre': total_registros,
        'gender': 'total',
        'male': num_hombres,
        'female': num_mujeres,

        '00-20_male': age_groups.loc['male', '00-20'] if 'male' in age_groups.index else 0,
        '21-40_male': age_groups.loc['male', '21-40'] if 'male' in age_groups.index else 0,
        '41-60_male': age_groups.loc['male', '41-60'] if 'male' in age_groups.index else 0,
        '61-80_male': age_groups.loc['male', '61-80'] if 'male' in age_groups.index else 0,

        '00-20_female': age_groups.loc['female', '00-20'] if 'female' in age_groups.index else 0,
        '21-40_female': age_groups.loc['female', '21-40'] if 'female' in age_groups.index else 0,
        '41-60_female': age_groups.loc['female', '41-60'] if 'female' in age_groups.index else 0,
        '61-80_female': age_groups.loc['female', '61-80'] if 'female' in age_groups.index else 0,

    }

    df_summary['state'] = df_summary.apply(lambda row: extract_state(row), axis=1)
    state_counts = df_summary.groupby(['state', 'gender']).size().unstack(fill_value=0)

    for state in state_counts.index:
        summary_data[f'{state}_male'] = state_counts.loc[state, 'male']
        summary_data[f'{state}_female'] = state_counts.loc[state, 'female']
        summary_data[f'{state}_other'] = state_counts.loc[state].sum() - state_counts.loc[state, ['male', 'female']].sum()



    df_summary['os'] = df_summary['userAgent'].apply(identify_os)
    os_types = ['Windows', 'Linux', 'macOS', 'Otro']  
    os_counts = df_summary['os'].value_counts().reindex(os_types, fill_value=0)
    for os_type, count in os_counts.items():
        summary_data[f'{os_type}'] = count
    
    

    summary_df = pd.DataFrame([summary_data])
    summary_filename = os.path.join(BASEDIR,f"files/summary/summary_{datetime.today().strftime('%Y%m%d')}.csv")
    summary_df.to_csv(summary_filename, index=False)

    return summary_filename 