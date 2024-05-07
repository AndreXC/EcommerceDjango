
from django.template import loader  # Importa o loader de templates
# def _email_Body(infoPedidos):
#     html_content = """
#         <html>
#         <head>
#             <style>
#                 table {
#                     border-collapse: collapse;
#                     width: 100%;
#                 }
#                 th, td {
#                     border: 1px solid #dddddd;
#                     text-align: left;
#                     padding: 8px;
#                 }
#                 th {
#                     background-color: #f2f2f2;
#                 }
#                 img {
#                     max-width: 100px;
#                     max-height: 100px;
#                 }
#             </style>
#         </head>
#         <body>
#             <h2>Pedidos do E-commerce</h2>
#             <table>
#                 <tr>
#                     <th>Produto</th>
#                     <th>Preço</th>
                   
#                 </tr>
#         """

#     for pedido in infoPedidos:
#         html_content += f"""
#             <tr>
#                 <td><img src="{% static 'img/lanche1.png' %}"></td>
#                 <td>{pedido['nome']}</td>
#                 <td>{pedido['preco']}</td>
#             </tr>
#         """

#     html_content += """
#         </table>
#     </body>
#     </html>
#     """

#     return html_content


def _email_Body(infoPedidos, preco_total, user, id):
    """
    Gera o corpo do email com os detalhes dos pedidos

    Args:
        infoPedidos (list): Lista de dicionários contendo detalhes dos pedidos

    Returns:
        str: Corpo do email em HTML
    """

    table_pedidos = """
    """
    for pedido in infoPedidos:
     table_pedidos+= f"""
        <tr>
          <td><img src="https://www.designi.com.br/images/preview/11052408.jpg" alt="Imagem do produto"></td>
          <td> { pedido['nome'] }</td>
          <td>R$ {float(pedido['preco']) }</td>
          <td class="quantidade">1</td>  
        </tr>
    """    
     






    context = {'table_pedidos': table_pedidos, 'total_geral': preco_total, 'user': user, 'id': id}  # Cria contexto com a lista de pedidos

    # Carrega o template de email
    template = loader.get_template('email_pedidos.html')  # Substitua 'email_pedidos.html' pelo seu nome de template

    # Renderiza o template com o contexto
    html_content = template.render(context)

    return html_content


def htmlFatec(infoPedidos, infouser, preçoTotal):
    # Conteúdo HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Resumo do seu Pedido</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
<style>
/* Reset CSS */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}
/* Global Styles */
body {{
    font-family: 'Raleway', sans-serif;
    background-color: #f9f9f9;
    margin: 0;
    padding: 20px;
    color: #333;
}}
/* Main Title */
h2 {{
    text-align: center;
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 30px;
    color: #555;
}}
/* Table Container */
.table-container {{
    width: 90%;
    margin: 0 auto;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}}
/* Table Styles */
table {{
    width: 100%;
    border-collapse: collapse;
}}
th, td {{
    padding: 15px;
    text-align: left;
    border-bottom: 1px solid #eee;
}}
th {{
    background-color: #f2f2f2;
    color: #555;
    text-transform: uppercase;
    font-weight: bold;
}}
/* Row Stripes */
tbody tr:nth-child(even) {{
    background-color: #f6f6f6;
}}
/* Cell Text Alignment */
.quantidade, .total-pedido, .total-geral {{
    text-align: center;
}}
.total-geral {{
    font-weight: bold;
    color: #3498db;
}}
/* Total Section Styles */
.total-section {{
    display: flex;
    justify-content: space-between;
    padding: 15px;
    border-top: 2px solid #ddd;
}}
.total-section span {{
    font-weight: bold;
}}
/* Image Styles */
img {{
    width: 60px;
    height: 60px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}}
/* User Message */
.user-message {{
    text-align: center;
    font-size: 18px;
    margin-bottom: 20px;
    line-height: 1.6;
}}
.user-message p {{
    margin-bottom: 10px;
}}
.user-message p:last-child {{
    margin-bottom: 0;
}}

/* Responsividade */
@media only screen and (max-width: 768px) {{
    .table-container {{
        width: 100%;
        border-radius: 0;
    }}
    img {{
        width: 50px;
        height: 50px;
    }}
}}
</style>

    </head>
    <body>
    <div class="user-message">
        <p>Kr Lanches!</p>
        <p>Olá, é um grande prazer tê-lo(a) aqui, {infouser['nome']}!</p>
        <p>Seu pedido número <strong>{infouser['id']}</strong> foi efetivado. Aqui está o resumo:</p>
        <p>Agradecemos por comprar conosco!</p>
    </div>
    <h2>Resumo do seu Pedido</h2>
    <div class="table-container">
        <table>
        <thead>
            <tr>
            <th></th>
            <th>Produto</th>
            <th>Preço Unitário</th>
            <th class="quantidade">Quantidade</th>
            </tr>
        </thead>
        <tbody>
            <!-- Loop through pedidos -->
    """
    # Adicionando o loop para cada item do pedido
    for pedido in infoPedidos:
        html_content += f"""
            <tr>
            <td><img src="https://www.designi.com.br/images/preview/11052408.jpg" alt="Imagem do produto"></td>
            <td>{pedido['nome']}</td>
            <td>R$ {pedido['preco']}</td>
            <td class="quantidade">1</td>  
            </tr>
        """
    # Continuação do HTML
    html_content += f"""
        </tbody>
        <tfoot>
            <tr class="total-section">
            <td colspan="3"><span>Total:</span></td>
            <td class="total-geral">R$ {preçoTotal}</td>
            </tr>
        </tfoot>
        </table>
    </div>
    </body>
    </html>
    """
    return html_content