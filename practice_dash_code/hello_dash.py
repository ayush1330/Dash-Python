from dash import Dash, dcc
import dash_bootstrap_components as dbc

# build your component
app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
my_text = dcc.Markdown(children = '# Hello World- python dashboard')

# customize you component
app.layout = dbc.Container([my_text])

#Run app
if __name__ == '__main__':
    app.run_server(port = 8051)
