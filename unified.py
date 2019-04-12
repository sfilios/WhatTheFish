# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import os
import pickle
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import base64
import glob2 as glob

# get the external stylesheets, images, names
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

predictions = pd.DataFrame(columns=['Name','Likelihood'])

# get the model
with open('Fish_Data/fat_model.pkl', 'rb') as pickle_file:
    m = pickle.load(pickle_file)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
html.Div([


    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='What the Fish?', children=[


         html.Label('Which sub-region will you fish in?'),
         dcc.Dropdown(id='sub_reg',
            options=[{'label':'North Atlantic (ME; NH; MA; RI; CT)', 'value':0},
                {'label': ' Mid-Atlantic (NY; NJ; DE; MD; VA)', 'value':1},
                {'label': ' South Atlantic (NC; SC; GA; East FL)', 'value':2},
                {'label': 'Gulf of Mexico (WFL; AL; MS; LA)', 'value':3}
            ],
            value=0),

        html.Label('How far from shore will you fish?'),
        dcc.Dropdown(id='area_x',
            options=[{'label':'<=3miles', 'value':0},
            {'label':'>3miles', 'value':1},
            {'label':'Inland', 'value':4},
            {'label':'<=10 miles (West Florida only)', 'value':2},
            {'label':'>10 miles (West Florida only)', 'value':3}],
            value=0),

        html.Label('Will you fish from land or sea?'),
        dcc.Dropdown(id='mode',
            options=[
            {'label':'Shore', 'value':0},
            {'label':'Headboat', 'value':1},
            {'label':'Charter Boat', 'value':2},
            {'label':'Private/Rental','value':3}],
            value=0),

        html.Label('In what type of habitat will you fish?'),
        dcc.Dropdown(id='hab',
            options=[
            {'label':'Open water', 'value':0},
            {'label':'Sound', 'value':1},
            {'label':'River', 'value':2},
            {'label':'Bay', 'value':3},
            {'label':'Other', 'value':4}],
            value=0),

        html.Label('During which month will you fish?'),
        dcc.Dropdown(id='month',
            options=[
            {'label':'January', 'value':0},
            {'label':'February', 'value':1},
            {'label':'March', 'value': 2},
            {'label': 'April', 'value':3},
            {'label': 'May', 'value':4},
            {'label': 'June', 'value':5},
            {'label': 'July', 'value':6},
            {'label': 'August', 'value':7},
            {'label': 'September','value':8},
            {'label': 'October','value':9},
            {'label': 'November','value':10},
            {'label': 'December', 'value':11}],
            value=0),

         html.Label('How many hours will you be out in a boat?'),
         dcc.Dropdown(id='bthrs',
            options=[{'label':x, 'value':x} for x in range(1,25)]+\
            [{'label':'UNKNOWN', 'value':99}],
            value=1),

        html.Label('Number of people who will fish together'),
        dcc.Dropdown(id='contributors',
            options=[{'label':x, 'value':x} for x in range(1,20)],
            value=1),

         html.Label('How many days have you been fishing in the past year?'),
         dcc.Dropdown(id='ffdys12',
            options=[{'label':x, 'value':x} for x in range(1,365)]+\
            [{'label':'UNKNOWN', 'value':999}],
            value=1)

        ]),

    ])
    ], style = {'display':'inline-block', 'width':'40%', 'marginLeft':'10%',
    'marginRight':'10%'}),
html.Div(children=[
    html.H1('Predicted Fish:'),
    html.Div(id='my-div')], style = {'display':'inline-block', 'width':'30%'})
])
# ], style={'marginLeft':'20%', 'marginRight':'20%'})

@app.callback(
   Output(component_id='my-div', component_property='children'),
    [Input(component_id='contributors', component_property='value'),
    Input(component_id='area_x', component_property='value'),
    Input(component_id='mode', component_property='value'),
    Input(component_id='sub_reg', component_property='value'),
    Input(component_id='hab', component_property='value'),
    Input(component_id='bthrs', component_property='value'),
    Input(component_id='ffdys12', component_property='value'),
    Input(component_id='month', component_property='value')]
)
def predictor(contributors, area_x, mode, sub_reg, hab,
    bthrs, ffdys12, month):

    X=np.array([area_x, mode, sub_reg, hab, bthrs,
    contributors,ffdys12, month])

    x=X.reshape(1,-1)
    test = m.predict_proba(x)

    predictions['Likelihood']=test[0]
    predictions['Name'] = m.classes_

    tops = predictions.sort_values(by='Likelihood', ascending=False)
    ret = tops.head(3)

    return html.Table(
    #header
    [html.Tr([html.Th(col) for col in ret.columns])] +
    #body
    [html.Tr([
        html.Td(ret.iloc[i][col]) for col in ret.columns
            ]) for i in range(min(len(ret), 3))]
    )


if __name__ == '__main__':
    app.run_server(debug=True)
