# 🧪 GUIA DE TESTE - VERIFICAÇÃO DE ABAS

## 📋 Checklist de Testes

### 1️⃣ Verificar Backend Rodando
- Abra o terminal do backend
- Confirme que está rodando em: http://localhost:8000
- Se não estiver, execute: `python backend/run_server.py`

### 2️⃣ Abrir DevTools no Navegador
- Abra `frontend/index.html` no navegador
- Pressione **F12** para abrir Developer Tools
- Vá para a aba **Console**

### 3️⃣ Verificar Logs de Inicialização
No console, você deve ver:
```
========================================
🚀 DOM Loaded - Iniciando aplicação...
========================================
✅ Event listener: formReality
✅ Event listener: formFuture
✅ Event listener: goalForm
----------------------------------------
📚 Carregando conteúdo educacional...
----------------------------------------
📚 Iniciando carregamento de glossário...
✅ Glossário recebido da API: 10 termos
✅ Glossário renderizado no DOM
💡 Iniciando carregamento de dicas...
✅ Dicas recebidas da API: 10 dicas
✅ Dicas renderizadas no DOM
💼 Iniciando carregamento de profissões...
✅ Profissões recebidas da API: 10 profissões
✅ Profissões renderizadas no DOM
========================================
✅ Aplicação inicializada com sucesso!
========================================
```

### 4️⃣ Testar Navegação entre Abas

**Aba "🚀 Simulação":**
- Deve estar visível por padrão
- Formulários "Realidade Atual" e "Futuro Profissional" devem estar visíveis

**Aba "🎯 Metas":**
- Clique no botão "🎯 Metas"
- Console deve mostrar: `📑 showTab called: metas`
- Calculadora de metas deve aparecer

**Aba "📚 Aprenda":**
- Clique no botão "📚 Aprenda"
- Console deve mostrar: `📑 showTab called: educacao`
- Deve ver:
  - Título "📚 Glossário Financeiro"
  - Grid com 10 termos (Ações, CDI, Diversificação, etc.)
  - Título "💡 Dicas Financeiras Práticas"
  - Lista com 10 dicas

**Aba "💼 Profissões":**
- Clique no botão "💼 Profissões"
- Console deve mostrar: `📑 showTab called: profissoes`
- Deve ver:
  - Título "💼 Guia de Profissões e Salários"
  - Grid com 10 profissões
  - Cada profissão mostrando salário e formação

### 5️⃣ Possíveis Problemas

#### ❌ Se NÃO aparecer conteúdo educacional:

**Problema 1: Erro de CORS**
```
❌ ERRO ao carregar glossário: Failed to fetch
```
**Solução:** Backend não está rodando ou CORS bloqueado
- Reinicie o backend
- Verifique se está em http://localhost:8000

**Problema 2: Elementos não encontrados**
```
❌ Elemento #glossaryContent não encontrado no DOM
```
**Solução:** HTML pode ter erro
- Verifique se os IDs estão corretos
- Inspecione elemento (F12 → Elements) e procure por `id="glossaryContent"`

**Problema 3: Aba não troca**
```
❌ Tab element not found: educacao
```
**Solução:** JavaScript showTab com erro
- Verifique se há erros de sintaxe no console
- Recarregue a página (Ctrl+F5)

#### ✅ Se aparecer conteúdo:
Parabéns! Tudo está funcionando corretamente!

### 6️⃣ Teste Completo de Funcionalidade

Preencha cada formulário:

**Realidade Atual:**
- Nome: Seu Nome
- Idade: 18
- Renda atual: 0
- Renda futura: 3000
- Profissão: Qualquer
- Clique "Salvar"

**Futuro Profissional:**
- Nome: Seu Nome
- Idade: 18
- Aporte mensal: 100
- Quantos anos: 10
- Clique "Calcular Minha Projeção"
- Deve aparecer:
  - Tabela com 3 cenários (Conservador, Moderado, Arriscado)
  - Gráfico de barras colorido
  - Simulação Monte Carlo com 3 cenários

**Calculadora de Metas:**
- Clique em "💻 Notebook (R$ 3.000)"
- Preencha "Quanto pode poupar por mês": 200
- Clique "Calcular Minha Meta"
- Deve mostrar tempo necessário e valores

## 📊 Resultado Esperado

Todas as abas devem ter conteúdo visível e todos os formulários devem funcionar!

## 🆘 Se ainda tiver problemas:

1. Capture screenshot do console com erro
2. Capture screenshot da aba vazia
3. Verifique arquivo: `frontend/test_tabs.html` (teste simplificado)
4. Execute no terminal: `Invoke-WebRequest -Uri "http://localhost:8000/api/glossary"`

---
**Data:** 2025-12-19
**Última atualização:** Correções no app.js, index.html, logging aprimorado
