from dash import dcc, html, Input, Output, State
import data
from figures import create_figures

def register_callbacks(app):
    @app.callback(Output('page-content', 'children'),
                  Input('url', 'pathname'))
    def display_page(pathname):
        df, df_A, df_M = data.get_data()
        fig_profit, fig_incomes, fig_expenses, fig_customers = create_figures(df)

        if pathname == '/report1':
            return html.Div([
                html.H3('Остатки на расчетных счетах'),
                html.Div([
                    dcc.Dropdown(
                        id='account-filter',
                        options=[{'label': account, 'value': account} for account in df['Банковский счет'].unique()],
                        value=[],  # Изначально ничего не выбрано
                        multi=True,
                        placeholder='Выберите банковский счет'
                    ),
                    dcc.Graph(id='profit-graph', figure=fig_profit, className='dcc-graph')
                ], className='graph-container-vertical'),
                html.Div([
                    dcc.Graph(id='incomes-graph', figure=fig_incomes, className='dcc-graph'),
                    dcc.Graph(id='expenses-graph', figure=fig_expenses, className='dcc-graph')
                ], className='graph-container')
            ], className='container')
        elif pathname == '/report2':
            return html.Div([
                html.H3('Анализ продаж')
            ], className='container')
        elif pathname == '/report3':
            return html.Div([
                html.H3('Расчеты с покупателями и поставщиками'),
                html.Div([
                    dcc.Graph(id='customers-graph', figure=fig_customers)
                ], className='graph-container-vertical')
            ], className='container')
        else:
            return html.Div([
                html.H3('Страница не найдена')
            ], className='container')

    @app.callback(
        [Output('profit-graph', 'figure'),
         Output('incomes-graph', 'figure'),
         Output('expenses-graph', 'figure')],
        [Input('account-filter', 'value'),
         Input('profit-graph', 'relayoutData')],
        State('profit-graph', 'figure')
    )
    def update_graphs(selected_accounts, relayoutData, profit_figure):
        df, df_A, df_M = data.get_data()
        
        # Filter by account
        if not selected_accounts:
            filtered_df = df
        else:
            filtered_df = df[df['Банковский счет'].isin(selected_accounts)]
        
        # Filter by selected range in the profit graph
        if relayoutData and 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
            start_date = relayoutData['xaxis.range[0]']
            end_date = relayoutData['xaxis.range[1]']
            filtered_df = filtered_df[(filtered_df['Дата'] >= start_date) & (filtered_df['Дата'] <= end_date)]
        
        fig_profit, fig_incomes, fig_expenses, _ = create_figures(filtered_df)
        return fig_profit, fig_incomes, fig_expenses
