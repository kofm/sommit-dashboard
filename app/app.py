import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html
import dash_bootstrap_components as dbc
from components import TocGauge, dropdown_factory, render_card_summary

# Read data
sommit_data = pd.read_csv("sommit-data.csv")
mfa_ind_coord = pd.read_csv("mfa-ind-coord.csv")
df = pd.concat([sommit_data, mfa_ind_coord], axis=1)


# App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Sommit Dashboard"
server = app.server


# Filter controls
fields_to_filter = [
    ("Moist Regime", "moistRegime", "dropdown-moist"),
    ("Temperature Regime", "tempRegime", "dropdown-temp"),
    ("N input", "N_input", "dropdown-nitrogen"),
    ("OM input", "OM_input_before", "dropdown-ominput"),
]

filter_control = [
    dbc.Row(
        dbc.Col(
            [
                html.Label("Choose your Narrative"),
                dcc.Dropdown(
                    ["ΣI_N0", "ΣI_N1", "ΣI_N2", "ΣI_N3"],
                    "ΣI_N0",
                    id="dropdown-narrative",
                ),
            ]
        )
    ),
    dbc.Row(
        [
            dropdown_factory(id, df, field, label)
            for label, field, id in fields_to_filter
        ]
    ),
    dbc.Row(
        dbc.Col(
            [
                html.Label("Crop"),
                dcc.Dropdown(
                    df["crop"].unique(), ["barley", "oat", "wheat", "durum wheat"], id="dropdown-crop", multi=True
                ),
            ]
        )
    ),
]

app.layout = dbc.Container(
    [
        html.H1(children="Sommit Dashboard", className="display-1"),
        html.Div(children=filter_control),
        dbc.Row(
            [
                dbc.Col(children=dcc.Graph("dist-plot"), width=8),
                dbc.Col(id="hover_summary"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(TocGauge(id="c-gauge", label="C stock")),
                dbc.Col(TocGauge(id="n2o-gauge", label="N2O emissions")),
                dbc.Col(TocGauge(id="no3-gauge", label="NO3 emissions")),
                dbc.Col(TocGauge(id="yield-gauge", label="Yield level")),
                dbc.Col(TocGauge(id="sommit-gauge", label="Sommit Index")),
            ]
        ),
    ]
)


@callback(
    Output("c-gauge", "value"),
    Output("n2o-gauge", "value"),
    Output("no3-gauge", "value"),
    Output("yield-gauge", "value"),
    Output("sommit-gauge", "value"),
    Output("hover_summary", "children"),
    Input("dist-plot", "hoverData"),
    Input("dropdown-narrative", "value"),
)
def display_hover_data(hover_data, narrative):
    if hover_data:
        rown = hover_data["points"][0]["customdata"][0]
        row = df.iloc[rown]
        card_summary = dbc.Row(render_card_summary(row), className="my-3 mx-1")
        return (
            row["CO2Q"],
            row["N2OQ"],
            row["NO3Q"],
            row["YQ"],
            row[narrative],
            card_summary,
        )


@callback(
    Output("dist-plot", "figure"),
    Input("dropdown-narrative", "value"),
    Input("dropdown-moist", "value"),
    Input("dropdown-temp", "value"),
    Input("dropdown-nitrogen", "value"),
    Input("dropdown-ominput", "value"),
    Input("dropdown-crop", "value"),
)
def update_dist_plot(narrative, moist, temp, nitrogen, ominput, crops):
    conditions = [
        {"column": "moistRegime", "value": moist},
        {"column": "tempRegime", "value": temp},
        {"column": "N_input", "value": nitrogen},
        {"column": "OM_input_before", "value": ominput},
    ]
    mask = pd.Series([True] * len(df))
    for cond in conditions:
        mask &= df[cond["column"]] == cond["value"]
    if type(crops) is str:
        mask &= df["crop"] == crops
    else:
        mask &= df["crop"].isin(crops)

    fig = px.scatter_3d(
        df[mask],
        x="Dim.1",
        y="Dim.2",
        z="Dim.3",
        color=narrative,
        opacity=0.7,
        range_color=[0.2, 0.8],
        hover_data={
            "ΣI_N0": ":.2f"
        },
        custom_data=[
            df[mask].index,
        ],
    )
    fig.update_scenes(aspectmode="cube")
    fig.update_traces(hovertemplate="ΣI_N0 %{marker.color:.2f}", selector=dict(type="scatter3d"))
    return fig


if __name__ == "__main__":
    app.run(debug=True)
