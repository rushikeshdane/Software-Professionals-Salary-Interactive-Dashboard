import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash,Input,Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pycountry
import pandas_datareader.data as web
import datetime
import pathlib
#import pycountry
#import pandas_datareader.data as web
import datetime


# Declare server for Heroku deployment. Needed for Procfile.

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()


df = pd.read_csv(DATA_PATH.joinpath("Salary_Dataset_with_Extra_Features.csv"))

df['Job Roles']= df['Job Roles'].astype("category")
df['Job Roles'] = df['Job Roles'].cat.rename_categories({'Android':'Android developer','Backend':'Backend developer','Database':'Database Administrator ',
                                                               'Frontend':'Frontend developer','IOS':'IOS developer',
                                                               'Java':'Java developer','Mobile':'Mobile developer',
 'Python':'Python developer','Web':'Web developer'})

# supporting functions  ( thig function will help our main function in app for plotting graphs)

# function to create plotly table
def Table(dff):
    data = dff['Company Name'].value_counts().head(20)

    fig = go.Figure()
    fig.add_trace(go.Table(columnwidth=[15, 6],

                           header=dict(values=['<b> Company <b>', '<b>Number of<br>Employees<b>'],
                                       line_color='black', font=dict(color='black', size=14), height=30,
                                       fill_color='lightskyblue',
                                       align=['left', 'center']),
                           cells=dict(values=[data.index, data.values],
                                      fill_color='lightcyan', line_color='grey',
                                      font=dict(color='black', family="Lato", size=15),
                                      align='left')))
    fig.update_layout(
        title={'text': "<b style:'color:blue;'>Top 20 Companys </b>", 'font': {'size': 16}}, title_x=0.5,

        # title_font_family="Times New Roman",
        title_font_color="slategray", margin=dict(l=0, r=0, b=0, t=27))
    return fig


def donut(data):
    fig = px.pie(names=data.index, values=data.values, hole=.5, color_discrete_sequence=px.colors.sequential.Blues_r,
                 height=350)
    fig.update_layout(
        autosize=True, legend_orientation="h",
        legend=dict(x=0.09, y=0., traceorder="normal"),
        title={'text': "<b style:'color:blue;'>Employment Status "
            , 'font': {'size': 16}}, title_x=0.5, title_y=0.97,
        # title_font_family="Times New Roman",
        title_font_color="slategray",
        font_color='slategray',

        # xaxis_title={'text': "<b style:'color:blue;'>Likes</b>", 'font': {'size':15}},
        # yaxis_title={'text': "<b style:'color:blue';></b>", 'font': {'size': 15}},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='lightblue'
        , margin=dict(b=0, l=12, r=12)
    )
    # fig.update_traces(showlegend=False)
    return fig


def salary_meter(data):
    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            {
                'mode': 'gauge+number',
                'number': {'font': {'color': '#1C4E80'}},
                'gauge': {'bar': {'color': 'skyblue'}, 'axis': {'range': [None, 100000]}},

                # 'delta' :{"reference": 100000, "valueformat": ".0f"},
                'value': data['Salary'].mean() / 10
                #     'title' :{'text': 'Rating', 'font': {'size': 20}}
            })
    )
    fig.update_layout(height=170, width=350, margin=dict(t=50, b=10))
    fig.update_layout(title={'text': 'Average Salary', 'font': {'size': 20}}, title_x=0.51, title_y=0.97,
                      title_font_color='dimgray')

    return fig


def location_sorting(df):
    location_count = df.groupby('Location')['Job Roles'].count()
    new_df = pd.DataFrame({'Location': location_count.index, 'Count': location_count.values})
    new_df.reset_index(drop=True, inplace=True)
    return new_df.sort_values('Count', ascending=False)


def meter(data):
    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            {
                'mode': 'gauge+number+delta',
                'number': {'font': {'color': '#1C4E80'}},
                'gauge': {'bar': {'color': 'skyblue'}, 'axis': {'range': [1, 5]}},

                'value': data['Rating'].mean()
                #     'title' :{'text': 'Rating', 'font': {'size': 20}}
            })
    )
    fig.update_layout(height=170, width=350, margin=dict(t=50, b=10))
    fig.update_layout(title={'text': 'Average Rating', 'font': {'size': 21}}, title_x=0.49, title_y=0.97,
                      title_font_color='dimgray')

    return fig


# dash plotly App


app = Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE]

                  , meta_tags=[{'name': 'viewport',
                                'content': 'width=device-width, initial-scale=1.0'}])

server = app.server
#########################################################  Frontend :App Layout  ############################################################################
list_of_job_roles = ['Android developer', 'Backend developer', 'Database Administrator ', 'Frontend developer',
                     'IOS developer', 'Java developer', 'Mobile developer', 'SDE',
                     'Python developer', 'Web developer', 'Testing', 'All']
list_of_location = ['Bangalore', 'Chennai', 'Hyderabad', 'New Delhi', 'Pune', 'Jaipur', 'Kerala', 'Kolkata',
                    'Madhya Pradesh', 'Mumbai', 'All']
dropdown1 = dcc.Dropdown(list_of_job_roles, placeholder='SDE', id='dropdown1', style={'background-color': '#F0FFFF'},
                         multi=False, value='All', className='dropup1')
dropdown2 = dcc.Dropdown(list_of_location, placeholder='All', id='dropdown2', style={'background-color': '#F0FFFF'},
                         multi=False, value='All', className='dropup2')
card = dbc.Card([
    dbc.CardBody([dcc.Graph(figure={}, style={'height': '118px'})
                  ])
], className='mb-2 h-20')
card2 = dbc.Card([dbc.CardHeader(html.H6('Rating')),
                  dbc.CardBody([dcc.Graph(figure={}, style={'height': '400px'})
                                ])
                  ], className='mb-2')

# card1=dcc.Graph(id='rating',figure={}  )
# card2= dbc.Card(dbc.CardBody(  ))
histogram = dbc.Card([
    dbc.CardBody([dcc.Graph(id='hist', figure={}, style={'height': '370px'})
                  ])
], className='mb-2', color='#FCFBFC')

average_salary = dbc.Card([
    dbc.CardBody([dcc.Graph(id='salary', figure={}, style={'height': '167px'})
                  ])
], className='mb-1 ')

rating = dbc.Card([
    dbc.CardBody([dcc.Graph(id='rating', figure={}, style={'height': '167px'})
                  ])
], className='mb-1 ')
barplot = dbc.Card([
    dbc.CardBody([dcc.Graph(id='bar', figure={}, style={'height': '350px'})
                  ])
], className='mr-0 ')

piechart = dbc.Card([
    dbc.CardBody([dcc.Graph(id='pie', figure={}, style={'height': '350px'})
                  ])
], className='mb-1 ')
table = dbc.Card([
    dbc.CardBody([dcc.Graph(id='table', figure={}, style={'height': '350px'})
                  ])
], className='mb-1 ')

# piechart=dcc.Graph(id='pie',figure={})
# barplot=dcc.Graph(id='bar',figure={})
# table=dcc.Graph(id='table',figure={})


app.layout = dbc.Container([dbc.Row(dbc.Col(html.H2(children=' Software Professionals Salary Dashboard  2022',
                                                    className=" text-center p-1 border  border-primary border-top-0  p-2",
                                                    style={'color': 'white', 'background-color': '#1C4E80',
                                                           'font-size': '30px'}), width=12)

                                    ), dbc.Row(),

                            dbc.Row([dbc.Col(html.H5('Select Job Role : ', style={'font-size': '20px','text-align':'right'}),
                                             style={'color': '#1C4E80'}, className='mb-2  mt-2', width=2),
                                     dbc.Col(dropdown1, className='mb-2  mt-1', width=4),
                                     dbc.Col(html.H5('Select Location : ', style={'font-size': '20px','text-align':'right'}),
                                             style={'color': '#1C4E80'}, className='mb-2  mt-2', width=2),
                                     dbc.Col(dropdown2, className='mb-2  mt-1', width=4)

                                     ]),
                            dbc.Row([dbc.Col(histogram, width=8),
                                     dbc.Col(dbc.Row([average_salary, rating]), width=4)

                                     ]),

                            dbc.Row([dbc.Col(barplot, width=4),
                                     dbc.Col(piechart, width=4),
                                     dbc.Col(table, width=4)

                                     ]),
                            dbc.Row(dbc.Col(html.H2('             '
                                                    )))

                            ]

                           , fluid=False, style={'background-color': '#F1F1F1'})


########################################### backend callbacks and functions #####################################################

@app.callback(
    Output('salary', 'figure'),
    [Input('dropdown1', 'value'),
     Input('dropdown2', 'value')]
)
def average_salary(role='All', location='All'):
    if role != 'All':
        temp_df = df[(df['Job Roles'] == role) & (df['Salary'] < 4000000)]
        if location != 'All':
            new_data = temp_df[temp_df['Location'] == location]

            fig = salary_meter(new_data)

        elif location == "All":

            fig = salary_meter(temp_df)
        else:

            fig = salary_meter(temp_df)

        return fig

    else:
        if location != 'All':
            temp_df = df[(df['Location'] == location) & (df['Salary'] < 4000000)]
            fig = salary_meter(temp_df)


        else:
            fig = salary_meter(df)
        return fig


############################################# rating component
@app.callback(
    Output('rating', 'figure'),
    [Input('dropdown1', 'value'),
     Input('dropdown2', 'value')]
)
def rating(role=dropdown1, location=dropdown2):
    if role != 'All':
        temp_df = df[(df['Job Roles'] == role) & (df['Salary'] < 4000000)]
        if location != 'All':
            new_data = temp_df[temp_df['Location'] == location]

            fig = meter(new_data)

        elif location == "All":

            fig = meter(temp_df)
        else:

            fig = meter(temp_df)

        return fig

    else:
        if location != 'All':
            temp_df = df[(df['Location'] == location) & (df['Salary'] < 4000000)]
            fig = meter(temp_df)


        else:
            fig = meter(df)
        return fig


################################################### salary histogram  component
@app.callback(
    Output('hist', 'figure'),
    [Input('dropdown1', 'value'),
     Input('dropdown2', 'value')]
)
def salary_hist(role=dropdown1, location=dropdown2):
    if role != 'All':
        temp_df = df[(df['Job Roles'] == role) & (df['Salary'] < 4000000)]
        if location != 'All':

            fig = px.histogram(temp_df[temp_df['Location'] == location], x='Salary', template='simple_white',
                               color_discrete_sequence=['#1C4E80'],
                               nbins=20, barmode='group')
            fig.update_layout(title={'text': "<b style:'color:blue;'>{0}  Salary at  {1}</b>".format(role, location),
                                     'font': {'size': 16}}, title_x=0.5,
                              # title_font_family="Times New Roman",
                              title_font_color="slategray", margin=dict(b=10, r=40),
                              yaxis_title={'text': "Number of Employees"}, font_color='slategray')
            # ,

            # xaxis_title={'text': "<b style:'color:blue;'>Likes</b>", 'font': {'size':15}},
            #  yaxis_title={'text': "<b style:'color:blue';>Number of Employees </b>"}

            # plot_bgcolor='rgba(0,0,0,0)'


        elif location == "All":
            fig = px.histogram(temp_df, x='Salary', template='simple_white', nbins=20, barmode='group',
                               color_discrete_sequence=['#1C4E80'])
            fig.update_layout(title={'text': "<b style:'color:blue;'>{0} Salary </b>".format(role)
                , 'font': {'size': 16}}, title_x=0.5,
                              # title_font_family="Times New Roman",
                              title_font_color="slategray", margin=dict(b=10, r=40),
                              yaxis_title={'text': "Number of Employees"}, font_color='slategray')
            # font_color='blue',

            # xaxis_title={'text': "<b style:'color:blue;'>Likes</b>", 'font': {'size':15}},
            # yaxis_title={'text': "<b style:'color:blue';></b>", 'font': {'size': 15}},
            # paper_bgcolor='white',
            #         plot_bgcolor='rgba(0,0,0,0)'

        else:

            fig = px.histogram(temp_df, x='Salary', template='simple_white', nbins=20, barmode='group', color=location,
                               color_discrete_sequence=['#1C4E80'])

        return fig

    else:

        if location != 'All':
            temp_df = df[(df['Location'] == location) & (df['Salary'] < 4000000)]
            fig = px.histogram(temp_df, x='Salary', template='simple_white', nbins=20, barmode='group',
                               color_discrete_sequence=['#1C4E80'])
            fig.update_layout(autosize=True, title={'text': "<b style:'color:blue;'>Salary at {0}</b>".format(location),
                                                    'font': {'size': 16}},
                              title_x=0.5, title_font_color="slategray", margin=dict(b=10, r=40),
                              yaxis_title={'text': "Number of Employees"}, font_color='slategray')
            # title_font_family="Times New Roman",

            # font_color='blue',

            # xaxis_title={'text': "<b style:'color:blue;'>Likes</b>", 'font': {'size':15}},
            # yaxis_title={'text': "<b style:'color:blue';></b>", 'font': {'size': 15}},
            #    paper_bgcolor='lightblue',
            #  plot_bgcolor='rgba(0,0,0,0)')



        else:
            fig = px.histogram(df[df['Salary'] < 4000000], x='Salary', template='simple_white', nbins=20,
                               color_discrete_sequence=['#1C4E80'])

            fig.update_layout(title={'text': "<b style:'color:blue;'>Overall Salary at All Locations</b>"
                , 'font': {'size': 16}}, title_x=0.5, title_font_color="slategray", margin=dict(b=10, r=40),
                              yaxis_title={'text': "Number of Employees"}, font_color='slategray')

            # title_font_family="Times New Roman",

            # font_color='blue',

            # xaxis_title={'text': "<b style:'color:blue;'>Likes</b>", 'font': {'size':15}},
            # yaxis_title={'text': "<b style:'color:blue';></b>", 'font': {'size': 15}},
            #   paper_bgcolor='white',
            #   plot_bgcolor='rgba(0,0,0,0)'

        return fig


######################################  Location bar chart   component
@app.callback(
    Output('bar', 'figure'),
    Input('dropdown1', 'value'),
)
def bar(role: str):
    if role == 'All':
        temp_df = location_sorting(df)
        fig = px.bar(temp_df, y='Location', x='Count', color='Location', template='simple_white',
                     color_discrete_sequence=px.colors.sequential.Blues_r,
                     orientation='h'
                     )
        fig.update_traces(showlegend=False)
        fig.update_layout(margin=dict(b=10, r=10, l=0),
                          title={'text': "<b style:'color:blue;'> Top Locations</b>", 'font': {'size': 16}},
                          title_x=0.5,
                          # title_font_family="Times New Roman",
                          title_font_color="slategray",
                          font_color='slategray',

                          # xaxis_title={'text': "<b style:'color:blue;'>Likes</b>", 'font': {'size':15}},
                          yaxis_title={'text': "<b style:'color:blue';></b>", 'font': {'size': 15}},
                          paper_bgcolor='white',
                          plot_bgcolor='rgba(0,0,0,0)')
        return fig

    else:
        temp_df = df[df['Job Roles'] == role]

        temp_df = location_sorting(temp_df)
        fig = px.bar(temp_df, y='Location', x='Count', color='Location', template='simple_white',
                     color_discrete_sequence=px.colors.sequential.Blues_r,
                     orientation='h')
        fig.update_traces(showlegend=False)
        fig.update_layout(
            title={'text': "<b style:'color:blue;'>Top Locations for {0}</b>".format(role), 'font': {'size': 15}},
            title_x=0.5,
            # title_font_family="Times New Roman",
            title_font_color="slategray", margin=dict(b=10, r=10, l=0),
            font_color='slategray',

            # xaxis_title={'text': "<b style:'color:blue;'>Likes</b>", 'font': {'size':15}},
            yaxis_title={'text': "<b style:'color:blue';></b>", 'font': {'size': 15}},
            paper_bgcolor='white',
            plot_bgcolor='rgba(0,0,0,0)')
        return fig


########################################################  Pie chart component
@app.callback(
    Output('pie', 'figure'),
    [Input('dropdown1', 'value'),
     Input('dropdown2', 'value')]
)
def pie(role=dropdown1, location=dropdown2):
    if role != 'All':
        temp_df = df[(df['Job Roles'] == role) & (df['Salary'] < 4000000)]
        if location != 'All':
            new_data = temp_df[temp_df['Location'] == location]
            data = new_data['Employment Status'].value_counts()
            fig = donut(data)

        elif location == "All":
            data = temp_df['Employment Status'].value_counts()
            fig = donut(data)
        else:
            data = temp_df['Employment Status'].value_counts()
            fig = donut(data)

        return fig

    else:

        if location != 'All':
            temp_df = df[(df['Location'] == location) & (df['Salary'] < 4000000)]

            data = temp_df['Employment Status'].value_counts()
            fig = donut(data)


        else:

            data = df['Employment Status'].value_counts()
            fig = donut(data)
        return fig


############################################################################# table component
@app.callback(
    Output('table', 'figure'),
    [Input('dropdown1', 'value'),
     Input('dropdown2', 'value')]
)
def Company_table(role=dropdown1, location=dropdown2):
    if role != 'All':
        temp_df = df[(df['Job Roles'] == role) & (df['Salary'] < 4000000)]
        if location != 'All':
            new_data = temp_df[temp_df['Location'] == location]

            fig = Table(new_data)

        elif location == "All":

            fig = Table(temp_df)
        else:

            fig = Table(temp_df)

        return fig

    else:
        if location != 'All':
            temp_df = df[(df['Location'] == location) & (df['Salary'] < 4000000)]
            fig = Table(temp_df)


        else:
            fig = Table(df)
        return fig
    ###############################################################################################


if __name__ == '__main__':
    app.run_server(debug=False)
