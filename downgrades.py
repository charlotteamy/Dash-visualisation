#Import packages
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import dash
import plotly.graph_objs as go
from dash.dependencies import Input,Output
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff

#Load data
name = 'Downgrade1.csv'
df1 = pd.read_csv(name)
df1.head()

#Build dimension dictionaries
cols = list((df1.columns))
dim = cols[0:7]
dimdict = [ {'label':i, 'value':i} for i in dim]
dimdict2 = [{'label': 'Age', 'value': 'Age'},
            {'label': 'Tenure', 'value': 'Tenure'},
            {'label': 'TRB band', 'value': 'Dim_TRB'},
            {'label': 'NPS', 'value': 'NPS'},
            {'label': 'Proposition', 'value': 'Proposition'},
            {'label': 'Revenue band', 'value': 'Dim_Revenue'},
            {'label': 'Income', 'value': 'Income'}]

#Measure dictionary
meas = cols[7:11]
measdict2 = [{'label': 'Number of Customers', 'value': 'Numcust'},
            {'label': 'Average TRB', 'value': 'TotTRB'},
            {'label': 'Average Revenue', 'value': 'Totrev'},
            {'label': 'Average years on book', 'value': 'TotMOB'}]






#Card content

card_cust = [dbc.CardBody([
                html.H1('62,107', className = 'card-title'),
                html.P('Number of downgrade customers', className = 'text=muted')
            ])]

card_trb = [dbc.CardBody([
                html.H1('£70bn', className = 'card-title'),
                html.P('Total TRB', className = 'text=muted')
            ])]

card_rev = [dbc.CardBody([
                html.H1('£121m', className = 'card-title'),
                html.P('Total revenue', className = 'text=muted')
            ])]


#Build app layout
app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])
app.layout = html.Div([
                    dbc.Row(
                        [html.H1('Customer downgrade profile')],
                        style = {'margin-bottom': '50px', 'margin-left': '7px'}),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card(card_cust, color = 'dark', inverse = True)
                        ], style = {'margin-left': '7px'}),
                        dbc.Col(
                            dbc.Card(card_trb, color = 'dark', inverse = True)
                        ),
                        dbc.Col(
                            [dbc.Card(card_rev, color = 'dark', inverse = True)],
                            style = {'margin-right': '7px'}
                        )

                    ]),
                    dbc.Row(
                        html.Hr(),
                        style = {'margin-top': '50px','margin-bottom': '50px'}

                    ),
                    dbc.Row([
                        dbc.Col(
                            [html.H3('Heatmap'),
                            dcc.Graph(id = 'heat')],
                            style = {'margin-right': '7px', 'margin-left': '7px'}

                        )
                    ]),
                    dbc.Row([
                        dbc.Col(
                            [html.H5('X axis input'),
                            dcc.Dropdown(id = 'yaxisid', options = dimdict2, value = 'Dim_TRB')],
                            style = {'margin-left': '7px'}),
                        dbc.Col(
                            [html.H5('Y axis input'),
                            dcc.Dropdown(id = 'xaxisid', options = dimdict2, value = 'Tenure')],
                            ),
                        dbc.Col(
                            [html.H5('Measure input'),
                            dcc.Dropdown(id = 'measid', options = measdict2, value = 'Numcust')],
                            style = {'margin-right': '7px'})

                    ])

                        ])



#Callbacks
@app.callback(
    Output(component_id = 'heat', component_property = 'figure'),
    Input(component_id = 'measid', component_property = 'value'),
    Input(component_id = 'xaxisid', component_property = 'value'),
    Input(component_id = 'yaxisid', component_property = 'value')
)


def heaty(meas,xaxis,yaxis):
    if meas in ['Numcust']:
        df2 = pd.crosstab(df1[xaxis], df1[yaxis], values = df1[meas], aggfunc = 'sum')
        fig = ff.create_annotated_heatmap(
            z = df2.to_numpy(),
            x = df2.columns.tolist(),
            y = df2.index.tolist(),
            colorscale = 'Viridis_r',
            showscale = True
        )
        return fig

    elif meas in ['Totrev','TotTRB','TotMOB']:
        dftest = df1.groupby([xaxis,yaxis]).agg({meas:'sum','Numcust':'sum'}).unstack()
        ls1 = []
        ls1 = df1[yaxis].unique()
        ls1.sort()

        for i in ls1:
            dftest[i] = dftest[meas,i] / dftest['Numcust',i]

        df5 = dftest.drop(level = 0, columns = [meas,'Numcust'])
        df6 = df5
        df6.columns = df5.columns.droplevel(1)
        za = df6.to_numpy()
        za = np.int32(za)
        fig10 = ff.create_annotated_heatmap(
            z = za,
            x = df6.columns.tolist(),
            y = df6.index.tolist(),
            colorscale = 'Viridis_r',
            showscale = True)
        return fig10



#Launch the app
if __name__ == "__main__":
    app.run_server(port = 8104)
