# 🚀 COMANDOS ÚTEIS PARA O PROJETO

## 🐍 Backend (Python/FastAPI)

### Instalar dependências
```bash
cd backend
pip install fastapi uvicorn pydantic python-multipart
```

### Executar servidor de desenvolvimento
```bash
cd backend
python app.py
```

### Testar APIs manualmente
```bash
# Testar glossário
curl http://localhost:8000/api/glossary

# Testar dicas
curl http://localhost:8000/api/tips

# Testar profissões
curl http://localhost:8000/api/professions
```

### Verificar banco de dados
```python
# No terminal Python
import sqlite3
conn = sqlite3.connect('backend/data.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM submissions")
print(cursor.fetchall())
conn.close()
```

## 🌐 Frontend (HTML/CSS/JS)

### Servir localmente (opção 1)
- Abrir `frontend/index.html` diretamente no navegador

### Servir com Python (opção 2)
```bash
cd frontend
python -m http.server 8080
# Acesse: http://localhost:8080
```

### Servir com Node.js (opção 3)
```bash
cd frontend
npx serve .
```

## 🧪 Testes

### Testar cálculos financeiros
```bash
cd backend
python calc.py
```

### Testar banco de dados
```bash
cd backend
python db.py
```

### Teste completo do sistema
1. Execute o backend: `python backend/app.py`
2. Abra `frontend/index.html` no navegador
3. Preencha os formulários
4. Verifique se os cálculos aparecem corretamente

## 📊 Monitoramento

### Ver logs do FastAPI
- Os logs aparecem no terminal onde rodou `python app.py`

### Ver logs do frontend
- Abra DevTools (F12) → Console

### Verificar requisições
- DevTools (F12) → Network → Filtrar por XHR/Fetch

## 🐛 Troubleshooting

### Backend não inicia
```bash
# Verificar se as dependências estão instaladas
pip list | grep fastapi

# Verificar se a porta está livre
netstat -an | findstr :8000
```

### Frontend não conecta
1. Verificar se backend está rodando (http://localhost:8000)
2. Verificar console do navegador por erros CORS
3. Verificar se URLs no `app.js` estão corretas

### Banco de dados com problemas
```bash
# Deletar e recriar
del backend/data.db
python backend/app.py
```

## 🚀 Deploy (Produção)

### Opções de deploy do backend
- **Heroku**: Gratuito, fácil setup
- **Railway**: Moderno, deploy automático  
- **PythonAnywhere**: Específico para Python
- **DigitalOcean**: VPS tradicional

### Opções de deploy do frontend
- **GitHub Pages**: Gratuito para repositórios públicos
- **Netlify**: Deploy automático, CDN global
- **Vercel**: Otimizado para frontend

### Arquivo Procfile (para Heroku)
```
web: uvicorn app:app --host=0.0.0.0 --port=${PORT:-5000}
```

### Variáveis de ambiente para produção
```bash
export DATABASE_URL="sqlite:///./production.db"
export CORS_ORIGINS="https://seudominio.com"
```

## 📈 Melhorias Futuras

### Backend
- [ ] Autenticação de usuários
- [ ] API de relatórios para professores
- [ ] Cache de cálculos pesados
- [ ] Rate limiting
- [ ] Logs estruturados

### Frontend  
- [ ] PWA (Progressive Web App)
- [ ] Modo offline
- [ ] Notificações push
- [ ] Temas dark/light
- [ ] Animações avançadas

### Educacional
- [ ] Mais tipos de investimento
- [ ] Simulador de inflação
- [ ] Calculadora de aposentadoria
- [ ] Jogos de educação financeira
- [ ] Quiz interativo

## 🔧 Configuração do VS Code

### Extensões recomendadas
- Python
- Pylance  
- FastAPI
- HTML CSS Support
- Live Server
- Thunder Client (testar APIs)

### settings.json
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "html.format.enable": true,
    "css.validate": true,
    "javascript.validate.enable": true
}
```

## 📚 Recursos de Aprendizado

### Documentação
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)

### Cursos relacionados
- Matemática Financeira básica
- Desenvolvimento Web com Python
- Design de Interfaces (UI/UX)
- Educação Financeira

## 👥 Contribuindo

### Setup do ambiente de desenvolvimento
```bash
git clone [seu-repo]
cd projeto_financeiro
pip install -r backend/requirements.txt
python backend/app.py
```

### Padrões de código
- Python: PEP 8
- JavaScript: ESLint recomendado  
- HTML: Semântico e acessível
- CSS: BEM methodology

### Fluxo de commits
```bash
git checkout -b feature/nova-funcionalidade
# fazer alterações
git add .
git commit -m "feat: adiciona calculadora de inflação"
git push origin feature/nova-funcionalidade
# abrir Pull Request
```