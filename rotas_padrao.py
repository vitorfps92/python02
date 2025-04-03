from flask import Blueprint, render_template_string, request
import sqlite3
import pandas as pd
import plotly.express as px
import random
import config

# Rota do gráfico1
parte1 = Blueprint('padrao', __name__)

@parte1.route('/grafico1')
def grafico1():
    conn = sqlite3.connect(config.caminho_banco)
    df = pd.read_sql_query('''
        SELECT country, total_litres_of_pure_alcohol
        FROM drinks
        ORDER BY total_litres_of_pure_alcohol DESC
        LIMIT 10
        ''', conn)
    conn.close()
    fig = px.bar(
        df,
        x='country',
        y='total_litres_of_pure_alcohol',
        title='Top 10 países com maior consumo de álcool'
    )
    return fig.to_html() 