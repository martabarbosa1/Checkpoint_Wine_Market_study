### Imports
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, dash_table
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
df_croix_knr_filled = pd.read_csv('Documents/GitHub/Checkpoint_Wine_Market_study/Data/df_croix_knr_filled.csv')
knr_price_pinot_noir_croix = df_croix_knr_filled[df_croix_knr_filled['variety'] == 'Pinot Noir']['price'].mean()
knr_price_Chardonnay_croix = df_croix_knr_filled[df_croix_knr_filled['variety'] == 'Chardonnay']['price'].mean()
price_pinot_noir_all = df_all[df_all['variety'] == 'Pinot Noir']['price'].mean()
price_Chardonnay_all = df_all[df_all['variety'] == 'Chardonnay']['price'].mean()

#to plot for numerical ML
df_to_plot_knr = pd.DataFrame({'variety' : ['Pinot Noir', 'Chardonay'], 'all' : [price_pinot_noir_all, price_Chardonnay_all], 'croix' : [knr_price_pinot_noir_croix, knr_price_Chardonnay_croix ]}).set_index('variety')

#croix dataset with predicted price from categories ML
df_final_croix = pd.read_csv('Documents/GitHub/Checkpoint_Wine_Market_study/Data/df_final_croix.csv')
price_pinot_noir_croix = df_final_croix[df_final_croix['variety'] == 'Pinot Noir']['price'].mean()
price_Chardonnay_croix = df_final_croix[df_final_croix['variety'] == 'Chardonnay']['price'].mean()

#to plot for category ML
df_to_plot = pd.DataFrame({'variety' : ['Pinot Noir', 'Chardonay'], 'all' : [price_pinot_noir_all, price_Chardonnay_all], 'croix' : [price_pinot_noir_croix, price_Chardonnay_croix]}).set_index('variety')

#dfs for table
df_num = pd.DataFrame({'R2 X_train, y_train' : 0.44, 'R2 X_test, y_test' : 0.35, 'MSE' : 464.9, 'index' : [0]}).set_index('index')
df_cat = pd.DataFrame({'R2 X_train, y_train' : 0.58, 'R2 X_test, y_test' : 0.48, 'MSE' : 398.3, 'index' : [0]}).set_index('index')

df_diff_num = pd.DataFrame({'variety' : ['Pinot Noir', 'Chardonay'], 'diff croix - all' : [50.79, 59.90]})
df_diff_cat = pd.DataFrame({'variety' : ['Pinot Noir', 'Chardonay'], 'diff croix - all' : [18.68, 55.49]})

#graphs
fig1 = px.bar(df_to_plot_knr, x = df_to_plot_knr.index, y = ['all', 'croix'], barmode='group', color_discrete_map = {
                    'all' : 'steelblue',
                    'croix' : 'goldenrod'},
                    labels={
                     "value": "price ($)"},)
fig1.update_layout(plot_bgcolor='white')
fig1.update_xaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
)
fig1.update_yaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
)


fig2 = px.bar(df_to_plot, x = df_to_plot .index, y = ['all', 'croix'], barmode='group', color_discrete_map = {
                    'all' : 'steelblue',
                    'croix' : 'goldenrod'},
                    labels={
                     "value": "price ($)"},)
fig2.update_layout(plot_bgcolor='white')
fig2.update_xaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
)
fig2.update_yaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
)


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
        dbc.Row(
                [
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-num'),
                    figure=fig1)),
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-cat'),
                    figure=fig2)),
                ]
                ),
        dbc.Row(
                [
                dbc.Col(dbc.Table.from_dataframe(df_num, striped=True, bordered=True, hover=True,id='num_tb')),
                dbc.Col(dbc.Table.from_dataframe(df_cat, striped=True, bordered=True, hover=True,id='cat_tb')),
                ]
                ),
        dbc.Row(
                [
                dbc.Col(dbc.Table.from_dataframe(df_diff_num, striped=True, bordered=True, hover=True,id='num_tb')),
                dbc.Col(dbc.Table.from_dataframe(df_diff_cat, striped=True, bordered=True, hover=True,id='cat_tb')),
                ]
                ),
    ]
)



# ### Callbacks
# ## Fig1:Map
# @callback(
#     Output('fig-n-wines-country-map', 'figure'),
#     Input('variety-dropdown', 'value'))

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
