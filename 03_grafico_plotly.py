from flask import Flask, render_template_string
import plotly.express as px
import pandas as pd

# Iniciar aplicação
app = Flask(__name__)

# Criar nosso dataframe
df_consolidado = pd.DataFrame({
    'Status':['Ativo','Inativo','Ativo','Inativo','Ativo','Inativo','Cancelado','Cancelado','Ativo']
})

# Rota do gráfico de pizza usando o plotly
@app.route('/')
def grafico_pizza():
    # Contagem de valor
    status_dist = df_consolidado['Status'].value_counts().reset_index()
    status_dist.columns = ['Status', 'Quantidade']

    # Criar o gráfico do plotly
    fig = px.pie(
                status_dist,
                values='Quantidade',
                names='Status',
                title='Distribuição do status'
                )
    # Converter para html
    grafico_html = fig.to_html(full_html = False)

    # HTML simples com o gráfico embutido
    html = f'''
        <html>
            <head>
                <meta charset="UTF-8">
                <title>
                Feito com ♥ por Vítor
                </title>
            </head>
            <body>
                <h2> Grafico com Plotly</h2>
                {grafico_html}
            </body>
        </html>
    '''

    # Renderiza a string de html usando o render_template. Sem isso, o html não é manipulado corretamente
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)