from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import random

# Вспомогательные функции
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

def generate_random_color():
    return '#{:06x}'.format(random.randint(0, 0xFFFFFF))

def prepare_data(df_filtered):
    df_filtered['Накопительно'] = df_filtered['Сумма'].cumsum()

    # Фильтрация данных
    expenses_df = df_filtered[df_filtered['Сумма'] < 0].copy()
    incomes_df = df_filtered[df_filtered['Сумма'] > 0].copy()

    # Подготовка данных по дате
    start_date = datetime.now()
    df_filtered_by_date = df_filtered[df_filtered['Дата'] >= start_date]
    df_filtered_by_date_undo = df_filtered[df_filtered['Дата'] < start_date]

    # Подготовка данных по неделям
    df_pos = df_filtered[df_filtered['Сумма'] > 0]
    df_neg = df_filtered[df_filtered['Сумма'] < 0]
    df_neg['Сумма'] = -df_neg['Сумма']

    weekly_pos = df_pos.resample('W-Mon', on='Дата')['Сумма'].sum().reset_index()
    weekly_neg = df_neg.resample('W-Mon', on='Дата')['Сумма'].sum().reset_index()

    return df_filtered, df_filtered_by_date, df_filtered_by_date_undo, weekly_pos, weekly_neg, expenses_df, incomes_df

def create_figures(df_filtered):
    # Подготовка данных
    df_filtered, df_filtered_by_date, df_filtered_by_date_undo, weekly_pos, weekly_neg, expenses_df, incomes_df = prepare_data(df_filtered)

    # Создание графиков
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

    # Добавление данных на графики
    fig_profit.add_trace(
        go.Bar(                             
            x=weekly_pos['Дата'],
            y=weekly_pos['Сумма'], 
            showlegend=False,
            marker=dict(color=[SetGreenColor(value) for value in weekly_pos['Сумма']])
        ),
        row=1, col=1
    ) 

    fig_profit.add_trace(
        go.Bar(                             
            x=weekly_neg['Дата'],
            y=weekly_neg['Сумма'], 
            showlegend=False,
            marker=dict(color=[SetRedColor(value) for value in weekly_neg['Сумма']])
        ),
        row=2, col=1
    ) 
    
    fig_profit.add_trace(
        go.Scatter(                             
            x=df_filtered_by_date['Дата'],
            y=df_filtered_by_date['Накопительно'], 
            showlegend=False,
            line=dict(color='blue'),
            connectgaps=True
        ),
        row=3, col=1
    )
    fig_profit.add_trace(
        go.Scatter(                             
            x=df_filtered_by_date_undo['Дата'],
            y=df_filtered_by_date_undo['Накопительно'], 
            showlegend=False,
            line=dict(color='#04adef'),
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

    # Обновление макета для fig_profit
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
        range=[4, 10],
        tickfont=dict(size=6),
        #tickvals=[1e4, 1e5, 1e6, 1e8, 1e9],  # Установка шагов на оси
        #ticktext=['10k', '100k', '1M', '100M', '1B'],  # Отображаемые значения
        row=1, col=1
    )
    fig_profit.update_yaxes(
        type='log',
        range=[4, 10],
        tickfont=dict(size=6),
        #tickvals=[1e4, 1e5, 1e6, 1e8, 1e9],  # Установка одинаковых шагов на оси
        #ticktext=['10k', '100k', '1M', '100M', '1B'],  # Отображаемые значения
        autorange='reversed',
        row=2, col=1
    )

    # Подготовка данных для расходных графиков
    expenses_df['Сумма'] = expenses_df['Сумма'].abs()
    grouped_expenses = expenses_df.groupby('Статья учета')['Сумма'].sum().reset_index()
    grouped_expenses_ = expenses_df.groupby(['Статья учета', 'Контрагент'])['Сумма'].sum().reset_index()

    expense_account_ids = [f"exp - {i}" for i in range(len(grouped_expenses))]
    expense_contractor_ids = [
        f"exp - {i} - {j}"
        for i in range(len(grouped_expenses))
        for j in range(len(grouped_expenses_.loc[grouped_expenses_['Статья учета'] == grouped_expenses.iloc[i, 0]]))
    ]
    expenses_labels = (
        [f"{row['Статья учета']}<br>{row['Сумма']:,.2f}" for _, row in grouped_expenses.iterrows()] +
        [f"{row['Контрагент']}<br>{row['Сумма']:,.2f}" for _, row in grouped_expenses_.iterrows()]
    )
    expenses_parents = (
        [''] * len(grouped_expenses) +
        [f"exp - {i}" for i in range(len(grouped_expenses)) for _ in range(len(grouped_expenses_.loc[grouped_expenses_['Статья учета'] == grouped_expenses.iloc[i, 0]]))]
    )
    expenses_values = [0] * len(grouped_expenses) + list(grouped_expenses_['Сумма'])
    account_colors = {label: generate_random_color() for label in grouped_expenses['Статья учета']}
    colors = [account_colors[label] for label in grouped_expenses['Статья учета']]
    
    # Создание графиков Treemap для расходов
    fig_expenses = go.Figure(go.Treemap(
        ids=expense_account_ids + expense_contractor_ids,
        labels=expenses_labels,
        parents=expenses_parents,
        values=expenses_values,
        marker=dict(colors=colors)
    ))
    fig_expenses.update_layout(title="Структура расходов")

    # Подготовка данных для доходных графиков
    grouped_incomes = incomes_df.groupby('Статья учета')['Сумма'].sum().reset_index()
    grouped_incomes_ = incomes_df.groupby(['Статья учета', 'Контрагент'])['Сумма'].sum().reset_index()

    income_account_ids = [f"inc - {i}" for i in range(len(grouped_incomes))]
    income_contractor_ids = [
        f"inc - {i} - {j}"
        for i in range(len(grouped_incomes))
        for j in range(len(grouped_incomes_.loc[grouped_incomes_['Статья учета'] == grouped_incomes.iloc[i, 0]]))
    ]
    incomes_labels = (
        [f"{row['Статья учета']}<br>{row['Сумма']:,.2f}" for _, row in grouped_incomes.iterrows()] +
        [f"{row['Контрагент']}<br>{row['Сумма']:,.2f}" for _, row in grouped_incomes_.iterrows()]
    )
    incomes_parents = (
        [''] * len(grouped_incomes) +
        [f"inc - {i}" for i in range(len(grouped_incomes)) for _ in range(len(grouped_incomes_.loc[grouped_incomes_['Статья учета'] == grouped_incomes.iloc[i, 0]]))]
    )
    incomes_values = [0] * len(grouped_incomes) + list(grouped_incomes_['Сумма'])
    account_colors_2 = {label: generate_random_color() for label in grouped_incomes['Статья учета']}
    colors_2 = [account_colors_2[label] for label in grouped_incomes['Статья учета']]
    
    # Создание графиков Treemap для доходов
    fig_incomes = go.Figure(go.Treemap(
        ids=income_account_ids + income_contractor_ids,
        labels=incomes_labels,
        parents=incomes_parents,
        values=incomes_values,
        marker=dict(colors=colors_2)
    ))
    fig_incomes.update_layout(title="Структура доходов")

    # Создание диаграмм Sunburst для расходов
    fig_pie_ras = go.Figure(go.Sunburst(
        ids=expense_account_ids + expense_contractor_ids,
        labels=expenses_labels,
        parents=expenses_parents,
        textinfo='label+percent entry',
        hovertemplate='<b>%{label}:</b> %{value}<br>Доля: %{percentRoot:.2%}<extra></extra>',
        values=expenses_values,
        insidetextorientation='radial',
        marker=dict(colors=colors)  # Применяем те же цвета
    ))
    fig_pie_ras.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    
    # Создание диаграмм Sunburst для доходов
    fig_pie_pos = go.Figure(go.Sunburst(
        ids=income_account_ids + income_contractor_ids,
        labels=incomes_labels,
        parents=incomes_parents,
        textinfo='label+percent entry',
        hovertemplate='<b>%{label}:</b> %{value}<br>Доля: %{percentRoot:.2%}<extra></extra>',
        values=incomes_values,
        insidetextorientation='radial',
        marker=dict(colors=colors_2)  # Применяем те же цвета
    ))
    fig_pie_pos.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    # Создание графика числа покупателей
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
