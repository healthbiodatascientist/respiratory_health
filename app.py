#!/usr/bin/env python
# coding: utf-8

# Import packages/libraries

# In[7]:


import pandas as pd
from dash import Dash, html, dash_table
import dash_bootstrap_components as dbc


# Import data and create tables

# In[8]:


def no_geometry():
    df_resp_prev_mapped = pd.read_csv('https://raw.githubusercontent.com/healthbiodatascientist/respiratory_health/refs/heads/main/resp_prev_mapped.csv')
    df_resp_prev_mapped = df_resp_prev_mapped.set_index('HBCode')
    df_hb_beds_table = df_resp_prev_mapped.drop('geometry', axis=1)
    return df_hb_beds_table
df_hb_beds_table = no_geometry()
df_numeric_columns = df_hb_beds_table.select_dtypes('number')


# Create app layout

# In[9]:


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
app.layout = dbc.Container([
    html.H1("Respiratory Disease Related Prevalence in Scotland's General Practices by Regional Health Board 2024/25", className='mb-2', style={'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col(html.Summary("The map below displays open source respiratory disease related data from Public Health Scotland (PHS) for each of the Scottish Health Board Regions. Click on or hover over your Health Board for an insight into the factors affecting chronic respiratory disease in your area:", className='mb-2', style={'padding': '10px 10px', 'list-style': 'none'}))]),
    dbc.Row([dbc.Col(html.Iframe(id='my_output', height=600, width=1000, srcDoc=open('respprevairqualmap.html', 'r').read()))], style={'text-align':'center'}),
    html.Figcaption("Figure 1: Map of the latest respiratory-related disease and air quality open data for the Scottish Health Board Regions", className='mb-2', style={'padding': '10px 10px', 'textAlign':'center'}),
    html.H4("Potential Data Relationships", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("Prevalence is how common a disease is in a population. If in a GP practice with 10,000 patients 1,000 meet the conditions for the cancer indicator, then this practice has a cancer prevalence of 10 per 100. In other words, prevalence rates represent how many people out of every 100 are recorded as having a particular disease.", className='mb-2'),
    html.Summary("SIMD quintiles divide Scotland's data zones into five equal groups, with Quintile 1 representing the 20% most deprived areas and Quintile 5 representing the 20% least deprived areas. This allows for the identification and targeting of resources to the areas of greatest need based on overall deprivation or specific factors like income, education, or health", className='mb-2'),
    html.Summary("Asthma is a chronic respiratory condition where airways become inflamed, sensitive, and narrow, causing symptoms like wheezing, coughing, chest tightness, and shortness of breath", className='mb-2'),
    html.Summary("Chronic obstructive pulmonary disease (COPD) is a common lung disease causing restricted airflow and breathing problems. It is sometimes called emphysema or chronic bronchitis", className='mb-2'),
    html.Summary("Smoking is the primary cause of COPD, the harmful chemicals in smoke damage lung tissues and airways, causing inflammation and making it difficult to breathe. Smoking also significantly worsens asthma by causing airway irritation, increased inflammation, and a higher risk of severe attacks and reduced response to medication", className='mb-2'),
    html.Summary("Age plays a key role in distinguishing asthma from COPD: Asthma can develop at any age, but COPD typically manifests in adulthood (after age 40) due to accumulated damage, often from smoking. While asthma prevalence decreases with age, COPD prevalence increases with age. Asthma-COPD overlap syndrome (ACOS), which combines features of both, is more common in older individuals", className='mb-2'),
    html.Summary("Deprivation is strongly linked to higher risks of developing and experiencing worse outcomes from asthma and COPD due to factors like increased exposure to air pollution, poor housing conditions, and higher smoking rates", className='mb-2'),
    html.Summary("Poor air quality significantly harms individuals with asthma and COPD by triggering symptoms like chest tightness and breathlessness and increasing the risk of exacerbations. Air pollutants, including particulate matter (PM), nitrogen dioxide (NO2), and ozone (O3), cause inflammation and irritation in the airways, leading to worsened lung function", className='mb-2'),
    html.Figcaption("Table 1: Latest open respiratory disease related data for the Scottish Health Board Regions with the highest 50% of column values highlighted in dark green", className='mb-2', style={'margin-bottom': '1em', 'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col(dash_table.DataTable(
    data=df_hb_beds_table.to_dict('records'),
    sort_action='native',
    columns=[{'name': i, 'id': i} for i in df_hb_beds_table.columns],
    style_cell={'textAlign': 'center'},
    fixed_columns={'headers': True, 'data': 1},
    style_table={'minWidth': '100%'},
    style_data_conditional=
    [
            {
                'if': {
                    'filter_query': '{{{}}} > {}'.format(col, value),
                    'column_id': col
                },
                'backgroundColor': '#06402B',
                'color': 'white'
            } for (col, value) in df_numeric_columns.quantile(0.1).items()
        ] +       
        [
            {
                'if': {
                    'filter_query': '{{{}}} <= {}'.format(col, value),
                    'column_id': col
                },
                'backgroundColor': '#98FB98',
                'color': 'white'
            } for (col, value) in df_numeric_columns.quantile(0.5).items()
        ]
    ))
    ]),
    html.H4("Open Data References", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("Public Health Scotland", style={'list-style': 'none'}),
    html.Li(html.Cite("https://publichealthscotland.scot/publications/general-practice-disease-prevalence-data-visualisation/general-practice-disease-prevalence-visualisation-8-july-2025/")),
    html.Li(html.Cite("https://publichealthscotland.scot/media/34174/diseaseprevalence_methodology_and_metadata_2025-for-publication.pdf")),
    html.Summary("Scotland's Census 2022 - National Records of Scotland", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.scotlandscensus.gov.uk/webapi/jsf/tableView/tableView.xhtml")),
    html.Summary("Scottish Surveys Core Questions 2023 - Scottish Government", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.gov.scot/publications/scottish-surveys-core-questions-2023/documents/")),
    html.Summary("Air Quality in Scotland - Scotland's Environment", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.scottishairquality.scot/latest/summary")),
    html.Li(html.Cite("https://www.scottishairquality.scot/data/data-selector")),
    ])


# Run app

# In[10]:


if __name__ == "__main__":
    app.run()

