# Importar as bibliotecas
from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio
import random

# Configura o plotly para abrir os arquivos no navegador por padrão
pio.renderers.default = 'browser'

# Carregar o drinks.csv
df = pd.read_csv('drinks.csv')

# Criar o banco de dados em sql e popular com os dados do arquivo csv
conn = sqlite3.connect('consumo_alcool.db')
df.to_sql('drinks', conn, if_exists='replace', index=False)
conn.commit()
conn.close()

# Iniciar o flask
app = Flask(__name__)

html_template = '''
    <h1> Dashboard - Consumo de álcool </h1>
    <h2> Parte 01 </h2>
        <ul>
            <li> <a href='/grafico1'> Top 10 países com maior consumo de álcool </a> </li>
            <li> <a href='/grafico2'> Média de consumo por tipo de bebida </a> </li>
            <li> <a href='/grafico3'> Consumo total por região </a> </li>
            <li> <a href='/grafico4'> Comparativo entre os tipos de bebidas </a> </li>
            <li> <a href='/pais?nome=Brazil'> Insight por país (ex: Brazil) </a> </li>
        </ul>
    <h2> Parte 02 </h2>
        <ul>
            <li><a href='/comparar'> Comparar </a></li>
            <li><a href='/upload_avengers'> Upload do csv </a></li>
            <li><a href='/apagar_avengers'> Apagar tabela Avengers </a></li>
            <li><a href='/atribuir_paises_avengers'> Atribuir países </a></li>
            <li><a href='/avengers_vs_drinks'> V.A.A (Vingadores Alcoolicos Anônimos) </a></li>
        </ul>
'''
# Rota inicial com os links para os gráficos
@app.route('/')
def index():
    return render_template_string(html_template)

# Rota do gráfico1
@app.route('/grafico1')
def grafico1():
    conn = sqlite3.connect('consumo_alcool.db')
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

# Rota 2 - Média do consumo por tipo de bebida
@app.route('/grafico2')
def grafico2():
    conn = sqlite3.connect('consumo_alcool.db')
    df = pd.read_sql_query('''
    SELECT AVG(beer_servings) AS cerveja, 
            AVG(spirit_servings) AS destilados, 
            AVG(wine_servings) AS vinho 
    FROM drinks''', conn)
    conn.close()
    df_melted = df.melt(var_name='Bebidas', value_name='Média de porções')
    fig = px.bar(df_melted, x='Bebidas', y='Média de porções', title='Média de consumo global por tipo de bebida')
    return fig.to_html()

# Rota 3 - Consumo total por região
@app.route('/grafico3')
def grafico3():
    #define grupos de países por região (simulando)
    regioes = {
        'Europa': ['France','Germany','Italy','Spain','Portugal', 'UK'],
        'Asia': ['China', 'Japan', 'India', 'Thailand'],
        'Africa': ['Angola', 'Nigeria', 'Egypt', 'Algeria'],
        'Americas': ['USA', 'Brazil', 'Canada', 'Argentina', 'Mexico']
    }
    dados=[]

    conn = sqlite3.connect('consumo_alcool.db')
    for regiao, paises in regioes.items():
        placeholders = ','.join([f"'{p}'" for p in paises])
        query = f'''
                SELECT SUM(total_litres_of_pure_alcohol) AS total
                FROM drinks
                WHERE country IN ({placeholders})
                '''
        total = pd.read_sql_query(query, conn)[0] or 0
        dados.append({'Região': regiao, 'Consumo total': total})
    conn.close()

    df_regioes = pd.DataFrame(dados)
    fig = px.pie(df_regioes, names='Região', values='Consumo total', title='Consumo total por região')
    return fig.to_html() + "<br><a href='/'></a>"

# Rota 4 - Comparativo entre os tipos de bebida
@app.route('/grafico4')
def grafico4():
    conn = sqlite3.connect('consumo_alcool.db')
    df = pd.read_sql_query('SELECT beer_servings, spirit_servings, wine_servings FROM drinks', conn)
    conn.close()

    medias = df.mean().reset_index()
    medias.columns = ['Tipo', 'Média']

    fig = px.pie(medias, names='Tipo', values='Média', title='Comparativo entre os tipos de bebida')
    return fig.to_html() + "<br><a href='/'></a>"

# Parte 2 - Rota comparar
@app.route('/comparar', methods=['GET','POST'])
def comparar():
    opcoes = ['beer_servings','spirit_servings','wine_servings','total_litres_of_pure_alcohol']
    if request.method == 'POST':
        eixo_x = request.form.get('eixo_x')
        eixo_y = request.form.get('eixo_y')
        
        if eixo_x == eixo_y:
            return "<h3> O valor do eixo x não pode ser igual ao valor do eixo y! </h3>"
        
        conn = sqlite3.connect('consumo_alcool.db')
        df = pd.read_sql_query('''
                            SELECT country, {}, {}
                            FROM drinks
                            '''.format(eixo_x,eixo_y), conn)
        conn.close()

        fig = px.scatter(df, x=eixo_x, y=eixo_y, title='Comparação entre {} e {}'.format(eixo_x, eixo_y))
        fig.update_traces(textposition="top center")
        return fig.to_html() + "<br/><a href='/'> Voltar ao início </a>"
    return render_template_string('''
        <h2> Comparar campos </h2>
        <form method='POST'>
            <label for="eixo_x"> Eixo X: </label>
            <select name = 'eixo_x'>
                {% for col in opcoes %}
                    <option value="{{ col }}"> {{ col }} </option>
                {% endfor %}
            </select><br><br>
                                  
            <label for="eixo_y"> Eixo Y: </label>
            <select name = 'eixo_y'>
                {% for col in opcoes %}
                    <option value="{{ col }}"> {{ col }} </option>
                {% endfor %}
            </select><br><br>
            <input type="submit" value="Comparar">
        </form>
    ''', opcoes=opcoes)

# Parte 2 - Rota Upload avengers
@app.route('/upload_avengers', methods = ['GET', 'POST'])
def upload_avengers():
    if request.method=='POST':
        file = request.files['file']
        if not file:
            return "<h2>Nenhum arquivo enviado!</h2>" + "<br><a href='/upload_avengers'></a>"
        df_avengers = pd.read_csv(file, encoding='latin1')
        conn = sqlite3.connect('consumo_alcool.db')
        df_avengers.to_sql('avengers', conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()
        return "<h2> Arquivo inserido com sucesso! </h2><a href='/'> Voltar </a>"
    return '''
    <h2> Upload do arquivo Avengers </h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv">
        <input type="submit" value="Enviar">
    </form>
'''

# Iniciar o servidor flask
if __name__ == '__main__':
    app.run(debug=True)