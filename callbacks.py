from dash import dcc, html, Input, Output, State
import data
from figures import create_figures
import pandas as pd

def register_callbacks(app):
    @app.callback(Output('page-content', 'children'),
                  Input('url', 'pathname'))
    def display_page(pathname):
        df, df_A, df_M = data.get_data()
        fig_profit, fig_incomes, fig_expenses, fig_customers = create_figures(df)
        df_cur, df_fut = data.get_data_cur_fut()
        
        # Очистка и приведение значений к строкам
        def clean_value(value):
            if isinstance(value, str):
                return value.strip()
            return str(value)

        account_options = [{'label': clean_value(account), 'value': clean_value(account)} for account in df_fut['Банковский счет'].unique()]
        bank_options = [{'label': clean_value(bank), 'value': clean_value(bank)} for bank in df_fut['Банк'].unique()]
        st_options = [{'label': clean_value(st), 'value': clean_value(st)} for st in df_fut['Статья учета'].unique()]
        dir_options = [{'label': clean_value(d), 'value': clean_value(d)} for d in df_fut['Направление деятельности'].unique()]
        
        dropdown_style = {
            'width': '300px',
            'textOverflow': 'ellipsis',
            'whiteSpace': 'nowrap',
            'overflow': 'hidden'
        }

        if pathname == '/report1':
            return html.Div([
                html.H3('Остатки на расчетных счетах'),
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='account-filter',
                            options=account_options,
                            value=[],  # Изначально ничего не выбрано
                            multi=True,
                            placeholder='Выберите банковский счет',
                            className='dcc-dropdown' ,  # Apply CSS class
                            optionHeight=120
                        ),
                        dcc.Dropdown(
                            id='bank-filter',
                            options=bank_options,
                            value=[],  # Изначально ничего не выбрано
                            multi=True,
                            placeholder='Выберите банк',
                            className='dcc-dropdown',  # Apply CSS class
                            optionHeight=120
                        ),
                        dcc.Dropdown(
                            id='st-filter',
                            options=st_options,
                            value=[],  # Изначально ничего не выбрано
                            multi=True,
                            placeholder='Какие статьи не учитывать',
                            className='dcc-dropdown' ,  # Apply CSS class
                            optionHeight=120

                        ),
                        dcc.Dropdown(
                            id='d-filter',
                            options=dir_options,
                            value=[],  # Изначально ничего не выбрано
                            multi=True,
                            placeholder='Выберите направление',
                            className='dcc-dropdown',  # Apply CSS class
                            optionHeight=60

                        )
                    ], className='graph-container-vertical'),
                    dcc.Graph(id='profit-graph', figure=fig_profit, className='dcc-graph')
                ], className='graph-container'),
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
         Input('profit-graph', 'relayoutData'),
         Input('bank-filter', 'value'),
         Input('d-filter', 'value'),
         Input('st-filter', 'value')],
        State('profit-graph', 'figure')
    )
    def update_graphs(selected_accounts, relayoutData, selected_banks, selected_d, selected_st, profit_figure):
        df, df_A, df_M = data.get_data()
        df_cur, df_fut = data.get_data_cur_fut()
                
        if selected_st:
            df_fut = df_fut[~df_fut['Статья учета'].isin(selected_st)]
        if selected_d:
            df_fut = df_fut[df_fut['Направление деятельности'].isin(selected_d)]
        if selected_accounts:
            df_fut = df_fut[df_fut['Банковский счет'].isin(selected_accounts)]
        if selected_banks:
            df_fut = df_fut[df_fut['Банк'].isin(selected_banks)]
        
        df = pd.concat([df_cur, df_fut], ignore_index=True)
        
        # Filter by selected range in the profit graph
        if relayoutData and 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
            start_date = relayoutData['xaxis.range[0]']
            end_date = relayoutData['xaxis.range[1]']
            
            df_f = df[(df['Дата'] < start_date)]
            df_f.loc[:, 'Накопительно'] = df_f['Сумма'].cumsum()

            last_row = df_f.tail(1)
            last_row.loc[:, 'Сумма'] = last_row['Накопительно']
            
            df = df[(df['Дата'] >= start_date) & (df['Дата'] <= end_date)]
            
            df = pd.concat([last_row, df], ignore_index=True)
        
        fig_profit, fig_incomes, fig_expenses, _ = create_figures(df)
        return fig_profit, fig_incomes, fig_expenses

    @app.callback(
        Output('account-filter', 'options'),
        Input('bank-filter', 'value')
    )
    def update_account_options(selected_banks):
        df, _, _ = data.get_data()
        df_cur, df_fut = data.get_data_cur_fut()
        if selected_banks:
            # Фильтрация данных по выбранным банкам
            filtered_df = df_fut[df_fut['Банк'].isin(selected_banks)]
        else:
            df = pd.concat([df_cur, df_fut], ignore_index=True)
            filtered_df = df 
        def clean_value(value):
            if isinstance(value, str):
                return value.strip()
            return str(value)
        # Получение уникальных банковских счетов из отфильтрованных данных
        account_options = [{'label': clean_value(account), 'value': clean_value(account)} for account in filtered_df['Банковский счет'].unique()]
        
        return account_options

    @app.callback(
        Output('bank-filter', 'options'),
        Input('account-filter', 'value')
    )
    def update_bank_options(selected_accounts):
        df, _, _ = data.get_data()
        df_cur, df_fut = data.get_data_cur_fut()        
        if selected_accounts:
            # Фильтрация данных по выбранным банковским счетам
            filtered_df = df_fut[df_fut['Банковский счет'].isin(selected_accounts)]
        else:
            df = pd.concat([df_cur, df_fut], ignore_index=True)    
            filtered_df = df
        def clean_value(value):
            if isinstance(value, str):
                return value.strip()
            return str(value)
        # Получение уникальных банков из отфильтрованных данных
        bank_options = [{'label': clean_value(bank), 'value': clean_value(bank)} for bank in filtered_df['Банк'].unique()]
        
        return bank_options
