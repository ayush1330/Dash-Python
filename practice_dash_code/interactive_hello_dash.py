from dash import Dash, dcc, Output,Input
import dash_bootstrap_components as dbc

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
my_text = dcc.Markdown(children ='')
my_input = dbc.Input(value = "# Hello World")

# Customize your own Layout
app.layout = dbc.Container([my_text, my_input])

# Callback allows components to interact
@app.callback(
    Output(my_text, component_property='children'),
    Input(my_input, component_property='value')
)
def update_title(user_input): # function arguments come from the component property of the Input
    return user_input # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run_server(port=8052)