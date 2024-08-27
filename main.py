from flask import Flask

import connect_to_database
import type_colors

import dash
from dash import dcc, Input, html, Output
import dash_bootstrap_components as dbc
import plotly.express as px


server = Flask(__name__)


app = dash.Dash(server=server, routes_pathname_prefix="/", external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.themes.DARKLY])

#Type list with NA is for the second type. Not every Pokemon is dual-typed.
type_list = list(type_colors.get_type_colors())
type_list_with_na = type_list.copy()
type_list_with_na.append('N/A')

app.layout = html.Div(
    [ 
        html.H1("Pokemon Stats"),
        dbc.Row(
            [
                dbc.Col(
                        [
                            #HP Bounds 
                            html.Div("HP", style={"font-size": "20px"}),
                            dcc.RangeSlider(0,255,value=[0,255], id='hp_slider'),
                            html.Div(id='output_container_hp_slider')
                        ]
                    ),
                dbc.Col(
                        [
                            #Attack Bounds
                            html.Div("Attack", style={"font-size": "20px"}),
                            dcc.RangeSlider(0,190,value=[0,190], id='atk_slider'),
                            html.Div(id='output_container_atk_slider')
                        ]
                    ),
                dbc.Col(   
                        [
                            #Defense Bounds
                            html.Div("Defense", style={"font-size": "20px"}),
                            dcc.RangeSlider(0,250,value=[0,250], id='dfs_slider'),
                            html.Div(id='output_container_dfs_slider')
                        ]
                    )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                        [
                            #Special Attack Bounds
                            html.Div("Special Attack", style={"font-size": "20px"}),
                            dcc.RangeSlider(0,194,value=[0,194], id='spatk_slider'),
                            html.Div(id='output_container_spatk_slider'),
                        ]
                    ),
                dbc.Col(
                        [
                            #Special Defense Bounds
                            html.Div("Special Defense", style={"font-size": "20px"}),
                            dcc.RangeSlider(0,250,value=[0,250], id='spdfs_slider'),
                            html.Div(id='output_container_spdfs_slider'),
                        ]
                    ),
                dbc.Col(   
                        [
                            #Speed Bounds
                            html.Div("Speed", style={"font-size": "20px"}),
                            dcc.RangeSlider(0,200,value=[0,200], id='spd_slider'),
                            html.Div(id='output_container_spd_slider'),
                        ]
                    )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                        [
                            #Type Sorting
                            html.Div("Type 1", style={"font-size": "20px"}),
                            dcc.Dropdown(type_list, multi=True, clearable=True, id='type1_select'),
                            html.Div(id='output_container_type1_select'),
                        ]
                    ),

                dbc.Col(
                        [
                            #Type Sorting
                            html.Div("Type 2", style={"font-size": "20px"}),
                            dcc.Dropdown(type_list_with_na, multi=True, clearable=True, id='type2_select'),
                            html.Div(id='output_container_type2_select'),
                        ]
                    ),
                
                dbc.Col(
                        [
                            #Generation Select
                            html.Div("Generation", style={"font-size": "20px"}),
                            dcc.Dropdown(list(range(1,10)), clearable=False, id='gen_select', multi=True),
                            html.Div(id='output_container_gen_select'),
                        ]
                ),
            ]
        ),        
        dcc.Graph(id="plot")
    ],
    style={"margin": 5, "maxWidth": 1800, "viewHeight": 900},
)

@app.callback(
    Output('output_container_hp_slider', 'children'),
    Output('output_container_atk_slider', 'children'),
    Output('output_container_dfs_slider', 'children'),
    Output('output_container_spatk_slider', 'children'),
    Output('output_container_spdfs_slider', 'children'),
    Output('output_container_spd_slider', 'children'),
    Output('output_container_type1_select', 'children'),
    Output('output_container_type2_select', 'children'),
    Output('output_container_gen_select', 'children'),

    Output("plot", "figure"),

    [Input('hp_slider', 'value'),
    Input('atk_slider', 'value'),
    Input('dfs_slider', 'value'),
    Input('spatk_slider', 'value'),
    Input('spdfs_slider', 'value'),
    Input('spd_slider', 'value'),
    Input('type1_select', 'value'),
    Input('type2_select', 'value'),
    Input('gen_select', 'value')],
)

def sync_input(hp_slider, atk_slider, dfs_slider, spatk_slider, spdfs_slider, spd_slider, type1_select, type2_select, gen_select):
    
    #If there are no selections, we show all.
    if not type1_select:
        type1_select = type_list
    if not type2_select:
        type2_select = type_list_with_na
    if not gen_select:
        gen_select = list(range(1,10))
                            
    
    df = connect_to_database.get_table(hp_slider,
                                        atk_slider, 
                                        dfs_slider, 
                                        spatk_slider, 
                                        spdfs_slider, 
                                        spd_slider,
                                        type1_select, 
                                        type2_select,
                                        gen_select) 
    

    fig = px.scatter_matrix(df, 
                    dimensions=['Total',
                                'HP', 
                                'Attack', 
                                'Defense', 
                                'SpAttack',
                                'SpDefense',
                                'Speed'],
                    hover_name='Name',
                    color='Type1', 
                    color_discrete_map=type_colors.get_type_colors(),
                )
    
    fig.update_layout(height=600, template='plotly_dark')

    return ('HP Range: {}'.format(hp_slider), 
            'Attack Range: {}'.format(atk_slider),  
            'Defense Range: {}'.format(dfs_slider), 
            'Special Attack Range: {}'.format(spatk_slider), 
            'Special Defense Range: {}'.format(spdfs_slider), 
            'Speed Range: {}'.format(spd_slider), 
            'Type 1: {}'.format(type1_select), 
            'Type 2: {}'.format(type2_select), 
            'Generation: {}'.format(gen_select), 
            fig)

if __name__ == "__main__":
    app.run(debug=True)
