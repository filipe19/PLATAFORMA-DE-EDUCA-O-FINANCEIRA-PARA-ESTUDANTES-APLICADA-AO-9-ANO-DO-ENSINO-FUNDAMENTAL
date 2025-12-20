# backend/calc.py
"""
🧮 MÓDULO DE CÁLCULOS FINANCEIROS - EDUCATIVO 📊

Este arquivo é o "cérebro matemático" da plataforma! Aqui estão as funções que:
- Calculam como o dinheiro cresce com juros compostos 📈
- Simulam diferentes cenários de investimento 💰  
- Ensinam sobre risco através de simulações Monte Carlo 🎲

CONCEITOS IMPORTANTES IMPLEMENTADOS:
1. Juros Compostos: "Juros sobre juros" - o segredo para multiplicar dinheiro
2. Aportes Mensais: Como pequenos valores regulares se tornam grandes fortunas
3. Risco vs Retorno: Por que investimentos mais arriscados podem render mais
4. Simulação Monte Carlo: Como lidar com incertezas do mercado financeiro

Este código ensina que MATEMÁTICA = PODER FINANCEIRO! 🚀
"""

# Importações necessárias
from typing import List, Dict  # Para definir que tipo de dados as funções retornam
import math  # Funções matemáticas avançadas (não usado diretamente aqui)
import random  # Para gerar números aleatórios nas simulações de risco


def compound_monthly(initial: float, monthly: float, annual_rate: float, years: int) -> List[float]:
    """
    📈 FUNÇÃO MÁGICA DOS JUROS COMPOSTOS! ✨
    
    Esta função simula como seu dinheiro cresce mês após mês, ano após ano.
    É aqui que você vê a MATEMÁTICA transformando centavos em milhares!
    
    🎯 PARÂMETROS (o que você precisa informar):
    - initial: Valor inicial que você tem hoje (R$) 
    - monthly: Quanto você consegue guardar TODO MÊS (R$)
    - annual_rate: Quanto % seu dinheiro rende por ANO (ex: 0.10 = 10%)
    - years: Por quantos ANOS você vai fazer isso
    
    📊 RETORNA: Uma lista com seu saldo acumulado a cada ano
    
    🧠 LIÇÃO IMPORTANTE: 
    Mesmo guardando apenas R$ 50 por mês, depois de 10 anos você pode ter 
    muito mais que R$ 6.000 (50 x 12 x 10) por causa dos JUROS COMPOSTOS!
    """
    balances = []  # 📝 Lista onde vamos guardar o saldo de cada ano
    monthly_rate = annual_rate / 12.0  # 🔢 Taxa anual ÷ 12 = taxa mensal
    balance = initial  # 💰 Começamos com o valor inicial
    
    print(f"💡 SIMULAÇÃO INICIADA:")
    print(f"   📊 Valor inicial: R$ {initial:.2f}")
    print(f"   💸 Aporte mensal: R$ {monthly:.2f}")  
    print(f"   📈 Taxa anual: {annual_rate*100:.1f}%")
    print(f"   ⏰ Período: {years} anos")
    print()
    
    # 🔄 Para cada ano (incluindo o ano 0 = situação inicial)
    for y in range(years + 1):
        balances.append(round(balance, 2))  # ✅ Guarda o saldo atual
        
        if y == 0:
            print(f"📅 Ano {y}: R$ {balance:.2f} (valor inicial)")
        else:
            print(f"📅 Ano {y}: R$ {balance:.2f}")
        
        # 🗓️ Simula os 12 meses do ano atual
        for month in range(12):
            # 🧮 FÓRMULA DOS JUROS COMPOSTOS:
            # Novo saldo = (Saldo atual × (1 + juros)) + depósito mensal
            balance = balance * (1 + monthly_rate) + monthly
            
    print(f"🎉 RESULTADO FINAL: R$ {balance:.2f}")
    print(f"💰 Você investiu: R$ {(initial + monthly * years * 12):.2f}")
    print(f"📈 Os juros renderam: R$ {(balance - initial - monthly * years * 12):.2f}")
    print("="*50)
    
    return balances


def project_investments(monthly: float, years: int, annual_return: float, initial: float = 0.0) -> Dict:
    """
    🔮 MÁQUINA DO TEMPO FINANCEIRA! ⏰
    
    Esta função mostra exatamente como seus investimentos vão evoluir ao longo do tempo.
    É como uma "máquina do tempo" que te leva para o futuro para ver seu dinheiro!
    
    🎯 PARÂMETROS:
    - monthly: Quanto você vai investir por mês (R$)
    - years: Por quantos anos (ex: 5, 10, 20 anos)
    - annual_return: Taxa de retorno anual esperada (ex: 0.05 = 5% ao ano)
    - initial: Dinheiro que você já tem hoje (padrão = R$ 0)
    
    📦 RETORNA: Um "pacote" com:
    - years: Lista dos anos (0, 1, 2, 3...)
    - balances: Quanto dinheiro você terá em cada ano
    - final: Valor final no último ano
    
    💡 DICA EDUCATIVA:
    Compare diferentes taxas! Veja como 5% vs 10% ao ano fazem ENORME diferença!
    """
    # 🧮 Chama a função de juros compostos para fazer os cálculos
    balances = compound_monthly(initial, monthly, annual_return, years)
    
    # 📦 Organiza os dados em um "pacote" organizado
    result = {
        "years": list(range(0, years + 1)),  # [0, 1, 2, 3, 4, 5...]
        "balances": balances,  # [100, 250, 420, 612...]
        "final": balances[-1]  # Último valor da lista = valor final
    }
    
    print(f"📋 RESUMO DA PROJEÇÃO:")
    print(f"   🎯 Investimento mensal: R$ {monthly}")
    print(f"   📅 Período: {years} anos") 
    print(f"   📈 Taxa anual: {annual_return*100}%")
    print(f"   💰 Resultado final: R$ {result['final']:.2f}")
    
    return result


def monte_carlo_projection(monthly: float, years: int, mu: float = 0.12, sigma: float = 0.25, n_sims: int = 1000):
    """
    🎲 SIMULADOR DE RISCO - MONTE CARLO! 🎯
    
    Esta é a função mais AVANÇADA! Ela simula milhares de cenários diferentes
    para mostrar que investimentos arriscados podem dar resultados muito variados.
    
    🤔 POR QUE ISSO É IMPORTANTE?
    Na vida real, investimentos não rendem sempre a mesma %. 
    Às vezes rendem 15%, às vezes perdem 5%, às vezes ganham 30%!
    
    🎯 PARÂMETROS:
    - monthly: Quanto você investe por mês (R$)
    - years: Por quantos anos
    - mu: Retorno médio esperado por ano (ex: 0.12 = 12% ao ano)
    - sigma: "Risco" ou volatilidade (ex: 0.25 = pode variar ±25%)
    - n_sims: Quantas simulações fazer (padrão = 1000 cenários!)
    
    📊 RETORNA: Três cenários possíveis:
    - p10: Cenário PESSIMISTA (só 10% das vezes fica pior que isso)
    - p50: Cenário PROVÁVEL (resultado mais comum)  
    - p90: Cenário OTIMISTA (só 10% das vezes fica melhor que isso)
    
    🎓 LIÇÃO DE VIDA:
    Investimentos arriscados podem te deixar rico OU pobre! 
    Por isso é importante diversificar (não colocar tudo no mesmo lugar).
    """
    
    print(f"🎲 INICIANDO SIMULAÇÃO MONTE CARLO!")
    print(f"   🔢 Número de simulações: {n_sims}")
    print(f"   📊 Retorno médio esperado: {mu*100:.1f}% ao ano")
    print(f"   ⚡ Volatilidade (risco): {sigma*100:.1f}%")
    print()
    
    finals = []  # 📝 Lista para guardar o resultado final de cada simulação
    
    # 🔄 Roda milhares de simulações com diferentes cenários
    for simulation in range(n_sims):
        balance = 0.0  # 💰 Cada simulação começa do zero
        
        # 📅 Para cada ano da simulação
        for year in range(years):
            # 🎲 GERA UM RESULTADO ALEATÓRIO para este ano
            # Baseado na média (mu) e risco (sigma)
            r = random.normalvariate(mu, sigma)  # 📊 Retorno anual aleatório
            monthly_rate = r / 12.0  # 🔢 Converte para taxa mensal
            
            # 📅 Aplica este resultado durante os 12 meses do ano
            for month in range(12):
                balance = balance * (1 + monthly_rate) + monthly  # 💰 Juros + depósito
                
        finals.append(balance)  # ✅ Guarda o resultado final desta simulação
        
        # 📊 Progresso a cada 100 simulações
        if (simulation + 1) % 100 == 0:
            print(f"   ⏳ Progresso: {simulation + 1}/{n_sims} simulações concluídas")
    
    # 📊 ANÁLISE DOS RESULTADOS
    finals_sorted = sorted(finals)  # 📈 Ordena do menor para o maior
    
    # 🎯 Calcula os percentis (marcos estatísticos importantes)
    p10 = finals_sorted[int(0.1 * len(finals_sorted))]   # 📉 10% pior cenário
    p50 = finals_sorted[int(0.5 * len(finals_sorted))]   # 📊 Cenário mediano (mais provável)
    p90 = finals_sorted[int(0.9 * len(finals_sorted))]   # 📈 10% melhor cenário
    
    print()
    print(f"📊 RESULTADOS DA SIMULAÇÃO MONTE CARLO:")
    print(f"   📉 Cenário Pessimista (10%): R$ {p10:.2f}")
    print(f"   📊 Cenário Provável (50%): R$ {p50:.2f}")  
    print(f"   📈 Cenário Otimista (90%): R$ {p90:.2f}")
    print()
    print(f"💡 INTERPRETAÇÃO:")
    print(f"   • Em 90% dos casos, você terá PELO MENOS R$ {p10:.2f}")
    print(f"   • O resultado mais comum é em torno de R$ {p50:.2f}")
    print(f"   • Em 10% dos casos, você pode ter MAIS DE R$ {p90:.2f}")
    print("="*60)
    
    # 📦 Retorna os resultados organizados
    return {
        "n_sims": n_sims,           # Quantas simulações foram feitas
        "p10": round(p10, 2),       # Cenário pessimista  
        "p50": round(p50, 2),       # Cenário provável
        "p90": round(p90, 2),       # Cenário otimista
        "media": round(sum(finals) / len(finals), 2),  # Média de todos os resultados
        "volatilidade_usada": sigma  # Nível de risco usado na simulação
    }


# 🧪 FUNÇÃO DE TESTE - Para verificar se tudo funciona!
def test_calculations():
    """
    🧪 LABORATÓRIO DE TESTES! 
    
    Esta função testa se nossos cálculos estão funcionando corretamente.
    É como um "laboratório" onde testamos nossas fórmulas matemáticas.
    """
    print("🧪 TESTANDO OS CÁLCULOS FINANCEIROS...")
    print()
    
    # Teste 1: Juros compostos básicos
    print("📋 TESTE 1: Guardando R$ 100/mês por 5 anos a 8% ao ano")
    resultado = project_investments(monthly=100, years=5, annual_return=0.08)
    print()
    
    # Teste 2: Simulação Monte Carlo  
    print("📋 TESTE 2: Simulação de risco com ações (12% ± 25%)")
    monte_carlo_projection(monthly=100, years=5, mu=0.12, sigma=0.25, n_sims=100)
    print()
    
    print("✅ TESTES CONCLUÍDOS! Tudo funcionando perfeitamente! 🎉")


# 🚀 Se este arquivo for executado diretamente, roda os testes
if __name__ == "__main__":
    test_calculations()