#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste completo para validar todas as funcionalidades da aplicação
"""
import requests
import json
import time

API_URL = "http://localhost:8000/api"

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def test_glossary():
    print_header("TESTANDO: Glossário Financeiro")
    try:
        response = requests.get(f"{API_URL}/glossary", timeout=5)
        data = response.json()
        print(f"✅ Glossário carregado com sucesso!")
        print(f"   Termos disponíveis: {len(data)}")
        print(f"   Primeiros termos: {list(data.keys())[:3]}")
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar glossário: {e}")
        return False

def test_tips():
    print_header("TESTANDO: Dicas Financeiras")
    try:
        response = requests.get(f"{API_URL}/tips", timeout=5)
        data = response.json()
        print(f"✅ Dicas carregadas com sucesso!")
        print(f"   Total de dicas: {len(data['tips'])}")
        print(f"   Primeira dica: {data['tips'][0][:50]}...")
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar dicas: {e}")
        return False

def test_professions():
    print_header("TESTANDO: Profissões")
    try:
        response = requests.get(f"{API_URL}/professions", timeout=5)
        data = response.json()
        print(f"✅ Profissões carregadas com sucesso!")
        print(f"   Total de profissões: {len(data)}")
        print(f"   Profissões: {list(data.keys())[:5]}")
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar profissões: {e}")
        return False

def test_reality_submission():
    print_header("TESTANDO: Submissão de Realidade")
    try:
        payload = {
            "nome": "João Silva",
            "idade": 15,
            "renda_atual": 0,
            "renda_futura_possivel": 3000.0,
            "profissao_interesse": "Engenheiro"
        }
        response = requests.post(f"{API_URL}/submit_reality", json=payload, timeout=5)
        data = response.json()
        print(f"✅ Realidade salva com sucesso!")
        print(f"   Status: {data['status']}")
        print(f"   Mensagem: {data['message']}")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar realidade: {e}")
        return False

def test_future_projections():
    print_header("TESTANDO: Projeções de Futuro")
    try:
        payload = {
            "nome": "Maria Santos",
            "idade": 15,
            "profissao_dos_sonhos": "Médica",
            "faixa_salarial": 8000.0,
            "poupanca_mensal": 500.0,
            "investimento_tipo": "moderado",
            "tempo_anos": 10
        }
        response = requests.post(f"{API_URL}/submit_future", json=payload, timeout=10)
        data = response.json()
        print(f"✅ Projeções calculadas com sucesso!")
        print(f"   Status: {data['status']}")
        print(f"   Tipos de investimento: {list(data['projections'].keys())}")
        
        for tipo, proj in data['projections'].items():
            print(f"   {tipo.capitalize()}: Final R$ {proj['final']:,.2f}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao calcular projeções: {e}")
        return False

def test_monte_carlo():
    print_header("TESTANDO: Simulação Monte Carlo")
    try:
        payload = {
            "nome": "Ana Costa",
            "idade": 15,
            "profissao_dos_sonhos": "Investidora",
            "faixa_salarial": 10000.0,
            "poupanca_mensal": 1000.0,
            "investimento_tipo": "arriscado",
            "tempo_anos": 5
        }
        response = requests.post(f"{API_URL}/simulate_montecarlo", json=payload, timeout=15)
        data = response.json()
        print(f"✅ Simulação Monte Carlo executada com sucesso!")
        print(f"   Status: {data['status']}")
        print(f"   Simulações: {data['montecarlo']['n_sims']}")
        print(f"   Cenário pessimista (p10): R$ {data['montecarlo']['p10']:,.2f}")
        print(f"   Cenário provável (p50): R$ {data['montecarlo']['p50']:,.2f}")
        print(f"   Cenário otimista (p90): R$ {data['montecarlo']['p90']:,.2f}")
        return True
    except Exception as e:
        print(f"❌ Erro na simulação Monte Carlo: {e}")
        return False

def test_goal_calculation():
    print_header("TESTANDO: Calculadora de Metas")
    try:
        payload = {
            "goal_amount": 10000.0,
            "monthly_saving": 500.0,
            "annual_rate": 0.05
        }
        response = requests.post(f"{API_URL}/calculate_goal", json=payload, timeout=5)
        data = response.json()
        print(f"✅ Meta calculada com sucesso!")
        print(f"   Tempo necessário: {data['years_needed']} anos ({data['months_needed']} meses)")
        print(f"   Total investido: R$ {data['total_invested']:,.2f}")
        print(f"   Juros ganhos: R$ {data['interest_earned']:,.2f}")
        print(f"   Valor final: R$ {data['final_amount']:,.2f}")
        return True
    except Exception as e:
        print(f"❌ Erro ao calcular meta: {e}")
        return False

def test_submissions_list():
    print_header("TESTANDO: Lista de Submissões")
    try:
        response = requests.get(f"{API_URL}/submissions", timeout=5)
        data = response.json()
        print(f"✅ Submissões recuperadas com sucesso!")
        print(f"   Total de submissões: {data['count']}")
        if data['data']:
            print(f"   Primeira submissão: {data['data'][0]}")
        return True
    except Exception as e:
        print(f"❌ Erro ao recuperar submissões: {e}")
        return False

def main():
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🧪 TESTE COMPLETO DA PLATAFORMA FINANCEIRA  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    tests = [
        ("Glossário", test_glossary),
        ("Dicas", test_tips),
        ("Profissões", test_professions),
        ("Realidade", test_reality_submission),
        ("Projeções", test_future_projections),
        ("Monte Carlo", test_monte_carlo),
        ("Metas", test_goal_calculation),
        ("Submissões", test_submissions_list),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ Erro ao executar teste {name}: {e}")
            results.append((name, False))
    
    # Resumo final
    print_header("RESUMO DOS TESTES")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status}  - {name}")
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TODAS AS FUNCIONALIDADES ESTÃO FUNCIONANDO PERFEITAMENTE! 🎉")
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam. Verifique os logs acima.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTeste interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro geral: {e}")
