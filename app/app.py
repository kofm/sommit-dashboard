import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html
import dash_bootstrap_components as dbc
from components import dropdown_factory, render_card_summary
from help import tab_help


# Read data
sommit_data = pd.read_csv("sommit-data.csv")
mfa_ind_coord = pd.read_csv("mfa-ind-coord.csv")
df = pd.concat([sommit_data, mfa_ind_coord], axis=1)


# App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Trade-off analysis"
server = app.server


# Filter controls
fields_to_filter_environment = [
    ("Moisture Regime", "moistRegime", "dropdown-moist"),
    ("Temperature Regime", "tempRegime", "dropdown-temp"),
]

fields_to_filter_management = [
    ("Nitrogen Input", "N_input", "dropdown-nitrogen"),
    ("Organic Matter Input", "OM_input_after", "dropdown-ominput"),
]

filter_control = [
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H4("Narrative"),
                    dcc.Dropdown(
                        [
                            {"label": "Balanced", "value": "ΣI_N0"},
                            {"label": "Young farmers", "value": "ΣI_N1"},
                            {"label": "Agrochem corporation", "value": "ΣI_N2"},
                            {"label": "CAP paying agency", "value": "ΣI_N3"},
                        ],
                        "ΣI_N0",
                        id="dropdown-narrative",
                    ),
                ],
            ),
        ]
    ),
    dbc.Row(
        [ html.H4("Environment") ] +
        [
            dropdown_factory(id, df, field, label)
            for label, field, id in fields_to_filter_environment
        ]
    ),
    dbc.Row(
        [ html.H4("Management") ] +
        [
            dropdown_factory(id, df, field, label)
            for label, field, id in fields_to_filter_management
        ]
    ),
    dbc.Row(
        dbc.Col(
            [
                html.Label("Crop"),
                dcc.Dropdown(
                    df["crop"].unique(),
                    ["barley", "oat", "wheat", "durum wheat"],
                    id="dropdown-crop",
                    multi=True,
                ),
            ]
        )
    ),
]

tab_dashboard = [
        dbc.Row(
            [
                dbc.Col(children=filter_control, width = 2),
                dbc.Col(children=dcc.Graph("dist-plot"), width=7),
                dbc.Col(
                    [
                        dbc.Row(dbc.Col(id="hover_summary")),
                        dbc.Row(dbc.Col(id="hover_indicators")),
                    ],
                    width=3
                ),
            ]
        )
        ]

tabs = dbc.Tabs(
    [
        dbc.Tab(tab_dashboard, label="Dashboard"),
        dbc.Tab(tab_help, label="Help"),
    ]
)

app.layout = dbc.Container(
    [
        html.H1(children="Trade-offs analysis", className="display-1"),
        html.Div(tabs, className="my-3"),
    ]
)

@callback(
    Output("hover_summary", "children"),
    Input("dist-plot", "hoverData"),
    Input("dropdown-narrative", "value"),
)
def display_hover_data(hover_data, narrative):
    if hover_data:
        rown = hover_data["points"][0]["customdata"][0]
        row = df.iloc[rown]
        card_summary = dbc.Row(
            render_card_summary(row, narrative), className="my-3 mx-1"
        )
        return card_summary


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
        {"column": "OM_input_after", "value": ominput},
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
        height=800,
        opacity=0.7,
        range_color=[0.2, 0.8],
        hover_data={"ΣI_N0": ":.2f"},
        custom_data=[
            df[mask].index,
        ],
    )
    fig.update_scenes(aspectmode="cube")
    fig.update_traces(
        hovertemplate="ΣI_N0 %{marker.color:.2f}", selector=dict(type="scatter3d")
    )
    fig.update_scenes(
        xaxis_showbackground=False,
        yaxis_showbackground=False,
        zaxis_showbackground=False,
    )
    fig.update_scenes(
        xaxis_showspikes=False, yaxis_showspikes=False, zaxis_showspikes=False
    )
    fig.update_scenes(
        xaxis_showticklabels=False,
        yaxis_showticklabels=False,
        zaxis_showticklabels=False,
    )
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False)
    fig.update_scenes(camera_eye_x=1, camera_eye_y=1, camera_eye_z=1)
    return fig


if __name__ == "__main__":
    app.run(debug=True)
