import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import dash_ag_grid as dag

# Инициализация приложения Dash с Bootstrap темой
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"])

# Определяем количество строк
num_rows = 10000

# Создаем примеры данных
data = {
    'Дата': pd.date_range(start='2023-01-01', periods=num_rows, freq='h'),
    'Контрагент': np.random.choice(['Компания А', 'Компания B', 'Компания C', 'Компания D', 
                                    'Компания E', 'Компания F', 'Компания G', 'Компания H', 
                                    'Компания I', 'Компания J'], size=num_rows),
    'Сумма': np.random.randint(-50000, 50000, size=num_rows),
    'Договор': [f'Договор №{i}' for i in np.random.randint(1, 1000, size=num_rows)],
    'Статья учета': np.random.choice(['Услуги', 'Товары', 'Аренда', 'Зарплата', 'Командировки', 
                                      'Закупки', 'Прочее', 'Капитальные затраты', 'Реклама', 
                                      'Консультации'], size=num_rows),
    'Банковский счет': [f'Счет №{np.random.randint(1000, 9999)}' for _ in range(num_rows)]
}

# Создаем DataFrame
df = pd.DataFrame(data)
df['ДатаД'] = df['Дата'].dt.to_period('D')
df['ДатаД'] = df['ДатаД'].dt.to_timestamp()
df['Дата '] = df['Дата'].dt.to_period('M')
df_M = df.groupby('Дата ')['Сумма'].sum().reset_index()
df_M['Дата '] = df_M['Дата '].dt.to_timestamp()
df_M['Цвета'] = df_M['Сумма'].apply(lambda x: 'rgb(0,255,0)' if x >= 0 else 'rgb(255,0,0)')
df_M['Накопительно'] = df_M['Сумма'].cumsum()

df_A = df[['ДатаД','Контрагент','Сумма','Договор','Статья учета','Банковский счет']].copy()

defaultColDef = {"flex": 1, "minWidth": 150}

# Функция для создания графиков
def create_figures(period): 
    fig_profit = go.Figure()
    fig_profit.add_trace(
        go.Scatter(                             
            x= df_M['Дата '],
            y= df_M['Накопительно'], 
            fill='tozeroy',
            line=dict(shape='spline'),
            mode='lines+markers'
            ))
    fig_profit.update_layout(
        title=' ', 
        yaxis_title='Динамика остатков на счету')    
    fig_profit.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='White')


    fig_contract = go.Figure()
    fig_contract.add_trace(
        go.Bar(
            x=df['Статья учета'], 
            y=df['Сумма'], 
            name='Статья'))
    fig_contract.add_trace(go.Bar(
        x=df['Контрагент'], 
        y=df['Сумма'], 
        name='Контрагент'))
    fig_contract.update_layout(
        title=' ', 
        barmode='group')

    fig_customers = go.Figure()
    fig_customers.add_trace(
        go.Scatter(
            x=df['Дата'], 
            y=df['Сумма'], 
            mode='lines+markers', 
            name='ПО'))
    fig_customers.add_trace(
        go.Scatter(
            x=df['Дата'], 
            y=df['Сумма'], 
            mode='lines+markers', 
            name=' '))
    fig_customers.update_layout(
        title='Число покупателей за месяц', 
        yaxis_title='Число покупателей (тыс.)')
    
    return fig_profit, fig_contract, fig_customers

# Создание начальных графиков
fig_profit, fig_contract, fig_customers = create_figures("2024")

grid_size = dbc.Row(dbc.Col(dbc.ButtonGroup([dbc.Button(id='less', n_clicks=0, children='<'),
                                             dbc.Button(id='more', n_clicks=0, children='>')]),
                            width={'size': 1, 'offset': 5}))

empty_rows = pd.DataFrame(np.nan, index=range(1000), columns=df.columns)

df_M = pd.concat([df_M, empty_rows], ignore_index=True)

dataTypeDefinitions = {
    "object": {
        "baseDataType": "object",
        "extendsDataType": "object",
        "valueParser": {"function": "({ name: params.newValue })"},
        "valueFormatter": {"function": "params.value == null ? '' : params.value.name"},
    },
}

col_defs = []
for col in df_A.columns:
    if pd.api.types.is_numeric_dtype(df_A[col]):
        col_type = 'Number'
    elif pd.api.types.is_datetime64_any_dtype(df_A[col]):
        col_type = 'dateString'
    else:
        col_type = 'text'
    col_defs.append({"field": col, 'editable': True})

datatable = dag.AgGrid(id='datatable',
                       rowData=df_A.to_dict('records'),
                       columnDefs=col_defs,
                       dashGridOptions={"dataTypeDefinitions": dataTypeDefinitions, "animateRows": False},
                       suppressDragLeaveHidesColumns=False,
                       persistence=True,
                       defaultColDef={'filter': True,
                                      'floatingFilter': True,
                                      'resizable': True,
                                      'sortable': True,
                                      'editable': False,
                                      'minWidth': 125,
                                      'wrapHeaderText': True,
                                      'autoHeaderHeight': True},
                       style={'resize': 'both',
                              'overflow': 'hidden',
                              "height": 1600}
                       )


# Создание функции для получения контента страницы
def get_page_content(pathname):
    if pathname == "/":
        return dbc.Card([
            dbc.CardHeader("Добро пожаловать на главную страницу")])
    elif pathname == "/report1":
        return dbc.Row([dbc.Row([
                dbc.Col([
                    dbc.Card([
                    dbc.CardHeader("Динамика денежных потоков"),
                    dbc.CardBody(dcc.Graph(id='profit-graph', figure=fig_profit))
                            ])
                        ])
                     ]),
                dbc.Row([
                    dbc.Col([
                    grid_size,
                    dcc.Loading(
                        children=[
                            dbc.Tabs([
                                dbc.Tab(datatable,
                                label='Product Detail')])
                            ],
                        fullscreen=True)
                            ])   
                     ])])
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

# Коллбек для обновления контента страницы
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    return get_page_content(pathname)

if __name__ == '__main__':
    app.run_server(debug=True)

