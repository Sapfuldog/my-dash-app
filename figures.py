from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, date
import random
from matplotlib import colors as mcolors

def wrap_text(text, max_length=20):
    """Разбивает текст на несколько строк, если его длина превышает max_length."""
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        # Если добавление слова в текущую строку превышает max_length
        if len(current_line) + len(word) + 1 > max_length:
            # Добавляем текущую строку в список строк и начинаем новую строку
            lines.append(current_line)
            current_line = word
        else:
            # Добавляем слово в текущую строку
            if current_line:
                current_line += ' '
            current_line += word
    
    # Добавляем последнюю строку в список строк
    if current_line:
        lines.append(current_line)
    
    # Возвращаем строки, соединенные переносами
    return '<br>'.join(lines)



def interpolate_color(start_color, end_color, factor):
    """Интерполирует цвет от start_color к end_color на основе фактора."""
    start_rgb = mcolors.hex2color(start_color)
    end_rgb = mcolors.hex2color(end_color)
    interpolated_rgb = [start + (end - start) * factor for start, end in zip(start_rgb, end_rgb)]
    return mcolors.to_hex(interpolated_rgb)

def generate_gradient_color(value, min_value, max_value, income=True):
    """Генерирует цвет на основе градиента для заданного значения."""
    # Нормализация значения
    if max_value == min_value:
        norm = 1  # Нормализация на случай, если все значения одинаковы
    else:
        norm = (value - min_value) / (max_value - min_value)

    # Обработка граничных условий
    if np.isnan(norm):
        norm = 1 if income else 0
    norm = np.clip(norm, 0, 1)

    if value == max_value:
        return '#29f340' if income else '#ff0000'  # Зеленый или Красный цвет на границе

    if income:
        # Градиент от синего к зеленому
        return interpolate_color('#0000ff', '#29f340', norm)
    else:
        # Градиент от фиолетового к красному
        return interpolate_color('#800080', '#ff0000', norm)
# Пользовательская палитра Teal
teal_colorscale = [
    (0, 'rgb(175, 238, 238)'),   # Pale Turquoise
    (0.05, 'rgb(159, 233, 233)'),
    (0.1, 'rgb(143, 228, 228)'),
    (0.15, 'rgb(127, 223, 223)'),
    (0.2, 'rgb(111, 218, 218)'),
    (0.25, 'rgb(127, 255, 212)'), # Aquamarine
    (0.3, 'rgb(100, 245, 201)'),
    (0.35, 'rgb(75, 235, 190)'),
    (0.4, 'rgb(50, 225, 179)'),
    (0.45, 'rgb(25, 215, 168)'),
    (0.5, 'rgb(72, 209, 204)'),  # Medium Turquoise
    (0.55, 'rgb(45, 200, 190)'),
    (0.6, 'rgb(20, 190, 176)'),
    (0.65, 'rgb(0, 180, 162)'),
    (0.7, 'rgb(0, 170, 148)'),
    (0.75, 'rgb(32, 178, 170)'), # Light Sea Green
    (0.8, 'rgb(20, 170, 155)'),
    (0.85, 'rgb(10, 160, 140)'),
    (0.9, 'rgb(0, 150, 125)'),
    (0.95, 'rgb(0, 140, 115)'),
    (1, 'rgb(0, 128, 128)')      # Teal
]

sunsetdark_colorscale = [
    (0, 'rgb(255, 241, 0)'),         # Bright Yellow
    (0.05, 'rgb(255, 232, 0)'),
    (0.1, 'rgb(255, 222, 0)'),
    (0.15, 'rgb(255, 212, 0)'),
    (0.2, 'rgb(255, 202, 0)'),
    (0.25, 'rgb(255, 82, 82)'),       # Light Coral
    (0.3, 'rgb(255, 108, 83)'),
    (0.35, 'rgb(255, 133, 85)'),
    (0.4, 'rgb(255, 158, 87)'),
    (0.45, 'rgb(255, 183, 90)'),
    (0.5, 'rgb(255, 193, 7)'),        # Amber
    (0.55, 'rgb(255, 206, 50)'),
    (0.6, 'rgb(255, 219, 90)'),
    (0.65, 'rgb(255, 232, 130)'),
    (0.7, 'rgb(255, 245, 170)'),
    (0.75, 'rgb(255, 152, 0)'),       # Orange
    (0.8, 'rgb(255, 167, 38)'),
    (0.85, 'rgb(255, 182, 76)'),
    (0.9, 'rgb(255, 197, 115)'),
    (0.95, 'rgb(255, 212, 154)'),
    (1, 'rgb(255, 87, 34)')           # Deep Orange (Sunset)
]

def assign_colors(values, colorscale):
    """
    Назначает цвета значениям из пользовательской палитры.
    
    :param values: список значений
    :param colorscale: список кортежей (порог, цвет)
    :return: список цветов
    """
    # Нормализация значений в диапазон [0, 1]
    if not values.empty:
        min_val = min(values)
        max_val = max(values)
    else:
        min_val = 1
        max_val = 1
    
    norm_values = [(val - min_val) / (max_val - min_val) if max_val != min_val else 1 for val in values]
    
    # Функция для интерполяции цвета
    def interpolate_color(t, colorscale):
        for i in range(1, len(colorscale)):
            if t <= colorscale[i][0]:
                t0, c0 = colorscale[i-1]
                t1, c1 = colorscale[i]
                ratio = (t - t0) / (t1 - t0)
                color = tuple(
                    int(c0[i] + ratio * (c1[i] - c0[i]))
                    for i in range(3)
                )
                return f'rgb{color}'
        return colorscale[-1][1]
    
    # Преобразование цветов из формата 'rgb(r, g, b)' в кортеж (r, g, b)
    colorscale = [(t, tuple(map(int, c[4:-1].split(',')))) for t, c in colorscale]
    
    # Назначение цветов
    colors = [interpolate_color(t, colorscale) for t in norm_values]
    
    return colors   
    

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
    incomes_df = incomes_df[incomes_df['Статья учета'] != 'Остаток на р/с']
    
    # Подготовка данных по дате
    start_date = datetime.now()
    df_filtered_by_date = df_filtered[df_filtered['Дата'] >= start_date]
    df_filtered_by_date_undo = df_filtered[df_filtered['Дата'] < start_date]

    # Подготовка данных по неделям
    df_pos = df_filtered[(df_filtered['Сумма'] > 0) & (df_filtered['Статья учета'] != 'Остаток на р/с')]
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
        column_widths=[0.7, 0.07],  # Устанавливаем ширину колонок
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
            line=dict(color='#0015ff'),
            connectgaps=True
        ),
        row=3, col=1
    )
    fig_profit.add_trace(
        go.Scatter(                             
            x=df_filtered_by_date_undo['Дата'],
            y=df_filtered_by_date_undo['Накопительно'], 
            showlegend=False,
            line=dict(color='#00fffb'),
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
        title={
        'font': {
            'size': 17,  # Размер шрифта
            'family': 'Open Sans'  # Семейство шрифта
        },
        'yanchor': 'top'
        },
        xaxis=dict(title='',gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(title='',gridcolor='rgba(128,128,128,0.2)'),
        xaxis2=dict(title='',gridcolor='rgba(128,128,128,0.2)'),
        yaxis2=dict(title='',gridcolor='rgba(128,128,128,0.2)'),
        xaxis3=dict(title='',gridcolor='rgba(128,128,128,0.2)'),
        yaxis3=dict(title='',gridcolor='rgba(128,128,128,0.2)'),
        xaxis4=dict(title='',gridcolor='rgba(128,128,128,0.2)'),
        yaxis4=dict(title='',gridcolor='rgba(128,128,128,0.2)'),
        xaxis5=dict(title='Дата',gridcolor='rgba(128,128,128,0.2)'),
        yaxis5=dict(title='',gridcolor='rgba(128,128,128,0.2)'),
        xaxis6=dict(title='',gridcolor='rgba(128,128,128,0.2)'),
        yaxis6=dict(title='',gridcolor='rgba(128,128,128,0.2)'),
        plot_bgcolor='rgba(0,0,0,0)',  # Прозрачный фон графика
        paper_bgcolor='rgba(0,0,0,0)'
    )

    fig_profit.update_xaxes(matches='x')
    fig_profit.update_xaxes(tickfont=dict(size=8), row=3, col=2)
    fig_profit.update_yaxes(
        type='log',
        range=[4, 10],
        tickfont=dict(size=8),
        #tickvals=[1e4, 1e5, 1e6, 1e8, 1e9],  # Установка шагов на оси
        #ticktext=['10k', '100k', '1M', '100M', '1B'],  # Отображаемые значения
        row=1, col=1
    )
    fig_profit.update_yaxes(
        type='log',
        range=[4, 10],
        tickfont=dict(size=8),
        #tickvals=[1e4, 1e5, 1e6, 1e8, 1e9],  # Установка одинаковых шагов на оси
        #ticktext=['10k', '100k', '1M', '100M', '1B'],  # Отображаемые значения
        autorange='reversed',
        row=2, col=1
    )

    # Подготовка данных для расходных графиков
    # Приведение сумм к абсолютному значению
    expenses_df['Сумма'] = expenses_df['Сумма'].abs()

    # Группировка данных
    grouped_expenses = expenses_df.groupby('Статья учета')['Сумма'].sum().reset_index()
    grouped_expenses_ = expenses_df.groupby(['Статья учета', 'Контрагент'])['Сумма'].sum().reset_index()
    grouped_expenses_d = expenses_df.groupby(['Статья учета', 'Контрагент', 'Договор'])['Сумма'].sum().reset_index()

    # Создание идентификаторов
    expense_account_ids = [f"exp_{i+1}" for i in range(len(grouped_expenses))]
    expense_contractor_ids = [
        f"exp_{i+1}_{j+1}"
        for i in range(len(grouped_expenses))
        for j in range(len(grouped_expenses_.loc[grouped_expenses_['Статья учета'] == grouped_expenses.iloc[i, 0]]))
    ]
    expense_contract_ids = [
        f"exp_{i+1}_{j+1}_{k+1}"
        for i in range(len(grouped_expenses))
        for j in range(len(grouped_expenses_.loc[grouped_expenses_['Статья учета'] == grouped_expenses.iloc[i, 0]]))
        for k in range(len(grouped_expenses_d.loc[(grouped_expenses_d['Статья учета'] == grouped_expenses.iloc[i, 0]) & (grouped_expenses_d['Контрагент'] == grouped_expenses_.loc[grouped_expenses_['Статья учета'] == grouped_expenses.iloc[i, 0]].iloc[j, 1])]))
    ]

    # Создание меток
    expenses_labels = (
        [f"{wrap_text(row['Статья учета'])}<br>{row['Сумма']:,.2f}" for _, row in grouped_expenses.iterrows()] +
        [f"{wrap_text(row['Контрагент'])}<br>{row['Сумма']:,.2f}" for _, row in grouped_expenses_.iterrows()] +
        [f"{wrap_text(row['Договор'])}<br>{row['Сумма']:,.2f}" for _, row in grouped_expenses_d.iterrows()]
    )

    # Создание родительских связей
    expenses_parents = (
        [''] * len(grouped_expenses) +
        [f"exp_{i+1}" for i in range(len(grouped_expenses)) for _ in range(len(grouped_expenses_.loc[grouped_expenses_['Статья учета'] == grouped_expenses.iloc[i, 0]]))] +
        [f"exp_{i+1}_{j+1}" for i in range(len(grouped_expenses)) 
                            for j in range(len(grouped_expenses_.loc[grouped_expenses_['Статья учета'] == grouped_expenses.iloc[i, 0]])) 
                            for _ in range(len(grouped_expenses_d.loc[(grouped_expenses_d['Статья учета'] == grouped_expenses.iloc[i, 0]) & (grouped_expenses_d['Контрагент'] == grouped_expenses_.loc[grouped_expenses_['Статья учета'] == grouped_expenses.iloc[i, 0]].iloc[j, 1])]))]
    )

    # Создание значений
    expenses_values = [0] * len(grouped_expenses) + [0] * len(grouped_expenses_) + list(grouped_expenses_d['Сумма'])
    expenses_values_C = list(grouped_expenses['Сумма']) + list(grouped_expenses_['Сумма']) + list(grouped_expenses_d['Сумма'])
    expenses_values_C = pd.DataFrame(expenses_values_C, columns=['Сумма'])
    expenses_values_C['Цвет'] = assign_colors(expenses_values_C['Сумма'], sunsetdark_colorscale)
    # Получение максимального и минимального значений
    max_value = grouped_expenses['Сумма'].max()
    min_value = grouped_expenses['Сумма'].min()

    # Создание графика Treemap для расходов
    fig_expenses = go.Figure(go.Treemap(
        ids=expense_account_ids + expense_contractor_ids + expense_contract_ids,
        labels=expenses_labels,
        parents=expenses_parents,
        values=expenses_values,
        marker=dict(        
            #colorscale="Sunsetdark",
            colors=expenses_values_C['Цвет'],
            line=dict(color='rgba(255,255,255,0.5)')
        )
    ))
    fig_expenses.update_layout(
        title={
        'font': {
            'size': 17,  # Размер шрифта
            'family': 'Open Sans'  # Семейство шрифта
        },
        'yanchor': 'top'
        },
        paper_bgcolor='rgba(0,0,0,0)')
    fig_expenses.update_traces(root=dict(color='white'))

    # Подготовка данных для доходных графиков
    grouped_incomes = incomes_df.groupby('Статья учета')['Сумма'].sum().reset_index()
    grouped_incomes_ = incomes_df.groupby(['Статья учета', 'Контрагент'])['Сумма'].sum().reset_index()
    grouped_incomes_d = incomes_df.groupby(['Статья учета', 'Контрагент', 'Договор'])['Сумма'].sum().reset_index()
    
    # Создание идентификаторов
    incomes_account_ids = [f"exp_{i+1}" for i in range(len(grouped_incomes))]
    incomes_contractor_ids = [
        f"exp_{i+1}_{j+1}"
        for i in range(len(grouped_incomes))
        for j in range(len(grouped_incomes_.loc[grouped_incomes_['Статья учета'] == grouped_incomes.iloc[i, 0]]))
    ]
    incomes_contract_ids = [
        f"exp_{i+1}_{j+1}_{k+1}"
        for i in range(len(grouped_incomes))
        for j in range(len(grouped_incomes_.loc[grouped_incomes_['Статья учета'] == grouped_incomes.iloc[i, 0]]))
        for k in range(len(grouped_incomes_d.loc[(grouped_incomes_d['Статья учета'] == grouped_incomes.iloc[i, 0]) & (grouped_incomes_d['Контрагент'] == grouped_incomes_.loc[grouped_incomes_['Статья учета'] == grouped_incomes.iloc[i, 0]].iloc[j, 1])]))
    ]

    # Создание меток
    incomes_labels = (
        [f"{wrap_text(row['Статья учета'])}<br>{row['Сумма']:,.2f}" for _, row in grouped_incomes.iterrows()] +
        [f"{wrap_text(row['Контрагент'])}<br>{row['Сумма']:,.2f}" for _, row in grouped_incomes_.iterrows()] +
        [f"{wrap_text(row['Договор'])}<br>{row['Сумма']:,.2f}" for _, row in grouped_incomes_d.iterrows()]
    )

    # Создание родительских связей
    incomes_parents = (
        [''] * len(grouped_incomes) +
        [f"exp_{i+1}" for i in range(len(grouped_incomes)) for _ in range(len(grouped_incomes_.loc[grouped_incomes_['Статья учета'] == grouped_incomes.iloc[i, 0]]))] +
        [f"exp_{i+1}_{j+1}" for i in range(len(grouped_incomes)) 
                            for j in range(len(grouped_incomes_.loc[grouped_incomes_['Статья учета'] == grouped_incomes.iloc[i, 0]])) 
                            for _ in range(len(grouped_incomes_d.loc[(grouped_incomes_d['Статья учета'] == grouped_incomes.iloc[i, 0]) & (grouped_incomes_d['Контрагент'] == grouped_incomes_.loc[grouped_incomes_['Статья учета'] == grouped_incomes.iloc[i, 0]].iloc[j, 1])]))]
    )

    # Создание значений
    incomes_values = [0] * len(grouped_incomes) + [0] * len(grouped_incomes_) + list(grouped_incomes_d['Сумма'])
    incomes_values_C = list(grouped_incomes['Сумма']) + list(grouped_incomes_['Сумма']) + list(grouped_incomes_d['Сумма'])
    incomes_values_C = pd.DataFrame(incomes_values_C, columns=['Сумма'])
    incomes_values_C['Цвет'] = assign_colors(incomes_values_C['Сумма'], teal_colorscale)
    # Создание графиков Treemap для доходов
    fig_incomes = go.Figure(go.Treemap(
        ids=incomes_account_ids + incomes_contractor_ids + incomes_contract_ids,
        labels=incomes_labels,
        parents=incomes_parents,
        values=incomes_values,
        marker=dict(
            #colorscale="Teal",
            colors=incomes_values_C['Цвет'],
            line=dict(color='rgba(255,255,255,0.5)')
        )
    ))

    fig_incomes.update_layout(
        title={
            'font': {
                'size': 17,  # Размер шрифта
                'family': 'Open Sans'  # Семейство шрифта
            },
            'yanchor': 'top'
        },
        paper_bgcolor='rgba(0,0,0,0)'
    )
    # Создание диаграмм Sunburst для расходов
    fig_pie_ras = go.Figure(go.Sunburst(
        ids=expense_account_ids + expense_contractor_ids + expense_contract_ids,
        labels=expenses_labels,
        parents=expenses_parents,
        textinfo='label+percent entry',
        hovertemplate='<b>%{label}:</b> %{value}<br>Доля: %{percentRoot:.2%}<extra></extra>',
        values=expenses_values,
        insidetextorientation='radial',
        marker=dict(
            #colorscale="Sunsetdark",
            colors=expenses_values_C['Цвет'],
            line=dict(color='rgba(255,255,255,0.5)')
            )  # Применяем те же цвета
    ))
    fig_pie_ras.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        title={
        #'text': "Удельный вес расходов",
        #'y': 0.9,  # Устанавливаем позицию заголовка по вертикали
        #'x': 0,  # Устанавливаем позицию заголовка по горизонтали
        #'yanchor': 'top'
        },
        paper_bgcolor='rgba(0,0,0,0)')
    
    # Создание диаграмм Sunburst для доходов
    fig_pie_pos = go.Figure(go.Sunburst(
        ids=incomes_account_ids + incomes_contractor_ids + incomes_contract_ids,
        labels=incomes_labels,
        parents=incomes_parents,
        textinfo='label+percent entry',
        hovertemplate='<b>%{label}:</b> %{value}<br>Доля: %{percentRoot:.2%}<extra></extra>',
        values=incomes_values,
        insidetextorientation='radial',
        marker=dict(
            #colorscale="Teal",
            colors=incomes_values_C['Цвет'],
            line=dict(color='rgba(255,255,255,0.5)')
        )
        # Применяем те же цвета
    ))
    # Устанавливаем размеры диаграммы
    fig_pie_pos.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        title={
        #'text': "Удельный вес доходов",
        #'y': 0.9,  # Устанавливаем позицию заголовка по вертикали
        #'x': 0,  # Устанавливаем позицию заголовка по горизонтали
        #'yanchor': 'top'
    },
    paper_bgcolor='rgba(0,0,0,0)')

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
