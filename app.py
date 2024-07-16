    alt.Chart(df)
    .mark_circle(size=60)
    .encode(
        x="tip",
        y="total_bill",
        color=alt.Color("day").scale(domain=["Thur", "Fri", "Sat", "Sun"]),
        tooltip=["day", "tip", "total_bill"],
    )
    .interactive()
)


app = Dash()
app.layout = html.Div(
    [
        html.H1("Vega-Altair Chart in a Dash App"),
        dvc.Vega(
            id="altair-chart",
            opt={"renderer": "svg", "actions": False},
            spec=chart.to_dict(),
        ),
    ]
)


if __name__ == "__main__":
    app.run(debug=True)
Vega-Altair Chart in a Dash App
2
4
6
8
10
3
5
7
9
tip
10
20
30
40
50
5
15
25
35
45
total_bill
Thur
Fri
Sat
Sun
day
Add a Dropdown
Let's create an interactive Dash app by allowing the user to filter the dataset by day, via a dropdown. In the example below, the callback's Input is used to register the dropdown's day value selected. Then, inside the callback function, the dataset is filtered and the Vega-Altair chart is built. Finally, the chart is assigned to the spec prop of dvc.Vega by returning it at the end of the callback function.

from dash import Dash, Input, Output, callback, dcc, html
import altair as alt
import dash_vega_components as dvc
import plotly.express as px

app = Dash()
app.layout = html.Div(
    [
        html.H1("Vega-Altair Chart in a Dash App"),
        dcc.Dropdown(
            options=["All", "Thur", "Fri", "Sat", "Sun"],
            value="All",
            id="origin-dropdown",
        ),
        dvc.Vega(
            id="altair-d-chart", opt={"renderer": "svg", "actions": False}, spec={}
        ),
    ]
)


@callback(
    Output(component_id="altair-d-chart", component_property="spec"),
    Input(component_id="origin-dropdown", component_property="value"),
)
def display_altair_chart(day_chosen):
    df = px.data.tips()

    if day_chosen != "All":
        df = df[df["day"] == day_chosen]

    chart = (
        alt.Chart(df)
        .mark_circle(size=60)
        .encode(
            x="tip",
            y="total_bill",
            color=alt.Color("day").scale(domain=["Thur", "Fri", "Sat", "Sun"]),
            tooltip=["day", "tip", "total_bill"],
        )
        .interactive()
    )

    return chart.to_dict()


if __name__ == "__main__":
    app.run(debug=True,port = 8050)
