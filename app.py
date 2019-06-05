# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 22:58:12 2019

@author: prajkumargoel
"""

import pymongo
import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

client = pymongo.MongoClient("mongodb+srv://pratham:mongodbatpratham95@cluster0-cjgfn.mongodb.net/test?retryWrites=true")
dbname="patient_detail"
db = client[dbname]

patient_metadata_collection = db["patient_metadata"]
patient_detail_collection = db["patient_detail"]

patient_metadata = patient_metadata_collection.find()
patient_detail = patient_detail_collection.find()


patient_metadata_list = []
for patient in patient_metadata:
    patient_metadata_list.append(patient)

patient_detail_list = []
for patient in patient_detail:
    patient_detail_list.append(patient)
    

client.close()

df = pd.DataFrame(patient_metadata_list)


df2 = pd.DataFrame(columns=['patient_id','symptom','accident'])

master_index=0
for document in patient_detail_list:
    for index,patient_history in enumerate([document[key] for key in document.keys() if 'patient_history' in key]):
        #print(patient_history)
        #print(master_index+index, patient_history)
        df2.loc[master_index+index,'patient_id'] = document['patient_id']
        if 'accident' in patient_history.keys():
            df2.loc[master_index+index,'accident'] = patient_history['accident']
        if 'symptom' in patient_history.keys():
            df2.loc[master_index+index,'symptom'] = patient_history['symptom']
    master_index+=index
    

df_master = pd.merge(df,df2,left_on='patient_id', right_on='patient_id')    

try:
    df_master.drop(['password', '_id'], axis=1, inplace=True)        
except:
    pass


symptom_counts = df_master.groupby(['symptom']).size().reset_index()
symptom_counts.rename(columns={0:'Count'}, inplace=True)

accident_counts = df_master.groupby(['accident']).size().reset_index()
accident_counts.rename(columns={0:'Count'}, inplace=True)

#gender_counts = df_master.groupby(['patient_gender']).size().reset_index()
#gender_counts.rename(columns={0:'Count'}, inplace=True)
#age_counts = df_master.groupby(['patient_age']).size().reset_index()
#age_counts.rename(columns={0:'Count'}, inplace=True)
#
#
##df_master.groupby(['symptom']).count().reset_index()['patient_gender'].groupby('patient_gender')[[0]].size()


symptom_gender = pd.DataFrame(df_master.groupby('symptom')['patient_gender'].value_counts())
symptom_age    = df_master.groupby('symptom')['patient_age'].value_counts()

symptom_gender = symptom_gender.unstack(level='patient_gender')
symptom_gender = symptom_gender.fillna(0)

symptom_age = symptom_age.unstack(level='patient_age')
symptom_age = symptom_age.fillna(0)

symptom_age['0-10'] = np.zeros(symptom_age.shape[0])
symptom_age['11-20'] = np.zeros(symptom_age.shape[0])
symptom_age['21-30'] = np.zeros(symptom_age.shape[0])
symptom_age['31-40'] = np.zeros(symptom_age.shape[0])
symptom_age['41-50'] = np.zeros(symptom_age.shape[0])
symptom_age['51-60'] = np.zeros(symptom_age.shape[0])
symptom_age['61-70'] = np.zeros(symptom_age.shape[0])
symptom_age['71-80'] = np.zeros(symptom_age.shape[0])
symptom_age['81-90'] = np.zeros(symptom_age.shape[0])
symptom_age['91-100'] = np.zeros(symptom_age.shape[0])

bins = ['0-10',
'11-20',
'21-30',
'31-40',
'41-50',
'51-60',
'61-70',
'71-80',
'81-90',
'91-100']
for age in list(symptom_age.columns):
    for bin in bins:
        try:
            if int(bin.split('-')[0]) <= age <= int(bin.split('-')[1]):
                print(age)
                symptom_age[bin] = symptom_age[bin] + symptom_age[age]
        except:
            pass

symptom_age_bins = symptom_age[bins]

accident_gender = pd.DataFrame(df_master.groupby('accident')['patient_gender'].value_counts())
accident_age    = df_master.groupby('accident')['patient_age'].value_counts()


accident_gender = accident_gender.unstack(level='patient_gender')
accident_gender = accident_gender.fillna(0)

accident_age = accident_age.unstack(level='patient_age')
accident_age = accident_age.fillna(0)

accident_age['0-10'] = np.zeros(accident_age.shape[0])
accident_age['11-20'] = np.zeros(accident_age.shape[0])
accident_age['21-30'] = np.zeros(accident_age.shape[0])
accident_age['31-40'] = np.zeros(accident_age.shape[0])
accident_age['41-50'] = np.zeros(accident_age.shape[0])
accident_age['51-60'] = np.zeros(accident_age.shape[0])
accident_age['61-70'] = np.zeros(accident_age.shape[0])
accident_age['71-80'] = np.zeros(accident_age.shape[0])
accident_age['81-90'] = np.zeros(accident_age.shape[0])
accident_age['91-100'] = np.zeros(accident_age.shape[0])

bins = ['0-10',
'11-20',
'21-30',
'31-40',
'41-50',
'51-60',
'61-70',
'71-80',
'81-90',
'91-100']
for age in list(accident_age.columns):
    for bin in bins:
        try:
            if int(bin.split('-')[0]) <= age <= int(bin.split('-')[1]):
                print(age)
                accident_age[bin] = accident_age[bin] + accident_age[age]
        except:
            pass

accident_age_bins = accident_age[bins]




app = dash.Dash()

app.layout = html.Div(children=[
        
        html.H1(children='App User Statistics Dashboard'),
        
        html.H3(children='High Level Distribution of Symptoms and Accidents'),
        dcc.Dropdown(id='input',
                options=[
                        {'label': 'Symptoms', 'value': 'symptom'},
                        {'label': 'Accidents', 'value': 'accident'},
                    ],
         value='symptom'
        ),
                
        html.Div(id='output-graph'),
        
        html.H3(children='Distribution of Symptoms and Accidents by Gender'),
        dcc.Dropdown(id='input2',
                options=[
                        {'label': 'Symptoms', 'value': 'symptom'},
                        {'label': 'Accidents', 'value': 'accident'},
                    ],
         value='symptom'
        ),
                
        html.Div(id='output-graph2'),
        
        html.H3(children='Distribution of Symptoms and Accidents by Age Group'),
        dcc.Dropdown(id='input3',
                options=[
                        {'label': 'Symptoms', 'value': 'symptom'},
                        {'label': 'Accidents', 'value': 'accident'},
                    ],
         value='symptom'
        ),
        
        dcc.Dropdown(id='age_group',
                options=[
                        {'label': '0-10', 'value': '0-10'},
                        {'label': '11-20', 'value': '11-20'},
                        {'label': '21-30', 'value': '21-30'},
                        {'label': '31-40', 'value': '31-40'},
                        {'label': '41-50', 'value': '41-50'},
                        {'label': '51-60', 'value': '51-60'},
                        {'label': '61-70', 'value': '61-70'},
                        {'label': '71-80', 'value': '71-80'},
                        {'label': '81-90', 'value': '81-90'},
                        {'label': '91-100', 'value': '91-100'},
                        
                    ],
         value='21-30'
        ),
                
        html.Div(id='output-graph3'),


        ]
        )
@app.callback(
        Output(component_id = 'output-graph', component_property='children'),
        [Input(component_id = 'input', component_property='value')])

def update_value(input_data):
    
    if input_data == "symptom":
        x = symptom_counts.symptom
        y = symptom_counts.Count
        title = 'Symptom Distribution'
    elif input_data == "accident":
        x = accident_counts.accident
        y = accident_counts.Count
        title = 'Accident Distribution'

    return dcc.Graph(id='graph1',
                  figure={
                          'data': [{'x':x, 'y':y, 'type':'bar', 'name':'Distribution'},
                                    ],
                          'layout': {
                                  'title': title,
                                  'yaxis':go.layout.YAxis(title='# of Reported Cases')
                                  }
                          }

                  )
    
    
@app.callback(
        Output(component_id = 'output-graph2', component_property='children'),
        [Input(component_id = 'input2', component_property='value')])

def update_value(input_data):
    
    if input_data == "symptom":
        
        women_bins = symptom_gender[symptom_gender.columns[0]]
        men_bins   = symptom_gender[symptom_gender.columns[1]]
    
        y = np.asarray(symptom_gender.index)
        title = 'Symptom'
        
    elif input_data == "accident":
        
        women_bins = accident_gender[accident_gender.columns[0]]
        men_bins   = accident_gender[accident_gender.columns[1]]
    
        y = np.asarray(accident_gender.index)
        title = 'Accident'
    
    
    women_bins = women_bins
    men_bins   = men_bins
    
    y = y
    title = title
    
    return dcc.Graph(id='graph2',
                  figure={
                          'data' :  [go.Bar(y=y,
                                   x=men_bins,
                                   orientation='h',
                                   name='Men',
                                   hoverinfo='x',
                                   marker=dict(color='powderblue')
                                   ),
    
                                   go.Bar(y=y,
                                   x=-1*women_bins,
                                   orientation='h',
                                   name='Women',
                                   text= -1 * women_bins.astype('int'),
                                   hoverinfo='text',
                                   marker=dict(color='seagreen')
                                   )],
                        'layout' : go.Layout(yaxis=go.layout.YAxis(),
                                               xaxis=go.layout.XAxis(
                                               range=[-40, 40],
                                               tickvals=[-30, -20, -10, 0, 10, 20, 30],
                                               ticktext=[-30, -20, -10, 0, 10, 20, 30],
                                               title='# Occurences'),
                                               barmode='overlay',
                                               bargap=0.1)
                    }

                  )
    
    
    
@app.callback(
        Output(component_id = 'output-graph3', component_property='children'),
        [Input(component_id = 'input3', component_property='value'), Input(component_id = 'age_group', component_property='value')])

def update_value(input_data, age_group):
    
    if input_data == "symptom":
        
        labels = np.asarray(symptom_age_bins.index)
        values = np.asarray(symptom_age_bins[age_group])
    
        title = 'Symptom'
        print(labels)
        print(values)
        
    elif input_data == "accident":
        
        labels = np.asarray(accident_age_bins.index)
        values = np.asarray(accident_age_bins[age_group])
    
        title = 'Accident'
        print(labels)
        print(values)
        pass
    
    
    
    labels=labels
    values=values
    title = title
    
    return dcc.Graph(id='graph3',
                  figure={
                          'data' :  [{'type':'pie', 'labels':labels, 'values':values}],

                        
                    }

            )
    
if __name__ == '__main__':
    app.run_server(debug=True)













