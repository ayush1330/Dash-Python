from dash import Dash, dcc, Output,Input
import dash_bootstrap_components as dbc
import plotly.express as px

# incorporate data into app
df = px.data.medals_long()

# Build your component
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
my_title = dcc.Markdown(children = '# App that analyzes olympic data')
my_graph = dcc.Graph(figure ={})
dropdown = dcc.Dropdown(options = ['Bar Plot', 'Scatter Plot'],
                        value = "Bar Plot", # by default selected value
                        clearable= False

)

# customize your layoutes
app.layout = dbc.Container([my_title, my_graph, dropdown])

#callback allows component to interact
@app.callback(
    Output(my_graph, component_property= 'figure'),
    Input(dropdown, component_property= 'value')
)
def update_graph(user_input): #function argument come from the component property of the Input
    if user_input == 'Bar Plot':
        #fig = px.bar(data_frame =df, x ="nation", y ="count", color ="medal")
        fig = df.head()

    elif user_input == 'Scatter Plot':
        fig = px.scatter(data_frame= df, x ="count", y ="nation", color ="medal",symbol = "medal" ) 

    return fig # returned objs are assigned to the component property of the output
       

# Run app
if __name__=='__main__':
    app.run_server(port=8053)
