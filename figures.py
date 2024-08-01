from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from datetime import datetime, date

def create_figures(df_filtered): 
    
    df_filtered['Накопительно'] = df_filtered['Сумма'].cumsum()
      # Фильтрация данных по расходам и доходам
    expenses_df = df_filtered[df_filtered['Сумма'] < 0].copy()
    incomes_df = df_filtered[df_filtered['Сумма'] > 0].copy()
    # Создание фигуры с несколькими подграфиками
    fig_profit = make_subplots(
        rows=3, cols=2,
        shared_xaxes=True, 
        shared_yaxes=True,
        vertical_spacing=0.02, 
        horizontal_spacing=0.01,
        row_heights=[0.7,0.7, 4.7],  # Устанавливаем высоту строк
        column_widths=[0.7, 0.02],  # Устанавливаем ширину колонок
        specs=[[{"type": "bar"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "histogram"}],
               [{"type": "scatter"}, {"type": "histogram"}]]
    )

    start_date = datetime.now()
    df_filtered_by_date = df_filtered[(df_filtered['Дата'] >= start_date)]
    df_filtered_by_date_undo = df_filtered[(df_filtered['Дата'] < start_date)]
    df_pos = df_filtered[df_filtered['Сумма'] > 0]
    df_neg = df_filtered[df_filtered['Сумма'] < 0] 
    df_neg.loc[:, 'Сумма'] = -df_neg['Сумма']
    
    weekly_pos = df_pos.resample('W-Mon', on='Дата')['Сумма'].sum().reset_index()
    weekly_neg = df_neg.resample('W-Mon', on='Дата')['Сумма'].sum().reset_index()
      
    
    def SetColor(y):
            if(y >= 50000000):
                return '#0ef725'
            elif(y >= 5000000):
                return '#e8f70e'
            elif(y >= 1000000):
                return '#0ef7e8'
            else:
                return '#01ff00'
     
    fig_profit.add_trace(
        go.Bar(                             
            x=weekly_pos['Дата'],
            y=weekly_pos['Сумма'], 
            showlegend=False,
            #fill='tozeroy',
            #line=dict(shape='spline'),
            marker=dict(color = list(map(SetColor, weekly_pos['Сумма'])))
        ),
        row=1, col=1
    ) 

    fig_profit.add_trace(
        go.Bar(                             
            x=weekly_neg['Дата'],
            y=weekly_neg['Сумма'], 
            showlegend=False,
            #fill='tozeroy',
            #line=dict(shape='spline'),
            marker=dict(color = list(map(SetColor, weekly_neg['Сумма'])))
        ),
        row=2, col=1
    ) 
    
        # Добавление трасс на график
    fig_profit.add_trace(
        go.Scatter(                             
            x=df_filtered_by_date['Дата'],
            y=df_filtered_by_date['Накопительно'], 
            #fill='tozeroy',
            #line=dict(shape='spline'),
            showlegend=False,
            marker_color='blue'
        ),
        row=3, col=1
    )
    fig_profit.add_trace(
        go.Scatter(                             
            x=df_filtered_by_date_undo['Дата'],
            y=df_filtered_by_date_undo['Накопительно'], 
            #fill='tozeroy',
            #line=dict(shape='spline'),
            showlegend=False,
            marker_color='#04adef'
        ),
        row=3, col=1
    )
    
    fig_profit.add_trace(
        go.Histogram(
            y=df_filtered['Накопительно'], 
            histfunc='sum',
            showlegend=False,
            marker_color='#01ffd0'
        ),
        row=3, col=2
    )    

    # Обновление макета графика
    fig_profit.update_layout(
        title='',
        xaxis=dict(title=''),  # Очищаем подпись для первой оси x
        yaxis=dict(title=''),  # Очищаем подпись для первой оси y
        xaxis2=dict(title=''),  # Очищаем подпись для второй оси x
        yaxis2=dict(title=''),  # Очищаем подпись для второй оси y
        xaxis3=dict(title=''),  # Очищаем подпись для третьей оси x
        yaxis3=dict(title=''),  # Очищаем подпись для третьей оси y
        xaxis4=dict(title=''),  # Добавляем подпись для четвертой оси x
        yaxis4=dict(title=''),  # Очищаем подпись для четвертой оси y
        xaxis5=dict(title='Дата'),  # Добавляем подпись для пятой оси x
        yaxis5=dict(title=''),  # Очищаем подпись для пятой оси y
        xaxis6=dict(title=''),  # Добавляем подпись для шестой оси x
        yaxis6=dict(title='')  # Очищаем подпись для шестой оси y
    )

    # fig_profit.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='White', tickfont=dict(size=6), row=1, col=1)
    # fig_profit.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='White', tickfont=dict(size=6),autorange='reversed', row=2, col=1)
    fig_profit.update_xaxes(matches='x')
    fig_profit.update_xaxes(tickfont=dict(size=1), row=3, col=2)
    fig_profit.update_yaxes(   
        type='log',
        range=[0,10],
        tickfont=dict(size=6),
        # tickvals=[0, 1e5, 1e6, 1e8, 1e9], 
        # ticktext=['0', '100k', '1M', '100M', '1B'],
        # tickformat=".2f",
        row=1, col=1
    )
    fig_profit.update_yaxes(   
        type='log',
        range=[0,5],
        tickfont=dict(size=6),
        # tickvals=[0, 1e5, 1e6, 1e8], 
        # ticktext=['0', '100k','-1M', '-100M'],
        # tickformat=".2f",
        autorange='reversed',
        row=2, col=1
    )
    
    
    

    # Преобразование отрицательных сумм расходов в положительные для корректного отображения в treemap
    expenses_df['Сумма'] = expenses_df['Сумма'].abs()

    # Группировка по 'Статья учета' и суммирование по 'Сумма' для расходов
    grouped_expenses = expenses_df.groupby('Статья учета')['Сумма'].sum().reset_index()
    grouped_expenses_ = expenses_df.groupby(['Статья учета', 'Контрагент'])['Сумма'].sum().reset_index()

    # Генерация уникальных идентификаторов
    expense_account_ids = [f"exp_{i}" for i in range(len(grouped_expenses))]
    expense_contractor_ids = [f"exp_{i}_{j}" for i in range(len(grouped_expenses)) for j in range(len(grouped_expenses_.loc[grouped_expenses_['Статья учета'] == grouped_expenses.iloc[i, 0]]))]

    # Создание списков для treemap по расходам
    expenses_labels = list(grouped_expenses['Статья учета']) + list(grouped_expenses_['Контрагент'])
    expenses_parents = [''] * len(grouped_expenses['Статья учета']) + [f"exp_{i}" for i in range(len(grouped_expenses)) for _ in range(len(grouped_expenses_.loc[grouped_expenses_['Статья учета'] == grouped_expenses.iloc[i, 0]]))]
    #expenses_values = list(grouped_expenses['Сумма']) + list(grouped_expenses_['Сумма'])
    expenses_values = ['0'] * len(grouped_expenses['Сумма']) + list(grouped_expenses_['Сумма'])
    expenses_ids = expense_account_ids + expense_contractor_ids

    # # # Создание графика treemap для расходов
    fig_expenses = go.Figure(go.Treemap(
         ids=expenses_ids,
         labels=expenses_labels,
         parents=expenses_parents,
         values=expenses_values
       ))
    fig_expenses.update_layout(title="Структура расходов")

    # Группировка по 'Статья учета' и суммирование по 'Сумма' для доходов
    grouped_incomes = incomes_df.groupby('Статья учета')['Сумма'].sum().reset_index()
    grouped_incomes_ = incomes_df.groupby(['Статья учета', 'Контрагент'])['Сумма'].sum().reset_index()

    # Генерация уникальных идентификаторов
    income_account_ids = [f"inc_{i}" for i in range(len(grouped_incomes))]
    income_contractor_ids = [f"inc_{i}_{j}" for i in range(len(grouped_incomes)) for j in range(len(grouped_incomes_.loc[grouped_incomes_['Статья учета'] == grouped_incomes.iloc[i, 0]]))]

    # Создание списков для treemap по доходам
    incomes_labels = list(grouped_incomes['Статья учета']) + list(grouped_incomes_['Контрагент'])
    incomes_parents = [''] * len(grouped_incomes['Статья учета']) + [f"inc_{i}" for i in range(len(grouped_incomes)) for _ in range(len(grouped_incomes_.loc[grouped_incomes_['Статья учета'] == grouped_incomes.iloc[i, 0]]))]
    #incomes_values = list(grouped_incomes['Сумма']) + list(grouped_incomes_['Сумма'])
    incomes_values = ['0'] * len(grouped_incomes['Сумма']) + list(grouped_incomes_['Сумма'])
    incomes_ids = income_account_ids + income_contractor_ids

    
    # # # Создание графика treemap для доходов
    fig_incomes = go.Figure(go.Treemap(
         ids=incomes_ids,
         labels=incomes_labels,
         parents=incomes_parents,
         values=incomes_values
      ))
    fig_incomes.update_layout(title="Структура доходов")

    # Создание графика для анализа клиентов
    fig_customers = go.Figure()
    fig_customers.add_trace(
        go.Scatter(
            x=df_filtered['Дата'], 
            y=df_filtered['Сумма'], 
            mode='lines+markers', 
            name='ПО'
        )
    )
    fig_customers.add_trace(
        go.Scatter(
            x=df_filtered['Дата'], 
            y=df_filtered['Сумма'], 
            mode='lines+markers', 
            name=' '
        )
    )
    fig_customers.update_layout(
        title='Число покупателей за месяц', 
        yaxis_title='Число покупателей (тыс.)'
    )
    
    return fig_profit, fig_incomes, fig_expenses, fig_customers
