import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import time

# Инициализация приложения Dash с Bootstrap темой
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"])

# Пример данных
months = {
    "2023": ["Jan 2023", "Apr 2023", "Jul 2023", "Oct 2023"],
    "2024": ["Jan 2024", "Apr 2024", "Jul 2024", "Oct 2024"]
}

profit_data = {
    "2023": [19, 20, 22, 21],
    "2024": [21, 25, 23, 27]
}

consulting_data = {
    "2023": [5, 6, 6.5, 7],
    "2024": [6, 7, 7.5, 8]
}

software_data = {
    "2023": [14, 14, 15.5, 16],
    "2024": [15, 16, 16.5, 18]
}

# Функция для создания графиков
def create_figures(period):
    fig_profit = go.Figure()
    fig_profit.add_trace(go.Scatter(x=months[period], y=profit_data[period], mode='lines+markers', name=period))
    fig_profit.update_layout(title='Операционная прибыль', yaxis_title='Прибыль (млн ₽)')

    fig_contract = go.Figure()
    fig_contract.add_trace(go.Bar(x=['ПО', 'Консалтинг', 'Прочее'], y=[111, 155, 45], name='2023'))
    fig_contract.add_trace(go.Bar(x=['ПО', 'Консалтинг', 'Прочее'], y=[117, 174, 68], name='2024'))
    fig_contract.update_layout(title='Средняя сумма контракта за месяц', barmode='group')

    fig_customers = go.Figure()
    fig_customers.add_trace(go.Scatter(x=months[period], y=[2115, 3050, 4300, 5600], mode='lines+markers', name='ПО'))
    fig_customers.add_trace(go.Scatter(x=months[period], y=[574, 800, 950, 1047], mode='lines+markers', name='Консалтинг'))
    fig_customers.update_layout(title='Число покупателей за месяц', yaxis_title='Число покупателей (тыс.)')

    return fig_profit, fig_contract, fig_customers

# Создание начальных графиков
fig_profit, fig_contract, fig_customers = create_figures("2024")

# Создание функции для получения контента страницы
def get_page_content(pathname):
    if pathname == "/":
        return html.H1("Добро пожаловать на главную страницу")
    elif pathname == "/report1":
        return dbc.Card([
            dbc.CardHeader("Операционная прибыль"),
            dbc.CardBody(dcc.Graph(id='profit-graph', figure=fig_profit))
        ])
    elif pathname == "/report2":
        return dbc.Card([
            dbc.CardHeader("Средняя сумма контракта за месяц"),
            dbc.CardBody(dcc.Graph(id='contract-graph', figure=fig_contract))
        ])
    elif pathname == "/report3":
        return dbc.Card([
            dbc.CardHeader("Число покупателей за месяц"),
            dbc.CardBody(dcc.Graph(id='customers-graph', figure=fig_customers))
        ])
    else:
        return html.H1("Страница не найдена")

# Макет приложения
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col([
            dbc.Nav([
                dbc.NavLink([html.I(className="bi bi-bank"), " Остатки на расчетных счетах"], href="/report1", className="nav-link"),
                dbc.NavLink([html.I(className="bi bi-bar-chart"), " Анализ продаж"], href="/report2", className="nav-link"),
                dbc.NavLink([html.I(className="bi bi-people"), " Расчеты с покупателями и поставщиками"], href="/report3", className="nav-link"),
                dbc.NavLink([html.I(className="bi bi-clock"), " Задолженность покупателей по срокам долга"], href="#", className="nav-link"),
                dbc.NavLink([html.I(className="bi bi-truck"), " Задолженность поставщикам по срокам долга"], href="#", className="nav-link"),
                dbc.NavLink([html.I(className="bi bi-boxes"), " Остатки товаров"], href="#", className="nav-link"),
                dbc.NavLink([html.I(className="bi bi-journal"), " Файловое хранилище"], href="#", className="nav-link"),
            ], className="navbar-vertical")
        ], width=2),
        dbc.Col([
            html.Div(id='page-content', className='page-transition')
        ], width=10)
    ])
], fluid=True)

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    return get_page_content(pathname)

@app.callback(
    Output('page-content', 'className'),
    [Input('url', 'pathname')]
)
def animate_page_transition(pathname):
    time.sleep(0.2)
    return 'page-transition page-enter-active'

if __name__ == '__main__':
    app.run_server(debug=True)
