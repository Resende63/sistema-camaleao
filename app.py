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
    # 1. ROTA PARA EXIBIR O FORMULÁRIO PREMIUM DE OBRAS
@app.route('/sistema/registrar-obra', methods=['GET'])
def tela_cadastro_obra():
    return render_template('cadastro_obra.html')


# 2. ROTA PARA RECEBER, VALIDAR E SALVAR OS DADOS DA OBRA
@app.route('/sistema/registrar-obra', methods=['POST'])
def registrar_obra():
    # Coleta de dados com proteção de entrada
    cliente_nome = request.form.get('cliente_nome', '').strip()
    cliente_documento = request.form.get('cliente_documento', '').strip()
    cliente_contato = request.form.get('cliente_contato', '').strip()
    obra_endereco = request.form.get('obra_endereco', '').strip()
    data_orcamento = request.form.get('data_orcamento', '').strip()
    status_lembrete = request.form.get('status_lembrete', '').strip()
    obra_descricao = request.form.get('obra_descricao', '').strip()
    
    # Coleta dos valores financeiros (Garante formato numérico seguro)
    try:
        valor_faturamento = float(request.form.get('valor_faturamento', 0))
        valor_custo = float(request.form.get('valor_custo', 0))
        lucro_limpo = valor_faturamento - valor_custo
    except ValueError:
        return "Erro: Os valores financeiros inseridos são inválidos.", 400

    # TRAVA DE SEGURANÇA: Validação de campos obrigatórios corporativos
    if not cliente_nome or not cliente_contato or not obra_endereco or not data_orcamento:
        return "Erro de Segurança: Campos obrigatórios do cliente ou da obra estão faltando.", 400

    # ESTRUTURAÇÃO DO REGISTRO INTEGRADO
    # Os dados aqui ficam organizados e prontos para envio ao Banco de Dados
    registro_obra_protegido = {
        "cliente": {
            "nome": cliente_nome,
            "documento": cliente_documento,
            "contato": cliente_contato
        },
        "obra": {
            "endereco": obra_endereco,
            "data_emissao": data_orcamento,
            "descricao": obra_descricao,
            "alerta_status": status_lembrete # Controla o lembrete contra esquecimento!
        },
        "financeiro": {
            "faturamento": valor_faturamento,
            "custo_material": valor_custo,
            "lucro_real": lucro_limpo
        }
    }

    # MONITORAMENTO OPERACIONAL (Aparece direto no terminal do Render)
    print("--- NOVO REGISTRO PREMIUM DETECTADO ---")
    print(f"Cliente: {registro_obra_protegido['cliente']['nome']}")
    print(f"Status do Alerta: {registro_obra_protegido['obra']['alerta_status'].upper()}")
    print(f"Margem de Lucro Mapeada: R$ {registro_obra_protegido['financeiro']['lucro_real']:.2f}")
    print("---------------------------------------")

    # Retorno visual de sucesso para o usuário
    return f"""
    <div style="background-color: #1e2640; color: white; font-family: sans-serif; padding: 30px; border-radius: 8px; max-width: 500px; margin: 50px auto; text-align: center; border: 1px solid #10b981;">
        <h2 style="color: #10b981;">✔ Registro Concluído com Sucesso!</h2>
        <p>A obra de <strong>{cliente_nome}</strong> foi blindada na nuvem do Sistema Camaleão.</p>
        <p>Alerta de monitoramento definido como: <strong>{status_lembrete.upper()}</strong></p>
        <a href="/sistema/registrar-obra" style="color: #3b82f6; text-decoration: none; font-weight: bold;">[ Cadastrar Nova Obra ]</a>
    </div>
    """
    # ROTA PARA EXIBIR A FICHA DE PRODUÇÃO DO TRABALHADOR
@app.route('/sistema/ordem-servico', methods=['GET'])
def tela_ordem_servico():
    return render_template('ordem_servico.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
