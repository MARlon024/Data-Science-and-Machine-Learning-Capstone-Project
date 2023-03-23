import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36',
                                                       'font-size': '40px'}),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'},
                          {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                          {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                          {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                          {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                 value='ALL',
                 placeholder='Select a Launch Site here',
                 searchable=True),
    
    html.Br(),
    
    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div([
        dcc.Graph(id='success-pie-chart')
    ]),
    
    html.Br(),
    
    # TASK 3: Add a callback function for interactive dropdown component
    html.P("The total number of successful launches : "),
    html.Div(id='success-pie-chart-text'),
    
    html.Br(),
    
    html.Hr(),
    
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div([
        dcc.Graph(id='success-payload-scatter-chart')
    ]),
    
    html.Br(),
    
    # TASK 5: Add a slider to select payload range
    html.P("Select Payload range (kg) : "),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[0, 10000]),
    
    html.Hr(),
    
    # TASK 6: Add a callback function for interactive scatter plot
    html.Div(id='selected-data'),
    
])
# TASK 3:
# Add a callback function for `site-dropdown` as input, `success-pie-chart-text` as output
@app.callback(
    Output(component_id='success-pie-chart-text', component_property='children'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_success_count(selected_site):
    if selected_site == 'ALL':
        filter_df = spacex_df
    else:
        filter_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    success_count = filter_df[filter_df['class'] == 1]['class'].count()
    return success_count

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(selected_site):
    if selected_site == 'ALL':
        filter_df = spacex_df
    else:
        filter_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    success_count = filter_df[filter_df['class'] == 1]['class'].count()
    fail_count = filter_df[filter_df['class'] == 0]['class'].count()
    fig = px.pie(values=[success_count, fail_count], names=['Success', 'Failure'], title='Total Success Launches for all Sites')
    return fig

        # return the outcomes piechart for a selected site
@app.callback(
    Output('selected-data', 'children'),
    [Input('payload-slider', 'selectedData')]
)
def display_selected_data(selectedData):
    if selectedData is not None:
        points = selectedData['points']
        selected = [f"Payload: {point['x']}, Success: {point['y']}" for point in points]
        return html.Ul([html.Li(s) for s in selected])
    else:
        return ''

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')])
def get_scatter_chart(site, payload):
    filtered_data = spacex_df[spacex_df['Launch Site'] == site]
    filtered_data = filtered_data[filtered_data['Payload Mass (kg)'].between(payload[0], payload[1])]
    
    fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                     title=f'Correlation between Payload and Success for {site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()