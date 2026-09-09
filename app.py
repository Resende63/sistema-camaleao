from flask import Flask, request, jsonify, render_template
from werkzeug.security import generate_password_hash
import os
import psycopg2 
from psycopg2.extras import RealDictCursor
import re

app = Flask(__name__)

# Configuração da URL do Banco de Dados obtida com segurança do Render
DATABASE_URL = os.environ.get('DATABASE_URL')

def obtener_conexao_banco():
    """Cria uma conexão segura com o banco de dados PostgreSQL na nuvem."""
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def inicializar_banco_de_dados():
    """Cria a tabela de orçamentos se ela não existir no sistema."""
    conn = obtener_conexao_banco()
    cursor = conn.cursor()
    
    # TABELA CORPORATIVA DE ORÇAMENTOS E MEDIDAS (FEITA PARA DURAR ANOS)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orcamentos_premium (
            id SERIAL PRIMARY KEY,
            cliente_nome VARCHAR(255) NOT NULL,
            cliente_contato VARCHAR(50) NOT NULL,
            obra_endereco TEXT NOT NULL,
            data_emissao DATE NOT NULL,
            status_lembrete VARCHAR(50) DEFAULT 'pendente',
            obra_descricao TEXT,
            largura NUMERIC(10, 2) DEFAULT 0,
            comprimento NUMERIC(10, 2) DEFAULT 0,
            valor_faturamento NUMERIC(10, 2) NOT NULL,
            valor_custo NUMERIC(10, 2) NOT NULL,
            lucro_limpo NUMERIC(10, 2) NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    print("🚀 Banco de dados PostgreSQL validado com precisão cirúrgica!")

# Inicializa o banco assim que o Camaleão acorda no Render
if DATABASE_URL:
    try:
        inicializar_banco_de_dados()
    except Exception as e:
        print(f"⚠️ Alerta ao iniciar o banco (Sem problemas se ainda não configuramos a URL): {e}")

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


# =========================================================================
# AS SUAS ROTAS DO SISTEMA (A interligação das telas que já funcionam)
# =========================================================================

# 1. ROTA DA PÁGINA INICIAL (PAINEL PRINCIPAL)
@app.route('/sistema', methods=['GET'])
def painel_principal():
    return render_template('index.html')

# 2. ROTA PARA EXIBIR A TELA DE LOGIN/CADASTRO DE USUÁRIO
@app.route('/sistema/cadastro', methods=['GET'])
def tela_cadastro():
    return render_template('cadastro.html')

# 3. ROTA PARA EXIBIR O FORMULÁRIO PREMIUM DE OBRAS
@app.route('/sistema/registrar-obra', methods=['GET'])
def tela_cadastro_obra():
    return render_template('cadastro_obra.html')

# 4. ROTA PARA EXIBIR A FICHA DE PRODUÇÃO DO OPERÁRIO
@app.route('/sistema/ordem-servico', methods=['GET'])
def tela_ordem_servico():
    return render_template('ordem_servico.html')

# 5. ROTA DO CALCULADOR DE ORÇAMENTOS
@app.route('/sistema/sistema', methods=['GET'])
def tela_calculador():
    return render_template('sistema.html')


# =========================================================================
# ROTAS DE SINAL VERDE (PROCESSAMENTO DOS DADOS)
# =========================================================================

# CADASTRO DE USUÁRIO (LOGIN SEGURO)
@app.route('/sistema/cadastro', methods=['POST'])
def cadastrar_usuario():
    username = request.form.get('username')
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    if not username or not email or not senha:
        return "Todos os campos são obrigatórios.", 400
    if not re.match(EMAIL_REGEX, email):
        return "Formato de e-mail inválido.", 400
    if len(senha) < 8:
        return "A senha deve ter no mínimo 8 caracteres.", 400

    senha_criptografada = generate_password_hash(senha, method='pbkdf2:sha256', salt_length=16)
    print(f"Usuário simulado no terminal: {username} | Senha: {senha_criptografada}")
    return "<h1>Cadastro de usuário realizado com segurança!</h1>"

# REGISTRO DE OBRA E ORÇAMENTOS
@app.route('/sistema/registrar-obra', methods=['POST'])
def registrar_obra():
    cliente_nome = request.form.get('cliente_nome', '').strip()
    cliente_documento = request.form.get('cliente_documento', '').strip()
    cliente_contato = request.form.get('cliente_contato', '').strip()
    obra_endereco = request.form.get('obra_endereco', '').strip()
    data_orcamento = request.form.get('data_orcamento', '').strip()
    status_lembrete = request.form.get('status_lembrete', '').strip()
    obra_descricao = request.form.get('obra_descricao', '').strip()
    
    try:
        valor_faturamento = float(request.form.get('valor_faturamento', 0))
        valor_custo = float(request.form.get('valor_custo', 0))
        lucro_limpo = valor_faturamento - valor_custo
    except ValueError:
        return "Erro: Os valores financeiros inseridos são inválidos.", 400

    if not cliente_nome or not cliente_contato or not obra_endereco or not data_orcamento:
        return "Erro de Segurança: Campos obrigatórios faltando.", 400

    print(f"Obra simulada no terminal: {cliente_nome} | Lucro: R$ {lucro_limpo:.2f}")
    return "<h1>Obra registrada com sucesso no sistema!</h1>"


if __name__ == '__main__':
    # Configuração padrão para rodar na nuvem do Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
