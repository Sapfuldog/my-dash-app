from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks

# Инициализация приложения Dash с Bootstrap темой и подавлением исключений колбэков
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"], suppress_callback_exceptions=True)

# Устанавливаем макет приложения
app.layout = create_layout()

# Регистрируем колбэки
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)

