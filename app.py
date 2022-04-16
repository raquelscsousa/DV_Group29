######################################################### IMPORTS #####################################################
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

explor_ = pd.read_excel(r'https://github.com/raquelscsousa/DV_Group29/blob/main/data/DV_Dataset.xlsx', engine='openpyxl')
explor_['GDP per capita'] = explor_['GDP'] / explor_['POP']

df = explor_.loc[:].copy()
df['GDP_PC'] = df['GDP'] / df['POP']

country_options = [
    dict(label='Country ' + country, value=country)
    for country in explor_['Country'].unique()]

region_options = [
    dict(label='region ' + region, value=region)
    for region in explor_['sub-region'].unique()]

year_options = [
    dict(label='Year ' + Year, value=Year)
    for Year in explor_['Year'].unique().astype(str)]

indicator_options = [
    dict(label='Indicators ' + var, value=var)
    for var in explor_.columns[-14:]]

###################### APP Structure
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([  # main container
    #### Title container
    html.Div([
        html.Div([
            html.H1('Employment Reality in Europe'),
            html.P('What is the best and the worst country to start a career?',
                   style={'padding-left': '0px', 'margin-top': '25px'}),
        ], id='Title Box'),

        html.Div([
            html.Img(src=app.get_asset_url('pic.png'),
                     style={'width': '70%', 'float': 'right', 'padding-left': '520px'}),
        ]),
    ], className='header'),

    #### First Row container
    html.H4('Select...'),
    html.Div([
        #### Country dropdown
        html.Div([
            html.H5('Country', style={'padding-left': '280px', 'padding-bottom': '4px'}),
            dcc.Dropdown(options=country_options,
                         id='country_drop',
                         value=explor_['Country'].unique(),
                         multi=True,
                         style={'border-color': '#005dae'}
                         ),
        ], style={'width': '40%', 'margin-left': '20px'}, className='dropdown'),

        html.Br(),

        #### Year Radio Items
        html.Div([
            html.H5('Year', style={'padding-bottom': '4px', 'padding-left': '220px'}),
            dbc.RadioItems(id='year_drop', className='radio',
                           options=[dict(label='2014', value=1), dict(label='2016', value=2),
                                    dict(label='2018', value=3), dict(label='All', value=4)],
                           value=4,
                           inline=True,
                           label_checked_style={"color": "#004684"}
                           ),

        ], style={'width': '30%', 'margin-left': '60px'}),

        html.Br(),

        #### Region Checklist
        html.Div([
            html.H5('Region', style={'padding-left': '100px'}),
            dbc.Checklist(
                options=region_options,
                value=explor_['sub-region'].unique(),
                id='region_drop',
                label_checked_style={"color": "black"},
                input_checked_style={
                    "backgroundColor": "#005dae",
                    "borderColor": "#004684",
                },
                style={'color': 'black'}
            ),
        ], style={'width': '20%'}),

        html.Br(),

    ], style={'display': 'flex', 'width': '100%'}),

    html.Br(),

    #### First row of graphics
    html.Div(
        [
            #### Poverty Graph + button
            html.Div([
                dcc.Graph(id='poverty_', style={'margin-bottom': '10px', 'align': 'center'}),
                dbc.Button(
                    "+Info",
                    id="poverty_button",
                    n_clicks=0,
                    outline=True, color="info",
                    className="me-1"
                ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Graph and metric information"),
                        dbc.PopoverBody(
                            "Relative Income Poverty: % of people whose household income is below 50% of the "
                            "national mean."),
                        dbc.PopoverBody("Total Employment: Average annual hours worked. Here divided by 100 so to be "
                                        "incorporated in the same scale."),
                    ],
                    trigger="hover",
                    target="poverty_button",
                ),
            ], className='graph_box'),

            #### Dependents Graph + button
            html.Div([

                dcc.Graph(id='dependents_', style={'margin-bottom': '10px', 'align': 'center'}),
                dbc.Button(
                    "+Info",
                    id="dependents_button",
                    n_clicks=0,
                    outline=True, color="info",
                    className="me-1"
                ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Graph and metric information"),
                        dbc.PopoverBody("Total Employment: Average annual hours worked."),
                        dbc.PopoverBody("Dependent Employment: Average annual hours worked as a dependent employee."),
                        dbc.PopoverBody("GDP per capita: Ratio between the total GDP and total Population"),
                    ],
                    trigger="hover",
                    target="dependents_button",

                ),

            ], className='graph_box'),

        ], id="Graph Box Row 1", className='containers'),

    html.Br(),

    #### Second row of graphics
    html.Div(
        [
            html.Div([
                #### Ends meet graph + button
                dcc.Graph(id='ends_meet_', style={'margin-bottom': '10px', 'align': 'center'}),
                dbc.Button(
                    "+Info",
                    id="ends_button",
                    n_clicks=0,
                    outline=True, color="info",
                    className="me-1"
                ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Graph and metric information"),
                        dbc.PopoverBody(
                            "Difficulty in making ends meet: % of households that report difficulty in making ends meet."),
                    ],
                    target="ends_button",
                    trigger="hover",
                ),

            ], className='graph_box'),

            #### Map plot + button
            html.Div([

                dcc.Graph(id='map_plot_', style={'margin-bottom': '10px', 'align': 'center'}),
                dbc.Button(
                    "+Info",
                    id="map_button",
                    n_clicks=0,
                    outline=True, color="info",
                    className="me-1"
                ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Graph and metric information"),
                        dbc.PopoverBody("Long-term unemployment rate: Number of people who have been unemployed "
                                        "for one year or more, as a % of the labour force ("
                                        "employed + unemployed)."),
                    ],
                    target="map_button",
                    trigger="hover",
                ),
            ], className='graph_box'),

        ], id="Graph Box Row 2", className='containers'),

    html.Br(),

    #### Third row of graphics
    html.Div(
        [
            #### Senior Young plot + button
            html.Div([

                dcc.Graph(id='senior_young_', style={'margin-bottom': '10px', 'align': 'center'}),
                dbc.Button(
                    "+Info",
                    id="senior_button",
                    n_clicks=0,
                    outline=True, color="info",
                    className="me-1"
                ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Graph and metric information"),
                        dbc.PopoverBody("Senior over prime-age: wage gaps defined as the difference between mean ("
                                        "median) earnings of 25-54 year-olds (prime age) and that of 55-64 "
                                        "year-olds."),
                        dbc.PopoverBody(
                            "Youth over prime-age: wage gaps defined as the difference between mean (median) earnings of 25-54 year-olds (prime age) and that of 15-24 year-olds. "),
                    ],
                    target="senior_button",
                    trigger="hover",
                ),
            ], className='graph_box'),

            #### Long hours plot + button
            html.Div([

                dcc.Graph(id='long_hours', style={'margin-bottom': '10px', 'align': 'center'}),
                dbc.Button(
                    "+Info",
                    id="long_button",
                    n_clicks=0,
                    outline=True, color="info",
                    className="me-1"
                ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Graph and metric information"),
                        dbc.PopoverBody("Average Wage: Average annual salary in US dollars."),
                        dbc.PopoverBody(
                            "Long hours in paid work: % of employees (all ages) whose usual working hours are 50h+ per week."),
                    ],
                    target="long_button",
                    trigger="hover",
                ),
            ], className='graph_box'),

        ], id="Graph Box Row 3", className='containers')

    ,

    #### Footer
    html.Div([

        html.P(['Team 29:', html.Br(),
                'Alice Vale r20181074 | Eva Ferrer r20181110 | Rafael Sequeira r20181128 | Raquel Sousa r20181102'],
               style={'width': '60%'}),
        html.P(['Sources:', html.Br(), html.A('OECD', href='https://data.oecd.org/jobs.htm', style={'color': 'white'})],
               style={'width': '10%'}),
        html.Img(src=app.get_asset_url('logo-branco.png'),
                 style={'width': '32%', 'float': 'right', 'padding-left': '500px'}),
    ], className='footer'),

], style={'background-color': '#eff7fd', 'width': '100%'})


######Callback

@app.callback(
    Output('poverty_', 'figure'),
    Output('dependents_', 'figure'),
    Output('ends_meet_', 'figure'),
    Output('map_plot_', 'figure'),
    Output('senior_young_', 'figure'),
    Output('long_hours', 'figure'),

    Input('country_drop', 'value'),
    Input('year_drop', 'value'),
    Input('region_drop', 'value')
)
def update_graph(country, year, region):
    if year == 1:
        year = [2014]
    elif year == 2:
        year = [2016]
    elif year == 3:
        year = [2018]
    elif year == 4:
        year = explor_['Year'].unique()

    dff = explor_[
        (explor_['Country'].isin(country)) & (explor_['Year'].isin(year)) & (explor_['sub-region'].isin(region))].copy()
    dff['Total employment1'] = dff['Total employment'] / 100
    dff['Year'] = dff['Year'].astype(str)

    dff1 = explor_[
        (explor_['Country'].isin(country)) & (explor_['Year'].isin(year) & (explor_['sub-region'].isin(region)))].copy()
    dff1['Year'] = dff1['Year'].astype(str)

    # poverty vs employment
    poverty = px.bar(data_frame=dff,
                     x='Country',
                     y='Relative income poverty ',
                     barmode='group', color='Year',
                     color_discrete_sequence=[
                         'rgb(127, 60, 141)' if year == '2014' else ('rgb(17, 165, 121)' if year == '2016'
                                                                     else (
                             'rgb(57, 105, 172)' if year == '2018' else 'rgb(242, 183, 1)')) for
                         year in dff['Year']])

    employment = px.line(data_frame=dff,
                         x='Country',
                         y='Total employment1',
                         color_discrete_sequence=[
                             'rgb(127, 60, 141)' if year == '2014' else ('rgb(17, 165, 121)' if year == '2016'
                                                                         else (
                                 'rgb(57, 105, 172)' if year == '2018' else 'rgb(242, 183, 1)')) for
                             year in dff['Year']],
                         color='Year', title='Poverty Comparison')

    poverty.layout.xaxis.title = "Countries"
    poverty.layout.yaxis.title = "Values"
    poverty.add_traces(employment.data)
    poverty.layout.title = 'Relative Income Poverty and Total Employment'

    # Total vs dependent employment
    dependents = px.scatter(
        data_frame=dff,
        x="Total employment",
        y="Dependent employment",
        size="GDP per capita",
        hover_name="Country",
        size_max=60,
        color='sub-region', title='Total vs Dependent Employment accounting for GDP per capita',
        color_discrete_sequence=px.colors.qualitative.Bold,
    )

    # ends meet
    ends_meet = px.bar(data_frame=dff1,
                       x='Country',
                       y='Difficulty making ends meet',
                       color='Year',
                       barmode='group',
                       title='Percentage of people who report having difficulty in making ends meet',
                       color_discrete_sequence=[
                           'rgb(127, 60, 141)' if year == '2014' else ('rgb(17, 165, 121)' if year == '2016'
                                                                       else (
                               'rgb(57, 105, 172)' if year == '2018' else 'rgb(242, 183, 1)')) for
                           year in dff['Year']], )
    ends_meet.layout.xaxis.title = 'Countries'
    ends_meet.layout.yaxis.title = 'Percentage'

    # map
    dff2 = explor_[
        (explor_['Country'].isin(country)) & (explor_['Year'].isin(year) & (explor_['sub-region'].isin(region)))].copy()
    data_choropleth = dict(type='choropleth',
                           locations=dff2['Country'],
                           autocolorscale=False,
                           locationmode='country names',
                           z=np.log(dff2['Long-term unemployment rate']),
                           text=dff2['Country'],
                           colorscale=['#ADD5F7', '#133463']
                           )

    layout_choropleth = dict(geo=dict(scope='europe',
                                      projection=dict(type='natural earth'),
                                      landcolor='grey',
                                      lakecolor='white',
                                      oceancolor='azure'
                                      ),
                             title=dict(text='Long-term unemployment rate')
                             )
    fig_choropleth = go.Figure(data=data_choropleth, layout=layout_choropleth)
    fig_choropleth.update_layout(margin=dict(l=25, r=25, t=70, b=25))

    # Senior vs Youth
    senior_young = px.bar(data_frame=dff,
                          x=['Senior over Prime-age', 'Youth over Prime-age'],
                          y='Country',
                          orientation='h',
                          barmode='group',
                          title='Wage gap between Prime-Age and Senior/Youth',
                          color_discrete_sequence=px.colors.qualitative.Bold)

    # Long Hours and avg wage
    dff1['Long hours in paid work'] = dff['Long hours in paid work']
    long_hours = px.scatter(data_frame=dff1,
                            x='Country',
                            y='AVWAGE',
                            size='Long hours in paid work',
                            color='Year',
                            title='Average Wage accounting for Long working hours',
                            color_discrete_sequence=[
                                'rgb(127, 60, 141)' if year == '2014' else ('rgb(17, 165, 121)' if year == '2016'
                                                                            else (
                                    'rgb(57, 105, 172)' if year == '2018' else 'rgb(242, 183, 1)')) for
                                year in dff['Year']], )

    long_hours.layout.yaxis.title = 'Average Wage'
    long_hours.layout.xaxis.title = 'Countries'

    return poverty, dependents, ends_meet, fig_choropleth, senior_young, long_hours


if __name__ == '__main__':
    app.run_server(debug=True)
