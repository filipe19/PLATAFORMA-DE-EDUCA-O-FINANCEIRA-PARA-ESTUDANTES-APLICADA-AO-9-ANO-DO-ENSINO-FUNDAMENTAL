#!/usr/bin/env python3
"""
SERVIDOR DE DADOS - Salva respostas dos alunos em CSV
Protocolo: HTTP POST (simples, confiável, compatível com navegadores)
"""

import http.server
import json
import csv
import os
from datetime import datetime
from pathlib import Path
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurações
PORT = 5000
CSV_FILE = Path(__file__).parent.parent / 'dados_alunos.csv'
STATIC_DIR = Path(__file__).parent.parent / 'frontend'

# Headers CORS para permitir requisições do frontend
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
}

class DadosHandler(http.server.BaseHTTPRequestHandler):
    """Handler para requisições HTTP"""
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        for key, value in CORS_HEADERS.items():
            self.send_header(key, value)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Customizar logs"""
        logger.info(format % args)
    
    # ==================== POST ====================
    def do_POST(self):
        """Receber dados POST do formulário"""
        
        if self.path == '/salvar_dados':
            try:
                # Ler JSON do corpo da requisição
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body)
                
                logger.info(f"📥 Dados recebidos de {data.get('nome', 'DESCONHECIDO')}")
                
                # Salvar em CSV
                self._salvar_csv(data)
                
                # Responder com sucesso
                self.send_response(200)
                for key, value in CORS_HEADERS.items():
                    self.send_header(key, value)
                self.end_headers()
                
                resposta = {
                    'sucesso': True,
                    'mensagem': 'Dados salvos com sucesso',
                    'timestamp': datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(resposta).encode('utf-8'))
                logger.info(f"✅ Resposta enviada: sucesso")
                
            except json.JSONDecodeError as e:
                logger.error(f"❌ JSON inválido: {e}")
                self._resposta_erro("JSON inválido", 400)
            except Exception as e:
                logger.error(f"❌ Erro ao processar: {e}")
                self._resposta_erro(str(e), 500)
        
        elif self.path == '/baixar_csv':
            """Permitir download do CSV"""
            try:
                if not CSV_FILE.exists():
                    self._resposta_erro("Nenhum dado coletado ainda", 404)
                    return
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/csv; charset=utf-8')
                self.send_header('Content-Disposition', f'attachment; filename=dados_alunos_{datetime.now().strftime("%d-%m-%Y")}.csv')
                self.end_headers()
                
                with open(CSV_FILE, 'rb') as f:
                    self.wfile.write(f.read())
                    
                logger.info("✅ CSV baixado")
            
            except Exception as e:
                logger.error(f"❌ Erro ao baixar CSV: {e}")
                self._resposta_erro(str(e), 500)
        else:
            self._resposta_erro("Endpoint não encontrado", 404)
    
    # ==================== GET ====================
    def do_GET(self):
        """Servir arquivos estáticos e JSON de dados"""
        
        if self.path == '/dados.json':
            """API: retornar dados em JSON"""
            try:
                if not CSV_FILE.exists():
                    dados = []
                else:
                    dados = self._ler_csv()
                
                self.send_response(200)
                for key, value in CORS_HEADERS.items():
                    self.send_header(key, value)
                self.end_headers()
                
                self.wfile.write(json.dumps({
                    'sucesso': True,
                    'total': len(dados),
                    'dados': dados
                }).encode('utf-8'))
                
            except Exception as e:
                logger.error(f"❌ Erro ao ler dados: {e}")
                self._resposta_erro(str(e), 500)
        
        elif self.path == '/status':
            """API: status do servidor"""
            try:
                total_registros = 0
                if CSV_FILE.exists():
                    with open(CSV_FILE, 'r', encoding='utf-8') as f:
                        total_registros = sum(1 for line in f) - 1  # -1 para header
                
                self.send_response(200)
                for key, value in CORS_HEADERS.items():
                    self.send_header(key, value)
                self.end_headers()
                
                self.wfile.write(json.dumps({
                    'servidor': 'ativo',
                    'porta': PORT,
                    'arquivo_csv': str(CSV_FILE),
                    'total_registros': total_registros,
                    'timestamp': datetime.now().isoformat()
                }).encode('utf-8'))
                
            except Exception as e:
                self._resposta_erro(str(e), 500)
        
        else:
            # Servir arquivos estáticos do frontend
            self._servir_arquivo_estático()
    
    # ==================== Métodos Auxiliares ====================
    
    def _salvar_csv(self, data):
        """Salvar dados em arquivo CSV"""
        
        # Colunas esperadas
        colunas = [
            'tipo', 'nome', 'idade_atual', 'idade_futura', 'renda_atual', 
            'renda_futura_possivel', 'profissao_interesse', 'profissao_sonhos',
            'faixa_salarial', 'poupanca_mensal', 'investimento_tipo',
            'tempo_anos', 'projecao_conservador', 'projecao_moderado', 
            'projecao_arriscado', 'goal_amount', 'monthly_saving', 'annual_rate',
            'timestamp'
        ]
        
        # Preparar linha
        linha = {}
        for col in colunas:
            # Permitir variações no nome
            if col in data:
                linha[col] = data[col]
            else:
                # Buscar aliases
                if col == 'idade_atual' and 'idade' in data:
                    linha[col] = data['idade']
                elif col == 'profissao_sonhos' and 'profissao_desejada' in data:
                    linha[col] = data['profissao_desejada']
                else:
                    linha[col] = data.get(col, '')
        
        linha['timestamp'] = data.get('timestamp', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
        # Se arquivo não existe, criar com header
        arquivo_existe = CSV_FILE.exists()
        
        with open(CSV_FILE, 'a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=colunas)
            
            if not arquivo_existe:
                writer.writeheader()
                logger.info(f"📄 Novo arquivo criado: {CSV_FILE}")
            
            writer.writerow(linha)
        
        logger.info(f"✅ Dados de {linha.get('nome', 'desconhecido')} salvos em CSV")
    
    def _ler_csv(self):
        """Ler todos os dados do CSV"""
        dados = []
        try:
            with open(CSV_FILE, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    dados.append(row)
        except Exception as e:
            logger.error(f"❌ Erro ao ler CSV: {e}")
        return dados
    
    def _resposta_erro(self, mensagem, codigo=400):
        """Enviar resposta de erro"""
        self.send_response(codigo)
        for key, value in CORS_HEADERS.items():
            self.send_header(key, value)
        self.end_headers()
        
        resposta = {
            'sucesso': False,
            'erro': mensagem,
            'timestamp': datetime.now().isoformat()
        }
        self.wfile.write(json.dumps(resposta).encode('utf-8'))
    
    def _servir_arquivo_estático(self):
        """Servir arquivos estáticos do frontend"""
        
        # Caminho solicitado
        if self.path == '/' or self.path == '/index.html':
            caminho = STATIC_DIR / 'index.html'
        else:
            caminho = STATIC_DIR / self.path.lstrip('/')
        
        # Validar segurança
        try:
            caminho = caminho.resolve()
            if not str(caminho).startswith(str(STATIC_DIR.resolve())):
                self._resposta_erro("Acesso negado", 403)
                return
        except:
            self._resposta_erro("Caminho inválido", 400)
            return
        
        # Servir arquivo
        if caminho.exists() and caminho.is_file():
            try:
                content_type = self._get_content_type(str(caminho))
                
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.end_headers()
                
                with open(caminho, 'rb') as f:
                    self.wfile.write(f.read())
                
                logger.info(f"✅ Arquivo servido: {self.path}")
            
            except Exception as e:
                logger.error(f"❌ Erro ao servir arquivo: {e}")
                self._resposta_erro(str(e), 500)
        else:
            self._resposta_erro("Arquivo não encontrado", 404)
    
    def _get_content_type(self, filepath):
        """Detectar tipo de conteúdo"""
        if filepath.endswith('.html'):
            return 'text/html; charset=utf-8'
        elif filepath.endswith('.js'):
            return 'text/javascript; charset=utf-8'
        elif filepath.endswith('.css'):
            return 'text/css; charset=utf-8'
        elif filepath.endswith('.json'):
            return 'application/json'
        elif filepath.endswith('.csv'):
            return 'text/csv'
        elif filepath.endswith('.png'):
            return 'image/png'
        elif filepath.endswith('.jpg') or filepath.endswith('.jpeg'):
            return 'image/jpeg'
        else:
            return 'application/octet-stream'

def main():
    """Iniciar servidor"""
    try:
        server_address = ('0.0.0.0', PORT)
        httpd = http.server.HTTPServer(server_address, DadosHandler)
        
        print("\n" + "="*60)
        print("🚀 SERVIDOR DE DADOS INICIADO COM SUCESSO!")
        print("="*60)
        print(f"📍 Endereço:     http://localhost:{PORT}")
        print(f"📁 Pasta:        {STATIC_DIR}")
        print(f"💾 Arquivo CSV:  {CSV_FILE}")
        print(f"⏰ Início:       {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*60)
        print("\n📡 Aguardando requisições...")
        print("💡 Dica: Abra http://localhost:5000 no navegador")
        print("⏹️  Pressione CTRL+C para parar\n")
        
        httpd.serve_forever()
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Servidor interrompido pelo usuário")
    except OSError as e:
        if e.errno == 98:  # Porta em uso
            print(f"\n❌ ERRO: Porta {PORT} já está em uso!")
            print(f"   Solução: Feche outro servidor ou use outra porta")
        else:
            print(f"\n❌ ERRO: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
