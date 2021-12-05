import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input,Output
from dash import callback_context
import dash_table as dt
from dash_extensions import Download
from dash.exceptions import PreventUpdate



#Read in the data and set the style
url = 'cube.csv'
df1 = pd.read_csv(url)

external_stylesheets = [dbc.themes.BOOTSTRAP]
colorsequence = ['#DB0011','#9FA1A4','#000000','#f2c0c4','#4D4D4D']
graphstylel = {
            'margin-left':'7px'
            }

graphstyler = {
            'margin-right':'7px'
            }


#Build the dictionaries

markets = df1['Market'].unique()
markets.sort()
marketdict = [{'label' : i, 'value' : i } for i in markets]

propositions = df1['Proposition'].unique()
propositions.sort()
propositiondict = [{'label' : i, 'value' : i } for i in propositions]

primary = df1['Primary'].unique()
primary.sort()
primarydict = [{'label' : i, 'value' : i } for i in primary]

tenure = df1['Tenure'].unique()
tenure.sort()
tenuredict = [{'label' : i, 'value' : i } for i in tenure]

age = df1['Age'].unique()
age.sort()
agedict = [{'label' : i, 'value' : i } for i in age]

international = df1['International'].unique()
international.sort()
internationaldict = [{'label' : i, 'value' : i } for i in international]

ca = df1['CA'].unique()
ca.sort()
cadict = [{'label' : i, 'value' : i } for i in ca]

card = df1['Card'].unique()
card.sort()
carddict = [{'label' : i, 'value' : i } for i in card]

ins = df1['Insurance'].unique()
ins.sort()
insdict = [{'label' : i, 'value' : i } for i in ins]

inv = df1['Investment'].unique()
inv.sort()
invdict = [{'label' : i, 'value' : i } for i in inv]

mort = df1['Mortgage'].unique()
mort.sort()
mortdict = [{'label' : i, 'value' : i } for i in mort]

nps = df1['NPS'].unique()
nps.sort()
npsdict = [{'label' : i, 'value' : i } for i in nps]

dig = df1['Digital'].unique()
dig.sort()
digdict = [{'label' : i, 'value' : i } for i in dig]


#Set up the sidebar
SIDEBAR_STYLE = {

    "top": 0,
    "left": 7,
    "bottom": 0,
    "width": "8rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

#Testing generating a Table

table1data = df1.groupby('Proposition')['Numcust'].sum().reset_index()
table1data['Percent'] = table1data['Numcust'] / table1data['Numcust'].sum()*100




#Function to filter the data
def filterdata1(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig):


    if mk is not None:
        market_selection = df1['Market'] == mk
    else:
        l1 = df1['Market'].unique().tolist()
        market_selection = df1['Market'].isin(l1)

    if proposition is not None:
        proposition_selection = df1['Proposition'] == proposition
    else:
        l2 = df1['Proposition'].unique().tolist()
        proposition_selection = df1['Proposition'].isin(l2)

    if primary is not None:
        primary_selection = df1['Primary'] == primary
    else:
        l3 = df1['Primary'].unique().tolist()
        primary_selection = df1['Primary'].isin(l3)

    if tenure is not None:
        tenure_selection = df1['Tenure'] == tenure
    else:
        l4 = df1['Tenure'].unique().tolist()
        tenure_selection = df1['Tenure'].isin(l4)

    if age is not None:
        age_selection = df1['Age'] == age
    else:
        l5 = df1['Age'].unique().tolist()
        age_selection = df1['Age'].isin(l5)

    if international is not None:
        international_selection = df1['International'] == international
    else:
        l6 = df1['International'].unique().tolist()
        international_selection = df1['International'].isin(l6)

    if ca is not None:
        ca_selection = df1['CA'] == ca
    else:
        l7 = df1['CA'].unique().tolist()
        ca_selection = df1['CA'].isin(l7)

    if card is not None:
        card_selection = df1['Card'] == card
    else:
        l8 = df1['Card'].unique().tolist()
        card_selection = df1['Card'].isin(l8)

    if ins is not None:
        ins_selection = df1['Insurance'] == ins
    else:
        l9 = df1['Insurance'].unique().tolist()
        ins_selection = df1['Insurance'].isin(l9)

    if inv is not None:
        inv_selection = df1['Investment'] == inv
    else:
        l10 = df1['Investment'].unique().tolist()
        inv_selection = df1['Investment'].isin(l10)

    if mort is not None:
        mort_selection = df1['Mortgage'] == mort
    else:
        l11 = df1['Mortgage'].unique().tolist()
        mort_selection  = df1['Mortgage'].isin(l11)

    if nps is not None:
        NPS_selection = df1['NPS'] == nps
    else:
        l12 = df1['NPS'].unique().tolist()
        NPS_selection  = df1['NPS'].isin(l12)

    if dig is not None:
        digital_selection = df1['Digital'] == dig
    else:
        l13 = df1['Digital'].unique().tolist()
        digital_selection  = df1['Digital'].isin(l13)


    dffilt = df1[(market_selection) &
                    (proposition_selection) &
                    (primary_selection) &
                    (tenure_selection) &
                    (age_selection) &
                    (international_selection) &
                    (ca_selection) &
                    (card_selection) &
                    (ins_selection) &
                    (inv_selection) &
                    (mort_selection) &
                    (NPS_selection) &
                    (digital_selection)
                    ]

    return dffilt


#Function to build the table
def tablebuilder(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig):
    x = filterdata1(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig)
    a = x.groupby('Proposition')['Numcust'].sum().reset_index()
    a['Percent'] = round(a['Numcust'] / a['Numcust'].sum()*100,1)
    a = a.rename(columns = {'Proposition':'Dimension', 'Numcust': 'Number of customers'})
    atit = pd.DataFrame(data= {'Dimension': 'Propositions'}, index = [0])



    b = x.groupby('Market')['Numcust'].sum().reset_index()
    b['Percent'] = round(b['Numcust'] / b['Numcust'].sum()*100,1)
    b = b.rename(columns = {'Market':'Dimension', 'Numcust': 'Number of customers'})
    btit = pd.DataFrame(data= {'Dimension': 'Markets'}, index = [0])

    c = x.groupby('Primary')['Numcust'].sum().reset_index()
    c['Percent'] = round(c['Numcust'] / c['Numcust'].sum()*100,1)
    c = c.rename(columns = {'Primary':'Dimension', 'Numcust': 'Number of customers'})
    ctit = pd.DataFrame(data= {'Dimension': 'Primary'}, index = [0])

    d = x.groupby('Tenure')['Numcust'].sum().reset_index()
    d['Percent'] = round(d['Numcust'] / d['Numcust'].sum()*100,1)
    d = d.rename(columns = {'Tenure':'Dimension', 'Numcust': 'Number of customers'})
    dtit = pd.DataFrame(data= {'Dimension': 'Tenure'}, index = [0])

    e = x.groupby('Age')['Numcust'].sum().reset_index()
    e['Percent'] = round(e['Numcust'] / e['Numcust'].sum()*100,1)
    e = e.rename(columns = {'Age':'Dimension', 'Numcust': 'Number of customers'})
    etit = pd.DataFrame(data= {'Dimension': 'Age'}, index = [0])

    f = x.groupby('International')['Numcust'].sum().reset_index()
    f['Percent'] = round(f['Numcust'] / f['Numcust'].sum()*100,1)
    f = f.rename(columns = {'International':'Dimension', 'Numcust': 'Number of customers'})
    ftit = pd.DataFrame(data= {'Dimension': 'International'}, index = [0])

    g = x.groupby('NPS')['Numcust'].sum().reset_index()
    g['Percent'] = round(g['Numcust'] / g['Numcust'].sum()*100,1)
    g = g.rename(columns = {'NPS':'Dimension', 'Numcust': 'Number of customers'})
    gtit = pd.DataFrame(data= {'Dimension': 'NPS'}, index = [0])

    h = x.groupby('Digital')['Numcust'].sum().reset_index()
    h['Percent'] = round(h['Numcust'] / h['Numcust'].sum()*100,1)
    h = h.rename(columns = {'Digital':'Dimension', 'Numcust': 'Number of customers'})
    htit = pd.DataFrame(data= {'Dimension': 'NPS'}, index = [0])

    i = x.groupby('CA')['Numcust'].sum().reset_index()
    i['Percent'] = round(i['Numcust'] / i['Numcust'].sum()*100,1)
    i = i.drop(i[i['CA'] == 'N'].index)
    i = i.rename(columns = {'CA':'Dimension', 'Numcust': 'Number of customers'})
    i = i.replace(to_replace = 'Y', value = 'Current account holder')
    itit = pd.DataFrame(data= {'Dimension': 'Product holdings'}, index = [0])

    j = x.groupby('Card')['Numcust'].sum().reset_index()
    j['Percent'] = round(j['Numcust'] / j['Numcust'].sum()*100,1)
    j = j.drop(j[j['Card'] == 'N'].index)
    j = j.rename(columns = {'Card':'Dimension', 'Numcust': 'Number of customers'})
    j = j.replace(to_replace = 'Y', value = 'Card holder')

    k = x.groupby('Mortgage')['Numcust'].sum().reset_index()
    k['Percent'] = round(k['Numcust'] / k['Numcust'].sum()*100,1)
    k = k.drop(k[k['Mortgage'] == 'N'].index)
    k = k.rename(columns = {'Mortgage':'Dimension', 'Numcust': 'Number of customers'})
    k = k.replace(to_replace = 'Y', value = 'Mortgage holder')

    l = x.groupby('Investment')['Numcust'].sum().reset_index()
    l['Percent'] = round(l['Numcust'] / l['Numcust'].sum()*100,1)
    l = l.drop(l[l['Investment'] == 'N'].index)
    l = l.rename(columns = {'Investment':'Dimension', 'Numcust': 'Number of customers'})
    l = l.replace(to_replace = 'Y', value = 'Investment holder')

    m = x.groupby('Insurance')['Numcust'].sum().reset_index()
    m['Percent'] = round(m['Numcust'] / m['Numcust'].sum()*100,1)
    m = m.drop(m[m['Insurance'] == 'N'].index)
    m = m.rename(columns = {'Insurance':'Dimension', 'Numcust': 'Number of customers'})
    m = m.replace(to_replace = 'Y', value = 'Insurance holder')

    z = btit.append([b,atit,a, ctit, c, dtit,d, etit,e, ftit, f, gtit, g, htit, h, itit, i, j, k,l,m])
    z = z.round(decimals=0)


    return z




#Build the app layout
app = dash.Dash(external_stylesheets=external_stylesheets)
app.layout = html.Div([
                    dbc.Row([
                        html.H1('Customer demographic dashboard')
                    ],
                    style = {'margin-left': '10px'}),
                    dbc.Row([
                        dbc.Col(
                            html.Div(
                                [html.H3('Filters'),
                                html.P('Markets'),
                                dcc.Dropdown(id = 'marketdd', options = marketdict),
                                html.P('Proposition'),
                                dcc.Dropdown(id = 'propositionsdd', options = propositiondict),
                                html.P('Primary banking'),
                                dcc.Dropdown(id = 'primarydd', options = primarydict),
                                html.P('Tenure'),
                                dcc.Dropdown(id = 'tenuredd', options = tenuredict),
                                html.P('Age'),
                                dcc.Dropdown(id = 'agedd', options = agedict),
                                html.P('International'),
                                dcc.Dropdown(id = 'internationaldd', options = internationaldict),
                                html.P('NPS'),
                                dcc.Dropdown(id = 'npsdd', options = npsdict),
                                html.P('Digital active'),
                                dcc.Dropdown(id = 'digdd', options = digdict),
                                html.P('Current account holder'),
                                dcc.RadioItems(id = 'cadd', options = cadict,  inputStyle={"margin-right": "5px", "margin-left": "5px"}),
                                html.P('Card holder'),
                                dcc.RadioItems(id = 'carddd', options = carddict, inputStyle={"margin-right": "5px", "margin-left": "5px"}),
                                html.P('Insurance holder'),
                                dcc.RadioItems(id = 'insdd', options = insdict, inputStyle={"margin-right": "5px", "margin-left": "5px"}),
                                html.P('Investment holder'),
                                dcc.RadioItems(id = 'invdd', options = invdict, inputStyle={"margin-right": "5px", "margin-left": "5px"}),
                                html.P('Mortgage holder'),
                                dcc.RadioItems(id = 'mortdd', options = mortdict, inputStyle={"margin-right": "5px", "margin-left": "5px"}),
                                #dbc.Button('Click to clear filters',id='clearbut', n_clicks = 0,className = 'me-1', color = 'secondary')]
                                ]

                            ),
                            width = 3,
                            style = SIDEBAR_STYLE
                        )
                    ,
                        dbc.Col([
                            dbc.Row([
                                dbc.Col(
                                    [dbc.Card(id = 'bigcustnum', color = 'dark', inverse = True)
                                    ]),
                                dbc.Col([
                                    dbc.Card(id = 'bigtrb', color = 'dark', inverse = True)
                                    ]),
                                dbc.Col(
                                    [dbc.Card(id = 'bigrev', color = 'dark', inverse = True)
                                    ])

                            ]),

                            dbc.Row([
                                html.Hr()
                            ]),

                            dbc.Row([
                                dbc.Col(
                                    dbc.Tabs([
                                        dbc.Tab(label = 'Graphs', children =
                                            [dbc.Row(
                                                html.Div([],style = {'margin-top': '25px'})
                                            ),


                                            dbc.Row([
                                                dbc.Col(html.H3('Proposition split')),
                                                dbc.Col(html.H3('Primary banking rate'))
                                                ]),

                                            dbc.Row([
                                                dbc.Col(
                                                    html.Div(
                                                        [dcc.Graph(id = 'proppie')],
                                                        style = graphstylel)),
                                                dbc.Col(
                                                    html.Div(
                                                        [dcc.Graph(id = 'primpie')],
                                                        style = graphstyler))
                                            ]),

                                            dbc.Row([
                                                html.Hr()
                                            ]),

                                            dbc.Row([

                                                dbc.Col(html.H3('Digital active rate')),
                                                dbc.Col(html.H3('Product penetration'))
                                            ]),

                                            dbc.Row([
                                                dbc.Col(
                                                    html.Div([
                                                        dcc.Graph(id = 'digpie')]
                                                        )),


                                                dbc.Col(
                                                    html.Div([
                                                        dcc.Graph(id='producthold')]
                                                        ))
                                            ])

                                            ]),


                                            dbc.Tab(label = 'Table',
                                                children = [
                                                    dbc.Row([

                                                        dbc.Col([
                                                            html.Br(),
                                                            dt.DataTable(
                                                                id = 'table1',
                                                                columns = [{"name": i, "id": i} for i in table1data.columns],
                                                                data = table1data.to_dict('records'),
                                                                style_cell_conditional=[{'if': {'column_id': 'Dimension'},'textAlign': 'left'}],
                                                                style_table= {'maxWidth': '50%'},
                                                                style_cell={'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'}
                                                            )
                                                        ]),
                                                        dbc.Col([
                                                            html.Br(),
                                                            dbc.Button("Download CSV", outline = True, color = "secondary",id="btn_csv"),
                                                            dcc.Download(id="download-dataframe-csv")


                                                        ])
                                                    ])
                                                ]
                                            )




                                        ])
                                        )
                                        ])



                            ]),


                        ])
                    ])


#Make the clear filters Button
#@app.callback(
    #Output(component_id = 'marketdd', component_property = 'value'),
    #Output(component_id = 'propositionsdd', component_property = 'value'),
    #Output(component_id = 'primarydd', component_property = 'value'),
    #Output(component_id = 'tenuredd', component_property = 'value'),
    #Output(component_id = 'agedd', component_property = 'value'),
    #Output(component_id = 'internationaldd', component_property = 'value'),
    #Output(component_id = 'npsdd', component_property = 'value'),
    #Output(component_id = 'digdd', component_property = 'value'),
    #Output(component_id = 'cadd', component_property = 'value'),
    #Output(component_id = 'carddd', component_property = 'value'),
    #Output(component_id = 'insdd', component_property = 'value'),
    #Output(component_id = 'invdd', component_property = 'value'),
    #Output(component_id = 'mortdd', component_property = 'value'),
    #Input(component_id = 'clearbut', component_property = 'n_clicks')
#)

#def clearbutton(clicks):
    #f clicks is not None :
        #return [None, None, None, None, None, None, None, None, None, None, None, None, None]

#Big customer number indicator
@app.callback(
    Output(component_id = 'bigcustnum', component_property = 'children'),
    Input(component_id = 'marketdd', component_property = 'value'),
    Input(component_id = 'propositionsdd', component_property = 'value'),
    Input(component_id = 'primarydd', component_property = 'value'),
    Input(component_id = 'tenuredd', component_property = 'value'),
    Input(component_id = 'agedd', component_property = 'value'),
    Input(component_id = 'internationaldd', component_property = 'value'),
    Input(component_id = 'cadd', component_property = 'value'),
    Input(component_id = 'carddd', component_property = 'value'),
    Input(component_id = 'insdd', component_property = 'value'),
    Input(component_id = 'invdd', component_property = 'value'),
    Input(component_id = 'mortdd', component_property = 'value'),
    Input(component_id = 'npsdd', component_property = 'value'),
    Input(component_id = 'digdd', component_property = 'value')
)

def bigcustnumfunc(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig):
    x = filterdata1(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig)
    cn = x['Numcust'].sum()
    if cn > 1000000:
        cn = round(cn/1000000,2)
        cn = f'{cn}m'
    else:
        cn
    card_cn = [dbc.CardBody([
                    html.H1(cn, className = 'card-title'),
                    html.P('Number of customers', className = 'text=muted')
                ])]
    return card_cn

#Big trb indicator
@app.callback(
    Output(component_id = 'bigtrb', component_property = 'children'),
    Input(component_id = 'marketdd', component_property = 'value'),
    Input(component_id = 'propositionsdd', component_property = 'value'),
    Input(component_id = 'primarydd', component_property = 'value'),
    Input(component_id = 'tenuredd', component_property = 'value'),
    Input(component_id = 'agedd', component_property = 'value'),
    Input(component_id = 'internationaldd', component_property = 'value'),
    Input(component_id = 'cadd', component_property = 'value'),
    Input(component_id = 'carddd', component_property = 'value'),
    Input(component_id = 'insdd', component_property = 'value'),
    Input(component_id = 'invdd', component_property = 'value'),
    Input(component_id = 'mortdd', component_property = 'value'),
    Input(component_id = 'npsdd', component_property = 'value'),
    Input(component_id = 'digdd', component_property = 'value')
)

def bigtrbfunc(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig):
    x = filterdata1(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig)

    trbn = int((x['TRB'].sum()) / (x['Numcust'].sum()))

    card_trbn = [dbc.CardBody([
                        html.H1(trbn, className = 'card-title'),
                        html.P('Average TRB / customer', className = 'text=muted')
                    ])]
    return card_trbn

#Big revenue indicator
@app.callback(
    Output(component_id = 'bigrev', component_property = 'children'),
    Input(component_id = 'marketdd', component_property = 'value'),
    Input(component_id = 'propositionsdd', component_property = 'value'),
    Input(component_id = 'primarydd', component_property = 'value'),
    Input(component_id = 'tenuredd', component_property = 'value'),
    Input(component_id = 'agedd', component_property = 'value'),
    Input(component_id = 'internationaldd', component_property = 'value'),
    Input(component_id = 'cadd', component_property = 'value'),
    Input(component_id = 'carddd', component_property = 'value'),
    Input(component_id = 'insdd', component_property = 'value'),
    Input(component_id = 'invdd', component_property = 'value'),
    Input(component_id = 'mortdd', component_property = 'value'),
    Input(component_id = 'npsdd', component_property = 'value'),
    Input(component_id = 'digdd', component_property = 'value')
)

def bigrevfunc(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig):
    x = filterdata1(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig)

    revn = int((x['Revenue'].sum()) / (x['Numcust'].sum()))
    card_revn = [dbc.CardBody([
                    html.H1(revn, className = 'card-title'),
                    html.P('Average revenue / customer', className = 'text=muted')
                ])]
    return card_revn


#Proposition graph
@app.callback(
    Output(component_id = 'proppie', component_property = 'figure'),
    Input(component_id = 'marketdd', component_property = 'value'),
    Input(component_id = 'propositionsdd', component_property = 'value'),
    Input(component_id = 'primarydd', component_property = 'value'),
    Input(component_id = 'tenuredd', component_property = 'value'),
    Input(component_id = 'agedd', component_property = 'value'),
    Input(component_id = 'internationaldd', component_property = 'value'),
    Input(component_id = 'cadd', component_property = 'value'),
    Input(component_id = 'carddd', component_property = 'value'),
    Input(component_id = 'insdd', component_property = 'value'),
    Input(component_id = 'invdd', component_property = 'value'),
    Input(component_id = 'mortdd', component_property = 'value'),
    Input(component_id = 'npsdd', component_property = 'value'),
    Input(component_id = 'digdd', component_property = 'value')
)

def propositionpie(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig):
    x = filterdata1(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig)
    propositionpie = x.groupby('Proposition')['Numcust'].sum()
    propositionpie = propositionpie.reset_index()

    fig = px.pie(propositionpie, values = 'Numcust', names = 'Proposition', color = 'Proposition', color_discrete_map={'1. Gold':'#000000','2. Silver':'#4D4D4D', '3. Bronze':'#9FA1A4'})
    fig.update_traces(showlegend = True)
    fig.update_traces(textinfo = 'label+percent', hoverinfo='label+value')

    return fig

#Primary graph
@app.callback(
    Output(component_id = 'primpie', component_property = 'figure'),
    Input(component_id = 'marketdd', component_property = 'value'),
    Input(component_id = 'propositionsdd', component_property = 'value'),
    Input(component_id = 'primarydd', component_property = 'value'),
    Input(component_id = 'tenuredd', component_property = 'value'),
    Input(component_id = 'agedd', component_property = 'value'),
    Input(component_id = 'internationaldd', component_property = 'value'),
    Input(component_id = 'cadd', component_property = 'value'),
    Input(component_id = 'carddd', component_property = 'value'),
    Input(component_id = 'insdd', component_property = 'value'),
    Input(component_id = 'invdd', component_property = 'value'),
    Input(component_id = 'mortdd', component_property = 'value'),
    Input(component_id = 'npsdd', component_property = 'value'),
    Input(component_id = 'digdd', component_property = 'value')
)

def primpie(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig):
    x = filterdata1(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig)
    primarypie = x.groupby('Primary')['Numcust'].sum()
    fig = px.pie(primarypie, values = 'Numcust', names = primarypie.index, color = primarypie.index, color_discrete_map={'1. Primary':'#9FA1A4', '2. Non primary':'#DB0011'})
    fig.update_traces(textinfo = 'label+percent', hoverinfo='label+value')
    return fig

#Digital graph
@app.callback(
    Output(component_id = 'digpie', component_property = 'figure'),
    Input(component_id = 'marketdd', component_property = 'value'),
    Input(component_id = 'propositionsdd', component_property = 'value'),
    Input(component_id = 'primarydd', component_property = 'value'),
    Input(component_id = 'tenuredd', component_property = 'value'),
    Input(component_id = 'agedd', component_property = 'value'),
    Input(component_id = 'internationaldd', component_property = 'value'),
    Input(component_id = 'cadd', component_property = 'value'),
    Input(component_id = 'carddd', component_property = 'value'),
    Input(component_id = 'insdd', component_property = 'value'),
    Input(component_id = 'invdd', component_property = 'value'),
    Input(component_id = 'mortdd', component_property = 'value'),
    Input(component_id = 'npsdd', component_property = 'value'),
    Input(component_id = 'digdd', component_property = 'value'))

def digpie(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig):
    x = filterdata1(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig)
    digpie = x.groupby('Digital')['Numcust'].sum()
    digpie = digpie.reset_index()
    fig = px.pie(digpie, values = 'Numcust', names = 'Digital',  color = 'Digital', color_discrete_map={'1. Digitally active':'#9FA1A4', '2. Not digitally active':'#DB0011'})
    fig.update_traces(textinfo = 'label+percent', hoverinfo='label+value')
    return fig


#Product graph
@app.callback(
    Output(component_id = 'producthold', component_property = 'figure'),
    Input(component_id = 'marketdd', component_property = 'value'),
    Input(component_id = 'propositionsdd', component_property = 'value'),
    Input(component_id = 'primarydd', component_property = 'value'),
    Input(component_id = 'tenuredd', component_property = 'value'),
    Input(component_id = 'agedd', component_property = 'value'),
    Input(component_id = 'internationaldd', component_property = 'value'),
    Input(component_id = 'cadd', component_property = 'value'),
    Input(component_id = 'carddd', component_property = 'value'),
    Input(component_id = 'insdd', component_property = 'value'),
    Input(component_id = 'invdd', component_property = 'value'),
    Input(component_id = 'mortdd', component_property = 'value'),
    Input(component_id = 'npsdd', component_property = 'value'),
    Input(component_id = 'digdd', component_property = 'value'))

def prodgraph(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig):
    x = filterdata1(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig)
    y = x[['Numcust', 'CA_holders', 'Card_holders', 'Ins_holders', 'Inv_holders','Mort_holders']]

    y = y.sum()
    y = y.reset_index()
    y = y.transpose()
    y.columns = y.iloc[0]
    y = y.drop(labels = 'index', axis = 0)


    y['Current account'] = (y['CA_holders'] / y['Numcust'])*100
    y['Card'] = (y['Card_holders'] / y['Numcust']) *100
    y['Insurance'] = (y['Ins_holders'] / y['Numcust']) *100
    y['Investment'] = (y['Inv_holders'] / y['Numcust']) *100
    y['Mortgage'] = (y['Mort_holders'] / y['Numcust']) *100

    y   = y.drop(labels = ['Numcust', 'CA_holders', 'Card_holders', 'Ins_holders', 'Inv_holders', 'Mort_holders'], axis = 1)
    y = y.transpose()
    y.columns = ['Percentage']
    figprod = px.bar(y, x = y.index, y = 'Percentage', color = y.index, color_discrete_sequence = colorsequence)
    figprod = figprod.update_layout(plot_bgcolor = 'white', xaxis_title = 'Product', yaxis_title = 'Penetration')

    return figprod

#Product graph
@app.callback(
    Output(component_id = 'table1', component_property = 'data'),
    Output(component_id = 'table1', component_property = 'columns'),
    Input(component_id = 'marketdd', component_property = 'value'),
    Input(component_id = 'propositionsdd', component_property = 'value'),
    Input(component_id = 'primarydd', component_property = 'value'),
    Input(component_id = 'tenuredd', component_property = 'value'),
    Input(component_id = 'agedd', component_property = 'value'),
    Input(component_id = 'internationaldd', component_property = 'value'),
    Input(component_id = 'cadd', component_property = 'value'),
    Input(component_id = 'carddd', component_property = 'value'),
    Input(component_id = 'insdd', component_property = 'value'),
    Input(component_id = 'invdd', component_property = 'value'),
    Input(component_id = 'mortdd', component_property = 'value'),
    Input(component_id = 'npsdd', component_property = 'value'),
    Input(component_id = 'digdd', component_property = 'value'))

def tablegenerator(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig):
    z = tablebuilder(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig)
    return z.to_dict('records'),[{"name": i, "id": i} for i in z.columns]


@app.callback(
    Output(component_id = "download-dataframe-csv", component_property = 'data'),
    Input(component_id = "btn_csv", component_property = 'n_clicks'),
    Input(component_id = 'marketdd', component_property = 'value'),
    Input(component_id = 'propositionsdd', component_property = 'value'),
    Input(component_id = 'primarydd', component_property = 'value'),
    Input(component_id = 'tenuredd', component_property = 'value'),
    Input(component_id = 'agedd', component_property = 'value'),
    Input(component_id = 'internationaldd', component_property = 'value'),
    Input(component_id = 'cadd', component_property = 'value'),
    Input(component_id = 'carddd', component_property = 'value'),
    Input(component_id = 'insdd', component_property = 'value'),
    Input(component_id = 'invdd', component_property = 'value'),
    Input(component_id = 'mortdd', component_property = 'value'),
    Input(component_id = 'npsdd', component_property = 'value'),
    Input(component_id = 'digdd', component_property = 'value'),
    prevent_initial_call = True
)

def download(n_clicks,mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if "btn_csv" in changed_id:
        x = tablebuilder(mk,proposition,primary,tenure,age,international,ca,card,ins,inv,mort,nps,dig)
        return dcc.send_data_frame(x.to_csv,'downloadeddata.csv')
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(port = 8164, debug=True)
