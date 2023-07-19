import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = "vscode"
import plotly.express as px
import pandas as pd
import numpy as np


data = pd.read_csv("premium_bottled_water.csv")
data_gdp = pd.read_csv("gdp_indicators.csv")

data_gdp.rename(
    columns=({"Country Name": "Country"}),
    inplace=True,
)


intersection_country = np.intersect1d(
    data_gdp["Country"].unique(), data["Country"].unique()
)


data_gdp = data_gdp[data_gdp["Country"].isin(intersection_country)]


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MINTY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

app.layout = app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "Sample Dashboard",
                            className="text-center text-primary mb-4",
                        )
                    ]
                )
            ],
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Year"),
                        dcc.Dropdown(
                            id="my-dpdn",
                            multi=True,
                            options=[
                                {"label": x, "value": x}
                                for x in sorted(data["Attribute"].unique())
                            ],
                            value="Attribute",
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.Label("Country"),
                        dcc.Dropdown(
                            id="my-dpdn2",
                            multi=True,
                            options=
                            # {"label": x, "value": x}
                            intersection_country
                            # for x in sorted(data["Country"].unique())
                            ,
                            value="Country",
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.Label("GDP Indicator"),
                        dcc.RadioItems(
                            id="my-dpdn3",
                            # multi=False,
                            options=[
                                "Population growth (annual %)",
                                "GDP growth (annual %)",
                                "GDP per capita (current US$)",
                            ],
                            value="Population growth (annual %)",
                        ),
                    ],
                    width=4,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Table 1"),
                        dcc.Graph(id="table-1", figure={}),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Label("Table 2"),
                        dcc.Graph(id="table-2", figure={}),
                    ],
                    width=6,
                ),
            ]
        ),
    ]
)


############ chart function ME Table ##################


@app.callback(
    Output("table-1", "figure"),
    Input("my-dpdn", "value"),
    Input("my-dpdn2", "value"),
)
def update_figure_me(year, country):
    dff = data.copy()

    if any([year, country]):
        if year is not None:
            if len(year) > 0:
                dff = dff.query(f"Attribute == {year}")

        if country is not None:
            if len(country) > 0:
                dff = dff.query(f"Country == {country}")

        ##################table_chart########################

        table_df = dff[dff["Segment"] == dff["Segment"].unique()[0]][
            ["Country", "Attribute", "Value"]
        ]
        df_year_pivot = table_df.pivot_table(
            index="Country", columns="Attribute", values="Value", aggfunc="sum"
        ).round(2)
        fig_table = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["Country"] + list(df_year_pivot.columns),
                        fill_color="paleturquoise",
                        align="left",
                    ),
                    cells=dict(
                        values=[df_year_pivot.index]
                        + [df_year_pivot[col] for col in df_year_pivot.columns],
                        fill_color="lavender",
                        align="left",
                    ),
                )
            ]
        )
    if not any([year, country]):
        ##################table_chart########################

        table_df = dff[dff["Segment"] == dff["Segment"].unique()[0]][
            ["Country", "Attribute", "Value"]
        ]
        df_year_pivot = table_df.pivot_table(
            index="Country", columns="Attribute", values="Value", aggfunc="sum"
        ).round(2)
        fig_table = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["Country"] + list(df_year_pivot.columns),
                        fill_color="paleturquoise",
                        align="left",
                    ),
                    cells=dict(
                        values=[df_year_pivot.index]
                        + [df_year_pivot[col] for col in df_year_pivot.columns],
                        fill_color="lavender",
                        align="left",
                    ),
                )
            ]
        )

    return fig_table


############ chart function API Table ##################
@app.callback(
    Output("table-2", "figure"),
    Input("my-dpdn2", "value"),
    Input("my-dpdn3", "value"),
)
def update_figure_api(country, gdp_indicator):
    dff_gdp = data_gdp.copy()

    if any([country, gdp_indicator]):
        if gdp_indicator is not None:
            if len(gdp_indicator) > 0:
                print("hee hee")
                dff_gdp = dff_gdp[dff_gdp["Series Name"] == gdp_indicator]
                # dff_gdp = dff_gdp.query(f"Series Name == {gdp_indicator}")
                print("hoo hoo")

        if country is not None:
            if len(country) > 0:
                dff_gdp = dff_gdp.query(f"Country == {country}")

        ################ table ###############

        table_gdp = dff_gdp[
            [
                "Country",
                "2017",
                "2018",
                "2019",
                "2020",
                "2021",
                "2022",
            ]
        ]
        fig_api_table = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=list(table_gdp.columns),
                        fill_color="paleturquoise",
                        align="left",
                    ),
                    cells=dict(
                        values=[table_gdp[col] for col in table_gdp.columns],
                        fill_color="lavender",
                        align="left",
                    ),
                )
            ]
        )

    if not any([country, gdp_indicator]):
        ################ table ###############

        table_gdp = dff_gdp[
            [
                "Country",
                "2017",
                "2018",
                "2019",
                "2020",
                "2021",
                "2022",
            ]
        ]
        fig_api_table = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=list(table_gdp.columns),
                        fill_color="paleturquoise",
                        align="left",
                    ),
                    cells=dict(
                        values=[table_gdp[col] for col in table_gdp.columns],
                        fill_color="lavender",
                        align="left",
                    ),
                )
            ]
        )
    return fig_api_table


if __name__ == "__main__":
    app.run(debug=True)
