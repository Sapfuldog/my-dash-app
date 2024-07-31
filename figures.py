from plotly.subplots import make_subplots
import plotly.graph_objects as go

def create_figures(df_filtered): 
    # Создание фигуры с несколькими подграфиками
    fig_profit = make_subplots(
        rows=2, cols=2,
        shared_xaxes=True, 
        shared_yaxes=True,
        vertical_spacing=0.05, 
        horizontal_spacing=0.01,
        row_heights=[0.2, 0.7],  # Устанавливаем высоту строк
        column_widths=[0.7, 0.02],  # Устанавливаем ширину колонок
        specs=[[{"type": "histogram"}, {"type": "scatter"}],
               [{"type": "scatter"}, {"type": "histogram"}]]
    )

    # Добавление трасс на график
    fig_profit.add_trace(
        go.Scatter(                             
            x=df_filtered['Дата'],
            y=df_filtered['Накопительно'], 
            fill='tozeroy',
            line=dict(shape='spline'),
            showlegend=False
        ),
        row=2, col=1
    )   

    fig_profit.add_trace(
        go.Histogram(
            x=df_filtered['Дата'], 
            histfunc='sum',
            showlegend=False
        ),
        row=1, col=1
    )
    
    fig_profit.add_trace(
        go.Histogram(
            y=df_filtered['Накопительно'], 
            histfunc='sum',
            showlegend=False
        ),
        row=2, col=2
    )    

    # Обновление макета графика
    fig_profit.update_layout(
        title='',
        xaxis3_title='Дата',
        yaxis3_title=''
    )

    fig_profit.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='White', row=1, col=1)
    fig_profit.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='White', row=2, col=1)
    fig_profit.update_xaxes(matches='x')

    # Создание графика для анализа контрактов
    fig_contract = go.Figure()
    fig_contract.add_trace(
        go.Bar(
            x=df_filtered['Статья учета'], 
            y=df_filtered['Сумма'], 
            name='Статья'
        )
    )
    fig_contract.add_trace(
        go.Bar(
            x=df_filtered['Контрагент'], 
            y=df_filtered['Сумма'], 
            name='Контрагент'
        )
    )
    fig_contract.update_layout(
        title=' ', 
        barmode='group'
    )

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
    
    return fig_profit, fig_contract, fig_customers
