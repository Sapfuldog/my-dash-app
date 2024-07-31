from dash import dcc, html, Input, Output
import data
from figures import create_figures

def register_callbacks(app):
    @app.callback(Output('page-content', 'children'),
                  Input('url', 'pathname'))
    def display_page(pathname):
        df, df_A, df_M = data.get_data()
        fig_profit, fig_contract, fig_customers = create_figures(df)

        if pathname == '/report1':
            return html.Div([
                html.H3('Остатки на расчетных счетах'),
                dcc.Dropdown(
                    id='account-filter',
                    options=[{'label': account, 'value': account} for account in df['Банковский счет'].unique()],
                    value=[],  # Изначально ничего не выбрано
                    multi=True,
                    placeholder='Выберите банковский счет'
                ),
                dcc.Graph(id='profit-graph', figure=fig_profit)
            ])
        elif pathname == '/report2':
            return html.Div([
                html.H3('Анализ продаж'),
                dcc.Graph(id='contract-graph', figure=fig_contract)
            ])
        elif pathname == '/report3':
            return html.Div([
                html.H3('Расчеты с покупателями и поставщиками'),
                dcc.Graph(id='customers-graph', figure=fig_customers)
            ])
        else:
            return html.Div([
                html.H3('Страница не найдена')
            ])

    @app.callback(
        Output('profit-graph', 'figure'),
        Input('account-filter', 'value')
    )
    def update_graph(selected_accounts):
        df, df_A, df_M = data.get_data()
        if not selected_accounts:
            filtered_df = df
        else:
            filtered_df = df[df['Банковский счет'].isin(selected_accounts)]
        
        fig_profit, _, _ = create_figures(filtered_df)
        return fig_profit
