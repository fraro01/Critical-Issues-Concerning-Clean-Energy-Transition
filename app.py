#pip install -q dash jupyter-dash
#pip install dash-bootstrap-components

#IMPORTIAMO I PACCHETTI
import dash
#import dash_core_components as dcc DEPRECATED SO:
from dash import dcc
#import dash_html_components as html SO:
from dash import html
from dash.dependencies import Output, Input
import pandas as pd #manipolare oggetti DataFrame
import plotly.express as px #graficare
#from jupyter_dash import JupyterDash #classe principale ove creiamo la dashboard
#from dash import Dash, html, dcc, Input, Output #grafici interattivi
import plotly.graph_objects as go #per i grafici coi due assi y
from plotly.subplots import make_subplots #per i grafici coi due assi y
from statsmodels.tsa.api import SimpleExpSmoothing, Holt #pacchetto per fare previsioni future con algoritmo Holt-Winter e Smoothing Esponenziale
import dash_bootstrap_components as dbc #per impaginazione

#puntatore alla cartella
folder_raws = "C:\\Users\\Francesco\\Desktop\\DeployWithRender\\src\\"
#DataFrame degli scenari
scenario_SDS_solarPV = pd.read_csv(folder_raws + "scenario SDS SolarPV .csv")
scenario_SDS_wind = pd.read_csv(folder_raws + "scenario SDS wind .csv")
scenario_STEPS_solarPV = pd.read_csv(folder_raws + "scenario STEPS SolarPV .csv")
scenario_STEPS_wind = pd.read_csv(folder_raws + "scenario STEPS Wind .csv")
#DataFrame Aggiunta di capacità
aggiunta_capacità_STEPS = pd.read_csv(folder_raws + "aggiunta di capacità STEPS .csv")
aggiunta_capacità_SDS = pd.read_csv(folder_raws + "aggiunta di capacità SDS .csv")

#PER I PRIMI DUE GRAFICI

#aggregazione degli scenari steps e sds per: molybden, nickel, silver, zinc,
#per il fotovoltaico, poichè tali materiali essendo in minore quantità sono di
#minore interesse
#df6 = df.query("country in ['Italy','Germany','France']")
others_STEPS_solarPV = scenario_STEPS_solarPV.query("material in ['molybdenum','nickel','silver','zinc']")
others_SDS_solarPV = scenario_SDS_solarPV.query("material in ['molybdenum','nickel','silver','zinc']")
#accorpiamo le quantità per il plot sulle ordinate, in due liste:
ord_others_STEPS_solarPV = [sum(others_STEPS_solarPV.loc[others_STEPS_solarPV.year == 2020].quantity),
sum(others_STEPS_solarPV.loc[others_STEPS_solarPV.year == 2030].quantity),
sum(others_STEPS_solarPV.loc[others_STEPS_solarPV.year == 2040].quantity)]
ord_others_SDS_solarPV = [sum(others_SDS_solarPV.loc[others_SDS_solarPV.year == 2020].quantity),
sum(others_SDS_solarPV.loc[others_SDS_solarPV.year == 2030].quantity),
sum(others_SDS_solarPV.loc[others_SDS_solarPV.year == 2040].quantity)]

#PER IL TERZO GRAFICO
#CALCOLI PER L'INTENSITA SUL TERZO GRAFICO LASCIARLI COSI!!!

sole = pd.DataFrame({'year': [2020,2030,2040,2020,2030,2040,2020,2030,2040],
                           'material': ['Silicon','Silicon','Silicon',
                                        'Copper','Copper','Copper',
                                        'Others*','Others*','Others*',],
                           'kt/GW STEPS': [3.678994,2.972416,2.778453,
                                           3.263875,3.299604,3.272829,
                                           0.05036,0.045588,0.041388],
                          'kt/GW SDS': [3.678994,2.871474,2.523519,
                                        3.263875,3.286373,3.091042,
                                        0.050363,0.043724,0.037066],
                                     })

vento = pd.DataFrame({'year': [2020,2030,2040,2020,2030,2040,2020,2030,2040,2020,2030,2040,2020,2030,2040,2020,2030,2040,2020,2030,2040],
                           'material': ['Zinc','Zinc','Zinc',
                                        'Copper','Copper','Copper',
                                        'Manganese','Manganese','Manganese',
                                        'Chromium','Chromium','Chromium',
                                         'Nickel','Nickel','Nickel',
                                        'Molybdenum','Molybdenum','Molybdenum',
                                        'Rare earths','Rare earths','Rare earths',],
                           'kt/GW STEPS': [5.352838,5.550859,5.481393,
                                           3.612730,4.548973,3.875882,
                                           0.763028,0.792892,0.782732,
                                           0.478866,0.505581,0.497948,
                                     0.350814,0.345048,0.352620,
                                     0.100250,0.105595,0.104036,
                                     0.068472,0.095428,0.075568],
                            'kt/GW SDS': [ 5.352838,5.311753,5.138572,
                                          3.612730,3.980295,3.811176,
                                          0.763028,0.757956,0.734011,
                                          0.478866,0.479505,0.468089,
                                      0.350814,0.339328,0.327100,
                                     0.100250,0.100265,0.097762,
                                     0.068472,0.077714,0.074656]
                                 })
sole = pd.melt(sole, id_vars=['year','material'], value_vars=['kt/GW STEPS','kt/GW SDS'])
vento = pd.melt(vento, id_vars=['year','material'], value_vars=['kt/GW STEPS','kt/GW SDS'])


#PER IL TERZO GRAFICO

sole = pd.DataFrame({'year': [2020, 2030, 2040],
                           '[$] cost STEPS': [92750000000, 133000000000, 212625000000],
                          '[$] cost SDS': [92750000000, 246750000000, 280000000000]})
vento = pd.DataFrame({'year': [2020, 2030, 2040],
                           '[$] cost STEPS': [72000000000, 102000000000, 128400000000],
                       '[$] cost SDS':[72000000000, 174000000000, 192000000000]})

sole = pd.melt(sole, id_vars=['year'], value_vars=['[$] cost STEPS','[$] cost SDS'])
vento = pd.melt(vento, id_vars=['year'], value_vars=['[$] cost STEPS','[$] cost SDS'])

# CHIAMATA PRINCIPALE

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#VIDEO SU RENDER
server = app.server

# STRUTTURA LAY-OUT

app.layout = html.Div([
    # uso un'unica riga
    dbc.Row([  # prima colonna ove pongo tutto il pannello di controllo
        dbc.Col([
            dcc.Markdown(children='**Sector**'),
            dcc.Dropdown(['Wind', 'Solar PV', 'Compare scenarios'], 'Wind', id='fonte'),
            html.Div(className="my-5"),
            html.Div(className="my-5"),
            html.Div(className="my-5"),

            dcc.Markdown(children='---'),
            dcc.Markdown(children='---'),

            html.Div(className="my-5"),
            html.Div(className="my-5"),
            html.Div(className="my-5"),
            dcc.Markdown(children='**Time Series and Predictions**'),
            dcc.Markdown(children='---'),

            dcc.Markdown(children=' **Material**'),
            dcc.Dropdown(['chromium',
                          'copper',
                          'manganese',
                          'molybdenum',
                          'nickel',
                          'rare-earths',
                          'silicon',
                          'silver',
                          'zinc'], 'silicon', id='materiale'),
            dcc.Markdown(children='---'),
            dcc.Markdown(children=' **Topic**'),
            dcc.Dropdown(['World production [t]', 'Unit value [$/t]'], 'Unit value [$/t]', id='serie'),
            dcc.Markdown(children='---'),
            dcc.Markdown(children=' **Algorithms**'),
            dcc.RadioItems(['Holt-Winters',
                            'Exponential Smoothing', 'both'], 'Holt-Winters', id='algorithm'),
            dcc.Markdown(children=' *parameter α of ESM*'),
            dcc.Slider(id='alpha_ese',
                       min=0,
                       max=1,
                       step=None,
                       value=0.2),
            dcc.Markdown(children=' *parameters α,β of H-W*'),
            dcc.Slider(id='alpha_H-W',
                       min=0,
                       max=1,
                       step=None,
                       value=0.8),
            dcc.Slider(id='beta_H-W',
                       min=0,
                       max=1,
                       step=None,
                       value=0.2),

            dcc.Markdown(id='Other')

        ], width={'size': 2, 'offset': 0},
            style={'padding': '2%'}),

        # altre colonne ove pongo solo i grafici
        dbc.Col([dcc.Graph(id='line_plot_STEPS', style={'margin-left': '1%'}), html.Div(className="my-1"),
                 dcc.Graph(id='line_plot', style={'margin-left': '1%', 'margin-bottom': '3%'})],
                width={'size': 5, 'offset': 0, }, className="g-1"),
        dbc.Col([dcc.Graph(id='line_plot_SDS', style={'margin-right': '3%'}), html.Div(className="my-1"),
                 dcc.Graph(id='plot', style={'margin-right': '3%', 'margin-bottom': '3%'})],
                width={'size': 5, 'offset': 0}, className="g-1"),
    ]),

],
    style={'width': '99%', 'height': '100%', 'background-color': '#FAEBD7'})  # per far stare tutto in una sola pagina


# TOGLIERE EVENTUALMENTE IL MARGIN-BOTTOM NEI DUE GRAFICI IN FONDO PER FAR STARE TUTTO IN UNA PAGINA


# CALLBACK PER IL FOOTER *OTHER
@app.callback(Output(component_id='Other', component_property='children'),
              Input(component_id='fonte', component_property='value'))
def update_footer(sector):
    if sector == 'Solar PV':
        return '*' + '*materials piled up together*'


# ------------------------------------------------------PRIMI DUE GRAFICI IN ALTO-----------------------------------------------------------------------------------------------

@app.callback(Output(component_id='line_plot_STEPS', component_property='figure'),
              Output(component_id='line_plot_SDS', component_property='figure'),
              Input(component_id='fonte', component_property='value')
              )
def update_figure_output(renewable):
    # FONTE FOTOVOLTAICO
    if renewable == 'Solar PV':
        # SCENARIO STEPS
        steps = make_subplots(specs=[[{"secondary_y": True}]])

        steps.add_trace(
            go.Scatter(x=scenario_STEPS_solarPV.loc[scenario_STEPS_solarPV.material == 'copper'].year,
                       y=scenario_STEPS_solarPV.loc[scenario_STEPS_solarPV.material == 'copper'].quantity,
                       name='Copper',
                       mode='markers+lines',
                       line=dict(color='brown')),
            secondary_y=False,
        )
        steps.add_trace(
            go.Scatter(x=scenario_STEPS_solarPV.loc[scenario_STEPS_solarPV.material == 'silicon'].year,
                       y=scenario_STEPS_solarPV.loc[scenario_STEPS_solarPV.material == 'silicon'].quantity,
                       name='Silicon',
                       mode='markers+lines',
                       line=dict(color='blue')),
            secondary_y=False,
        )
        steps.add_trace(
            go.Scatter(x=others_STEPS_solarPV.year,
                       y=ord_others_STEPS_solarPV,
                       name='Others*',
                       mode='markers+lines',
                       line=dict(color='red')),
            secondary_y=False,
        )
        steps.add_trace(
            go.Scatter(x=aggiunta_capacità_STEPS.loc[aggiunta_capacità_STEPS.sector == 'solar PV'].year,
                       y=aggiunta_capacità_STEPS.loc[aggiunta_capacità_STEPS.sector == 'solar PV'].quantity,
                       mode='markers+lines',
                       name="Added capacity",
                       line=dict(color='yellow', width=5),
                       marker=dict(symbol='square', size=10, color='orange')),
            secondary_y=True,
        )
        steps.update_layout(title='Scenario STEPS solar PV',
                            showlegend=False,
                            xaxis_title="Year",
                            yaxis=dict(title='Quantity [Kt]', side='left', color='black',
                                       titlefont=dict(color='black')),
                            yaxis2=dict(title='Added capacity  [GW]', overlaying='y', side='right', color='black',
                                        titlefont=dict(color='black')),
                            paper_bgcolor='#FFFAF0',
                            # plot_bgcolor = '#F0F8FF'
                            )

        steps.update_layout(
            yaxis2=dict(
                title='Added capacity  [GW]',
                overlaying='y',
                side='right',
                color='black',
                titlefont=dict(color='black'),
                range=[0, 500])
        )

        # SCENARIO SDS
        sds = make_subplots(specs=[[{"secondary_y": True}]])

        sds.add_trace(
            go.Scatter(x=scenario_SDS_solarPV.loc[scenario_STEPS_solarPV.material == 'copper'].year,
                       y=scenario_SDS_solarPV.loc[scenario_STEPS_solarPV.material == 'copper'].quantity,
                       name='Copper',
                       mode='markers+lines',
                       line=dict(color='brown')),
            secondary_y=False,
        )
        sds.add_trace(
            go.Scatter(x=scenario_SDS_solarPV.loc[scenario_STEPS_solarPV.material == 'silicon'].year,
                       y=scenario_SDS_solarPV.loc[scenario_STEPS_solarPV.material == 'silicon'].quantity,
                       name='Silicon',
                       mode='markers+lines',
                       line=dict(color='blue')),
            secondary_y=False,
        )
        sds.add_trace(
            go.Scatter(x=others_SDS_solarPV.year,
                       y=ord_others_SDS_solarPV,
                       name='Others*',
                       mode='markers+lines',
                       line=dict(color='red')),
            secondary_y=False,
        )
        sds.add_trace(
            go.Scatter(x=aggiunta_capacità_SDS.loc[aggiunta_capacità_SDS.sector == 'solar PV'].year,
                       y=aggiunta_capacità_SDS.loc[aggiunta_capacità_SDS.sector == 'solar PV'].quantity,
                       mode='markers+lines',
                       name="Added capacity",
                       line=dict(color='yellow', width=5),
                       marker=dict(symbol='square', size=10, color='orange')),
            secondary_y=True,
        )
        sds.update_layout(title='Scenario SDS solar PV',
                          xaxis_title="Year",
                          yaxis=dict(title='Quantity  [Kt]', side='left', color='black', titlefont=dict(color='black')),
                          yaxis2=dict(title='Added capacity', overlaying='y', side='right', color='black',
                                      titlefont=dict(color='black')),
                          legend=dict(
                              font=dict(
                                  size=10,
                                  color='black'),
                              # bgcolor='white',
                              # bordercolor='Black',
                              # borderwidth=1
                          ),
                          paper_bgcolor='#FFFAF0',
                          # plot_bgcolor = '')
                          )

        sds.update_layout(
            yaxis2=dict(
                title='[GW]',
                overlaying='y',
                side='right',
                color='black',
                titlefont=dict(color='black'),
                range=[0, 500],
            )
        )

    # FONTE EOLICO
    if renewable == 'Wind':
        # SCENARIO STEPS
        steps = make_subplots(specs=[[{"secondary_y": True}]])

        steps.add_trace(
            go.Scatter(x=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'zinc'].year,
                       y=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'zinc'].quantity,
                       name='Zinc',
                       mode='markers+lines',
                       line=dict(color='purple')),
            secondary_y=False,
        )
        steps.add_trace(
            go.Scatter(x=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'copper'].year,
                       y=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'copper'].quantity,
                       name='Copper',
                       mode='markers+lines',
                       line=dict(color='brown')),
            secondary_y=False,
        )
        steps.add_trace(
            go.Scatter(x=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'manganese'].year,
                       y=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'manganese'].quantity,
                       name='Manganese',
                       mode='markers+lines',
                       line=dict(color='orange')),
            secondary_y=False,
        )
        steps.add_trace(
            go.Scatter(x=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'chromium'].year,
                       y=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'chromium'].quantity,
                       name='Chromium',
                       mode='markers+lines',
                       line=dict(color='red')),
            secondary_y=False,
        )
        steps.add_trace(
            go.Scatter(x=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'nickel'].year,
                       y=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'nickel'].quantity,
                       name='Nickel',
                       mode='markers+lines',
                       line=dict(color='gold')),
            secondary_y=False,
        )
        steps.add_trace(
            go.Scatter(x=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'molybdenum'].year,
                       y=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'molybdenum'].quantity,
                       name='Molybdenum', mode='markers+lines',
                       line=dict(color='grey')),
            secondary_y=False,
        )
        steps.add_trace(
            go.Scatter(x=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'rare earths'].year,
                       y=scenario_STEPS_wind.loc[scenario_STEPS_wind.material == 'rare earths'].quantity,
                       name='Rare earths',
                       mode='markers+lines',
                       line=dict(color='blue')),
            secondary_y=False,
        )
        steps.add_trace(
            go.Scatter(x=aggiunta_capacità_STEPS.loc[aggiunta_capacità_STEPS.sector == 'wind'].year,
                       y=aggiunta_capacità_STEPS.loc[aggiunta_capacità_STEPS.sector == 'wind'].quantity,
                       mode='markers+lines',
                       name="Added capacity",
                       line=dict(color='yellow', width=5),
                       marker=dict(symbol='square', size=10, color='orange')),
            secondary_y=True,
        )
        steps.update_layout(title='Scenario STEPS wind',
                            showlegend=False,
                            xaxis_title="Year",
                            yaxis=dict(title='Quantity  [Kt]', side='left', color='black',
                                       titlefont=dict(color='black')),
                            yaxis2=dict(title='Added capacity  [GW]', overlaying='y', side='right', color='black',
                                        titlefont=dict(color='black')),
                            paper_bgcolor='#FFFAF0',
                            # plot_bgcolor = '')
                            )

        steps.update_layout(
            yaxis2=dict(
                title='Added capacity  [GW]',
                overlaying='y',
                side='right',
                color='black',
                titlefont=dict(color='black'),
                range=[0, 200])
        )

        # SCENARIO SDS
        sds = make_subplots(specs=[[{"secondary_y": True}]])

        sds.add_trace(
            go.Scatter(x=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'zinc'].year,
                       y=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'zinc'].quantity,
                       name='Zinc',
                       mode='markers+lines',
                       line=dict(color='purple')),
            secondary_y=False,
        )
        sds.add_trace(
            go.Scatter(x=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'copper'].year,
                       y=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'copper'].quantity,
                       name='Copper',
                       mode='markers+lines',
                       line=dict(color='brown')),
            secondary_y=False,
        )
        sds.add_trace(
            go.Scatter(x=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'manganese'].year,
                       y=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'manganese'].quantity,
                       name='Manganese',
                       mode='markers+lines',
                       line=dict(color='orange')),
            secondary_y=False,
        )
        sds.add_trace(
            go.Scatter(x=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'chromium'].year,
                       y=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'chromium'].quantity,
                       name='Chromium',
                       mode='markers+lines',
                       line=dict(color='red')),
            secondary_y=False,
        )
        sds.add_trace(
            go.Scatter(x=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'nickel'].year,
                       y=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'nickel'].quantity,
                       name='Nickel',
                       mode='markers+lines',
                       line=dict(color='gold')),
            secondary_y=False,
        )
        sds.add_trace(
            go.Scatter(x=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'molybdenum'].year,
                       y=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'molybdenum'].quantity,
                       name='Molybdenum', mode='markers+lines',
                       line=dict(color='grey')),
            secondary_y=False,
        )
        sds.add_trace(
            go.Scatter(x=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'rare earths'].year,
                       y=scenario_SDS_wind.loc[scenario_SDS_wind.material == 'rare earths'].quantity,
                       name='Rare earths',
                       mode='markers+lines',
                       line=dict(color='blue')),
            secondary_y=False,
        )

        sds.add_trace(
            go.Scatter(x=aggiunta_capacità_SDS.loc[aggiunta_capacità_SDS.sector == 'wind'].year,
                       y=aggiunta_capacità_SDS.loc[aggiunta_capacità_SDS.sector == 'wind'].quantity,
                       mode='markers+lines',
                       name="Added capacity",
                       line=dict(color='yellow', width=5),
                       marker=dict(symbol='square', size=10, color='orange')),
            secondary_y=True,
        )
        sds.update_layout(title='Scenario SDS wind',
                          xaxis_title="Year",
                          yaxis=dict(title='Quantity  [Kt]', side='left', color='black', titlefont=dict(color='black')),
                          yaxis2=dict(overlaying='y', side='right', color='black', titlefont=dict(color='black')),
                          legend=dict(
                              font=dict(
                                  size=10,
                                  color='black'),
                              # bgcolor='white',
                              # bordercolor='Black',
                              # borderwidth=1
                          ), paper_bgcolor='#FFFAF0',
                          # plot_bgcolor = ''
                          )
        sds.update_layout(
            yaxis2=dict(
                title_text='',
                overlaying='y',
                side='right',
                color='black',
                titlefont=dict(color='black'),
                range=[0, 200],
            ),
        )

    # COMPARAZIONE TRA I DUE SCENARI
    if renewable == 'Compare scenarios':
        steps = go.Figure(
            data=go.Scatter(x=aggiunta_capacità_STEPS.loc[aggiunta_capacità_STEPS.sector == 'solar PV'].year,
                            y=aggiunta_capacità_STEPS.loc[aggiunta_capacità_STEPS.sector == 'solar PV'].quantity,
                            name='Scenario STEPS',
                            line=dict(color='orange')
                            ))
        steps.add_trace(go.Scatter(x=aggiunta_capacità_SDS.loc[aggiunta_capacità_SDS.sector == 'solar PV'].year,
                                   y=aggiunta_capacità_SDS.loc[aggiunta_capacità_SDS.sector == 'solar PV'].quantity,
                                   name="Scenario SDS",
                                   line=dict(color='red')))
        steps.update_layout(title='Solar PV',
                            xaxis_title="Year",
                            yaxis=dict(title='Added capacity  [GW]', side='left', color='black',
                                       titlefont=dict(color='black')),
                            showlegend=False, paper_bgcolor='#FFFAF0',
                            # plot_bgcolor = '')
                            )

        sds = go.Figure(data=go.Scatter(x=aggiunta_capacità_STEPS.loc[aggiunta_capacità_STEPS.sector == 'wind'].year,
                                        y=aggiunta_capacità_STEPS.loc[
                                            aggiunta_capacità_STEPS.sector == 'wind'].quantity,
                                        name='Scenario STEPS',
                                        line=dict(color='orange')
                                        ))
        sds.add_trace(go.Scatter(x=aggiunta_capacità_SDS.loc[aggiunta_capacità_SDS.sector == 'wind'].year,
                                 y=aggiunta_capacità_SDS.loc[aggiunta_capacità_SDS.sector == 'wind'].quantity,
                                 name="Scenario SDS",
                                 line=dict(color='red')))
        sds.update_layout(title='Wind',
                          xaxis_title="Year",
                          yaxis=dict(title='Added capacity  [GW]', side='left', color='black',
                                     titlefont=dict(color='black')),
                          paper_bgcolor='#FFFAF0',
                          # plot_bgcolor = '')
                          )

    return steps, sds


# ------------------------------------------------------------------TERZO GRAFICO------------------------------------------------------------------------------------------------

@app.callback(Output(component_id='plot', component_property='figure'),
              Input(component_id='fonte', component_property='value'))
def update_graph(sector):
    if sector == 'Solar PV':
        fig = px.bar(sole, x='year', y='value', facet_col='variable', barmode='stack')
        fig.update_yaxes(title_text='')
        fig.update_xaxes(tickvals=[2020, 2030, 2040], ticktext=['2020', '2030', '2040'])

        fig.update_layout(title='Solar PV global investment',
                          paper_bgcolor='#FFFAF0',
                          # plot_bgcolor = '')
                          )

    if sector == 'Wind':
        fig = px.bar(vento, x='year', y='value', facet_col='variable', barmode='stack')
        fig.update_yaxes(title_text='')
        fig.update_xaxes(tickvals=[2020, 2030, 2040], ticktext=['2020', '2030', '2040'])

        fig.update_layout(title='Wind global investment',
                          paper_bgcolor='#FFFAF0',
                          # plot_bgcolor = '')
                          )

    if sector == 'Compare scenarios':
        fig = px.bar(sole, x='year', y='value', facet_col='variable', barmode='stack')
        fig.update_yaxes(title_text='')
        fig.update_xaxes(tickvals=[2020, 2030, 2040], ticktext=['2020', '2030', '2040'])

        fig.update_layout(title='Solar PV global investment',
                          paper_bgcolor='#FFFAF0',
                          # plot_bgcolor = '')
                          )
        # pass

    return fig


# -----------------------------------------------------------------QUARTO GRAFICO------------------------------------------------------------------------------------------

@app.callback(Output(component_id='line_plot', component_property='figure'),
              Input(component_id='materiale', component_property='value'),
              Input(component_id='serie', component_property='value'),
              Input(component_id='algorithm', component_property='value'),
              Input(component_id='alpha_ese', component_property='value'),
              Input(component_id='alpha_H-W', component_property='value'),
              Input(component_id='beta_H-W', component_property='value')
              )
def update_graph(materia, valori, algoritmo, alpha1, alpha2, beta):
    # sfruttiamo i parametri e creiamo un oggetto dataframe
    materia_df = pd.read_csv(folder_raws + materia + '.csv')

    # generiamo un time serie di dati, e applichiamo l'algoritmo dal 2000 in poi
    data = materia_df.loc[materia_df.Year >= 2000][f'{valori}']
    time_series = pd.Series(data)
    # fittiamo il metodo di Holt alla time series data
    model_holt = Holt(time_series).fit(smoothing_level=alpha2, smoothing_trend=beta)
    # fittiamo l'Exponential Smoothing alla time series data
    model_ses = SimpleExpSmoothing(time_series).fit(smoothing_level=alpha1, optimized=False)

    # prediciamo i valori futuri della serie temporale
    ultimo_anno = int(materia_df.iloc[-1]['Year'])
    numero_previsioni = int(2040 - ultimo_anno)
    prima_ascissa_prevista = int(ultimo_anno + 1)

    # lancio delle previsioni HOLT
    future_holt = model_holt.forecast(numero_previsioni)
    lista_futura_holt = list(future_holt)
    # lancio delle previsioni SES
    future_ses = model_ses.forecast(numero_previsioni)
    lista_futura_ses = list(future_ses)

    # dataframe con le due previsioni holt & ses
    df_predicted_values_holt = pd.DataFrame({
        'Year2': [year for year in range(prima_ascissa_prevista, 2041)],
        'Ordinate': lista_futura_holt})
    df_predicted_values_ses = pd.DataFrame({
        'Year2': [year for year in range(prima_ascissa_prevista, 2041)],
        'Ordinate': lista_futura_ses})

    fig = px.line(data_frame=materia_df,
                  x=materia_df.loc[materia_df.Year >= 1975].Year,
                  y=materia_df.loc[materia_df.Year >= 1975][f"{valori}"],
                  labels={'x': 'Year', 'y': f"{valori}"},
                  )

    if algoritmo == 'Holt-Winters':
        # aggiungiamo la previsione futura con l'algoritmo di Holt
        fig.add_trace(go.Scatter(x=df_predicted_values_holt['Year2'],
                                 y=df_predicted_values_holt['Ordinate'],
                                 name="H-W",
                                 line=dict(color='red')))

        fig.update_layout(paper_bgcolor='#FFFAF0',
                          # plot_bgcolor = '')
                          )
    if algoritmo == 'Exponential Smoothing':
        # aggiungiamo la previsione futura con l'algoritmo dello smoothin esponenziale
        fig.add_trace(go.Scatter(x=df_predicted_values_ses['Year2'],
                                 y=df_predicted_values_ses['Ordinate'],
                                 name='ESM',
                                 line=dict(color='orange')))

        fig.update_layout(paper_bgcolor='#FFFAF0',
                          # plot_bgcolor = '')
                          )
    if algoritmo == 'both':
        # li aggiungiamo tutti e due
        fig.add_trace(go.Scatter(x=df_predicted_values_holt['Year2'],
                                 y=df_predicted_values_holt['Ordinate'],
                                 name="H-W",
                                 line=dict(color='red')))
        fig.add_trace(go.Scatter(x=df_predicted_values_ses['Year2'],
                                 y=df_predicted_values_ses['Ordinate'],
                                 name='ESM',
                                 line=dict(color='orange')))

        fig.update_layout(paper_bgcolor='#FFFAF0',
                          # plot_bgcolor = '')
                          )

    # anche qui bisogna togliere la velocità di transizione velocità di transizione pari a 2000millisec
    # fig.update_layout()
    fig.update_layout(title='Time series and predictions of ' + f"{materia}")

    return fig

if __name__ == '__main__':
    app.run_server(debug=False)
