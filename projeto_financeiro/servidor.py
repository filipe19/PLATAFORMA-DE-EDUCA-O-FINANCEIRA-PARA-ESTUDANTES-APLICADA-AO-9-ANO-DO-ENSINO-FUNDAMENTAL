#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor HTTP Simples - Porta 8080
Executa: python servidor.py
"""

import http.server
import socketserver
import os
import sys

PORT = 8080
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'frontend')

# Verificar se a pasta frontend existe
if not os.path.exists(FRONTEND_DIR):
    print(f"❌ Erro: Pasta 'frontend' não encontrada em {FRONTEND_DIR}")
    print(f"📁 Diretório atual: {os.getcwd()}")
    print(f"📁 Conteúdo: {os.listdir('.')}")
    sys.exit(1)

os.chdir(FRONTEND_DIR)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

try:
    Handler = MyHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("\n" + "="*60)
        print("🚀 SERVIDOR INICIADO COM SUCESSO!")
        print("="*60)
        print(f"📁 Pasta: {FRONTEND_DIR}")
        print(f"🌐 URL: http://localhost:{PORT}")
        print(f"🌐 URL: http://127.0.0.1:{PORT}")
        print("")
        print("📊 Links Úteis:")
        print(f"  - Formulário: http://localhost:{PORT}")
        print(f"  - Debug Console: http://localhost:{PORT}/debug_console.html")
        print(f"  - Dados/CSV: http://localhost:{PORT}/debug_dados.html")
        print(f"  - Diagnóstico: http://localhost:{PORT}/diagnostico.html")
        print("")
        print("⏸️  Pressione Ctrl+C para parar")
        print("="*60 + "\n")
        
        httpd.serve_forever()
        
except KeyboardInterrupt:
    print("\n\n⏹️  Servidor parado pelo usuário")
    sys.exit(0)
except Exception as e:
    print(f"❌ Erro: {e}")
    sys.exit(1)
