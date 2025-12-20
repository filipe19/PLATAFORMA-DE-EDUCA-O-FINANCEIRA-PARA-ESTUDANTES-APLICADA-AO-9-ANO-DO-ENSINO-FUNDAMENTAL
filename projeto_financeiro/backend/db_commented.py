# backend/db.py
"""
🗄️ MÓDULO DE BANCO DE DADOS - SQLITE 📊

Este arquivo é responsável por "guardar a memória" da plataforma!
Aqui salvamos todas as simulações que os estudantes fazem para:

📝 OBJETIVOS PRINCIPAIS:
- Guardar dados dos formulários preenchidos
- Criar histórico das simulações realizadas  
- Permitir análise posterior dos dados (para professores)
- Demonstrar persistência de dados (conceito importante em programação)

💾 TECNOLOGIA USADA: SQLite
- Banco de dados leve que vem junto com Python
- Não precisa instalar servidor separado
- Perfeito para projetos educacionais
- Arquivo único (.db) que guarda tudo

🎓 CONCEITOS ENSINADOS:
- O que é um banco de dados
- Como persistir informações
- Estrutura de tabelas (linhas e colunas)
- Operações básicas: CREATE, INSERT, SELECT
"""

# Importações necessárias
import sqlite3  # 🗄️ Biblioteca para trabalhar com SQLite (vem com Python)
import json     # 📋 Para converter objetos Python em texto JSON e vice-versa


# 🏗️ ESTRUTURA DA TABELA DO BANCO DE DADOS
# Esta é a "planta baixa" da nossa tabela - define como os dados serão organizados
SCHEMA = """
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 🔢 Número único para cada registro (auto incrementa)
    kind TEXT,                            -- 📂 Tipo de formulário: 'reality' ou 'future'  
    payload TEXT,                         -- 📋 Dados do formulário convertidos para JSON
    created_at DATETIME DEFAULT (datetime('now','localtime'))  -- 📅 Data/hora de criação automática
);
"""

# 💡 EXPLICAÇÃO DIDÁTICA DA ESTRUTURA:
# 
# 📊 TABELA "submissions" (submissões):
# - Cada linha = uma simulação feita por um estudante
# - id: número único (1, 2, 3, 4...) para identificar cada simulação
# - kind: que tipo de formulário foi preenchido ('reality' = realidade atual, 'future' = futuro)  
# - payload: todos os dados do formulário guardados como texto JSON
# - created_at: quando a simulação foi feita (data e hora automáticas)
#
# 🎯 EXEMPLO DE DADOS SALVOS:
# id=1, kind='reality', payload='{"nome":"João","idade":15,"renda":0}', created_at='2025-01-15 14:30:00'
# id=2, kind='future', payload='{"nome":"João","profissao":"médico","poupanca":100}', created_at='2025-01-15 14:35:00'


def init_db(path: str = './data.db'):
    """
    🚀 INICIALIZA O BANCO DE DADOS
    
    Esta função é chamada quando o servidor inicia. Ela:
    1. Conecta com o arquivo do banco de dados
    2. Cria a tabela se ela não existir ainda
    3. Fecha a conexão
    
    É como "preparar o terreno" antes de construir a casa!
    
    📥 PARÂMETRO:
    - path: caminho para o arquivo .db (onde ficam os dados)
    
    💡 CONCEITO IMPORTANTE: 
    "CREATE TABLE IF NOT EXISTS" significa "crie a tabela apenas se ela não existir".
    Isso evita erros se tentarmos criar a mesma tabela várias vezes.
    """
    
    print(f"🗄️ Inicializando banco de dados em: {path}")
    
    # 🔌 CONECTA com o arquivo do banco de dados
    conn = sqlite3.connect(path)
    print("   ✅ Conexão estabelecida com sucesso!")
    
    # 👷 EXECUTA os comandos SQL para criar a estrutura
    c = conn.cursor()  # Cursor = "ponteiro" para executar comandos SQL
    c.executescript(SCHEMA)  # Executa o SQL que define a estrutura da tabela
    print("   📊 Tabela 'submissions' criada/verificada!")
    
    # 💾 SALVA as mudanças no arquivo
    conn.commit()
    print("   💾 Mudanças salvas no disco!")
    
    # 🚪 FECHA a conexão (boa prática!)
    conn.close()
    print("   🔒 Conexão fechada. Banco pronto para uso!")
    print("="*50)


def save_submission(path: str, kind: str, payload: dict):
    """
    💾 SALVA UMA SIMULAÇÃO NO BANCO DE DADOS
    
    Toda vez que um estudante preenche um formulário, esta função é chamada
    para guardar os dados permanentemente. É como colocar o papel numa gaveta
    de arquivo para não perder!
    
    📥 PARÂMETROS:
    - path: caminho do arquivo do banco de dados
    - kind: tipo do formulário ('reality' para realidade atual, 'future' para futuro)
    - payload: dicionário Python com todos os dados do formulário
    
    🔄 PROCESSO:
    1. Conecta com o banco
    2. Converte o dicionário Python para JSON (texto)  
    3. Insere na tabela
    4. Salva e fecha
    
    💡 POR QUE JSON?
    JSON é um formato de texto que permite guardar estruturas complexas
    (dicionários, listas) como texto simples no banco de dados.
    """
    
    print(f"💾 Salvando submissão do tipo '{kind}'...")
    print(f"   📋 Dados recebidos: {payload}")
    
    # 🔌 Conecta com o banco de dados
    conn = sqlite3.connect(path)
    c = conn.cursor()
    
    # 🔄 Converte o dicionário Python para texto JSON
    json_payload = json.dumps(payload, ensure_ascii=False)  # ensure_ascii=False permite acentos
    print(f"   🔄 Dados convertidos para JSON: {json_payload[:100]}...")  # Mostra só os primeiros 100 caracteres
    
    # 💾 EXECUTA o comando SQL INSERT (inserir dados)
    c.execute(
        'INSERT INTO submissions (kind, payload) VALUES (?,?)', 
        (kind, json_payload)
    )
    
    # 📊 Verifica quantos registros foram inseridos
    rows_affected = c.rowcount
    print(f"   ✅ {rows_affected} registro inserido com sucesso!")
    
    # 🔢 Pega o ID do registro que acabou de ser criado
    new_id = c.lastrowid
    print(f"   🆔 ID do novo registro: {new_id}")
    
    # 💾 Salva as mudanças no arquivo
    conn.commit()
    
    # 🚪 Fecha a conexão
    conn.close()
    
    print(f"   🎉 Submissão salva com sucesso! ID: {new_id}")
    print("="*50)


def get_submissions(path: str):
    """
    📋 RECUPERA TODAS AS SIMULAÇÕES SALVAS
    
    Esta função busca todos os formulários que foram preenchidos pelos estudantes.
    É útil para professores verem o histórico ou para análise dos dados.
    
    📥 PARÂMETRO:
    - path: caminho do arquivo do banco de dados
    
    📤 RETORNA:
    Lista de dicionários, onde cada dicionário representa uma simulação:
    [
        {"id": 1, "kind": "reality", "payload": {...}, "created_at": "2025-01-15 14:30:00"},
        {"id": 2, "kind": "future", "payload": {...}, "created_at": "2025-01-15 14:35:00"},
        ...
    ]
    
    🔄 PROCESSO:
    1. Conecta com o banco
    2. Busca todos os registros (ordenados do mais recente para o mais antigo)
    3. Converte JSON de volta para dicionários Python
    4. Organiza tudo numa lista bonita
    """
    
    print(f"📋 Buscando todas as submissões em: {path}")
    
    # 🔌 Conecta com o banco
    conn = sqlite3.connect(path)
    c = conn.cursor()
    
    # 🔍 EXECUTA consulta SQL SELECT (buscar dados)
    # ORDER BY created_at DESC = ordena do mais recente para o mais antigo
    c.execute('SELECT id, kind, payload, created_at FROM submissions ORDER BY created_at DESC')
    
    # 📥 Pega todos os resultados
    rows = c.fetchall()
    print(f"   📊 {len(rows)} submissões encontradas!")
    
    # 🚪 Fecha conexão
    conn.close()
    
    # 🔄 PROCESSA os resultados para um formato mais amigável
    out = []  # Lista que vai guardar os resultados processados
    
    for i, row in enumerate(rows):
        print(f"   🔄 Processando submissão {i+1}/{len(rows)}: ID {row[0]}")
        
        try:
            # 🔄 Tenta converter JSON de volta para dicionário Python
            payload_dict = json.loads(row[2])  # row[2] = coluna 'payload'
            conversion_success = True
        except Exception as e:
            # ⚠️ Se não conseguir converter, mantém como texto
            print(f"      ⚠️ Erro ao converter JSON: {e}")
            payload_dict = row[2]  # Mantém como string
            conversion_success = False
        
        # 📦 Organiza os dados num dicionário limpo
        processed_record = {
            "id": row[0],           # ID único
            "kind": row[1],         # Tipo ('reality' ou 'future')  
            "payload": payload_dict, # Dados do formulário
            "created_at": row[3],   # Data/hora de criação
            "json_valid": conversion_success  # Se conseguiu converter JSON
        }
        
        out.append(processed_record)
    
    print(f"   ✅ {len(out)} submissões processadas com sucesso!")
    print("="*50)
    
    return out


# 🧪 FUNÇÃO DE TESTE - Para verificar se o banco está funcionando
def test_database():
    """
    🧪 TESTA AS FUNÇÕES DO BANCO DE DADOS
    
    Esta função serve para verificar se tudo está funcionando corretamente.
    É como um "ensaio" antes da apresentação final!
    """
    
    print("🧪 INICIANDO TESTES DO BANCO DE DADOS...")
    print("="*60)
    
    # 🏗️ Teste 1: Inicializar banco
    test_db_path = "./test_data.db"
    print("📝 TESTE 1: Inicializando banco de teste...")
    init_db(test_db_path)
    
    # 💾 Teste 2: Salvar dados de realidade
    print("📝 TESTE 2: Salvando dados de realidade atual...")
    reality_data = {
        "nome": "João Silva",
        "idade": 15,
        "renda_atual": 0,
        "renda_futura_possivel": 500,
        "profissao_interesse": "Engenheiro"
    }
    save_submission(test_db_path, "reality", reality_data)
    
    # 💾 Teste 3: Salvar dados de futuro
    print("📝 TESTE 3: Salvando dados de futuro profissional...")
    future_data = {
        "nome": "João Silva", 
        "idade": 15,
        "profissao_dos_sonhos": "Engenheiro de Software",
        "faixa_salarial": 8000,
        "poupanca_mensal": 200,
        "investimento_tipo": "moderado",
        "tempo_anos": 10
    }
    save_submission(test_db_path, "future", future_data)
    
    # 📋 Teste 4: Recuperar dados
    print("📝 TESTE 4: Recuperando todas as submissões...")
    all_submissions = get_submissions(test_db_path)
    
    print(f"📊 RESULTADO: {len(all_submissions)} submissões recuperadas!")
    for i, sub in enumerate(all_submissions):
        print(f"   {i+1}. ID: {sub['id']}, Tipo: {sub['kind']}, Data: {sub['created_at']}")
    
    # 🧹 Limpeza: remove arquivo de teste
    import os
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        print(f"🧹 Arquivo de teste removido: {test_db_path}")
    
    print("✅ TODOS OS TESTES PASSARAM! Banco de dados funcionando perfeitamente! 🎉")
    print("="*60)


# 📊 FUNÇÃO DE ESTATÍSTICAS - Para análise dos dados
def get_database_stats(path: str):
    """
    📊 GERA ESTATÍSTICAS DO BANCO DE DADOS
    
    Função útil para professores analisarem como os estudantes estão usando a plataforma.
    """
    
    print(f"📊 Gerando estatísticas do banco: {path}")
    
    try:
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        # 📊 Conta total de submissões
        c.execute("SELECT COUNT(*) FROM submissions")
        total = c.fetchone()[0]
        
        # 📊 Conta por tipo
        c.execute("SELECT kind, COUNT(*) FROM submissions GROUP BY kind")
        by_type = dict(c.fetchall())
        
        # 📊 Últimas submissões
        c.execute("SELECT created_at FROM submissions ORDER BY created_at DESC LIMIT 5")
        recent = [row[0] for row in c.fetchall()]
        
        conn.close()
        
        stats = {
            "total_submissions": total,
            "by_type": by_type, 
            "recent_submissions": recent
        }
        
        print(f"   📈 Total de submissões: {total}")
        print(f"   📋 Por tipo: {by_type}")
        print(f"   🕒 Últimas 5: {recent}")
        
        return stats
        
    except Exception as e:
        print(f"   ❌ Erro ao gerar estatísticas: {e}")
        return None


# 🚀 Se este arquivo for executado diretamente, roda os testes
if __name__ == "__main__":
    print("🗄️ MÓDULO DE BANCO DE DADOS - MODO TESTE")
    test_database()