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
        row_heights=[0.7, 0.7, 4.7],  # Устанавливаем высоту строк
        column_widths=[0.7, 0.02],  # Устанавливаем ширину колонок
        specs=[[{"type": "bar"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "histogram"}],
               [{"type": "scatter"}, {"type": "histogram"}]]
    )

    start_date = datetime.now()
    df_filtered_by_date = df_filtered[df_filtered['Дата'] >= start_date]
    df_filtered_by_date_undo = df_filtered[df_filtered['Дата'] < start_date]

    df_pos = df_filtered[df_filtered['Сумма'] > 0]
    df_neg = df_filtered[df_filtered['Сумма'] < 0] 
    df_neg.loc[:, 'Сумма'] = -df_neg['Сумма']

    weekly_pos = df_pos.resample('W-Mon', on='Дата')['Сумма'].sum().reset_index()
    weekly_neg = df_neg.resample('W-Mon', on='Дата')['Сумма'].sum().reset_index()

    def SetGreenColor(y):
        start_color = (153, 255, 153)  # (99ff99)
        end_color = (0, 128, 0)        # (008000)
        
        if y <= 0:
            return '#{:02x}{:02x}{:02x}'.format(*start_color)
        elif y >= 50000000:
            return '#{:02x}{:02x}{:02x}'.format(*end_color)
        else:
            ratio = y / 50000000
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    
    def SetRedColor(y):
        start_color = (255, 153, 153)  # (ff9999)
        end_color = (128, 0, 0)        # (800000)
        
        if y <= 0:
            return '#{:02x}{:02x}{:02x}'.format(*start_color)
        elif y >= 50000000:
            return '#{:02x}{:02x}{:02x}'.format(*end_color)
        else:
            ratio = y / 50000000
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    fig_profit.add_trace(
        go.Bar(                             
            x=weekly_pos['Дата'],
            y=weekly_pos['Сумма'], 
            showlegend=False,
            marker=dict(color=list(map(SetGreenColor, weekly_pos['Сумма'])))
        ),
        row=1, col=1
    ) 

    fig_profit.add_trace(
        go.Bar(                             
            x=weekly_neg['Дата'],
            y=weekly_neg['Сумма'], 
            showlegend=False,
            marker=dict(color=list(map(SetRedColor, weekly_neg['Сумма'])))
        ),
        row=2, col=1
    ) 
    
    fig_profit.add_trace(
        go.Scatter(                             
            x=df_filtered_by_date['Дата'],
            y=df_filtered_by_date['Накопительно'], 
            showlegend=False,
            marker_color='blue',
            connectgaps=True
        ),
        row=3, col=1
    )
    fig_profit.add_trace(
        go.Scatter(                             
            x=df_filtered_by_date_undo['Дата'],
            y=df_filtered_by_date_undo['Накопительно'], 
            showlegend=False,
            marker_color='#04adef',
            connectgaps=True
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

    fig_profit.update_layout(
        title='',
        xaxis=dict(title=''),
        yaxis=dict(title=''),
        xaxis2=dict(title=''),
        yaxis2=dict(title=''),
        xaxis3=dict(title=''),
        yaxis3=dict(title=''),
        xaxis4=dict(title=''),
        yaxis4=dict(title=''),
        xaxis5=dict(title='Дата'),
        yaxis5=dict(title=''),
        xaxis6=dict(title=''),
        yaxis6=dict(title='')
    )

    fig_profit.update_xaxes(matches='x')
    fig_profit.update_xaxes(tickfont=dict(size=1), row=3, col=2)
    fig_profit.update_yaxes(
        type='log',
        range=[0, 10],
        tickfont=dict(size=6),
        row=1, col=1
    )
    fig_profit.update_yaxes(
        type='log',
        range=[0, 5],
        tickfont=dict(size=6),
        autorange='reversed',
        row=2, col=1
    )

    expenses_df['Сумма'] = expenses_df['Сумма'].abs()

    grouped_expenses = expenses_df.groupby('Статья учета')['Сумма'].sum().reset_index()
    grouped_expenses_ = expenses_df.groupby(['Статья учета', 'Контрагент'])['Сумма'].sum().reset_index()
    grouped_expenses_1_ = expenses_df.groupby(['Статья учета', 'Контрагент', 'Заказ'])['Сумма'].sum().reset_index()

    expense_account_ids = [f"exp - {i}" for i in range(len(grouped_expenses))]
    expense_contractor_ids = []
    expense_order_ids = []

    for i in range(len(grouped_expenses)):
        contractors = grouped_expenses_.loc[grouped_expenses_['Статья учета'] == grouped_expenses.iloc[i, 0]]
        for j in range(len(contractors)):
            expense_contractor_ids.append(f"exp - {i} - {j}")


    expenses_labels = (
        [f"{row['Статья учета']}<br>{row['Сумма']:,}" for _, row in grouped_expenses.iterrows()] +
        [f"{row['Контрагент']}<br>{row['Сумма']:,}" for _, row in grouped_expenses_.iterrows()]
    )
    
    expenses_parents = (
        [''] * len(grouped_expenses) +
        [f"exp - {i}" for i in range(len(grouped_expenses)) for _ in range(len(grouped_expenses_.loc[grouped_expenses_['Статья учета'] == grouped_expenses.iloc[i, 0]]))] 
    )
    
    expenses_values = (
        ['0'] * len(grouped_expenses) +
        list(grouped_expenses_['Сумма'])
    )
    
    fig_expenses = go.Figure(go.Treemap(
        ids=expense_account_ids + expense_contractor_ids + expense_order_ids,
        labels=expenses_labels,
        parents=expenses_parents,
        values=expenses_values
    ))
    fig_expenses.update_layout(title="Структура расходов")

    grouped_incomes = incomes_df.groupby('Статья учета')['Сумма'].sum().reset_index()
    grouped_incomes_ = incomes_df.groupby(['Статья учета', 'Контрагент'])['Сумма'].sum().reset_index()
    grouped_incomes_1_ = incomes_df.groupby(['Статья учета', 'Контрагент', 'Заказ'])['Сумма'].sum().reset_index()

    income_account_ids = [f"inc - {i}" for i in range(len(grouped_incomes))]
    income_contractor_ids = []
    income_order_ids = []

    for i in range(len(grouped_incomes)):
        contractors = grouped_incomes_.loc[grouped_incomes_['Статья учета'] == grouped_incomes.iloc[i, 0]]
        for j in range(len(contractors)):
            income_contractor_ids.append(f"inc - {i} - {j}")

    incomes_labels = (
        [f"{row['Статья учета']}<br>{row['Сумма']:,}" for _, row in grouped_incomes.iterrows()] +
        [f"{row['Контрагент']}<br>{row['Сумма']:,}" for _, row in grouped_incomes_.iterrows()]
    )
    
    incomes_parents = (
        [''] * len(grouped_incomes) +
        [f"inc - {i}" for i in range(len(grouped_incomes)) for _ in range(len(grouped_incomes_.loc[grouped_incomes_['Статья учета'] == grouped_incomes.iloc[i, 0]]))])
    
    incomes_values = (
        ['0'] * len(grouped_incomes) +
        list(grouped_incomes_['Сумма'])
    )
    
    fig_incomes = go.Figure(go.Treemap(
        ids=income_account_ids + income_contractor_ids + income_order_ids,
        labels=incomes_labels,
        parents=incomes_parents,
        values=incomes_values
    ))
    fig_incomes.update_layout(title="Структура доходов")

    fig_pie_ras = go.Figure(go.Sunburst(
        ids= expense_account_ids + expense_contractor_ids + expense_order_ids,
        labels = expenses_labels,
        parents = expenses_parents,
        textinfo='label+percent entry',  # добавляем подписи с долями
        hovertemplate='<b>%{label}:</b> %{value}<br>Доля: %{percentRoot:.2%}<extra></extra>',
        values = expenses_values       
        )  
    )
    fig_pie_ras.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    
    
    
    fig_pie_pos = go.Figure(go.Sunburst(
        ids= income_account_ids + income_contractor_ids + income_order_ids,
        labels = incomes_labels,
        parents = incomes_parents,
        textinfo='label+percent entry',  # добавляем подписи с долями
        hovertemplate='<b>%{label}:</b> %{value}<br>Доля: %{percentRoot:.2%}<extra></extra>',
        values = incomes_values        
        )  
    )
    fig_pie_ras.update_layout(margin = dict(t=0, l=0, r=0, b=0))

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
    
    return fig_profit, fig_incomes, fig_expenses, fig_customers, fig_pie_ras, fig_pie_pos
