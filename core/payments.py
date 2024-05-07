import mercadopago
    

def gerar_link_pagamento(items):
    sdk = mercadopago.SDK("TEST-3850728559392708-050420-02d7aa28217bd33bd4c9726b98c3e0d5-263804782")
    items_list = []

    # Loop através dos itens da descrição e adiciona-os à lista de itens
    for idx, item in enumerate(items, start=1):
        items_list.append({
            "id": str(item['id']),  # Assume que o ID começa de 1 e é incrementado para cada item
            "title": item['nome'],  # Obtém o título do item da descrição
            "quantity": 1,  # Aqui você pode definir a quantidade desejada para cada item, se necessário
            "currency_id": "BRL",  # Define a moeda como BRL
            "unit_price": float(item['preco'])  # Obtém o preço unitário do item da descrição e converte para float
        })

    payment_data = {
        "items": items_list,
        "back_urls": {
            "success": "127.0.0.1:8000/Aproved",
            "failure": "https://127.0.0.1:8000/",
            "pending": "https://127.0.0.1:8000/",
        },
        "auto_return": "all"
    }
    result = sdk.preference().create(payment_data)
    payment = result["response"]
    link_iniciar_pagamento = payment["init_point"]
    return link_iniciar_pagamento

