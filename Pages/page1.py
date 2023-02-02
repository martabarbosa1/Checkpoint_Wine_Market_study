### Imports
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
import pandas as pd
import plotly.express as px
from PIL import Image

### Link
dash.register_page(__name__,path='/', name = 'Wine Market Overview') #slash is homepage

### Load the datasets
df_all = pd.read_csv('https://raw.githubusercontent.com/martabarbosa1/Checkpoint_Wine_Market_study/main/Data/df_all_clean.csv')
df_all['country'] = df_all['country'].replace(['US'],'United States')

df_croix = pd.read_csv('https://raw.githubusercontent.com/martabarbosa1/Checkpoint_Wine_Market_study/main/Data/df_croix_clean.csv')

###dropdown list
dropdown_list = [{'label' : 'All', 'value': 'All'}, {'label' : 'Pinot Noir', 'value' : 'Pinot Noir'}]


###design
layout = html.Div(
    [
        dbc.Row([html.H1("Wine Market Overview"), 
                ]),
        dbc.Row([html.Br()]),
        dbc.Row([
                dcc.Dropdown(
                id = 'variety-dropdown', 
                placeholder = 'Select the variety',
                options = dropdown_list),        
        ]),
        dbc.Row([html.Br()]),
        dbc.Row(
                [
                dbc.Col(html.Div(html.H5("Number of wines by country")),
                       width=7),
                    # style={'textAlign': 'center'})]),   
                dbc.Col(html.H5("Number of wines per year")),
                ]
                ),
        dbc.Row(
                [
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-n-wines-country-map')),
                    # figure=fig)), 
                    width=7),   
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-n-wines-year')),
                    width=5
                        )
                ]
                ),
        dbc.Row([html.Br()]),
        dbc.Row(
                [
                dbc.Col(html.Div(html.H5("Price&Points of wines by country")),
                       width=7),
                    # style={'textAlign': 'center'})]),   
                dbc.Col(html.H5("Price&Points of wines per year")),
                ]
                ),
        dbc.Row(
                [
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-price-wines-country')),
                    # figure=fig)),
                    width=7
                    ),
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-price-wines-year')),
                    # figure=fig)),
                    width=5
                    ),
                ]),
        dbc.Row(
                [
                dbc.Col(html.Div(html.H5("All wines description"))),
                dbc.Col(html.Div(html.H5("Pinot Noir description"))),
                dbc.Col(html.Div(html.H5("Burgundy province description"))),   
                ]),
        dbc.Row(
                [
                dbc.Col(html.Img(src=r'assets/bottle_all_wordcloud.png', alt='image')),
                dbc.Col(html.Img(src=r'assets/bottle_pinot_noir_wordcloud.png', alt='image')),
                dbc.Col(html.Img(src=r'assets/bottle_burgundy_wordcloud.png', alt='image')),   
                ])
    ]
)

#         dbc.Row([html.Br()]),
#         dbc.Row(
#             # [
#             #     dbc.Col(html.Div(
#             #         dcc.Graph(id='fig-auth1'),),md=6,),
#             #     dbc.Col(html.Div(
#             #         dcc.Graph(id='fig-auth2'),),md=6,),
#             # ]
#         ),
#         dbc.Row([html.Br()]),
#         dbc.Row(dbc.Col(html.Div(html.H5(["Restaurants"])))),
#         dbc.Row(
#             [
#                 # dbc.Col(html.Div(
#                 #     dcc.Graph(id='fig-auth4'),),md=6,),
#                 # dbc.Col(html.Div(
#                 #     dcc.Graph(id='fig-auth5'),),md=6,),
#             ]
#         ),

### Callbacks
## Fig1:Map
@callback(
    Output('fig-n-wines-country-map', 'figure'),
    Input('variety-dropdown', 'value'))

def update_figure1(selected_variety):
    if selected_variety == 'All':
        data = df_all.pivot_table(values =['title', 'variety'], 
                                    index = 'country', 
                                    aggfunc = {'title': 'count','variety': 'count'}).sort_values(by = 'title', ascending = False)
        data.rename(columns = {'title' : 'count'}, inplace = True)
        
    else:
        df_filt = df_all[df_all['variety'] == selected_variety]
        data = df_filt.pivot_table(values =['title', 'variety'], 
                                    index = 'country', 
                                    aggfunc = {'title': 'count','variety': 'count'}).sort_values(by = 'title', ascending = False)
        data.rename(columns = {'title' : 'count'}, inplace = True)
        
    fig = px.choropleth(locations=data.index, 
                    locationmode='country names', 
                    scope="world", 
                    color=data['count'],
                    # title="Number of wines produced by country",  
                    labels={'color':'#wines'})
    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
    
    return fig

## Fig2:barplot yearx#wines
@callback(
    Output('fig-n-wines-year', 'figure'),
    Input('variety-dropdown', 'value'))

def update_figure2(selected_variety):
    if selected_variety == 'All':
        data = df_all.pivot_table(values =['price', 'points', 'title'], 
                                            index = 'year', 
                                            aggfunc={'price': 'mean',
                                            'points': 'mean', 'title' : 'count'}).sort_values(by = 'price', ascending = False)
        data.rename(columns = {'title' : 'count'}, inplace = True)


    else:
        df_filt = df_all[df_all['variety'] == selected_variety]    
        data = df_filt.pivot_table(values =['price', 'points', 'title'], 
                                            index = 'year', 
                                            aggfunc={'price': 'mean',
                                            'points': 'mean', 'title' : 'count'}).sort_values(by = 'price', ascending = False)
        data.rename(columns = {'title' : 'count'}, inplace = True)
        
    
    fig = px.line(data, x = data.index, y = 'count')
    fig.update_yaxes(range=[0, 16000])
    
    return fig



## Fig3:barplot countryxprice
@callback(
    Output('fig-price-wines-country', 'figure'),
    Input('variety-dropdown', 'value'))

def update_figure2(selected_variety):
    if selected_variety == 'All':
        data = df_all.pivot_table(values =['price', 'points'], 
                                                index = 'country', 
                                                aggfunc={'price': 'mean',
                             'points': 'mean'}).sort_values(by = 'price', ascending = False)

    else:
        df_filt = df_all[df_all['variety'] == selected_variety]    
        data = df_filt.pivot_table(values =['price', 'points'], 
                                                index = 'country', 
                                                aggfunc={'price': 'mean',
                             'points': 'mean'}).sort_values(by = 'price', ascending = False)
        
    
    fig = px.bar(data, x = data.index, y = 'price', color='points')
    
    return fig

## Fig4:barplot yearxprice
@callback(
    Output('fig-price-wines-year', 'figure'),
    Input('variety-dropdown', 'value'))

def update_figure2(selected_variety):
    if selected_variety == 'All':
        data = df_all.pivot_table(values =['price', 'points', 'title'], 
                                                        index = 'year', 
                                                        aggfunc={'price': 'mean',
                                     'points': 'mean', 'title' : 'count'}).sort_values(by = 'price', ascending = False)

    else:
        df_filt = df_all[df_all['variety'] == selected_variety]    
        data = df_filt.pivot_table(values =['price', 'points', 'title'], 
                                                        index = 'year', 
                                                        aggfunc={'price': 'mean',
                                     'points': 'mean', 'title' : 'count'}).sort_values(by = 'price', ascending = False)

    fig = px.bar(data, x = data.index, y = 'price', color='points')
    
    return fig

# @callback(
#     Output('fig-auth2', 'figure'),
#     Input('demo-dropdown', 'value'))
# def update_figure2(selected_airport):
#     df_filt = df_all[df_all['ORIGIN'] ==selected_airport]
#     dest = df_filt['DEST'].value_counts()
#     fig = px.histogram(data_frame=dest[:10].reset_index(), x='index', y='DEST', color='index')
#     fig.update_yaxes(showticklabels=False)
#     fig.update_layout(title="Major destinations", xaxis_visible=True ,yaxis_visible=False ,showlegend=False,)
#     return fig


# ## Second Row of plots
# @callback(
#     Output('fig-auth4', 'figure'),
#     Input('demo-dropdown', 'value'))
# def update_figure4(selected_airport):
#     rest_5 = restaurants[restaurants['Airport']==selected_airport]['Description'].value_counts()
#     fig = px.pie(data_frame=rest_5.reset_index(), values='Description', names='index',color_discrete_map={'Bar':'blue', 'Grab & Go':'red', 'Coffee':'green', 'Pizza':'purple', 'FastFood':'orange', 'Asian':'turquoise','Restaurant':'pink'}, hole=.5)
#     fig.update_layout(title="Number of Restaurants by Airport")
#     return fig

# @callback(
#     Output('fig-auth5', 'figure'),
#     Input('demo-dropdown', 'value'))
# def update_figure5(selected_airport):
#     df_lax = restaurants[restaurants['Airport'] == selected_airport]
#     top_5_names = df_lax['Name'].value_counts().nlargest(5).index.tolist()
#     df_top_5 = df_lax[df_lax['Name'].isin(top_5_names)]
#     fig = px.histogram(df_top_5, x='Name', color='Description', 
#                    color_discrete_map={'Bar':'blue', 'Grab & Go':'red', 'Coffee':'green', 'Pizza':'purple', 'FastFood':'orange', 'Asian':'turquoise','Restaurant':'pink'})
#     fig.update_layout(title="Number of Restaurants by Airport and Type",xaxis_visible=True ,yaxis_visible=False ,showlegend=False)
#     return fig
