import altair as alt
from dash import Dash, Input, Output, callback, dcc, html
from vega_datasets import data

import dash_vega_components as dvc

# Passing a stylesheet is not required
app = Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

app.layout = html.Div(
    [
        html.H1("Altair Chart"),
        dcc.Dropdown(["All", "USA", "Europe", "Japan"], "All", id="origin-dropdown"),
        # Optionally, you can pass options to the Vega component.
        # See https://github.com/vega/vega-embed#options for more details.
        dvc.Vega(id="altair-chart", opt={"renderer": "svg", "actions": False}),
    ]
)


@callback(Output("altair-chart", "spec"), Input("origin-dropdown", "value"))
def display_altair_chart(origin):
    source = data.cars()

    if origin != "All":
        source = source[source["Origin"] == origin]

    chart = (
        alt.Chart(source)
        .mark_circle(size=60)
        .encode(
            x="Horsepower",
            y="Miles_per_Gallon",
            color=alt.Color("Origin").scale(domain=["Europe", "Japan", "USA"]),
            tooltip=["Name", "Origin", "Horsepower", "Miles_per_Gallon"],
        )
        .interactive()
    )
    return chart.to_dict()


if __name__ == "__main__":
    app.run(debug=True, port = 8050)
