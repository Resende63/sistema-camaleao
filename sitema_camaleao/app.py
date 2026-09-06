from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 1. ROTA DA PÁGINA INICIAL DE VENDAS
@app.route("/")
def home():
    return render_template("index.html")

# 2. ROTA DA CALCULADORA DO SISTEMA
@app.route("/sistema")
def abrir_sistema():
    return render_template("sistema.html")

# 3. ROTA QUE FAZ OS CÁLCULOS INTELIGENTES
@app.route("/calcular", methods=["POST"])
def calcular():
    dados = request.json
    
    # Cálculo por Área (m²)
    largura = float(dados.get("largura", 0) or 0)
    comprimento = float(dados.get("comprimento", 0) or 0)
    preco_m2 = float(dados.get("preco_m2", 0) or 0)
    custo_m2 = float(dados.get("custo_m2", 0) or 0)
    
    area = largura * comprimento
    faturamento_area = area * preco_m2
    custo_area = area * custo_m2
    
    # Cálculo por Itens (Tomadas, Bocais, etc.)
    itens = dados.get("itens", [])
    faturamento_itens = 0
    custo_itens = 0
    
    for item in itens:
        qtd = float(item.get("quantidade", 0) or 0)
        venda_uni = float(item.get("venda", 0) or 0)
        custo_uni = float(item.get("custo", 0) or 0)
        
        faturamento_itens += (qtd * venda_uni)
        custo_itens += (qtd * custo_uni)
        
    # Totais Consolidados
    total_cliente = faturamento_area + faturamento_itens
    custo_total = custo_area + custo_itens
    lucro_liquido = total_cliente - custo_total
    
    return jsonify({
        "area": round(area, 2),
        "total_cliente": round(total_cliente, 2),
        "custo_total": round(custo_total, 2),
        "lucro_liquido": round(lucro_liquido, 2)
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)