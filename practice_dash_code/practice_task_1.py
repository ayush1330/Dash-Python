from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Good_to_Know/Dash2.0/social_capital.csv")
print(df.head())

# Build your component
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
my_title = dcc.Markdown(children ='')
my_graph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=df.columns.values[2:],
                        value = 'Cesarean Delivery Rate',
                        clearable = False
                        )

#customize layout

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([my_title], width = 6)
    ], justify= 'center'),
    dbc.Row([
        dbc.Col([my_graph], width = 6),
        dbc.Col([dropdown], width = 6)                    
    ]),
   # dbc.Row([
    #    dbc.Col([dropdown], width  =  6 )
   # ], justify= "end"),
], fluid = True)

#Callback allows component to interact
@app.callback(
    Output(my_graph, 'figure'),
    Output(my_title, 'children'),
    Input(dropdown, 'value')
)
def update_graph(column_name):

    print(column_name)
    print(type(column_name))

     # https://plotly.com/python/choropleth-maps/
    fig = px.choropleth(data_frame= df,
                         locations = 'STATE',
                         locationmode= 'USA-states',
                         scope = 'usa',
                         color = column_name,
                         animation_frame='YEAR')
    

    return fig, '#'+column_name # returned objects are assigned to the component property of the Output



# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8054)