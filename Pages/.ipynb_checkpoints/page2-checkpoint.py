### Imports
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, dash_table, ctx
import pandas as pd
import plotly.express as px
from PIL import Image

### Link
dash.register_page(__name__, name = 'Predict wine price')

### Load the datasets
#all dataset
df_all = pd.read_csv('https://raw.githubusercontent.com/martabarbosa1/Checkpoint_Wine_Market_study/main/Data/df_all_clean.csv')
df_all['country'] = df_all['country'].replace(['US'],'United States')

#croix dataset with predicted price from numerical ML
df_croix_dt_filled = pd.read_csv('https://raw.githubusercontent.com/martabarbosa1/Checkpoint_Wine_Market_study/main/Data/df_croix_knr_filled.csv')
dt_price_pinot_noir_croix = df_croix_dt_filled[df_croix_dt_filled['variety'] == 'Pinot Noir']['price'].mean()
dt_price_Chardonnay_croix = df_croix_dt_filled[df_croix_dt_filled['variety'] == 'Chardonnay']['price'].mean()
price_pinot_noir_all = df_all[df_all['variety'] == 'Pinot Noir']['price'].mean()
price_Chardonnay_all = df_all[df_all['variety'] == 'Chardonnay']['price'].mean()
price_burgundy_all = df_all[df_all['province'] == 'Burgundy']['price'].mean()
price_burgundy_pinot_noir_all = df_all[(df_all['province'] == 'Burgundy') & (df_all['variety'] == 'Pinot Noir')]['price'].mean()
price_burgundy_chardonnay_all = df_all[(df_all['province'] == 'Burgundy') & (df_all['variety'] == 'Chardonnay')]['price'].mean()

#to plot for numerical ML
df_to_plot_dt = pd.DataFrame({'variety' : ['Pinot Noir', 'Chardonay'], 'all' : [price_pinot_noir_all, price_Chardonnay_all], 'croix' : [dt_price_pinot_noir_croix, dt_price_Chardonnay_croix], 'Burgundy' : [price_burgundy_pinot_noir_all, price_burgundy_chardonnay_all]}).set_index('variety')

#croix dataset with predicted price from categories ML
df_final_croix = pd.read_csv('https://raw.githubusercontent.com/martabarbosa1/Checkpoint_Wine_Market_study/main/Data/df_final_croix.csv')
price_pinot_noir_croix = df_final_croix[df_final_croix['variety'] == 'Pinot Noir']['price'].mean()
price_Chardonnay_croix = df_final_croix[df_final_croix['variety'] == 'Chardonnay']['price'].mean()
price_pinot_noir_all = df_all[df_all['variety'] == 'Pinot Noir']['price'].mean()
price_Chardonnay_all = df_all[df_all['variety'] == 'Chardonnay']['price'].mean()
price_burgundy_pinot_noir_all = df_all[(df_all['province'] == 'Burgundy') & (df_all['variety'] == 'Pinot Noir')]['price'].mean()
price_burgundy_chardonnay_all = df_all[(df_all['province'] == 'Burgundy') & (df_all['variety'] == 'Chardonnay')]['price'].mean()

#to plot for category ML
df_to_plot = pd.DataFrame({'variety' : ['Pinot Noir', 'Chardonay'], 'all' : [price_pinot_noir_all, price_Chardonnay_all], 'croix' : [price_pinot_noir_croix, price_Chardonnay_croix], 'Burgundy' : [price_burgundy_pinot_noir_all, price_burgundy_chardonnay_all]}).set_index('variety')


#can the points be affecting most?
#croix dataset with predicted price from num ML
points_pinot_noir_croix = df_croix_dt_filled[df_croix_dt_filled['variety'] == 'Pinot Noir']['points'].mean()
points_Chardonnay_croix = df_croix_dt_filled[df_croix_dt_filled['variety'] == 'Chardonnay']['points'].mean()
points_pinot_noir_all = df_all[df_all['variety'] == 'Pinot Noir']['points'].mean()
points_Chardonnay_all = df_all[df_all['variety'] == 'Chardonnay']['points'].mean()
points_burgundy_pinot_noir_all = df_all[(df_all['province'] == 'Burgundy') & (df_all['variety'] == 'Pinot Noir')]['points'].mean()
points_burgundy_chardonnay_all = df_all[(df_all['province'] == 'Burgundy') & (df_all['variety'] == 'Chardonnay')]['points'].mean()

df_to_plot_points_num = pd.DataFrame({'variety' : ['Pinot Noir', 'Chardonay'], 'all' : [points_pinot_noir_all, points_Chardonnay_all], 'croix' : [points_pinot_noir_croix, points_Chardonnay_croix ], 'Burgundy' : [points_burgundy_pinot_noir_all, points_burgundy_chardonnay_all]}).set_index('variety')

#croix dataset with predicted price from categories ML
points_pinot_noir_croix = df_final_croix[df_final_croix['variety'] == 'Pinot Noir']['points'].mean()
points_Chardonnay_croix = df_final_croix[df_final_croix['variety'] == 'Chardonnay']['points'].mean()
points_pinot_noir_all = df_all[df_all['variety'] == 'Pinot Noir']['points'].mean()
points_Chardonnay_all = df_all[df_all['variety'] == 'Chardonnay']['points'].mean()
points_burgundy_pinot_noir_all = df_all[(df_all['province'] == 'Burgundy') & (df_all['variety'] == 'Pinot Noir')]['points'].mean()
points_burgundy_chardonnay_all = df_all[(df_all['province'] == 'Burgundy') & (df_all['variety'] == 'Chardonnay')]['points'].mean()

df_to_plot_points = pd.DataFrame({'variety' : ['Pinot Noir', 'Chardonay'], 'all' : [price_pinot_noir_all, price_Chardonnay_all], 'croix' : [price_pinot_noir_croix, price_Chardonnay_croix], 'Burgundy' : [price_burgundy_pinot_noir_all, price_burgundy_chardonnay_all]}).set_index('variety')

#dfs for table
df_num = pd.DataFrame({'R2 X_train, y_train' : 0.44, 'R2 X_test, y_test' : 0.35, 'MSE' : 464.9, 'index' : [0]}).set_index('index')
df_cat = pd.DataFrame({'R2 X_train, y_train' : 0.58, 'R2 X_test, y_test' : 0.48, 'MSE' : 398.3, 'index' : [0]}).set_index('index')

# df_diff_num = pd.DataFrame({'variety' : ['Pinot Noir', 'Chardonay'], 'diff croix - all' : [50.79, 59.90]})
# df_diff_cat = pd.DataFrame({'variety' : ['Pinot Noir', 'Chardonay'], 'diff croix - all' : [18.68, 55.49]})


###design
layout = html.Div(
    [
        dbc.Row([html.H1("Predict wine price"), 
                ]),
        dbc.Row([html.Br()]),
        dbc.Row(
                [
                dbc.Col(html.H5("ML: Numerical")),
                dbc.Col(html.H5("ML: Categories")),
                ]
                ),
        dbc.Row([html.Br()]),
        dbc.Row(
                [
                dbc.Col(html.H5("Best evaluation: DecisionTreeRegressor()")),
                dbc.Col(html.H5("Best evaluation: KNN regressor() + robustScaler()")),
                ]
                ),
        dbc.Row([html.Br()]),
        dbc.Row(
                [
                dbc.Col(dbc.Table.from_dataframe(df_num, striped=True, bordered=True, hover=True,id='num_tb')),
                dbc.Col(dbc.Table.from_dataframe(df_cat, striped=True, bordered=True, hover=True,id='cat_tb')),
                ]
                ),
        dbc.Row(
                [
                dbc.Col(html.Button('Show graph', id='btn-nclicks-1', n_clicks=0)),
                dbc.Col(html.Button('Show graph', id='btn-nclicks-2', n_clicks=0)),
                ]    
                ),
        dbc.Row(
                [
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-num')), width=6),
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-cat')), width=6),
                ]
                ),
        dbc.Row(
                [
                dbc.Col(html.Button('Show graph', id='btn-nclicks-3', n_clicks=0)),
                ]    
                ),
        dbc.Row(
                [
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-cat-points'))),
                ]
                ),
    ]
)


### Callbacks
## Show figures
@callback(
    Output('fig-num', 'figure'),
    Input('btn-nclicks-1', 'n_clicks'),
)
def displayClick(btn1):
    if "btn-nclicks-1" == ctx.triggered_id:
        fig = px.bar(df_to_plot_dt, x = df_to_plot_dt.index, y = ['all', 'Burgundy', 'croix'], barmode='group', color_discrete_map = {
                            'all' : 'steelblue',
                            'croix' : 'goldenrod',
                            'Burgundy' : 'mediumaquamarine'},
                            labels={
                             "value": "price ($)"},)
        fig.update_layout(plot_bgcolor='white')
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
        )
    return fig

@callback(
    Output('fig-cat', 'figure'),
    Input('btn-nclicks-2', 'n_clicks'),
)
def displayClick(btn1):
    if "btn-nclicks-2" == ctx.triggered_id:
        fig = px.bar(df_to_plot, x = df_to_plot .index, y = ['all', 'Burgundy', 'croix'], barmode='group', color_discrete_map = {
                            'all' : 'steelblue',
                            'croix' : 'goldenrod',
                            'Burgundy' : 'mediumaquamarine'},
                            labels={
                             "value": "price ($)"},)
        fig.update_layout(plot_bgcolor='white')
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
        )
    return fig

# @callback(
#     Output('fig-num-points', 'figure'),
#     Input('btn-nclicks-3', 'n_clicks'),
# )
# def displayClick(btn1):
#     if "btn-nclicks-3" == ctx.triggered_id:
#         fig = px.bar(df_to_plot_points_num, x = df_to_plot_points_num.index, y = ['all', 'Burgundy', 'croix'], barmode='group', color_discrete_map = {
#                             'all' : 'steelblue',
#                             'croix' : 'goldenrod',
#                             'Burgundy' : 'mediumaquamarine'},
#                             labels={
#                              "value": "points"},)
#         fig.update_layout(plot_bgcolor='white')
#         fig.update_xaxes(
#             mirror=True,
#             ticks='outside',
#             showline=True,
#             linecolor='black',
#         )
#         fig.update_yaxes(
#             mirror=True,
#             ticks='outside',
#             showline=True,
#             linecolor='black',
#             range = [85,96]
#         )
#     return fig

@callback(
    Output('fig-cat-points', 'figure'),
    Input('btn-nclicks-3', 'n_clicks'),
)
def displayClick(btn1):
    if "btn-nclicks-3" == ctx.triggered_id:
        fig = px.bar(df_to_plot_points, x = df_to_plot_points.index, y = ['all', 'Burgundy', 'croix'], barmode='group', color_discrete_map = {
                            'all' : 'steelblue',
                            'croix' : 'goldenrod',
                            'Burgundy' : 'mediumaquamarine'},
                            labels={
                             "value": "points"},)
        fig.update_layout(plot_bgcolor='white')
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
        )
    return fig
# def update_figure1(selected_variety):
#     if selected_variety == 'All':
#         data = df_all.pivot_table(values =['title', 'variety'], 
#                                     index = 'country', 
#                                     aggfunc = {'title': 'count','variety': 'count'}).sort_values(by = 'title', ascending = False)
#         data.rename(columns = {'title' : 'count'}, inplace = True)
        
#     else:
#         df_filt = df_all[df_all['variety'] == selected_variety]
#         data = df_filt.pivot_table(values =['title', 'variety'], 
#                                     index = 'country', 
#                                     aggfunc = {'title': 'count','variety': 'count'}).sort_values(by = 'title', ascending = False)
#         data.rename(columns = {'title' : 'count'}, inplace = True)
        
#     fig = px.choropleth(locations=data.index, 
#                     locationmode='country names', 
#                     scope="world", 
#                     color=data['count'],
#                     # title="Number of wines produced by country",  
#                     labels={'color':'#wines'})
#     fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
    
#     return fig

# ## Fig2:barplot yearx#wines
# @callback(
#     Output('fig-n-wines-year', 'figure'),
#     Input('variety-dropdown', 'value'))

# def update_figure2(selected_variety):
#     if selected_variety == 'All':
#         data = df_all.pivot_table(values =['price', 'points', 'title'], 
#                                             index = 'year', 
#                                             aggfunc={'price': 'mean',
#                                             'points': 'mean', 'title' : 'count'}).sort_values(by = 'price', ascending = False)
#         data.rename(columns = {'title' : 'count'}, inplace = True)


#     else:
#         df_filt = df_all[df_all['variety'] == selected_variety]    
#         data = df_filt.pivot_table(values =['price', 'points', 'title'], 
#                                             index = 'year', 
#                                             aggfunc={'price': 'mean',
#                                             'points': 'mean', 'title' : 'count'}).sort_values(by = 'price', ascending = False)
#         data.rename(columns = {'title' : 'count'}, inplace = True)
        
    
#     fig = px.line(data, x = data.index, y = 'count')
#     fig.update_yaxes(range=[0, 16000])
    
#     return fig



# ## Fig3:barplot countryxprice
# @callback(
#     Output('fig-price-wines-country', 'figure'),
#     Input('variety-dropdown', 'value'))

# def update_figure2(selected_variety):
#     if selected_variety == 'All':
#         data = df_all.pivot_table(values =['price', 'points'], 
#                                                 index = 'country', 
#                                                 aggfunc={'price': 'mean',
#                              'points': 'mean'}).sort_values(by = 'price', ascending = False)

#     else:
#         df_filt = df_all[df_all['variety'] == selected_variety]    
#         data = df_filt.pivot_table(values =['price', 'points'], 
#                                                 index = 'country', 
#                                                 aggfunc={'price': 'mean',
#                              'points': 'mean'}).sort_values(by = 'price', ascending = False)
        
    
#     fig = px.bar(data, x = data.index, y = 'price', color='points')
    
#     return fig

# ## Fig4:barplot yearxprice
# @callback(
#     Output('fig-price-wines-year', 'figure'),
#     Input('variety-dropdown', 'value'))

# def update_figure2(selected_variety):
#     if selected_variety == 'All':
#         data = df_all.pivot_table(values =['price', 'points', 'title'], 
#                                                         index = 'year', 
#                                                         aggfunc={'price': 'mean',
#                                      'points': 'mean', 'title' : 'count'}).sort_values(by = 'price', ascending = False)

#     else:
#         df_filt = df_all[df_all['variety'] == selected_variety]    
#         data = df_filt.pivot_table(values =['price', 'points', 'title'], 
#                                                         index = 'year', 
#                                                         aggfunc={'price': 'mean',
#                                      'points': 'mean', 'title' : 'count'}).sort_values(by = 'price', ascending = False)

#     fig = px.bar(data, x = data.index, y = 'price', color='points')
    
#     return fig
