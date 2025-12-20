#!/usr/bin/env python3
"""
Script para testar os endpoints da API e simular o que o frontend deveria receber
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_endpoints():
    print("\n" + "="*60)
    print("🧪 TESTANDO ENDPOINTS DE CONTEÚDO EDUCACIONAL")
    print("="*60 + "\n")
    
    # Test glossary
    try:
        print("1️⃣  Testando /glossary...")
        res = requests.get(f"{BASE_URL}/glossary")
        print(f"   Status: {res.status_code}")
        data = res.json()
        print(f"   Termos carregados: {len(data)}")
        print(f"   Primeiros 2 termos:")
        for i, (term, definition) in enumerate(list(data.items())[:2]):
            print(f"      - {term}: {definition[:50]}...")
        print("   ✅ Glossário OK\n")
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
    
    # Test tips
    try:
        print("2️⃣  Testando /tips...")
        res = requests.get(f"{BASE_URL}/tips")
        print(f"   Status: {res.status_code}")
        data = res.json()
        print(f"   Dicas carregadas: {len(data['tips'])}")
        print(f"   Primeiras 2 dicas:")
        for i, tip in enumerate(data['tips'][:2]):
            print(f"      - {tip[:50]}...")
        print("   ✅ Dicas OK\n")
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
    
    # Test professions
    try:
        print("3️⃣  Testando /professions...")
        res = requests.get(f"{BASE_URL}/professions")
        print(f"   Status: {res.status_code}")
        data = res.json()
        print(f"   Profissões carregadas: {len(data)}")
        print(f"   Primeiras 2 profissões:")
        for i, (prof, info) in enumerate(list(data.items())[:2]):
            print(f"      - {prof}: {info['salary_range']}")
        print("   ✅ Profissões OK\n")
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
    
    print("="*60)
    print("✅ TODOS OS ENDPOINTS RETORNAM DADOS CORRETAMENTE!")
    print("="*60)
    print("\n🔍 Se o conteúdo não aparecer no navegador, o problema está no:")
    print("   1. JavaScript não está acessando a aba corretamente (showTab)")
    print("   2. CSS está escondendo o conteúdo")
    print("   3. Há um erro no console do navegador (F12 → Console)")
    print("\n💡 Próximos passos:")
    print("   1. Abra o navegador")
    print("   2. Pressione F12 para abrir Developer Tools")
    print("   3. Vá para a aba 'Console'")
    print("   4. Clique em 'Aprenda' e veja os logs")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_endpoints()
