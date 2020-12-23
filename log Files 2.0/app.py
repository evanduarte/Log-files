#-------------------------------- ESSAIE NUMERO 1 PRINCIPAL -----------------------------------------
import base64
import os
from urllib.parse import quote as urlquote
import pandas as pd
from pandas import Timestamp
import io
from io import StringIO
from flask import Flask, send_from_directory
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ClientsideFunction
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from django.utils import timezone
import re
import datetime
from datetime import date
import matplotlib.pyplot as plt
import random
import base64
import dash_table
import dash_bootstrap_components as dbc
from datetime import datetime as dt
import pathlib
from dash.exceptions import PreventUpdate
import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

server = Flask(__name__)
app = dash.Dash(server=server)


#import data txt
df_data=pd.read_excel (r'log data\log_data.xlsm')
df_ID_user=df_data['globaluserid']
df_name=df_data['Name']
df_deptname=list(set(df_data['deptname']))
df_jobfamily=list(set(df_data['jobfamily']))
df_position=list(set(df_data['position']))

#Analyse procedure fonctions les plus utilisées
df_utilisation = pd.DataFrame(columns=['Ordre','Name','Type'])
df_nb_utilisation= pd.DataFrame(columns=['Name','Number'])
df_utilisation_2= pd.DataFrame(columns=['Name','Formula Input','Sensory Prediction','Simple analyse','Formulas Comparaison','Look for formula','Look for Benchmark'])
df_utilisation_2.set_index('Name', inplace = True)
df_utilisation_3= pd.DataFrame(columns=['Function','Date','Log Name','Number of used function'])
df_log_name= pd.DataFrame(columns=['Name'])


day_list = [
    "Sunday",
    "Saturday",
    "Friday",
    "Thursday",
    "Wednesday",
    "Tuesday",
    "Monday",
]

import_list=['From anywhere','From specific directory']

#--------------
df_screen = pd.DataFrame(columns=['Contenu'])

#Sensory Prediction of the formula
df_sensory=pd.DataFrame(columns=['Contenu'])

#IPC manquant
df_IPC=pd.DataFrame(columns=['Contenu'])

#Simple Analysis of the formula
df_analysis=pd.DataFrame(columns=['Contenu'])

#Comparaison of the formula
df_comparaison=pd.DataFrame(columns=['Contenu'])

#looking at the formula with columns
df_looking=pd.DataFrame(columns=['Contenu'])

#looking at the Benchmarks with columns
df_lookBench=pd.DataFrame(columns=['Contenu'])


def utilisation(iterator,name):

    motif=re.compile("--------------")
    motif2=re.compile("Sensory Prediction of the formula")
    motif4=re.compile("Simple Analysis of the formula")
    motif5=re.compile("Comparaison of the formula")
    motif6=re.compile("looking at the formula with columns")
    motif7=re.compile("looking at the Benchmarks with columns")

    obj=motif.search(name)
    obj2=motif2.search(name)
    obj4=motif4.search(name)
    obj5=motif5.search(name)
    obj6=motif6.search(name)
    obj7=motif7.search(name)

    if obj:
        df_utilisation.loc[iterator, 'Ordre'] = iterator
        df_utilisation.loc[iterator, 'Name'] = name
        df_utilisation.loc[iterator, 'Type'] = "Input de formule"
    elif obj2:
        df_utilisation.loc[iterator, 'Ordre'] = iterator
        df_utilisation.loc[iterator, 'Name'] = name
        df_utilisation.loc[iterator, 'Type'] = "Prediction sensorielle"
    elif obj4:
        df_utilisation.loc[iterator, 'Ordre'] = iterator
        df_utilisation.loc[iterator, 'Name'] = name
        df_utilisation.loc[iterator, 'Type'] = "Simple analyse"
    elif obj5:
        df_utilisation.loc[iterator, 'Ordre'] = iterator
        df_utilisation.loc[iterator, 'Name'] = name
        df_utilisation.loc[iterator, 'Type'] = "Comparaison de formule"
    elif obj6:
        df_utilisation.loc[iterator, 'Ordre'] = iterator
        df_utilisation.loc[iterator, 'Name'] = name
        df_utilisation.loc[iterator, 'Type'] = "Recherche de formule"
    elif obj7:
        df_utilisation.loc[iterator, 'Ordre'] = iterator
        df_utilisation.loc[iterator, 'Name'] = name
        df_utilisation.loc[iterator, 'Type'] = "Recherche de Benchmark"

def utilisation_2(name,file):

    motif=re.compile("--------------")
    motif2=re.compile("Sensory Prediction of the formula")
    motif4=re.compile("Simple Analysis of the formula")
    motif5=re.compile("Comparaison of the formula")
    motif6=re.compile("looking at the formula with columns")
    motif7=re.compile("looking at the Benchmarks with columns")

    obj=motif.search(name)
    obj2=motif2.search(name)
    obj4=motif4.search(name)
    obj5=motif5.search(name)
    obj6=motif6.search(name)
    obj7=motif7.search(name)


    if obj:
        df_utilisation_2.loc[file, 'Formula Input'] +=1
    elif obj2:
        df_utilisation_2.loc[file, 'Sensory Prediction'] +=1
    elif obj4:
        df_utilisation_2.loc[file, 'Simple analyse']+=1
    elif obj5:
        df_utilisation_2.loc[file, 'Formulas Comparaison'] +=1
    elif obj6:
        df_utilisation_2.loc[file, 'Look for formula']+=1
    elif obj7:
        df_utilisation_2.loc[file, 'Look for Benchmark'] +=1

def utilisation_3(name,file,date,iteration):


    motif=re.compile("--------------")
    motif2=re.compile("Sensory Prediction of the formula")
    motif4=re.compile("Simple Analysis of the formula")
    motif5=re.compile("Comparaison of the formula")
    motif6=re.compile("looking at the formula with columns")
    motif7=re.compile("looking at the Benchmarks with columns")

    obj=motif.search(name)
    obj2=motif2.search(name)
    obj4=motif4.search(name)
    obj5=motif5.search(name)
    obj6=motif6.search(name)
    obj7=motif7.search(name)

    if obj:
        df_utilisation_3.loc[iteration, 'Number of used function'] +=1
        df_utilisation_3.loc[iteration, 'Date'] =date[iteration]
        df_utilisation_3.loc[iteration, 'Log Name'] =file
        df_utilisation_3.loc[iteration, 'Function'] = "Formula Input"
    elif obj2:
        df_utilisation_3.loc[iteration, 'Number of used function'] +=1
        df_utilisation_3.loc[iteration, 'Date'] =date[iteration]
        df_utilisation_3.loc[iteration, 'Log Name'] =file
        df_utilisation_3.loc[iteration, 'Function'] = "Sensory Prediction"
    elif obj4:
        df_utilisation_3.loc[iteration, 'Number of used function']+=1
        df_utilisation_3.loc[iteration, 'Date'] =date[iteration]
        df_utilisation_3.loc[iteration, 'Log Name'] =file
        df_utilisation_3.loc[iteration, 'Function'] = "Simple analyse"
    elif obj5:
        df_utilisation_3.loc[iteration, 'Number of used function'] +=1
        df_utilisation_3.loc[iteration, 'Date'] =date[iteration]
        df_utilisation_3.loc[iteration, 'Log Name'] =file
        df_utilisation_3.loc[iteration, 'Function'] = "Formulas Comparaison"
    elif obj6:
        df_utilisation_3.loc[iteration, 'Number of used function']+=1
        df_utilisation_3.loc[iteration, 'Date'] =date[iteration]
        df_utilisation_3.loc[iteration, 'Log Name'] =file
        df_utilisation_3.loc[iteration, 'Function'] = "Look for formula"
    elif obj7:
        df_utilisation_3.loc[iteration, 'Number of used function'] +=1
        df_utilisation_3.loc[iteration, 'Date'] =date[iteration]
        df_utilisation_3.loc[iteration, 'Log Name'] =file
        df_utilisation_3.loc[iteration, 'Function'] = "Look for Benchmark"
    else:
        df_utilisation_3.loc[iteration, 'Number of used function'] +=1
        df_utilisation_3.loc[iteration, 'Date'] =date[iteration]
        df_utilisation_3.loc[iteration, 'Log Name'] =file
        df_utilisation_3.loc[iteration, 'Function'] = "Nothing"

def categorie(iterator,name):

    motif=re.compile("--------------")
    motif2=re.compile("Sensory Prediction of the formula")
    motif3=re.compile("IPC manquant")
    motif4=re.compile("Simple Analysis of the formula")
    motif5=re.compile("Comparaison of the formula")
    motif6=re.compile("looking at the formula with columns")
    motif7=re.compile("looking at the Benchmarks with columns")

    obj=motif.search(name)
    obj2=motif2.search(name)
    obj3=motif3.search(name)
    obj4=motif4.search(name)
    obj5=motif5.search(name)
    obj6=motif6.search(name)
    obj7=motif7.search(name)


    if obj:
        df_screen.loc[iterator, 'Contenu'] = name
    elif obj2:
        df_sensory.loc[iterator, 'Contenu'] = name
    elif obj3:
        df_IPC.loc[iterator, 'Contenu'] = name
    elif obj4:
        df_analysis.loc[iterator, 'Contenu'] = name
    elif obj5:
        df_comparaison.loc[iterator, 'Contenu'] = name
    elif obj6:
        df_looking.loc[iterator, 'Contenu'] = name
    elif obj7:
        df_lookBench.loc[iterator, 'Contenu'] = name



load_image=  'url(https://www.actu-environnement.com/images/illustrations/news/32794_large.jpg'

app.layout = html.Div(children=[
    html.Div(' ',className='light',style={'margin-bottom':'20px','height':'180px','background-image':load_image}),
    html.Div(
        children=[
            html.Div((
                dcc.Store(id='file_list_drag',data=''),
                dcc.Store(id='drag_formula',data='',modified_timestamp=-1),
                dcc.Store(id='drag_formula_2',data='',modified_timestamp=-1),
                dcc.Store(id='drag_formula_name',data='',modified_timestamp=-1),

                dcc.Store(id='file_list_upload',data=''),
                dcc.Store(id='upload_formula',data='',modified_timestamp=-1),
                dcc.Store(id='upload_formula_2',data='',modified_timestamp=-1),
                dcc.Store(id='upload_formula_name',data='',modified_timestamp=-1),
                dcc.Store(id='upload_update',data='',modified_timestamp=-1),

                dcc.Store(id='current_formula',data=''),
                dcc.Store(id='current_formula_2',data=''),
                dcc.Store(id='current_formula_name',data=''),

                dcc.Store(id='clinic-list',data='No person yet'),
                dcc.Store(id='admit-list',data=[]),
                dcc.Store(id='deptname-list',data=None),
                dcc.Store(id='jobfamily-list',data=None),
                dcc.Store(id='position-list',data=None),


                html.Img(className='zoom',
                    src='https://image4.owler.com/logo/iff_owler_20191216_022622_original.png',
                    style={
                   'height': '13%',
                   'width': '13%'
                           }
                        ),
                html.H2("Welcome to the Logs Analytics Dashboard",className='shine',style={'color':'#0075C9','font-weight':'bold','border-style':'double','border-color':'#77b5fe','border-width':'7px'}),
                html.Hr(style={'color':'#0075C9'}),
                html.H3("Import files",style={'color':'#0075C9'}),
                dcc.Dropdown(
                    id='import',
                    options=[{"label": i, "value": i} for i in import_list],value=import_list[0],style={'marginLeft': '30%',"max-width": "40%",'textAlign': 'center'}
                ),
                html.Br(),
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(
                        ["Drag and drop or click to select a file to upload."]
                    ),
                    style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "0px",
                        },
                        multiple=True,
                ),
                html.Button("Upload files",id="button0",n_clicks=0, style = {'display':'None'}),

                html.Hr(style={'color':'#0075C9'}),
                html.H3("File List",style={'color':'#0075C9'}),
                html.Ul(id="file-list", style = {'padding-left' : '35%','padding-right':'35%','list-style-type':'circle'}),
                html.Hr(style={'color':'#0075C9'}),
                html.H3("Sort by",style={'color':'#0075C9'}),
                html.Div([
                    html.H6("Localisation"),
                    dcc.Dropdown(
                        id='deptname',
                        options=[{"label": i, "value": i} for i in df_deptname],value="All",style={'marginLeft': '15%',"max-width": "70%",'textAlign': 'center'}
                    ),
                    html.H6("Sector"),
                    dcc.Dropdown(
                        id='jobfamily',
                        options=[{"label": i, "value": i} for i in df_jobfamily],value="All",style={'marginLeft': '15%',"max-width": "70%",'textAlign': 'center'}
                    ),
                    html.H6("Job"),
                    dcc.Dropdown(
                        id='position',
                        options=[{"label": i, "value": i} for i in df_position],value="All",style={'marginLeft': '15%',"max-width": "70%",'textAlign': 'center'}
                    )
                ],style={'display':'block','margin-bottom':'20px'}),
                html.Hr(style={'color':'#0075C9'}),
                html.H3("Functions",style={'color':'#0075C9'}),
                html.Button("Used Functions",id="button1", className = 'launch-graph-button',n_clicks=0, style = {'margin-bottom' : '20px'}),
                html.Button("Uploaded Formulas",id="button2", className = 'launch-graph-button',n_clicks=0, style = {'margin-bottom' : '20px','marginLeft':'10px'}),
                html.Button("Missing IPC",id="button3", className = 'launch-graph-button',n_clicks=0, style = {'margin-bottom' : '20px','marginLeft':'10px'}),
                html.Button("Frequency of Used Functions",id="button4", className = 'launch-graph-button',n_clicks=0, style = {'margin-bottom' : '20px','marginLeft':'10px'}),
                html.Button("Volume of Analyzes per Person",id="button5", className = 'launch-graph-button',n_clicks=0, style = {'margin-bottom' : '20px','marginLeft':'10px'}),
                #function 1
                html.Label(dcc.Graph(id='function1', style = {'display' : 'none'})),
                #function 2
                html.Label(dash_table.DataTable(id='function2')),
                #function 3
                html.Label(dash_table.DataTable(id='function3')),
                #functon 4
                html.Label(dcc.Graph(id='function4', style = {'display' : 'none'})))),
            #function 5
            html.Div(id="function5",
                children=[
                    html.Div(
                        id="description-card",
                        children=[
                        html.H5("Logs Analytics"),
                        html.Div(
                            id="intro",
                            children="Explore how many function people use per day or per week and which functions they used.",
                                ),
                                 ],
                            ),
                    html.Div(
                        id="control-card",
                        children=[
                            html.P("Select Person"),
                            dcc.Dropdown(id="clinic-select",options=[{"label": i, "value": i} for i in ['']],value=['']),
                            html.Br(),
                            html.P("Select Time Interval"),
                            dcc.DatePickerRange(
                                id="date-picker-select",
                                start_date=dt(2020, 1, 1),
                                end_date=dt(2020, 1, 31),
                                min_date_allowed=dt(2020, 1, 1),
                                max_date_allowed=dt(2020, 12, 31),
                                initial_visible_month=dt(2020, 1, 1),
                            )]),
                    html.Div(id="control-card-2",
                        children=[
                            html.Br(),
                            html.Br(),
                            html.P("Select Functions"),
                            dcc.Dropdown(id="admit-select",options=[{"label": i, "value": i} for i in ['']],value=[''],multi=True),
                            html.Br()
                                ]
                            ),
                    html.Div(
                        id="reset-btn-outer",
                        children=html.Button(id="reset-btn", children="Reset", n_clicks=0,style={'margin-bottom':'20px','display':'none'}),
                            ),
            html.Div(
                id="patient_volume_card",
                children=[
                    html.B("Function Volume"),
                    html.Hr(),
                    dcc.Graph(id="patient_volume_hm",style ={'height':'500px'}),
                         ],
                    ),
                ],
                    style={"display": "none"},
            ),
            html.Hr(style={'color':'#0075C9'}),
                ],
            style={'marginLeft': '15%',"max-width": "70%",'textAlign': 'center'}
        )
    ]
)

class DashCallbackVariables:
    """Class to store information useful to callbacks"""

    def __init__(self):
        self.n_clicks = {1: 0, 2: 0, 3: 0, 4:0, 5:0,6:0}

    def update_n_clicks(self, nclicks, bt_num):
        self.n_clicks[bt_num] = nclicks

callbacks_vars = DashCallbackVariables()

@app.callback([
                Output('upload-data','style'),
                Output('button0','style')
              ],
              [
                Input('import','value')
              ]
              )

def import_files(import_value):
    style1={'display':'block','textAlign':'center','margin':'auto'}
    style2={'display':'None'}
    style3={
        "width": "100%",
        "height": "60px",
        "lineHeight": "60px",
        "borderWidth": "1px",
        "borderStyle": "dashed",
        "borderRadius": "5px",
        "textAlign": "center",
        "margin": "0px",
        }
    if import_value=="From anywhere":
        return style3,style2
    elif import_value=="From specific directory":
        return style2,style1
    else:
        return style2, style2

def parse_contents(contents, filename, df):
    _, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    try:
        if 'txt' in filename:
            # Assume that the user uploaded a CSV file
            df = df + decoded.decode("utf-8")

            return df

    except Exception as e:
        #print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

def parse_contents_2(contents, filename, df_2):
    _, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    try:
        if 'txt' in filename:
            # Assume that the user uploaded a CSV file
            #df_2.append(decoded.decode("utf-8"))

            return df_2 + [decoded.decode("utf-8")]

    except Exception as e:
        #print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

#Output('file-list', 'children'),
@app.callback([Output('drag_formula','data'),Output('drag_formula_2','data'),Output('drag_formula_name','data')],
              [Input('upload-data', 'contents')],
              [
              State('upload-data', 'filename')
              ])


def update_output(list_of_contents, list_of_names):

    df=''
    df_2=[]
    filename=[]
    if list_of_contents is not None:

        children =[parse_contents(c, n, df) for c, n in zip(list_of_contents, list_of_names)]
        children_2 =[parse_contents_2(c, n, df_2) for c, n in zip(list_of_contents, list_of_names)]
    if list_of_names is None:
        raise PreventUpdate
    elif len(list_of_names) == 0:
        raise PreventUpdate
    else:
        for filenames in list_of_names:
            filename.append(filenames)
        return children,children_2,filename

@app.callback([Output('upload_formula','data'),Output('upload_formula_2','data'),Output('upload_formula_name','data'),Output('upload_update','data')],
              [Input('button0', 'n_clicks')])


#coder le boutton
def update_output_upload(n_clicks):
    df_u=[]
    df_u_2=[]
    if int(n_clicks) != callbacks_vars.n_clicks[6]:
        callbacks_vars.update_n_clicks(n_clicks, 6)
        #n_clicks=0
        dirs=os.listdir('log files')
        for file in dirs:
            data=''
            with open('log files/'+file,'r') as l:
                for line in l:
                    data=data+l.read()+'\n'


                df_u=df_u+[data]

                df_u_2.append([data])
                l.close()


        return df_u,df_u_2,dirs,n_clicks
    else:
        raise PreventUpdate

@app.callback([
                Output('file-list', 'children'),
                Output('current_formula','data'),
                Output('current_formula_2','data'),
                Output('current_formula_name','data')],
              [
                Input('drag_formula','modified_timestamp'),
                Input('drag_formula_2','modified_timestamp'),
                Input('drag_formula_name','modified_timestamp'),
                Input('upload_formula','modified_timestamp'),
                Input('upload_formula_2','modified_timestamp'),
                Input('upload_formula_name','modified_timestamp'),
                Input('upload_update','modified_timestamp')
              ],
              [
                State('drag_formula','data'),
                State('drag_formula_2','data'),
                State('drag_formula_name','data'),
                State('upload_formula','data'),
                State('upload_formula_2','data'),
                State('upload_formula_name','data'),
                State('upload_update','data')
              ])



def update_out(ts1,ts2,ts3,ts4,ts5,ts6,ts7,children,children_2,filename,upload_children,upload_children_2,upload_filename,update_click):

    if ((ts1 ==-1 and ts2==-1 and ts3 ==-1) and (ts4 ==-1 and ts5 ==-1 and ts6 ==-1))or((ts1 !=-1 and ts2==-1 and ts3 ==-1) and (ts4 !=-1 and ts5 ==-1 and ts6 ==-1)) or ((ts1 !=-1 and ts2!=-1 and ts3 ==-1) and (ts4 !=-1 and ts5 !=-1 and ts6 ==-1)):

        raise PreventUpdate
    else:

        today = datetime.date.today()
        moment = datetime.datetime.now().time()
        now = datetime.datetime.combine(today, moment)
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta= now - epoch


        if (ts3>ts7):

            filenames=filename
            ts1=-1
            ts2=-1
            ts3=-1
            ts4=-1
            ts5=-1
            ts6=-1
            return [html.Li(file) for file in filenames],children,children_2,filenames
        elif (ts7>ts3):

            filenames=upload_filename
            ts1=-1
            ts2=-1
            ts3=-1
            ts4=-1
            ts5=-1
            ts6=-1
            return [html.Li(file) for file in filenames],upload_children,upload_children_2,filenames
        else:
            ts1=-1
            ts2=-1
            ts3=-1
            ts4=-1
            ts5=-1
            ts6=-1
            return [html.Li("No files yet!")],'',[],[]


@app.callback(
              [
                  Output('deptname', 'options'),
                  Output('deptname', 'value'),
              ],
              [Input('deptname-list', 'data')])

def deptname(deptname):

    options= [{"label": i, "value": i} for i in df_deptname]
    if deptname ==None:
        return options,None
    else:
        return options,df_deptname[0]

@app.callback(
              [
                  Output('jobfamily', 'options'),
                  Output('jobfamily', 'value'),
              ],
              [Input('jobfamily-list', 'data')])

def jobfamily(jobfamily):

    options= [{"label": i, "value": i} for i in df_jobfamily]
    if jobfamily ==None:
        return options,None
    else:
        return options,df_jobfamily[0]


@app.callback(
              [
                  Output('position', 'options'),
                  Output('position', 'value'),
              ],
              [Input('position-list', 'data')])

def position(position):

    options= [{"label": i, "value": i} for i in df_position]
    if position ==None:
        return options,None
    else:
        return options,df_dposition[0]





@app.callback(
              [
                  Output('function1', 'figure'),
                  Output('function1', 'style'),
                  Output('function2', 'columns'),
                  Output('function2', 'data'),
                  Output('function3', 'columns'),
                  Output('function3', 'data'),
                  Output('function4', 'figure'),
                  Output('function4', 'style'),
                  Output('function5', 'style'),
                  Output('clinic-list', 'data'),
                  Output('admit-list', 'data'),

              ],
              [
              Input('button1', 'n_clicks'),
              Input('button2', 'n_clicks'),
              Input('button3', 'n_clicks'),
              Input('button4', 'n_clicks'),
              Input('button5', 'n_clicks')
              ],
              [
              State('current_formula','data'),
              State('current_formula_2','data'),
              State('current_formula_name','data'),
              State('deptname','value'),
              State('jobfamily','value'),
              State('position','value')
              ])



def traitement(n_clicks,n_clicks_2,n_clicks_3,n_clicks_4,n_clicks_5,df,df_2,filename,deptname,jobfamily,position):


    if n_clicks is None:
        n_clicks = 0
    if n_clicks_2 is None:
        n_clicks_2 = 0
    if n_clicks_3 is None:
        n_clicks_3 = 0
    if n_clicks_4 is None:
        n_clicks_4 = 0
    if n_clicks_5 is None:
        n_clicks_5 = 0

    if n_clicks == 0 and n_clicks_2 == 0 and n_clicks_3 == 0 and n_clicks_4 == 0 and n_clicks_5 == 0:
        raise PreventUpdate ## TODO: import PreventUpdate
    b=0
    log_name=[]
    filename_id=[]
    df_id=[]
    df_2_id=[]
    for i,name in enumerate(filename):
        ajouter=True

        df_log_name.loc[i]=0
        for j,user in enumerate(df_ID_user):
            if user in name:
                df_log_name.loc[i]=df_data.iloc[df_data.loc[df_data['globaluserid']==user].index.item(),1]
        name_id=df_log_name.iloc[i,0]

        if not deptname==None:
            try:
                if not (deptname==df_data.iloc[df_data.loc[df_data['Name']==name_id].index.item(),2]):
                    #if not deptname==df_data.iloc[df_data.loc[df_data['Name']==name_id].index.item(),2] or not name_id==0:
                    ajouter=False

            except:
                try:
                    if name_id==0:
                        ajouter=False

                except:
                    pass

        if not jobfamily==None:
            try:
                if not (jobfamily==df_data.iloc[df_data.loc[df_data['Name']==name_id].index.item(),3]):
                    #if not deptname==df_data.iloc[df_data.loc[df_data['Name']==name_id].index.item(),2] or not name_id==0:
                    ajouter=False

            except:
                try:
                    if name_id==0:
                        ajouter=False

                except:
                    pass
        if not position==None:
            try:
                if not (position==df_data.iloc[df_data.loc[df_data['Name']==name_id].index.item(),4]):
                    #if not deptname==df_data.iloc[df_data.loc[df_data['Name']==name_id].index.item(),2] or not name_id==0:
                    ajouter=False

            except:
                try:
                    if name_id==0:
                        ajouter=False

                except:
                    pass
        if ajouter==True:
            if name_id != 0:
                filename_id.append(name_id)
            else:
                filename_id.append(filename[i])

            df_id.append(df[i])
            df_2_id.append(df_2[i])

    dateparse =('%d/%m/%Y %H:%M:%S: ')
    date=[]
    listofcontenu=[]
    contenu=[]
    #AttributeError: 'list' object has no attribute 'split'

    df_id= '\n'.join(df_id).split('\n')
    for line in df_id :
        match=re.search(r'\d{2}/\d{2}/\d{4}', line)
        if (match):
            ladate = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()
            date.append(ladate)

            listofcontenu.append(contenu)
            contenu=[":".join(line.split(":")[3:])]

        else:
            contenu.append(line)
    listofcontenu.append(contenu)
    listofcontenu.pop(0)

    ar = np.array(listofcontenu)
    data = pd.DataFrame(ar, index = date, columns = ['Contenu'])


    df_screen.drop(df_screen.index, inplace=True)
    df_sensory.drop(df_sensory.index, inplace=True)
    df_IPC.drop(df_IPC.index, inplace=True)
    df_analysis.drop(df_analysis.index, inplace=True)
    df_comparaison.drop(df_comparaison.index, inplace=True)
    df_looking.drop(df_looking.index, inplace=True)
    df_lookBench.drop(df_lookBench.index, inplace=True)
    for iterator,x in enumerate(data['Contenu']):
        x=" ".join(x)
        categorie(iterator,x)
    #if n_clicks>0 :
    if n_clicks != callbacks_vars.n_clicks[1]:
        callbacks_vars.update_n_clicks(n_clicks, 1)
        style = {'display' : 'block', 'height' : '500px','width':'100%'}
        n_clicks=0


        df_utilisation.drop(df_utilisation.index, inplace=True)


        for iterator,x in enumerate(data['Contenu']):
            x=" ".join(x)
            utilisation(iterator,x)


        a=0
        b=0
        c=0
        d=0
        e=0
        f=0

        for iterator,x in enumerate(df_utilisation['Type']):
            if "Input de formule" in x:
                a=a+1
            elif "Prediction sensorielle" in x:
                b=b+1
            elif "Simple analyse" in x:
                c=c+1
            elif "Comparaison de formule" in x:
                d=d+1
            elif "Recherche de formule" in x:
                e=e+1
            elif "Recherche de Benchmark" in x:
                f=f+1

        df_nb_utilisation.loc[0, 'Name'] = "Formula Imput"
        df_nb_utilisation.loc[1, 'Name'] = "Sensory Prediction"
        df_nb_utilisation.loc[2, 'Name'] = "Simple analyse"
        df_nb_utilisation.loc[3, 'Name'] = "Formulas Comparaison"
        df_nb_utilisation.loc[4, 'Name'] = "Look for formula"
        df_nb_utilisation.loc[5, 'Name'] = "Look for Benchmark"

        df_nb_utilisation.loc[0, 'Number'] = a
        df_nb_utilisation.loc[1, 'Number'] = b
        df_nb_utilisation.loc[2, 'Number'] = c
        df_nb_utilisation.loc[3, 'Number'] = d
        df_nb_utilisation.loc[4, 'Number'] = e
        df_nb_utilisation.loc[5, 'Number'] = f

        random_x = df_nb_utilisation['Name']
        random_y = df_nb_utilisation['Number']



        figure = {
            'data': [
                {'x':random_x, 'y':random_y, 'type':'bar', 'name': 'Series1'}
            ],
            'layout': {
                'title': 'List of functions the most used',
                 'yaxis':{'title': 'Frequency'},
            },

        }

        style2={'display':'none'}


        return figure, style,[],[],[],[],{},style2,style2,['No One'],[]

    if int(n_clicks_2) != callbacks_vars.n_clicks[2]:

        callbacks_vars.update_n_clicks(n_clicks_2, 2)
        n_clicks_2=0


        #df_comp : comparaison des formules
        df_comp = pd.DataFrame(columns=['Name','IPC','Type'])
        liste=[]
        t=0
        for iterator,x in enumerate(df_comparaison['Contenu']):
            name=":".join(x.split(":")[1:]).strip()
            for i in name.split(","):
                t=t+1
                df_comp.loc[t, 'Name'] = i
                try:
                    IPC_debut=re.search(u'CPA', name).start()
                    df_comp.loc[t, 'IPC'] = i[IPC_debut:IPC_debut+8]
                    df_comp.loc[t, 'Type'] = 'CPA'
                except:
                    try:
                        IPC_debut=re.search(u'30F', name).start()
                        df_comp.loc[t, 'IPC'] = i[IPC_debut:IPC_debut+8]
                        df_comp.loc[t, 'Type'] = 'Parfumeur'
                    except:
                        df_comp.loc[iterator, 'IPC'] = 'Aucun'
                        df_comp.loc[iterator, 'Type'] = 'Aucun'

        df_comp=df_comp.dropna()
        df_test=df_comp['Name'].value_counts()
        df_test = df_test.reset_index()
        df_test.rename(columns = {'index' : 'Most Frequently Formula name', 'Name' : 'Frequency'}, inplace = True)
        columns = [{'name' : col, 'id': col} for col in df_test.columns]
        data = df_test.to_dict('records')

        style2={'display':'none'}
        style={'display':'block'}

        return {}, style2,columns,data,[],[],{},style2,style2,['No One'],[]


    if int(n_clicks_3) != callbacks_vars.n_clicks[3]:

        callbacks_vars.update_n_clicks(n_clicks_3, 3)
        n_clicks_3=0
        #---------------------- Analyse 5: récuperer les IPC manquant --------------------
        list_enlever= 'IPC manquant:'
        df_IPC_data = pd.DataFrame(columns=['IPC missing','Frequency'])
        for iterator,x in enumerate(list(df_IPC['Contenu'])):
            contenu=''.join(x)
            #for val in list_enlever :
            contenu2=contenu.replace(list_enlever,'')
            contenu3=contenu2.replace('\n','')
            contenu4=contenu3.replace(' ','')
            df_IPC_data.loc[iterator,'IPC missing']=contenu4
            df_IPC_data.loc[iterator,'Frequency']=1

        df_IPC_data = df_IPC_data.groupby(by = 'IPC missing', as_index = False).sum()
        df_IPC_data.sort_values(by = 'Frequency', ascending = False, inplace = True)

        columns_IPC = [{'name' : col, 'id': col} for col in df_IPC_data.columns]
        data_IPC = df_IPC_data.to_dict('records')
        style2={'display':'none'}
        style={'display':'block'}
        return {}, style2,[],[],columns_IPC,data_IPC,{},style2,style2,['No One'],[]

    #if n_clicks_4>0 :
    if int(n_clicks_4) != callbacks_vars.n_clicks[4]:

        callbacks_vars.update_n_clicks(n_clicks_4, 4)
        style = {'display' : 'block', 'height' : '500px','width':'100%'}
        n_clicks_4=0
        df_2_update=[]


        dateparse =('%d/%m/%Y %H:%M:%S: ')
        date=[]
        #listofcontenu=[]
        contenu=[]

        for i in range(0,len(df_2_id)):
            lines=df_2_id[i]
            listofcontenu=[]
            lines= '\n'.join(lines).split('\n')

            for line in lines:
                match=re.search(r'\d{2}/\d{2}/\d{4}', line)
                if (match):
                    #ladate = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()
                    #date.append(ladate)

                    listofcontenu.append(contenu)
                    contenu=[":".join(line.split(":")[3:])]
                else:
                    contenu.append(line)
            listofcontenu.append(contenu)
            listofcontenu.pop(0)
            df_2_update.append(listofcontenu)

        df_utilisation_2.drop(index = df_utilisation_2.index,inplace=True)

        for i in range(0,len(df_2_update)):

            df_utilisation_2.loc[filename_id[i]] = 0

            for iterator,x in enumerate(df_2_update[i]):
                x=" ".join(x)
                utilisation_2(x,filename_id[i])

        trace1 = go.Bar(x=df_utilisation_2.index, y=df_utilisation_2[('Formula Input')], name='Formula Input')
        trace2 = go.Bar(x=df_utilisation_2.index, y=df_utilisation_2[('Sensory Prediction')], name='Sensory Prediction')
        trace3 = go.Bar(x=df_utilisation_2.index, y=df_utilisation_2[('Simple analyse')], name='Simple analyse')
        trace4 = go.Bar(x=df_utilisation_2.index, y=df_utilisation_2[('Formulas Comparaison')], name='Formulas Comparaison')
        trace5 = go.Bar(x=df_utilisation_2.index, y=df_utilisation_2[('Look for formula')], name='Look for formula')
        trace6 = go.Bar(x=df_utilisation_2.index, y=df_utilisation_2[('Look for Benchmark')], name='Look for Benchmark')
        figure={
            'data': [trace1, trace2, trace3, trace4, trace5, trace6],
            'layout':
            go.Layout(title='Frequency of used fonction by log', barmode='stack')
        }
        style2={'display':'none'}
        return {}, style2,[],[],[],[],figure,style,style2,['No One'],[]


    if int(n_clicks_5) != callbacks_vars.n_clicks[5]:
        callbacks_vars.update_n_clicks(n_clicks_5, 5)
        n_clicks_5=0
        style = {'display' : 'block','width':'100%'   }
        style2={'display' : 'none'}
        df_2_update=[]


        dateparse =('%d/%m/%Y %H:%M:%S: ')
        date=[]
        #listofcontenu=[]
        contenu=[]
        df_utilisation_3.drop(index = df_utilisation_3.index,inplace=True)
        for i in range(0,len(df_2_id)):
            lines=df_2_id[i]
            listofcontenu=[]
            lines= '\n'.join(lines).split('\n')

            for line in lines:
                match=re.search(r'[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)

                if (match):
                    ladate = line[:19]
                    date.append(ladate)

                    listofcontenu.append(contenu)
                    contenu=[":".join(line.split(":")[3:])]
                else:
                    contenu.append(line)
            listofcontenu.append(contenu)
            listofcontenu.pop(0)
            df_2_update.append(listofcontenu)
        d=0

        for i in range(0,len(df_2_update)):
            for iterator,x in enumerate(df_2_update[i]):
                x=" ".join(x)
                df_utilisation_3.loc[d] = 0
                utilisation_3(x,filename_id[i],date,d)
                d=d+1

        clinic_list = df_utilisation_3["Log Name"].unique()
        df_utilisation_3["Function"] = df_utilisation_3["Function"].fillna("Not Identified")
        admit_list = df_utilisation_3["Function"].unique().tolist()

        if clinic_list.size==0:
            clinic_list="No person yet"


        return {}, style2,[],[],[],[],{},style2,style,clinic_list,admit_list

@app.callback(
              [
                  Output('clinic-select', 'options'),
                  Output('clinic-select', 'value'),
              ],
              [Input('clinic-list', 'data')])



def clinic_list(clinic_list):
    if clinic_list =="No person yet":
        return [],''
    else:
        options= [{"label": i, "value": i} for i in clinic_list]
        return options,clinic_list[0]





@app.callback(
              [
                  Output('admit-select', 'options'),
                  Output('admit-select', 'value'),
              ],
              [Input('admit-list', 'data')])

def admit_list(admit_list):
    options= [{"label": i, "value": i} for i in admit_list]
    return options,admit_list




def generate_patient_volume_heatmap(start, end, clinic, hm_click, admit_type, reset):
    """
    :param: start: start date from selection.
    :param: end: end date from selection.
    :param: clinic: clinic from selection.
    :param: hm_click: clickData from heatmap.
    :param: admit_type: admission type from selection.
    :param: reset (boolean): reset heatmap graph if True.
    :return: Patient volume annotated heatmap.
    """
    # Date ,df_utilisation_3["Function"],df_utilisation_3["Log Name"],df_utilisation_3["Number of used function"]
    #,df_utilisation_3_1,df_utilisation_3_2,df_utilisation_3_3



    df= pd.DataFrame(columns=['Days of Wk','Function','Date','Log Name','Number of used function','check-in-hour'])
    # Format checkin Time

    for i,line in enumerate(df_utilisation_3['Date']):
        df.loc[i]=0
        df.loc[i,"Date"]=line


    #df['Date']=df_utilisation_3['Date']
    df['Function']=df_utilisation_3['Function']
    df['Log Name']=df_utilisation_3['Log Name']
    df['Number of used function']=df_utilisation_3['Number of used function']

    df["Date"] = df["Date"].apply(
    lambda x: dt.strptime(x, "%d/%m/%Y %H:%M:%S")
    )  # String -> Datetime


    df["Days of Wk"] = df['check-in-hour']= df["Date"]


    # Insert weekday and hour of checkin time

    df["Days of Wk"] = df["Days of Wk"].apply(
    lambda x: dt.strftime(x, "%A")
    )  # Datetime -> weekday string

    df['check-in-hour'] = df['check-in-hour'].apply(
    lambda x: dt.strftime(x, "%I %p")
    )  # Datetime -> int(hour) + AM/PM

    try:
        filtered_df = df[
            (df["Log Name"] == clinic) & (df["Function"].isin(admit_type))
        ]

    except Exception as e:

        return {}
    filtered_df = filtered_df.sort_values("Date").set_index("Date")[
        start:end
    ]




    x_axis = [datetime.time(i).strftime("%I %p") for i in range(24)]  # 24hr time list
    y_axis = day_list

    hour_of_day = ""
    weekday = ""
    shapes = []


    if hm_click is not None:

        hour_of_day = hm_click["points"][0]["x"]
        weekday = hm_click["points"][0]["y"]

        # Add shapes
        x0 = x_axis.index(hour_of_day) / 24
        x1 = x0 + 1 / 24
        y0 = y_axis.index(weekday) / 7
        y1 = y0 + 1 / 7

        shapes = [
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=x0,
                x1=x1,
                y0=y0,
                y1=y1,
                line=dict(color="#ff6347"),
            )
        ]

    # Get z value : sum(number of records) based on x, y,

    z = np.zeros((7, 24))
    annotations = []


    for ind_y, day in enumerate(y_axis):
        filtered_day = filtered_df[filtered_df["Days of Wk"] == day]
        for ind_x, x_val in enumerate(x_axis):
            sum_of_record = filtered_day[filtered_day["check-in-hour"] == x_val][
                "Number of used function"
            ].sum()
            z[ind_y][ind_x] = sum_of_record

            annotation_dict = dict(
                showarrow=False,
                text="<b>" + str(sum_of_record) + "<b>",
                xref="x",
                yref="y",
                x=x_val,
                y=day,
                font=dict(family="sans-serif"),
            )
            # Highlight annotation text by self-click
            if x_val == hour_of_day and day == weekday:
                if not reset:
                    annotation_dict.update(size=15, font=dict(color="#ff6347"))

            annotations.append(annotation_dict)


    # Heatmap
    hovertemplate = "<b> %{y}  %{x} <br><br> %{z} Function Records"


    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=z,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=False,
            colorscale=[[0, "#caf3ff"], [1, "#2c82ff"]],
        )
    ]

    layout = dict(
        margin=dict(l=70, b=50, t=50, r=50),
        modebar={"orientation": "v"},
        font=dict(family="Open Sans"),
        annotations=annotations,
        shapes=shapes,
        xaxis=dict(
            side="top",
            ticks="",
            ticklen=2,
            tickfont=dict(family="sans-serif"),
            tickcolor="#ffffff",
        ),
        yaxis=dict(
            side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" "
        ),
        hovermode="closest",
        showlegend=False,
    )



    return {"data": data, "layout": layout}

#admit-select a remettre en input et pas en state ou cas ou
@app.callback(
    Output("patient_volume_hm", "figure"),
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("clinic-select", "value"),
        Input("patient_volume_hm", "clickData"),
        Input("reset-btn", "n_clicks"),
        Input("admit-select", "value")
    ]

)

def update_heatmap(start, end, clinic, hm_click,  reset_click,admit_type):

    start = start.replace('T',' ')
    end = end.replace('T',' ')

    reset = False
    # Find which one has been triggered
    ctx = dash.callback_context
    """
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "reset-btn":
            reset = True
    """

    # Return to original hm(no colored annotation) by resetting

    return generate_patient_volume_heatmap(
        start, end, clinic, hm_click, admit_type, reset
    )


if __name__ == "__main__":
    app.run_server(debug=True)
