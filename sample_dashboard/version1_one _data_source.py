import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = "vscode"
import plotly.express as px
import pandas as pd


data = pd.read_csv("premium_bottled_water.csv")
# print(data.head())

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
                            options=[
                                {"label": x, "value": x}
                                for x in sorted(data["Country"].unique())
                            ],
                            value="Country",
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.Label("Segment"),
                        dcc.Dropdown(
                            id="my-dpdn3",
                            multi=False,
                            options=[x for x in data.Segment.unique()],
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
                        html.Label("Bar Chart"),
                        dcc.Graph(id="bar-chart", figure={}),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Label("CAGR"),
                        dcc.Graph(id="area-chart", figure={}),
                    ],
                    width=6,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Table"),
                        dcc.Graph(id="table", figure={}),
                    ]
                )
            ]
        ),
    ]
)


@app.callback(
    Output("bar-chart", "figure"),
    Output("area-chart", "figure"),
    Output("table", "figure"),
    Input("my-dpdn", "value"),
    Input("my-dpdn2", "value"),
    # Input('my-dpdn3', 'value')
)
def update_figure(year, country):
    dff = data.copy()
    if any([year, country]):
        if year is not None:
            if len(year) > 0:
                dff = dff.query(f"Attribute == {year}")

        if country is not None:
            if len(country) > 0:
                dff = dff.query(f"Country == {country}")

        ########################### bar chart #########################

        df_seg_year = (
            dff[dff["Segment"] == dff["Segment"].unique()[0]]
            .groupby("Attribute", as_index=False)["Value"]
            .sum()
        )
        fig_bar = (
            px.bar(df_seg_year, x="Attribute", y="Value")
            .update_traces(
                marker=dict(
                    color=[
                        "#CCCCCC"
                        if year <= 2021
                        else "#86D9C5"
                        if year == 2022
                        else "#003A5D"
                        for year in df_seg_year["Attribute"]
                    ]
                )
            )
            .update_layout(xaxis=dict(type="category"))
        )
        #########################cagr chart########################

        df_seg_cagr = (
            dff[dff["Attribute"] == dff["Attribute"].unique()[0]]
            .groupby("Segment", as_index=False)["CAGR"]
            .mean()
        )
        df_seg_cagr["CAGR"] = df_seg_cagr["CAGR"].apply("{:.2%}".format)
        df_seg_cagr["CAGR"] = (
            df_seg_cagr["CAGR"].str.rstrip("%").astype("float") / 100.0
        )
        colors = [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
        ]
        fig_scatter = (
            px.scatter(
                df_seg_cagr,
                x="Segment",
                y="CAGR",
                color="Segment",
                color_discrete_sequence=colors,
                opacity=0.8,
                hover_name="Segment",
                # text="CAGR",
            )
            .update_traces(marker=dict(line=dict(color="black", width=1)))
            .update_layout(
                showlegend=True,
                annotations=[
                    dict(
                        x=row["Segment"],
                        y=row["CAGR"],
                        xref="x",
                        yref="y",
                        text=f"{row['CAGR']*100:.2f}%",
                        font=dict(family="Arial", size=12, color="black"),
                        showarrow=True,
                        arrowhead=5,
                        ax=0,
                        ay=-40,
                    )
                    for i, row in df_seg_cagr.iterrows()
                ],
            )
        )

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
        ########################### bar chart #########################

        df_seg_year = (
            dff[dff["Segment"] == dff["Segment"].unique()[0]]
            .groupby("Attribute", as_index=False)["Value"]
            .sum()
        )
        fig_bar = (
            px.bar(df_seg_year, x="Attribute", y="Value")
            .update_traces(
                marker=dict(
                    color=[
                        "#CCCCCC"
                        if year <= 2021
                        else "#86D9C5"
                        if year == 2022
                        else "#003A5D"
                        for year in df_seg_year["Attribute"]
                    ]
                )
            )
            .update_layout(xaxis=dict(type="category"))
        )
        #########################cagr chart########################

        df_seg_cagr = (
            dff[dff["Attribute"] == dff["Attribute"].unique()[0]]
            .groupby("Segment", as_index=False)["CAGR"]
            .mean()
        )
        df_seg_cagr["CAGR"] = df_seg_cagr["CAGR"].apply("{:.2%}".format)
        df_seg_cagr["CAGR"] = (
            df_seg_cagr["CAGR"].str.rstrip("%").astype("float") / 100.0
        )
        colors = [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
        ]
        fig_scatter = (
            px.scatter(
                df_seg_cagr,
                x="Segment",
                y="CAGR",
                color="Segment",
                color_discrete_sequence=colors,
                opacity=0.8,
                hover_name="Segment",
                # text="CAGR",
            )
            .update_traces(marker=dict(line=dict(color="black", width=1)))
            .update_layout(
                showlegend=True,
                annotations=[
                    dict(
                        x=row["Segment"],
                        y=row["CAGR"],
                        xref="x",
                        yref="y",
                        text=f"{row['CAGR']*100:.2f}%",
                        font=dict(family="Arial", size=12, color="black"),
                        showarrow=True,
                        arrowhead=5,
                        ax=0,
                        ay=-40,
                    )
                    for i, row in df_seg_cagr.iterrows()
                ],
            )
        )

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

    return fig_bar, fig_scatter, fig_table


if __name__ == "__main__":
    app.run(debug=True)
