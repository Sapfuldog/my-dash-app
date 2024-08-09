import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import data
from figures import create_figures
import pandas as pd
from datetime import datetime, date




def clean_value(value):
    if isinstance(value, str):
        return value.strip()
    return str(value)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def register_callbacks(app):
    @app.callback(Output('page-content', 'children'),
                  Input('url', 'pathname'))
    def display_page(pathname):
        df = data.get_data()
        fig_profit, fig_incomes, fig_expenses, fig_customers, fig_pie_ras, fig_pie_pos = create_figures(df)
        df_cur, df_fut = data.get_data_cur_fut()

        account_options = [{'label': clean_value(account), 'value': clean_value(account)} for account in df_fut['Банковский счет'].unique()]
        bank_options = [{'label': clean_value(bank), 'value': clean_value(bank)} for bank in df_fut['Банк'].unique()]
        st_options = [{'label': clean_value(st), 'value': clean_value(st)} for st in df_fut['Статья учета'].unique()]
        dir_options = [{'label': clean_value(d), 'value': clean_value(d)} for d in df_fut['Направление деятельности'].unique()]
        lastDat = df_cur['Дата'].iloc[-1].date()
        lastDat = lastDat.strftime('%d.%m.%Y')
        min_date = datetime.now()
        max_date = df['Дата'].max().date()
        balance = df_cur['Накопительно'].iloc[-1]
        
        
        
        if pathname == '/report1':
            return dbc.Tabs([
            dbc.Tab(
                    [html.Div([
                        dbc.Card([
                            html.Div([dcc.Markdown('Текущий баланс'),
                                      dcc.Markdown(f'_на  {lastDat}_',className='grey_title')
                                      ], className='title_custom_top'),
                            dcc.Markdown(f'₽ {balance:,.2f}',className='title_custom')                            
                    ], className='card_top')
                    ], className='box2')],                     
                    label="Текущий баланс остатков на расчетных счетах",
                    tab_id="tab-2",
                    className='box-tab'),
            dbc.Tab([
                    html.Div([
                        #html.Div(html.H3('Остатки на расчетных счетах'), className='H3-grid'),
                        html.Div([
                            html.Div(html.H4('Фильтры'), className='H4-grid'),
                            dcc.DatePickerRange(
                                id='date-picker-range',
                                start_date=min_date,
                                end_date=max_date,
                                display_format='DD.MM.YYYY',  # формат отображения даты
                                style={'margin': '10px 0'}
                            ),
                            dcc.Dropdown(
                                id='data-filter',
                                options=['Фильтровать все значения', 'Фильтровать плановые значения'], 
                                value='Фильтровать все значения'),
                            dcc.Dropdown(
                                id='account-filter',
                                options=account_options,
                                value=[],
                                multi=True,
                                placeholder='Выберите банковский счет',
                                optionHeight=120
                            ),
                            dcc.Dropdown(
                                id='bank-filter',
                                options=bank_options,
                                value=[],
                                multi=True,
                                placeholder='Выберите банк',
                                optionHeight=120
                            ),
                            dcc.Dropdown(
                                id='st-filter',
                                options=st_options,
                                value=[],
                                multi=True,
                                placeholder='Какие статьи не учитывать',
                                optionHeight=120
                            ),
                            dcc.Dropdown(
                                id='d-filter',
                                options=dir_options,
                                value=[],
                                multi=True,
                                placeholder='Выберите направление',
                                optionHeight=60
                            )
                        ], className='dropdown'),
                        html.Div([
                            dcc.Graph(id='profit-graph', figure=fig_profit)], className='graph-prof'),
                        dcc.Graph(id='incomes-graph', figure=fig_incomes, className='child-income1'),
                        dcc.Graph(id='pie-income-graph', figure=fig_pie_pos, className='child-income2 modified_pie'),
                        dcc.Graph(id='expenses-graph', figure=fig_expenses, className='child-expence1'),
                        dcc.Graph(id='pie-expenses-graph', figure=fig_pie_ras, className='child-expence2 modified_pie')
                    ], className='box2')
                ],                     
                    label="Динамика остатков и структура доходов/расходов",
                    tab_id="tab-1",
                    className='box-tab')

            ], id='tabs', active_tab='tab-2',className='box-tabs')
        elif pathname == '/report2':
            return html.Div([
                html.H3('Анализ продаж')
            ], className='container')
        elif pathname == '/report3':
            return html.Div([
                html.H3('Расчеты с покупателями и поставщиками'),
                html.Div([
                    dcc.Loading(
                        id="loading-customers",
                        type="circle",
                        children=dcc.Graph(id='customers-graph', figure=fig_customers)
                    )
                ], className='graph-container-vertical')
            ], className='container')
        else:
            return html.Div([
                html.H3('Страница не найдена')
            ], className='container')

    @app.callback(
        [Output('profit-graph', 'figure'),
         Output('incomes-graph', 'figure'),
         Output('expenses-graph', 'figure'),
         Output('pie-income-graph', 'figure'),
         Output('pie-expenses-graph', 'figure')],
        [Input('data-filter','value'),
         Input('account-filter', 'value'),
         Input('bank-filter', 'value'),
         Input('d-filter', 'value'),
         Input('st-filter', 'value'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_graphs(selected_data, selected_accounts, selected_banks, selected_d, selected_st, start_date, end_date):
        df = data.get_data()
        df_cur, df_fut = data.get_data_cur_fut()
        
        if selected_data =='Фильтровать все значения':
            flag_d = True
        else:
            flag_d = False
            
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        if flag_d:
            df_fut = df
                
        if selected_st:
            df_fut = df_fut[~df_fut['Статья учета'].isin(selected_st)]
        if selected_d:
            df_fut = df_fut[df_fut['Направление деятельности'].isin(selected_d)]
        if selected_accounts:
            df_fut = df_fut[df_fut['Банковский счет'].isin(selected_accounts)]
        if selected_banks:
            df_fut = df_fut[df_fut['Банк'].isin(selected_banks)]
        
        if not flag_d:
            df = pd.concat([df_cur, df_fut], ignore_index=True)
        else:
            df = df_fut
        
        df = df[(df['Дата'] >= start_date) & (df['Дата'] <= end_date)]
        
        fig_profit, fig_incomes, fig_expenses, _, fig_pie_ras, fig_pie_pos = create_figures(df)
        return fig_profit, fig_incomes, fig_expenses, fig_pie_pos, fig_pie_ras

    @app.callback(
        Output('account-filter', 'options'),
        Input('bank-filter', 'value')
    )
    def update_account_options(selected_banks):
        df_cur, df_fut = data.get_data_cur_fut()
        if selected_banks:
            filtered_df = df_fut[df_fut['Банк'].isin(selected_banks)]
        else:
            df = pd.concat([df_cur, df_fut], ignore_index=True)
            filtered_df = df 
        
        account_options = [{'label': clean_value(account), 'value': clean_value(account)} for account in filtered_df['Банковский счет'].unique()]
        
        return account_options

    @app.callback(
        Output('bank-filter', 'options'),
        Input('account-filter', 'value')
    )
    def update_bank_options(selected_accounts):
        df_cur, df_fut = data.get_data_cur_fut()        
        if selected_accounts:
            filtered_df = df_fut[df_fut['Банковский счет'].isin(selected_accounts)]
        else:
            df = pd.concat([df_cur, df_fut], ignore_index=True)    
            filtered_df = df
        
        bank_options = [{'label': clean_value(bank), 'value': clean_value(bank)} for bank in filtered_df['Банк'].unique()]
        
        return bank_options

