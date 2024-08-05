from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import data
from figures import create_figures
import pandas as pd

def create_layout():
    df, df_A, df_M = data.get_data()
    df_cur, df_fut= data.get_data_cur_fut()
    df = pd.concat([df_cur, df_fut], ignore_index=True)

    grid_size = dbc.Row(dbc.Col(dbc.ButtonGroup([dbc.Button(id='less', n_clicks=0, children='<'),
                                                 dbc.Button(id='more', n_clicks=0, children='>')]),
                                width={'size': 1, 'offset': 5}))

    datatable = dag.AgGrid(id='datatable',
                           rowData=df_A.to_dict('records'),
                           columnDefs=[{"field": col, 'editable': True} for col in df_A.columns],
                           dashGridOptions={"dataTypeDefinitions": {"object": {"baseDataType": "object", "extendsDataType": "object", "valueParser": {"function": "({ name: params.newValue })"}, "valueFormatter": {"function": "params.value == null ? '' : params.value.name"}}}},
                           suppressDragLeaveHidesColumns=False,
                           persistence=True,
                           defaultColDef={'filter': True, 'floatingFilter': True, 'resizable': True, 'sortable': True, 'editable': False, 'minWidth': 125, 'wrapHeaderText': True, 'autoHeaderHeight': True},
                           style={'resize': 'both', 'overflow': 'hidden', "height": 1600})

    return dbc.Container([
        dcc.Location(id='url', refresh=False),
        html.Div(dbc.Nav([
                    dbc.NavLink([html.I(className="bi bi-bank"), " Остатки на расчетных счетах"], href="/report1", className="nav-link"),
                    dbc.NavLink([html.I(className="bi bi-bar-chart"), " Анализ продаж"], href="/report2", className="nav-link"),
                    dbc.NavLink([html.I(className="bi bi-people"), " Расчеты с покупателями и поставщиками"], href="/report3", className="nav-link"),
                    dbc.NavLink([html.I(className="bi bi-clock"), " Задолженность покупателей по срокам долга"], href="/report4", className="nav-link"),
                    dbc.NavLink([html.I(className="bi bi-truck"), " Задолженность поставщикам по срокам долга"], href="/report5", className="nav-link"),
                    dbc.NavLink([html.I(className="bi bi-boxes"), " Остатки товаров"], href="/report6", className="nav-link"),
                    dbc.NavLink([html.I(className="bi bi-journal"), " Файловое хранилище"], href="/report7", className="nav-link"),
                ], vertical=True, pills=True, className="navbar-vertical"),className = 'child1'),
        html.Div(id='page-content', className='child2')
        ], fluid=True, className = 'parent')
