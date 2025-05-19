from flask import Flask, jsonify
import requests

app = Flask(__name__)

def buscar_produtos_filtrados():
    url = "https://api.minhaxbz.com.br:5001/api/clientes/GetListaDeProdutos"
    params = {
        "cnpj": "48783884000124",
        "token": "X410CDFEAA"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        produtos = response.json()

        filtrados = []
        for produto in produtos:
            item = {
                "codigo_composto": produto.get("codigoComposto") or produto.get("codigo"),
                "nome": produto.get("nome") or produto.get("descricao"),
                "descricao": produto.get("descricao"),
                "site_link": produto.get("url") or produto.get("linkSite"),
                "image_link": produto.get("imagem") or produto.get("urlImagem"),
                "preco_venda_formatado": produto.get("precoVendaFormatado") or (
                    f"R$ {produto.get('precoVenda'):.2f}" if produto.get("precoVenda") else None
                ),
                "quantidade_disponivel": produto.get("quantidadeDisponivel") or produto.get("estoque"),
                "ncm": produto.get("ncm")
            }
            filtrados.append(item)

        return filtrados

    except requests.RequestException as e:
        return {"erro": str(e)}

@app.route("/produtos", methods=["GET"])
def produtos():
    return jsonify(buscar_produtos_filtrados())

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
