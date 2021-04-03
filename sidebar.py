import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import date
import pandas as pd

import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from datetime import date
import dash
import dash_html_components as html
import dash_core_components as dcc
import re
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
import datetime
import pandas as pd


df = pd.read_excel(r'D:\STUDY MATERIAL\finaldashboard - Copy\data.xlsx',sheet_name = 'Sheet2')
df['Start Month']=df['Start Date'].dt.month
df['End Month']=df['End Date'].dt.month
df['End Year']=df['End Date'].dt.year
df['Start Year']=df['Start Date'].dt.year

#-----------email and issue file
df1 = pd.read_excel(r'D:\STUDY MATERIAL\finaldashboard - Copy\data.xlsx',sheet_name = 'Sheet3')
df100 = df1
# -----------------------
df100['upcoming_meeting_date'] = df100['Meeting Date'].shift(periods=-1)
df100['days_between_meeting']=df100['upcoming_meeting_date']-df100['Meeting Date']
df100['firstcount']=(df100['Emails to D']+df100['Email to O']+df100['Email to GC']+df100['PlanGrid']+df100['Unifier'])
df100['secondcount']=df100['firstcount'].shift(periods=1)
df100['days_between_meeting']=df100['days_between_meeting'].astype('str')
def func1(x):
    x=x[:2]
    return x
df100['num_of_days']=df100.apply(lambda x: func1(x['days_between_meeting']), axis=1)
df100['num_of_days']=df100['num_of_days'].replace('Na',0)
df100['secondcount']=df100['secondcount'].fillna(0)
df100['secondcount']=df100['secondcount'].astype('int')
df100['num_of_days']=df100['num_of_days'].astype('int')
df100['dv']=(df100['firstcount']-df100['secondcount'])/df100['num_of_days']
df100['dv']=df100['dv'].replace(df100['dv'][0],0)
df100['sum_of_issues']=(df100['Issues to O']+df100['Issues to GC']+df100['Issues to D'])
df100['sum_of_issues']=df100['sum_of_issues'].fillna(0)
df100['sum_of_issues']=df100['sum_of_issues'].astype('int')
df100['sum_of_issues_second_meet']=df100['sum_of_issues'].shift(periods=1)
df100['WIP']=(df100['sum_of_issues']-df100['sum_of_issues_second_meet'])
df100['WIP']=df100['WIP'].fillna(0)
df100['Month']=df100['Meeting Date'].dt.month
df1001=df100[['Meeting Date','upcoming_meeting_date','dv','WIP','Month']]

# --------------------------

df1  = df1.rename(columns={'Issues to D':'Email to D Issues', 'Issues to O':'Email to O Issues','Issues to GC':'Email to GC Issues','Emails to D':'Email to D'})
df1['Start Date'] = df1['Meeting Date']
df5 = df.merge(df1, how='inner', on='Start Date')
abc = df5
group = df5.groupby(['Description','Responsible Party','Start Date','End Date','Days to Complete','Start Year','Start Month','End Year','End Month'])[['Email to D','Email to D Issues','Email to O','Email to O Issues','Email to GC','Email to GC Issues']].sum().reset_index()


#-----------type of issues-----------------

df15 = pd.read_excel(r'D:\STUDY MATERIAL\finaldashboard - Copy\data1.xlsx',sheet_name='Types of Issues')
df16=df15[['Recirpocal']]
df16=df16.dropna()
df16['name']='Recirpocal'
df16.columns=['Description', 'name']
df17=df15[['Pooled']]
df17=df17.dropna()
df17['name']='Pooled'
df17.columns=['Description', 'name']
df18=df15[['Intensive']]
df18=df18.dropna()
df18['name']='Intensive'
df18.columns=['Description', 'name']
df19=df15[['Sequential']]
df19=df19.dropna()
df19['name']='Sequential'
df19.columns=['Description', 'name']
df20 =pd.concat([df16,df17,df18,df19],axis=0)
df19.columns=['Description', 'name']
df21=df.merge(df16,how = 'inner',on='Description')
df22=df.merge(df17,how = 'inner',on='Description')
df23=df.merge(df18,how = 'inner',on='Description')
df24=df.merge(df19,how = 'inner',on='Description')
df26 = pd.concat([df21,df22,df23,df24],axis=0)
df27=df26.groupby(['name','Start Month','Responsible Party', 'End Month'])[['Description']].count().reset_index()
print(df27.head(1))


external_stylesheets = 'bootstrap.css'

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


layout_1 = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.I('Start Year'),
            dcc.Dropdown(id='input1', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in sorted(group['Start Year'].unique())])],width={'size':2}),

        dbc.Col([
            html.I('Start Month'),
            dcc.Dropdown(id='input2', multi=False, value=1,options=[{'label':x, 'value':x}
                                  for x in sorted(group['Start Month'].unique())])],width={'size':2}),

        dbc.Col([
            html.I('End Year'),
            dcc.Dropdown(id='input3', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in sorted(group['End Year'].unique())]
                )],width={'size':2}),

        dbc.Col([
            html.I('End Month'),
            dcc.Dropdown(id='input4', multi=False, value=1,options=[{'label':x, 'value':x}
                                  for x in sorted(group['End Month'].unique())])],width={'size':2}),


        ],style = {"padding": "2rem 0rem"}),
    dbc.Row([
        dbc.Col([dcc.Loading(dcc.Graph(id='output', figure={},style = {"border":"10px groove"}  ,)),],width={'size':12})

        ])],style = {"padding": "2rem 0rem"}  )


layout2 = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.I('Start Year'),
            dcc.Dropdown(id='input1', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in sorted(group['Start Year'].unique())])],width={'size':2}),

        dbc.Col([
            html.I('Start Month'),
            dcc.Dropdown(id='input2', multi=False, value=1,options=[{'label':x, 'value':x}
                                  for x in sorted(group['Start Month'].unique())])],width={'size':2}),

        dbc.Col([
            html.I('End Year'),
            dcc.Dropdown(id='input3', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in sorted(group['End Year'].unique())]
                )],width={'size':2}),

        dbc.Col([
            html.I('End Month'),
            dcc.Dropdown(id='input4', multi=False, value=1,options=[{'label':x, 'value':x}
                                  for x in sorted(group['End Month'].unique())])],width={'size':2}),


        ],style = {"padding": "2rem 0rem"}),
    # dbc.Row([
    #     dbc.Col([dcc.Loading(dcc.Graph(id='output', figure={},style = {"border":"10px groove"}  ,)),],width={'size':12})

    #     ]),

    dbc.Row([
        dbc.Col([dcc.Loading(dcc.Graph(id='output5', figure={},style = {"border":"10px groove"}  ,)),],width={'size':12})

        ])])


layout3 = dbc.Container([
   
    dbc.Row([
        dbc.Col([
            html.I('Meeting Month'),
            dcc.Dropdown(id='input5', multi=False, value=2,options=[{'label':x, 'value':x}
                                  for x in sorted(group['Start Month'].unique())])],width={'size':2}),
        ],style = {"padding": "2rem 0rem"}),

    dbc.Row([
        
        dbc.Col([dcc.Loading(dcc.Graph(id='output3', figure={},style = {"border":"10px groove"}  ,)),],width={'size':6}),
        dbc.Col([dcc.Loading(dcc.Graph(id='output4', figure={},style = {"border":"10px groove"}  ,)),],width={'size':6})

        ])

    ])

navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("☰", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
        # dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("More pages", header=True),
        #         dbc.DropdownMenuItem("Page 2", href="#"),
        #         dbc.DropdownMenuItem("Page 3", href="#"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="More",
        # ),
    ],
    brand="Bottelneck Dectection tool",
    brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
)

layout4 = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.I('Start Year'),
            dcc.Dropdown(id='input1', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in sorted(group['Start Year'].unique())])],width={'size':2}),

        dbc.Col([
            html.I('Start Month'),
            dcc.Dropdown(id='input2', multi=False, value=1,options=[{'label':x, 'value':x}
                                  for x in sorted(group['Start Month'].unique())])],width={'size':2}),

        dbc.Col([
            html.I('End Year'),
            dcc.Dropdown(id='input3', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in sorted(group['End Year'].unique())]
                )],width={'size':2}),

        dbc.Col([
            html.I('End Month'),
            dcc.Dropdown(id='input4', multi=False, value=1,options=[{'label':x, 'value':x}
                                  for x in sorted(group['End Month'].unique())])],width={'size':2}),


        ],style = {"padding": "2rem 0rem"}),
    

    dbc.Row([
        dbc.Col([dcc.Loading(dcc.Graph(id='output1', figure={},style = {"border":"10px groove"}  ,)),],width={'size':6}),
        dbc.Col([dcc.Loading(dcc.Graph(id='output2', figure={},style = {"border":"10px groove"}  ,)),],width={'size':6})

        ])
   

    ])



# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "17rem",
    "margin-right": "1rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "1rem",
    "margin-right": "1rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
}

date =date.today()
sidebar = html.Div(
    [
        # html.H2("Sidebar", className="display-4"),
        html.I('Date :: {}'.format(date)),
        html.Hr(),
        # html.P(
        #     "A simple sidebar layout with navigation links", className="lead"
        # ),
        dbc.Nav(
            [
                dbc.NavLink("Information Trend", href="/page-1", id="page-1-link"),
                dbc.NavLink("Issue Report", href="/page-2", id="page-2-link"),
                dbc.NavLink("WIP & DV", href="/page-3", id="page-3-link"),
                dbc.NavLink("Avg Days to Complete & Productivity", href="/page-4", id="page-4-link"),
                # dbc.NavLink("WIP", href="/page-3", id="page-5-link"),
                # dbc.NavLink("DV", href="/page-3", id="page-6-link"),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(

    id="page-content",
    style=CONTENT_STYLE)

app.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
)


@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return [layout_1]
    elif pathname == "/page-2":
        return [layout2]
    elif pathname == "/page-3":
        return [layout3]
    elif pathname == "/page-4":
        return [layout4]    
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )



@app.callback(
    Output("output", "figure"),
    Input("input1", "value"),
    Input("input2", "value"),
    Input("input3", "value"),
    Input("input4", "value"),
)   
def func(start_year,start_month,end_year,end_month):
    df = group[(group['Start Year']==start_year)&(group['End Year']==end_year)&(group['Start Month']==start_month)&(group['End Month']==end_month)]
    dff =pd.melt(df, id_vars=['Description','Responsible Party','Start Year','Start Month','End Year','End Month','Start Date','End Date','Days to Complete'], var_name=[('Email to D','Email to D Issues','Email to O','Email to O Issues','Email to GC','Email to GC Issues')], value_name='value')
    dff.columns = ['Description','Responsible Party','Start Year','Start Month','End Year','End Month','Start Date','End Date','Days to Complete','colnames','value']
    dff=dff.groupby(['Description','Responsible Party','Start Month','End Month','Start Year','End Year','colnames'])[['value']].sum().reset_index()
    return px.bar(dff, x='colnames', y='value',template = 'plotly_dark',color='Description',title='Information Trend', height=480)\
    .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5)       

@app.callback(
    Output("output5", "figure"),
    Input("input2", "value"),
    Input("input4", "value"),
)
def func1011(startmonth,endmonth):
    df28=df27[(df27['Start Month']==startmonth)&(df27['End Month']==endmonth)]
    return px.bar(df28, x='name', y='Description',color = 'Responsible Party',template = 'plotly_dark',title='Issue Report', height=480)\
    .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5)

@app.callback(
    Output("output3", "figure"),
    Input("input5", "value"),
)
def func100(month):
    df12=df1001[df1001['Month']==month]
    return px.bar(df12, x='Meeting Date', y='WIP',color = 'Meeting Date',template = 'plotly_dark',title='WIP', height=480)\
    .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5)

@app.callback(
    Output("output4", "figure"),
    Input("input5", "value"),
)
def dv(month):
    df12=df1001[df1001['Month']==month]
    return px.bar(df12, x='Meeting Date', y='dv',color = 'Meeting Date',template = 'plotly_dark',title='DV', height=480)\
    .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5)


@app.callback(
    Output("output1", "figure"),
    Input("input1", "value"),
    Input("input2", "value"),
    Input("input3", "value"),
    Input("input4", "value"),
)   
def func1(start_year,start_month,end_year,end_month):
    owner = abc[(abc['Responsible Party']=='O')&(abc['Start Year']==start_year)&(abc['End Year']==end_year)&(abc['Start Month']==start_month)&(abc['End Month']==end_month)]
    owner=owner[['Responsible Party','Email to O','Email to O Issues','Days to Complete']]
    owner['average_days_to_complete']=owner['Days to Complete'].mean()
    owner['total_email']=owner['Email to O'].sum()
    owner['email']=owner['Email to O Issues'].sum()
    owner['productivity'] = (owner['email']/owner['total_email'])*100
    owner  =owner[['Responsible Party','total_email','productivity','average_days_to_complete']]
    owner=owner[0:1]
    gc = abc[(abc['Responsible Party']=='GC')&(abc['Start Year']==start_year)&(abc['End Year']==end_year)&(abc['Start Month']==start_month)&(abc['End Month']==end_month)]
    gc=gc[['Responsible Party','Email to GC','Email to GC Issues','Days to Complete']]
    gc['average_days_to_complete']=gc['Days to Complete'].mean()
    gc['total_email']=gc['Email to GC'].sum()
    gc['email']=gc['Email to GC Issues'].sum()
    gc['productivity'] = (gc['email']/gc['total_email'])*100
    gc  =gc[['Responsible Party','total_email','productivity','average_days_to_complete']]
    gc=gc[0:1]
    d = abc[(abc['Responsible Party']=='D')&(abc['Start Year']==start_year)&(abc['End Year']==end_year)&(abc['Start Month']==start_month)&(abc['End Month']==end_month)]
    d=d[['Responsible Party','Email to D','Email to D Issues','Days to Complete']]
    d['average_days_to_complete']=d['Days to Complete'].mean()
    d['total_email']=d['Email to D'].sum()
    d['email']=d['Email to D Issues'].sum()
    d['productivity'] = (d['email']/d['total_email'])*100
    d  =d[['Responsible Party','total_email','productivity','average_days_to_complete']]
    d=d[0:1]
    frames = [owner, d, gc]
    result = pd.concat(frames)
    pie_fig = px.pie(result, names=result['Responsible Party'], values='average_days_to_complete' ,height = 480,hole = .3,template = 'plotly_dark',color = 'Responsible Party' , title='Average Days to Complete')\
            .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5).update_traces(textposition='inside',  textinfo='label+percent+value')
    return pie_fig



@app.callback(
    Output("output2", "figure"),
    Input("input1", "value"),
    Input("input2", "value"),
    Input("input3", "value"),
    Input("input4", "value"),
)
def func3(start_year,start_month,end_year,end_month):
    owner1 = abc[(abc['Responsible Party']=='O')&(abc['Start Year']==start_year)&(abc['End Year']==end_year)&(abc['Start Month']==start_month)&(abc['End Month']==end_month)]
    owner1=owner1[['Responsible Party','Email to O','Email to O Issues','Days to Complete']]
    owner1['average_days_to_complete']=owner1['Days to Complete'].mean()
    owner1['total_email']=owner1['Email to O'].sum()
    owner1['email']=owner1['Email to O Issues'].sum()
    owner1['productivity'] = (owner1['email']/owner1['total_email'])*100
    owner1  =owner1[['Responsible Party','total_email','productivity','average_days_to_complete']]
    owner1=owner1[0:1]
    gc1 = abc[(abc['Responsible Party']=='GC')&(abc['Start Year']==start_year)&(abc['End Year']==end_year)&(abc['Start Month']==start_month)&(abc['End Month']==end_month)]
    gc1=gc1[['Responsible Party','Email to GC','Email to GC Issues','Days to Complete']]
    gc1['average_days_to_complete']=gc1['Days to Complete'].mean()
    gc1['total_email']=gc1['Email to GC'].sum()
    gc1['email']=gc1['Email to GC Issues'].sum()
    gc1['productivity'] = (gc1['email']/gc1['total_email'])*100
    gc1  =gc1[['Responsible Party','total_email','productivity','average_days_to_complete']]
    gc1=gc1[0:1]
    d1 = abc[(abc['Responsible Party']=='D')&(abc['Start Year']==start_year)&(abc['End Year']==end_year)&(abc['Start Month']==start_month)&(abc['End Month']==end_month)]
    d1=d1[['Responsible Party','Email to D','Email to D Issues','Days to Complete']]
    d1['average_days_to_complete']=d1['Days to Complete'].mean()
    d1['total_email']=d1['Email to D'].sum()
    d1['email']=d1['Email to D Issues'].sum()
    d1['productivity'] = (d1['email']/d1['total_email'])*100
    d1  =d1[['Responsible Party','total_email','productivity','average_days_to_complete']]
    d1=d1[0:1]
    frames = [owner1, d1, gc1]
    result = pd.concat(frames)
    pie_fig = px.pie(result, names=result['Responsible Party'], values='productivity' ,height = 480,hole = .3,template = 'plotly_dark',color = 'Responsible Party' , title='Productivity')\
            .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5).update_traces(textposition='inside',  textinfo='label+percent+value')
    return pie_fig
   
   

if __name__ == "__main__":
    app.run_server(debug=True, port=8086,dev_tools_ui=False)