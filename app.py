from dash import Dash, html
import altair as alt
import dash_vega_components as dvc
import plotly.express as px

df = px.data.tips()
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
