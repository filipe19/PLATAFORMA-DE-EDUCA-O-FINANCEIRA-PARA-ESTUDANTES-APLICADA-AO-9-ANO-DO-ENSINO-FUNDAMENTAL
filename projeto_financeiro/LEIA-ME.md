# 🚀 GUIA RÁPIDO - MEU FUTURO FINANCEIRO

## ⚡ INÍCIO RÁPIDO (3 passos)

### 1️⃣ Duplo clique em `INICIAR.bat`
   - Abrirá 2 janelas de comando
   - NÃO FECHE ESSAS JANELAS!

### 2️⃣ Aguarde o navegador abrir
   - Abre automaticamente em http://localhost:8080
   - Se não abrir, digite esse endereço manualmente

### 3️⃣ Use a plataforma!
   - Preencha o formulário
   - Clique "⚡ CALCULAR TUDO AGORA"
   - Veja seus resultados com gráfico

---

## 📊 O QUE MUDOU NESTA VERSÃO

### ✅ MELHORIAS
- **3 abas** ao invés de 4 (mais simples)
- **1 botão** ao invés de 2 (faz tudo de uma vez)
- Campos **nome e idade** mais fáceis de clicar
- Abas **carregam instantaneamente**
- **Calculadora de metas** integrada na mesma página

### 🧹 LIMPEZA
- Removidos 35+ arquivos de teste
- Mantidos apenas arquivos essenciais
- Projeto mais organizado e rápido

---

## 🎯 COMO USAR

### Aba 1: 🚀 PLANEJE SEU FUTURO

**Parte 1 - Simulação Completa**
1. Digite seu **nome** (campo fica roxo ao clicar)
2. Digite sua **idade**
3. Preencha **dados atuais** (renda, profissão)
4. Preencha **planos futuros** (profissão dos sonhos, salário)
5. Defina **investimento** (quanto poupar, tipo)
6. (Opcional) Adicione uma **meta**
7. Clique **⚡ CALCULAR TUDO AGORA**

**Resultado:**
- 📊 Gráfico com 3 projeções
- 💰 3 cards resumo
- 📈 Tabela completa de investimentos
- ⏰ Tempo para atingir sua meta

**Parte 2 - Calculadora de Metas** (mesma página, abaixo)
1. Clique em meta rápida OU digite valor
2. Informe quanto pode poupar por mês
3. Ajuste taxa de juros (arraste slider)
4. Clique **🚀 Calcular Minha Meta!**

**Resultado:**
- ⏰ Tempo necessário (anos e meses)
- 💰 Valor da meta
- 📈 Poupança mensal

### Aba 2: 📚 APRENDA
- **Glossário**: Termos financeiros explicados
- **Dicas**: 4 práticas essenciais de educação financeira
- **Carrega instantaneamente** ao clicar

### Aba 3: 💼 PROFISSÕES
- Lista de profissões com salários médios
- Médico, Engenheiro, Professor, Advogado, Designer, etc
- **Carrega instantaneamente** ao clicar

---

## ⚙️ ESTRUTURA DO SISTEMA

```
Você clica INICIAR.bat
         ↓
Abre Backend (porta 5000) - Salva dados
         ↓
Abre Frontend (porta 8080) - Interface
         ↓
Navegador abre automaticamente
         ↓
Tudo pronto para usar! ✅
```

---

## 📁 ARQUIVOS PRINCIPAIS

| Arquivo | Função |
|---------|--------|
| `INICIAR.bat` | Inicia tudo com 1 clique |
| `servidor.py` | Servidor frontend (porta 8080) |
| `backend/servidor_dados.py` | API backend (porta 5000) |
| `frontend/index.html` | Interface visual |
| `frontend/app_unificado_integrado.js` | Lógica completa |
| `frontend/styles.css` | Cores e design |

---

## 🆘 RESOLVENDO PROBLEMAS

### Problema: "Porta já em uso"
**Solução:** Feche outras instâncias rodando
```powershell
Get-Process python | Stop-Process
```

### Problema: "Gráfico não aparece"
**Solução:** Pressione F5 para recarregar página

### Problema: "Dados não salvam"
**Solução:** Verifique se backend está rodando na porta 5000

### Problema: "Campos difíceis de clicar"
**Solução:** Esta versão já corrigiu isso! Campos têm padding maior e bordas coloridas ao focar

---

## ✅ TESTES ANTES DE USAR COM ALUNOS

- [ ] INICIAR.bat abre 2 janelas
- [ ] Navegador abre automaticamente
- [ ] Campo nome recebe foco automático
- [ ] Campos ficam roxos ao clicar
- [ ] Botão "CALCULAR TUDO" funciona
- [ ] Gráfico aparece após calcular
- [ ] Calculadora de metas funciona
- [ ] Aba "Aprenda" abre rápido
- [ ] Aba "Profissões" abre rápido
- [ ] Dados salvam em CSV (backend/dados_*.csv)

---

## 📊 PARA O PROFESSOR

**Ver dados coletados:**
```
backend/dados_financeiros_DD-MM-YYYY.csv
```

**Ou clique no botão:**
```
📥 Baixar Dados
```

Abre no Excel para análise completa.

---

## 🎉 PRONTO!

Sistema otimizado e simplificado.  
**Basta clicar em INICIAR.bat e usar!**

---

*Versão otimizada - Fevereiro 2026*
