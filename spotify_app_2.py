from dash import Dash, html, dash_table, dcc, callback, callback_context, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

spotify_df = pd.read_csv('spotify-2023.csv', encoding= "ISO-8859-1")
spotify_df.set_index(['track_name'], inplace=True)
indexdrop = spotify_df[spotify_df['streams'] == 'BPM110KeyAModeMajorDanceability53Valence75Energy69Acousticness7Instrumentalness0Liveness17Speechiness3'].index
spotify_df.drop(indexdrop, inplace=True)
spotify_df['streams'] = spotify_df['streams'].astype('int64')
spotify_acousitc_df = spotify_df[spotify_df['instrumentalness_%'] > 0]



features = ['danceability_%','energy_%','instrumentalness_%','acousticness_%','speechiness_%']

figure = px.scatter(spotify_df,
            x='danceability_%', 
            y='energy_%',
            opacity=0.8,
            template='plotly_dark',
            color='energy_%',
            color_continuous_scale='OrRd',
            )

# barchart_figure = px.bar(spotify_gb_artists,
#     x='artist(s)_name',
#     y='streams',
#     color='streams',
#     template='plotly_dark',
#     color_continuous_scale='thermal'
# )

# barchart_figure.update_xaxes(showgrid=False)
# barchart_figure.update_yaxes(showgrid=False)

app = Dash(external_stylesheets=[dbc.themes.SOLAR])

dropdown = html.Div(
    [
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem(
                    'Danceability & Energy',
                    id='dance_energy',
                    active=True
                ),
                dbc.DropdownMenuItem(
                    'Acousticness & Instrumentalness',
                    id='acoust_instru',
                    active=True
                ),
                dbc.DropdownMenuItem(
                    'Livliness & Speechiness',
                    id='live_speech',
                    active=True
                ),
            ],
            label='Scatter Options',
            
        ),
        html.P(id="item-clicks", className="mt-3")
    ],
)

radio_gradient = html.Div(
    [
        dcc.RadioItems(
            id='gradient-scheme',
            options=[
                {'label': 'Orange to Red', 'value':'OrRd'},
                {'label': 'Viridis', 'value':'Viridis'},
                {'label': 'Plasma', 'value':'Plasma'},

            ],
            value='Viridis',
            labelStyle={'float': 'left', 'display':'inline-block'}
        ),
    ],
)

app.layout = dbc.Container([
        html.H1("Spotify Streams Analysis"),
        html.Div(id='debug_text'),
        dbc.Row
            ([
                html.H4('Artists by Streams'),
                dbc.Col(dcc.Graph(figure={}, id='bar_chart'))
            ]),
        dbc.Row
            ([
                dbc.Col(dropdown),
                dbc.Col(radio_gradient)
            ]),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure={}, id='chart'), width=6)
            ],
        ),
    ], 
fluid=False
)

@callback(
    Output(component_id='chart', component_property='figure'),
    [
        Input(component_id='dance_energy', component_property= 'n_clicks_timestamp'),
        Input(component_id='acoust_instru', component_property='n_clicks_timestamp'),
        Input(component_id='live_speech', component_property='n_clicks_timestamp'),
        Input(component_id='gradient-scheme', component_property='value')
    ]
)

def scatter_chart(dance, acoust, live, gradient):
    # fig = figure
    counter = 0
    feature_dict = {
        'dance': dance,
        'acoust': acoust,
        'live': live
    }

    for i in feature_dict:
        if feature_dict[i] == None:
            feature_dict[i] = 0

    ctx = callback_context
    if ctx.triggered_id =='gradient-scheme':
        current_plot = max(feature_dict, key= lambda x: feature_dict[x])
        if current_plot == 'dance':
            fig = dance_scatter(gradient) 
        elif current_plot == 'acoust':
            fig = acoust_scatter(gradient)
        else:
            fig = live_scatter(gradient) 
    elif ctx.triggered_id =='dance_energy':
        fig = dance_scatter(gradient) 
    elif ctx.triggered_id =='acoust_instru':
        fig = acoust_scatter(gradient)
    else:
        fig = live_scatter(gradient)
    return fig
    
def dance_scatter(gradient):
    hover_names = [] 
    for ix, val in zip(spotify_df.index.values, spotify_df['artist(s)_name'].values):
        hover_names.append(f'{ix} by <br>{val}')

    fig = px.scatter(
        spotify_df,
        x='danceability_%', 
        y='energy_%',
        opacity=0.8,
        template='plotly_dark',
        color='energy_%',
        size='streams',
        color_continuous_scale=gradient,
        hover_name=hover_names,
    )
    fig.update_traces(customdata=spotify_df.index)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_traces(customdata=spotify_df['artist(s)_name'])

    fig.update_layout(
        height=450,
        width=800,
        hovermode='closest'
    )
    return fig

def acoust_scatter(gradient):
    hover_names = [] 
    for ix, val in zip(spotify_acousitc_df.index.values, spotify_acousitc_df['artist(s)_name'].values):
        hover_names.append(f'{ix} by <br>{val}')

    fig = px.scatter(
        spotify_acousitc_df,
        x='instrumentalness_%', 
        y='acousticness_%',
        opacity=0.8,
        template='plotly_dark',
        color='acousticness_%',
        size='streams',
        color_continuous_scale=gradient,
        hover_name=hover_names,
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_traces(customdata=spotify_acousitc_df['artist(s)_name'])

    fig.update_layout(
        height=450,
        width=800,
        hovermode='closest',
    )
    return fig

def live_scatter(gradient):
    hover_names = [] 
    for ix, val in zip(spotify_df.index.values, spotify_df['artist(s)_name'].values):
        hover_names.append(f'{ix} by <br>{val}')

    fig = px.scatter(
        spotify_df,
        x='liveness_%', 
        y='speechiness_%',
        opacity=0.8,
        template='plotly_dark',
        color='speechiness_%',
        size='streams',
        color_continuous_scale=gradient,
        hover_name=hover_names,
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_traces(customdata=spotify_df['artist(s)_name'])

    fig.update_layout(
        height=450,
        width=800,
        hovermode='closest'
    )

    return fig

@callback(
    Output(component_id='bar_chart', component_property='figure'),
    [
        Input(component_id='chart', component_property= 'hoverData')
    ]
)

def build_barchart(hoverData):
    t = hoverData.get('points')
    artist_hover = (t[0].get('customdata'))
    spotify_artists = spotify_df[spotify_df['artist(s)_name'] == artist_hover]
    spotify_artists = spotify_artists[['artist(s)_name', 'streams']]
    print(spotify_artists)
    
    # fig = px.bar
    # (spotify_artists,
    #     x='artist(s)_name',
    #     y='streams',
    #     color='streams',
    #     template='plotly_dark',
    #     color_continuous_scale='thermal'
    # )

    # hover_artist = hoverData.get('hovertext')
    # print(hover_artist)
    return None
    
if __name__ == "__main__":
    app.run(debug=True)