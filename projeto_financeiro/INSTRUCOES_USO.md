# 🚀 Como Executar o Projeto - Meu Futuro Financeiro

## ✅ Projeto Corrigido e Pronto para Uso!

### 📋 O que foi corrigido:
1. ✅ Erro de indentação no arquivo `backend/db.py`
2. ✅ Dependências instaladas no ambiente virtual
3. ✅ Servidor configurado para rodar sem interrupções
4. ✅ Scripts de inicialização criados

---

## 🎯 Formas de Executar o Projeto

### **Opção 1: Usando o script batch (Mais Fácil - Windows)**
```bash
# Clique duas vezes no arquivo:
start_server.bat
```

### **Opção 2: Linha de comando manual**
```bash
# 1. Abra um terminal PowerShell no diretório do projeto
cd "c:\Users\filipealves\Desktop\Lic-Matemática\PraticasExtencionistasII\projeto_financeiro"

# 2. Ative o ambiente virtual
.venv\Scripts\Activate.ps1

# 3. Inicie o servidor
python backend\run_server.py
```

### **Opção 3: Pelo VS Code**
```bash
# No terminal integrado do VS Code:
python backend\run_server.py
```

---

## 🌐 Como Acessar a Aplicação

Depois de iniciar o servidor, você verá a mensagem:
```
🚀 INICIANDO SERVIDOR - MEU FUTURO FINANCEIRO
📍 Servidor será iniciado em: http://localhost:8000
```

### **Acessar o Frontend:**
1. Abra seu navegador (Chrome, Firefox, Edge)
2. Abra o arquivo: `frontend/index.html`
   - Ou navegue até: `c:\Users\filipealves\Desktop\Lic-Matemática\PraticasExtencionistasII\projeto_financeiro\frontend\index.html`

---

## 🛑 Como Parar o Servidor

- Pressione `CTRL + C` no terminal onde o servidor está rodando
- Ou feche a janela do terminal

---

## 📁 Estrutura do Projeto

```
projeto_financeiro/
├── backend/                    # Código do servidor
│   ├── app.py                 # API principal
│   ├── calc.py                # Cálculos financeiros
│   ├── db.py                  # Banco de dados
│   ├── run_server.py          # Script para iniciar servidor
│   └── requirements.txt       # Dependências
├── frontend/                   # Interface do usuário
│   ├── index.html             # Página principal
│   ├── app.js                 # Lógica JavaScript
│   └── styles.css             # Estilos
├── .venv/                      # Ambiente virtual Python 
├── start_server.bat           # Iniciar servidor fácil
└── INSTRUCOES_USO.md          # Este arquivo
```

---

## 🔧 Tecnologias Utilizadas

- **Backend**: Python + FastAPI + SQLite
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Servidor**: Uvicorn

---

## 💡 Funcionalidades

1. 📊 **Simulação de Investimentos** - Calcule o crescimento do seu dinheiro
2. 🎯 **Metas Financeiras** - Defina e acompanhe objetivos
3. 📚 **Educação Financeira** - Glossário e dicas práticas
4. 💼 **Guia de Profissões** - Salários médios e carreiras

---

## ⚠️ Problemas Comuns

### Porta 8000 já em uso?
```bash
# Windows PowerShell
netstat -ano | Select-String ":8000"
Stop-Process -Id [PID_DO_PROCESSO] -Force
```

### Erro de módulo não encontrado?
```bash
# Reinstale as dependências
pip install -r backend/requirements.txt
```

---

## 📞 Suporte

Se encontrar algum problema:
1. Verifique se o ambiente virtual está ativado
2. Confirme que todas as dependências foram instaladas
3. Certifique-se de que a porta 8000 está livre

---

## ✨ Projeto Finalizado!

O projeto está totalmente funcional e pronto para uso educacional! 🎓💰

---

**Data de Correção**: 17 de Dezembro de 2025
**Status**: ✅ OPERACIONAL
