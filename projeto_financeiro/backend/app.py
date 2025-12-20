# backend/app.py
"""
API principal da Plataforma de Educação Financeira
Este arquivo contém todas as rotas e endpoints da API que alimenta o frontend
"""

# Importações necessárias para criar a API
from fastapi import FastAPI, HTTPException  # FastAPI para criar a API REST
from fastapi.middleware.cors import CORSMiddleware  # Para permitir requisições do frontend
from fastapi.staticfiles import StaticFiles  # Para servir arquivos estáticos
from pydantic import BaseModel, Field  # Para validação de dados de entrada
from typing import Optional, List  # Para tipagem de dados
import sqlite3  # Banco de dados SQLite (incluído no Python)
import json  # Para manipular dados JSON

# Importações de módulos locais
from calc import project_investments, monte_carlo_projection  # Funções de cálculo financeiro
from db import init_db, save_submission, get_submissions  # Funções de banco de dados

# Configuração do banco de dados
import os  # Para manipular caminhos de arquivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Diretório atual do arquivo
DB_PATH = os.path.join(BASE_DIR, "data.db")  # Caminho completo para o banco de dados
if not os.path.exists(BASE_DIR):  # Se o diretório não existir
    os.makedirs(BASE_DIR)  # Cria o diretório
init_db(DB_PATH)  # Inicializa o banco de dados com as tabelas necessárias

# Criação da aplicação FastAPI
app = FastAPI(title="Plataforma de Matemática Financeira - API")

# Configuração do CORS (Cross-Origin Resource Sharing)
# Permite que o frontend (HTML/JS) faça requisições para a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos HTTP
)

# Modelo de dados para o formulário "Realidade Atual"
class RealityForm(BaseModel):
    """
    Estrutura de dados que o aluno preenche sobre sua situação atual
    """
    nome: str  # Nome do estudante
    idade: int = Field(..., ge=8, le=120)  # Idade (entre 8 e 120 anos)
    renda_atual: float = Field(..., ge=0)  # Renda atual em reais (maior ou igual a 0)
    renda_futura_possivel: Optional[float] = 0.0  # Possível renda futura (opcional)
    profissao_interesse: Optional[str] = ""  # Profissão de interesse (opcional)

# Modelo de dados para o formulário "Futuro Profissional"
class FutureForm(BaseModel):
    """
    Estrutura de dados para simulação do futuro financeiro do aluno
    """
    nome: str  # Nome do estudante
    idade: int = Field(..., ge=8, le=120)  # Idade atual
    profissao_dos_sonhos: str  # Profissão que deseja seguir
    faixa_salarial: float = Field(..., ge=0)  # Salário esperado por mês
    poupanca_mensal: float = Field(..., ge=0)  # Quanto consegue poupar por mês
    investimento_tipo: str = Field(..., pattern="^(conservador|moderado|arriscado)$")  # Tipo: conservador, moderado ou arriscado
    tempo_anos: int = Field(..., ge=1, le=100)  # Por quantos anos vai investir (1 a 100 anos)

# Modelo de dados para cálculo de metas financeiras
class GoalCalculation(BaseModel):
    """
    Estrutura para calcular quanto tempo leva para atingir uma meta
    """
    goal_amount: float = Field(..., ge=0)  # Valor da meta em reais
    monthly_saving: float = Field(..., ge=0)  # Quanto consegue poupar por mês
    annual_rate: float = Field(default=0.05, ge=0, le=1)  # Taxa de juros anual (padrão 5%)

# =============================================================================
# ENDPOINTS DA API (ROTAS QUE O FRONTEND PODE ACESSAR)
# =============================================================================

@app.post('/api/submit_reality')
def submit_reality(payload: RealityForm):
    """
    Endpoint para salvar os dados da realidade atual do estudante
    Recebe: dados do formulário "Sua Realidade Atual"
    Retorna: confirmação de que os dados foram salvos
    """
    save_submission(DB_PATH, 'reality', payload.dict())  # Salva no banco de dados
    return {"status": "ok", "message": "Realidade salva com sucesso"}

@app.post('/api/submit_future')
def submit_future(payload: FutureForm):
    """
    Endpoint principal para calcular projeções de investimento
    Recebe: dados do formulário "Futuro Profissional"  
    Retorna: projeções para os 3 tipos de investimento (conservador, moderado, arriscado)
    """
    # Define as taxas de retorno anuais para cada tipo de investimento
    rates = {"conservador": 0.05, "moderado": 0.08, "arriscado": 0.12}  # 5%, 8% e 12%
    results = {}  # Dicionário para armazenar os resultados
    for k, r in rates.items():
        proj = project_investments(monthly=payload.poupanca_mensal, years=payload.tempo_anos, annual_return=r)
        results[k] = proj
    
    save_submission(DB_PATH, 'future', payload.dict())
    return {"status": "ok", "projections": results}

@app.post('/api/simulate_montecarlo')
def simulate_mc(payload: FutureForm):
    """Simulação Monte Carlo para investimentos arriscados"""
    try:
        sims = monte_carlo_projection(
            monthly=payload.poupanca_mensal, 
            years=payload.tempo_anos, 
            mu=0.12, 
            sigma=0.25, 
            n_sims=1000
        )
        return {"status": "ok", "montecarlo": sims}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/submissions')
def list_submissions():
    """Lista todas as submissões salvas"""
    data = get_submissions(DB_PATH)
    return {"count": len(data), "data": data}

@app.get('/api/glossary')
def get_glossary():
    """Retorna glossário de termos financeiros para educação"""
    glossary = {
        "Juros Compostos": "Juros calculados sobre o valor inicial mais os juros já acumulados. É o 'juro sobre juro' que faz seu dinheiro crescer mais rápido!",
        "CDI": "Certificado de Depósito Interbancário - taxa de referência do mercado financeiro brasileiro.",
        "Poupança": "Investimento de baixo risco com rendimento menor, mas garantido pelo governo.",
        "Ações": "Participação em empresas. Maior potencial de retorno, mas também maior risco.",
        "Inflação": "Aumento geral dos preços que reduz o poder de compra do seu dinheiro ao longo do tempo.",
        "Diversificação": "Estratégia de espalhar investimentos para reduzir riscos - 'não colocar todos os ovos numa cesta'.",
        "Renda Fixa": "Investimentos com rentabilidade previsível, como CDB, Tesouro Direto.",
        "Renda Variável": "Investimentos com rentabilidade que varia conforme o mercado, como ações e fundos.",
        "Reserva de Emergência": "Dinheiro guardado para situações imprevistas, equivalente a 3-6 meses de gastos.",
        "Meta Financeira": "Objetivo específico que você quer alcançar, como comprar algo ou juntar uma quantia."
    }
    return glossary

@app.get('/api/tips')
def get_financial_tips():
    """Retorna dicas práticas de educação financeira"""
    tips = [
        "📊 Anote todos os seus gastos por uma semana para entender para onde vai seu dinheiro",
        "⏰ Antes de comprar algo, espere 24 horas e pergunte: 'Eu realmente preciso disso?'",
        "💰 Guarde pelo menos R$ 1 por dia - em um ano serão R$ 365!",
        "🔍 Compare preços antes de comprar - use aplicativos ou pesquise em várias lojas",
        "🎯 Defina uma meta de economia mensal, mesmo que pequena",
        "🤔 Aprenda a diferença entre 'querer' e 'precisar'",
        "📈 Comece a investir cedo, mesmo com pouco dinheiro - o tempo é seu maior aliado!",
        "📝 Evite compras por impulso - faça uma lista antes de sair de casa",
        "🏦 Abra uma conta poupança e automatize a transferência mensal",
        "📚 Leia sobre finanças pelo menos 15 minutos por semana"
    ]
    return {"tips": tips}

@app.post('/api/calculate_goal')
def calculate_goal(payload: GoalCalculation):
    """Calcula quanto tempo levará para atingir uma meta financeira"""
    if payload.monthly_saving <= 0:
        raise HTTPException(status_code=400, detail="Valor mensal deve ser maior que zero")
    
    monthly_rate = payload.annual_rate / 12
    months = 0
    accumulated = 0
    
    while accumulated < payload.goal_amount and months < 600:  # limite de 50 anos
        accumulated = accumulated * (1 + monthly_rate) + payload.monthly_saving
        months += 1
    
    years = months / 12
    return {
        "months_needed": months,
        "years_needed": round(years, 1),
        "total_invested": payload.monthly_saving * months,
        "interest_earned": round(accumulated - (payload.monthly_saving * months), 2),
        "final_amount": round(accumulated, 2)
    }

@app.get('/api/professions')
def get_professions_info():
    """Retorna informações sobre profissões e salários médios"""
    professions = {
        "Médico": {"salary_range": "8000-25000", "education": "Graduação + Residência"},
        "Engenheiro": {"salary_range": "5000-15000", "education": "Graduação"},
        "Professor": {"salary_range": "2000-8000", "education": "Graduação + Licenciatura"},
        "Programador": {"salary_range": "3000-12000", "education": "Graduação ou Cursos Técnicos"},
        "Enfermeiro": {"salary_range": "3000-8000", "education": "Graduação"},
        "Advogado": {"salary_range": "3000-20000", "education": "Graduação + OAB"},
        "Designer": {"salary_range": "2500-10000", "education": "Graduação ou Cursos"},
        "Administrador": {"salary_range": "3000-12000", "education": "Graduação"},
        "Psicólogo": {"salary_range": "2500-8000", "education": "Graduação + CRP"},
        "Dentista": {"salary_range": "4000-15000", "education": "Graduação + CRO"}
    }
    return professions

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=False)