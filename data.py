import numpy as np
import pandas as pd


# Определяем количество строк
num_rows = 10000

# Создаем примеры данных
data = {
    'Дата': pd.date_range(start='2023-01-01', periods=num_rows, freq='h'),
    'Контрагент': np.random.choice(['Компания А', 'Компания B', 'Компания C', 'Компания D', 
                                    'Компания E', 'Компания F', 'Компания G', 'Компания H', 
                                    'Компания I', 'Компания J'], size=num_rows),
    'Сумма': np.random.randint(-48000, 50000, size=num_rows),
    'Договор': [f'Договор №{i}' for i in np.random.randint(1, 1000, size=num_rows)],
    'Статья учета': np.random.choice(['Услуги', 'Товары', 'Аренда', 'Зарплата', 'Командировки', 
                                      'Закупки', 'Прочее', 'Капитальные затраты', 'Реклама', 
                                      'Консультации'], size=num_rows),
    'Банковский счет': [f'Счет №{np.random.randint(1000, 9999)}' for _ in range(num_rows)]
}

# Создаем DataFrame
df = pd.DataFrame(data)
df['ДатаД'] = df['Дата'].dt.to_period('D').dt.to_timestamp()
df['ДатаМ'] = df['Дата'].dt.to_period('M').dt.to_timestamp()
df['Дата '] = df['Дата'].dt.to_period('M')
df['Накопительно'] = df['Сумма'].cumsum()

# Группируем по дате и считаем сумму
df_sum = df.groupby('Дата ')['Сумма'].sum().reset_index()

# Группируем по дате и считаем количество записей
df_count = df.groupby('Дата ')['Сумма'].count().reset_index()
df_count.rename(columns={'Сумма': 'Количество'}, inplace=True)

# Объединяем данные о суммах и количестве
df_M = pd.merge(df_sum, df_count, on='Дата ')
df_M['Дата '] = df_M['Дата '].dt.to_timestamp()
df_M['Цвета'] = df_M['Сумма'].apply(lambda x: 'rgb(0,255,0)' if x >= 0 else 'rgb(255,0,0)')

# Создаем DataFrame для таблицы
df_A = df[['Дата', 'Контрагент', 'Сумма', 'Договор', 'Статья учета', 'Банковский счет']].drop_duplicates()

def get_data():
    return df, df_A, df_M
