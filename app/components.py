from dash_daq import Gauge
import dash_bootstrap_components as dbc
from dash import dcc, html


class TocGauge(Gauge):
    def __init__(self, value=None, min=0, max=1, *args, **kwargs) -> None:
        super().__init__(value=value, min=min, max=max, *args, **kwargs)


def dropdown_factory(id, df, field, label):
    unique_vals = df[field].unique()
    return dbc.Col(
        [
            html.Label(label),
            dcc.Dropdown(unique_vals, unique_vals[0], id=id, clearable=False),
        ]
    )


def _render_list_item(label, value):
    #return html.Li(f"{label}: {value}", className="list-group-item")
    return html.Li(
        [html.Span(label, style={"float": "left"}), html.Span(value, style={"float": "right"})],
        style={"overflow": "hidden", "padding": "5px 0"},
        className="list-group-item"
    )  # Clearfix


def render_card_summary(row, selected=False):
    card_title = html.H4(row["crop"].capitalize(), className="card-title")
    card_subtitle = None
    if selected:
        card_subtitle = html.H6("Selected", className="card-subtitle mb-2 text-muted")
    items_to_display = [
        {"label": "Soil", "value": row["soilTexture"]},
        {"label": "Organic N", "value": row["organic_N"]},
        {"label": "Mineral N", "value": row["mineral_N"]},
        {"label": "Irrigation", "value": row["irrigation"]},
    ]
    card_list = html.Ul([_render_list_item(item["label"], item["value"]) for item in items_to_display], className="list-group list-group-flush")
    card_body = [
        dbc.CardBody(
            [
                card_title,
                card_subtitle,
                html.P(
                    card_list,
                    className="card-text",
                ),
            ]
        )
    ]
    card = dbc.Card(
        card_body,
        className="col",
    )
    return card
