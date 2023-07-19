import dash                     # pip install dash
from dash.dependencies import Input, Output, State
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
import plotly.express as px     # pip install plotly
import pandas as pd             # pip install pandas


df  =  pd.read_csv("Animals_Inventory.csv")

df["Intake_Time"] = pd.to_datetime(df["Intake_Time"]).dt.hour # changing time to hour datetime

#print(df.head())

'''
predefined styles that someone has created and shared on CodePen. These styles can be 
used by others to quickly apply a specific visual 
theme or design to their webpages without having to write the CSS code from scratch.

'''

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Analytics Dashboard of Dallas Animal Shelter (Dash Plotly)", style={"textAlign":"center"}),
    html.Hr(),
    html.P("Choose animal of interest:"),
    html.Div(html.Div([
        dcc.Dropdown(id='Animal_Type', clearable=False,
                     value="DOG",
                     options=[{'label': x, 'value': x} for x in
                              df["Animal_Type"].unique()]),
    ],className="two columns"),className="row"),

    html.Div(id="output-div", children=[]),
])

@app.callback(Output(component_id="output-div", component_property="children"),
              Input(component_id="Animal_Type", component_property="value"),
)
def make_graphs(animal_chosen):
    # HISTOGRAM
    df_hist = df[df["Animal_Type"]==animal_chosen]
    fig_hist = px.histogram(df_hist, x="Animal Breed")
    fig_hist.update_xaxes(categoryorder="total descending")

    # STRIP CHART
    fig_strip = px.strip(df_hist, x="Animal Stay Days", y="Intake_Type")

    # SUNBURST
    df_sburst = df.dropna(subset=['Chip_Status'])
    df_sburst = df_sburst[df_sburst["Intake_Type"].isin(["STRAY", "FOSTER", "OWNER SURRENDER"])]
    fig_sunburst = px.sunburst(df_sburst, path=["Animal_Type", "Intake_Type", "Chip_Status"])

    # Empirical Cumulative Distribution
    df_ecdf = df[df["Animal_Type"].isin(["DOG","CAT"])]
    fig_ecdf = px.ecdf(df_ecdf, x="Animal Stay Days", color="Animal_Type")

    # LINE CHART
    df_line = df.sort_values(by=["Intake_Time"], ascending=True)
    df_line = df_line.groupby(
        ["Intake_Time", "Animal_Type"]).size().reset_index(name="count")
    fig_line = px.line(df_line, x="Intake_Time", y="count",
                       color="Animal_Type", markers=True)

    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_strip)], className="six columns"),
        ], className="row"),
        html.H2("All Animals", style={"textAlign":"center"}),
        html.Hr(),
        html.Div([
            html.Div([dcc.Graph(figure=fig_sunburst)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_ecdf)], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([dcc.Graph(figure=fig_line)], className="twelve columns"),
        ], className="row"),
    ]


if __name__ == '__main__':
    app.run_server(debug=True)