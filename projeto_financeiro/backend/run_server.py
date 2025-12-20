#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para iniciar o servidor da aplicação
"""
import uvicorn
import os
import sys

# Adiciona o diretório backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("=" * 60)
    print("  🚀 INICIANDO SERVIDOR - MEU FUTURO FINANCEIRO")
    print("=" * 60)
    print()
    print("📍 Servidor será iniciado em: http://localhost:8000")
    print("📁 Abra o frontend em: ../frontend/index.html")
    print()
    print("⚠️  Pressione CTRL+C para parar o servidor")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
