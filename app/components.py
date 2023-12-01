from dash_daq import GraduatedBar
import dash_bootstrap_components as dbc
from dash import dcc, html


class TocGauge(GraduatedBar):
    def __init__(self, value=None, max=1, step=0.1, *args, **kwargs) -> None:
        super().__init__(value=value, max=max, step=step, showCurrentValue=True, *args, **kwargs)


def dropdown_factory(id, df, field, label):
    unique_vals = df[field].unique()
    return dbc.Row(dbc.Col(
        [
            html.Label(label),
            dcc.Dropdown(unique_vals, unique_vals[0], id=id, clearable=False),
        ]
    ))


def _render_list_item(label, value):
    return html.Li(
        [
            html.Span(label, style={"float": "left"}),
            html.Span(value, style={"float": "right"}),
        ],
        style={"overflow": "hidden", "padding": "1px 0"},
        className="list-group-item",
    )  # Clearfix


def render_card_summary(row, narrative, selected=False):
    card_title = html.H4(row["Crop"].capitalize(), className="card-title")
    card_subtitle = None

    if selected:
        card_subtitle = html.H6("Selected", className="card-subtitle mb-2 text-muted")

    items_to_display = [
        {"label": "Soil texture", "value": row["Soil_texture"]},
        {"label": "Soil tillage", "value": row["Soil_tillage_(0)"]},
        {"label": "Irrigation Type", "value": row["Irrigation"]},
        {"label": "Organic Nitrogen", "value": row["Organic_N_type"]},
        {"label": "Mineral Nitrogen", "value": row["Mineral_N_type"]},
        {"label": "Crop residues", "value": row["Crop_residues"]},
    ]

    card_list = html.Ul(
        [_render_list_item(item["label"], item["value"]) for item in items_to_display],
        className="list-group list-group-flush",
    )

    indicators_to_display = [
        {"label": "ΔSOC (COeq)", "value": row["ΔSOC(CO2_emissions)"], "color": {"gradient": True, "ranges": {"#1cc948": [0, 0.55], "white": [0.55, 0.65], "#c91c1c": [0.65, 1]}}},
        {"label": "N2O emissions", "value": row["N2O_emissions_(CO2_eq.)"], "color": "#234074"},
        {"label": "N-NO3 leaching", "value": row["N-NO3_leaching"], "color": "#61399D"},
        {"label": "Crop yield", "value": row["Crop_yield"], "color": "#0C3B2B"},
    ]

    card_indicators = dbc.Row(
        [
            TocGauge(label=indicator["label"], value=indicator["value"], color=indicator["color"], min=indicator.get("min", 0))
            for indicator in indicators_to_display
        ]
    )

    card_body = dbc.CardBody(
        [
            card_title,
            card_subtitle,
            html.P(
                card_list,
                className="card-text",
            ),
            card_indicators,
        ]
    )

    card_footer = dbc.CardFooter(
        TocGauge(label="Σommit Index", value=row[narrative], color={"gradient": True, "ranges": {"#0F0751": [0, 0.20], "#551065": [0.20, 0.35], "#8B4254": [0.35, 0.50], "#A05E49": [0.50, 0.65], "#B3B13E": [0.65, 1]}})
    )
    card = dbc.Card(
        [card_body, card_footer],
    )
    return card
