// frontend/app.js
/**
 * 🌐 JAVASCRIPT INTERATIVO DA PLATAFORMA FINANCEIRA ⚡
 * 
 * Este arquivo é o "cérebro" do frontend! Ele conecta a interface bonita
 * que o usuário vê com os cálculos poderosos que acontecem no backend.
 * 
 * 🎯 PRINCIPAIS FUNÇÕES:
 * - Captura dados dos formulários 📝
 * - Envia dados para a API Python 🐍  
 * - Recebe resultados dos cálculos 🧮
 * - Mostra resultados de forma visual 📊
 * - Cria gráficos simples 📈
 * - Carrega conteúdo educativo 📚
 * 
 * 💡 TECNOLOGIAS USADAS:
 * - Fetch API: Para comunicar com o backend
 * - DOM Manipulation: Para atualizar a página
 * - Canvas API: Para desenhar gráficos simples
 * - Event Listeners: Para reagir aos cliques do usuário
 */

// 🌐 CONFIGURAÇÃO DA API
// Esta é a "ponte" entre o frontend e backend
const API = 'http://localhost:8000/api'  // Endereço onde o servidor Python está rodando

// 🛠️ FUNÇÕES AUXILIARES (pequenas funções que ajudam em tarefas repetitivas)

/**
 * 🔍 Função para encontrar elementos HTML mais facilmente
 * Em vez de escrever "document.getElementById" toda hora, usamos "qs"
 */
function qs(id) { 
    return document.getElementById(id) 
}

/**
 * 💰 Função para formatar números como dinheiro brasileiro
 * Transforma "1500.50" em "R$ 1.500,50"
 */
function formatCurrency(value) { 
    return new Intl.NumberFormat('pt-BR', { 
        style: 'currency', 
        currency: 'BRL' 
    }).format(value) 
}

// 🚀 INICIALIZAÇÃO DA PÁGINA
// Quando a página carrega, executa estas funções automaticamente
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🎉 Plataforma carregada! Iniciando sistemas...');
    
    // Carrega conteúdo educativo em paralelo (ao mesmo tempo)
    await Promise.all([
        loadGlossary(),    // 📚 Carrega glossário de termos financeiros
        loadTips(),        // 💡 Carrega dicas práticas
        loadProfessions()  // 💼 Carrega informações sobre profissões
    ]);
    
    console.log('✅ Todos os sistemas carregados com sucesso!');
});

// 📋 FORMULÁRIO "REALIDADE ATUAL"
// Captura dados sobre a situação atual do estudante
qs('formReality').addEventListener('submit', async (e) => {
    e.preventDefault(); // ⛔ Impede o formulário de recarregar a página
    
    console.log('📝 Enviando dados da realidade atual...');
    
    // 📦 Organiza os dados do formulário em um objeto
    const payload = {
        nome: qs('r_nome').value,                                    // Nome do estudante
        idade: Number(qs('r_idade').value),                         // Idade (convertida para número)
        renda_atual: Number(qs('r_renda').value),                   // Renda atual em R$
        renda_futura_possivel: Number(qs('r_renda_futura').value) || 0, // Renda futura (0 se vazio)
        profissao_interesse: qs('r_profissao').value || ""          // Profissão de interesse (vazio se não preenchido)
    }
    
    console.log('📊 Dados capturados:', payload);
    
    try {
        // 🚀 Envia dados para o servidor Python
        const res = await fetch(API + '/submit_reality', {
            method: 'POST',                                    // Tipo de requisição
            headers: { 'Content-Type': 'application/json' },  // Formato dos dados
            body: JSON.stringify(payload)                      // Converte objeto para texto JSON
        });
        
        const j = await res.json(); // 📥 Recebe resposta do servidor
        
        // ✅ Mostra mensagem de sucesso na tela
        qs('realityResult').innerHTML = `
            <div class="success-message">
                ✅ ${j.message}
                <p><strong>🎯 Próximo passo:</strong> Agora preencha o formulário "Futuro Profissional" para ver suas projeções!</p>
                <p>💡 <strong>Dica:</strong> Quanto mais realista você for, melhores serão suas simulações!</p>
            </div>
        `;
        
        console.log('✅ Realidade atual salva com sucesso!');
        
    } catch (error) {
        // ❌ Se algo der errado, mostra erro amigável
        console.error('❌ Erro ao enviar realidade:', error);
        qs('realityResult').innerHTML = `
            <div class="error-message">
                ❌ Ops! Algo deu errado: ${error.message}
                <p>💡 Verifique sua conexão e tente novamente!</p>
            </div>
        `;
    }
});

// 🔮 FORMULÁRIO "FUTURO PROFISSIONAL"  
// Aqui acontece a mágica! Calculamos projeções de investimento
qs('formFuture').addEventListener('submit', async (e) => {
    e.preventDefault(); // ⛔ Impede recarregamento da página
    
    console.log('🔮 Calculando projeções do futuro...');
    
    // 📦 Captura todos os dados do formulário
    const payload = {
        nome: qs('f_nome').value,
        idade: Number(qs('f_idade').value),
        profissao_dos_sonhos: qs('f_profissao').value,
        faixa_salarial: Number(qs('f_faixa').value),
        poupanca_mensal: Number(qs('f_poupanca').value),
        investimento_tipo: qs('f_tipo').value,
        tempo_anos: Number(qs('f_tempo').value)
    }
    
    console.log('📊 Dados do futuro capturados:', payload);
    
    // 🛡️ Validação básica dos dados
    if (payload.poupanca_mensal <= 0) {
        qs('futureResult').innerHTML = `
            <div class="error-message">
                ❌ O valor poupado por mês deve ser maior que R$ 0!
                <p>💡 Mesmo R$ 10 por mês já faz diferença!</p>
            </div>
        `;
        return;
    }
    
    if (payload.tempo_anos <= 0) {
        qs('futureResult').innerHTML = `
            <div class="error-message">
                ❌ O tempo deve ser maior que 0 anos!
                <p>💡 Tente pelo menos 1 ano para ver resultados interessantes!</p>
            </div>
        `;
        return;
    }
    
    try {
        // 🚀 Envia dados para cálculo no servidor
        console.log('🧮 Enviando para cálculo...');
        
        const res = await fetch(API + '/submit_future', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const j = await res.json();
        
        if (j.status === 'ok') {
            console.log('📊 Projeções recebidas:', j.projections);
            
            // 🎨 Mostra resultados na tela de forma bonita
            displayProjections(j.projections, payload);
            
            // 🎲 Busca simulação Monte Carlo para investimentos arriscados
            if (payload.investimento_tipo === 'arriscado') {
                await displayMonteCarloSimulation(payload);
            }
        }
        
    } catch (error) {
        console.error('❌ Erro ao calcular projeções:', error);
        qs('futureResult').innerHTML = `
            <div class="error-message">
                ❌ Erro ao calcular: ${error.message}
                <p>💡 Verifique os dados e tente novamente!</p>
            </div>
        `;
    }
});

/**
 * 📊 FUNÇÃO PARA MOSTRAR PROJEÇÕES DE INVESTIMENTO
 * 
 * Esta função pega os cálculos do backend e transforma em uma 
 * apresentação visual bonita e fácil de entender.
 */
function displayProjections(projections, payload) {
    const resultDiv = qs('futureResult');
    
    console.log('🎨 Criando visualização das projeções...');
    
    // 🧮 Cálculo do total investido (para comparar com o rendimento)
    const totalInvestido = payload.poupanca_mensal * payload.tempo_anos * 12;
    
    // 📋 Nomes amigáveis para os tipos de investimento
    const tipos = {
        'conservador': '🛡️ Conservador (Poupança/CDI)',
        'moderado': '⚖️ Moderado (Fundos)',
        'arriscado': '🚀 Arriscado (Ações)'
    };
    
    // 🎨 Cria HTML bonito para mostrar os resultados
    let html = `
        <div class="projections-container">
            <h3>📊 Suas Projeções de Investimento</h3>
            <div class="highlight-box">
                <p><strong>💰 Investindo ${formatCurrency(payload.poupanca_mensal)} por mês durante ${payload.tempo_anos} anos</strong></p>
                <p>👨‍🎓 Profissão desejada: <strong>${payload.profissao_dos_sonhos}</strong></p>
                <p>💼 Salário esperado: <strong>${formatCurrency(payload.faixa_salarial)}/mês</strong></p>
            </div>
            
            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>🎯 Tipo de Investimento</th>
                            <th>💰 Valor Final</th>
                            <th>📈 Rendimento dos Juros</th>
                            <th>💸 Total Investido</th>
                            <th>🚀 Multiplicador</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    
    // 📊 Para cada tipo de investimento, cria uma linha na tabela
    Object.keys(projections).forEach(tipo => {
        const proj = projections[tipo];
        const valorFinal = proj.final;
        const rendimento = valorFinal - totalInvestido;
        const multiplicador = (valorFinal / totalInvestido).toFixed(2);
        
        // 🎨 Cor diferente dependendo do tipo de investimento
        let rowClass = '';
        if (tipo === 'conservador') rowClass = 'conservador-row';
        if (tipo === 'moderado') rowClass = 'moderado-row';  
        if (tipo === 'arriscado') rowClass = 'arriscado-row';
        
        html += `
            <tr class="${rowClass}">
                <td><strong>${tipos[tipo]}</strong></td>
                <td class="highlight">${formatCurrency(valorFinal)}</td>
                <td class="gain">${formatCurrency(rendimento)}</td>
                <td>${formatCurrency(totalInvestido)}</td>
                <td class="multiplier">${multiplicador}x</td>
            </tr>
        `;
    });
    
    html += `
                    </tbody>
                </table>
            </div>
            
            <div class="insights">
                <h4>💡 O que isso significa na prática?</h4>
                <div class="insights-grid">
                    <div class="insight-item">
                        <span class="insight-icon">🛡️</span>
                        <div>
                            <strong>Conservador:</strong> Menor risco, menor retorno. 
                            <br>💡 <em>Ideal para reserva de emergência!</em>
                        </div>
                    </div>
                    <div class="insight-item">
                        <span class="insight-icon">⚖️</span>
                        <div>
                            <strong>Moderado:</strong> Equilibrio entre risco e retorno. 
                            <br>💡 <em>Boa opção para metas de médio prazo!</em>
                        </div>
                    </div>
                    <div class="insight-item">
                        <span class="insight-icon">🚀</span>
                        <div>
                            <strong>Arriscado:</strong> Maior risco, maior potencial. 
                            <br>💡 <em>Para objetivos de longo prazo!</em>
                        </div>
                    </div>
                </div>
                
                <div class="tip">
                    🎯 <strong>Estratégia Inteligente:</strong> Uma boa ideia é diversificar! 
                    Coloque parte do dinheiro em cada tipo de investimento para equilibrar 
                    segurança e potencial de crescimento.
                </div>
            </div>
            
            <div class="chart-container">
                <h4>📈 Gráfico Visual das Projeções</h4>
                <canvas id="projectionsChart" width="500" height="300"></canvas>
            </div>
        </div>
    `;
    
    resultDiv.innerHTML = html;
    
    // 🎨 Desenha o gráfico de barras
    setTimeout(() => drawProjectionsChart(projections), 100);
    
    console.log('✅ Projeções exibidas com sucesso!');
}

/**
 * 🎲 SIMULAÇÃO MONTE CARLO PARA INVESTIMENTOS ARRISCADOS
 * 
 * Mostra diferentes cenários possíveis quando se investe em ações.
 * Ensina que investimentos arriscados podem dar resultados muito variados!
 */
async function displayMonteCarloSimulation(payload) {
    console.log('🎲 Buscando simulação Monte Carlo...');
    
    try {
        const res = await fetch(API + '/simulate_montecarlo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const j = await res.json();
        
        if (j.status === 'ok') {
            const mc = j.montecarlo;
            const resultDiv = qs('futureResult');
            
            console.log('📊 Dados Monte Carlo recebidos:', mc);
            
            // 🎨 Adiciona seção de simulação de risco
            resultDiv.innerHTML += `
                <div class="monte-carlo-section">
                    <h4>🎲 Simulação de Risco (Investimento em Ações)</h4>
                    <p>📊 Baseado em <strong>1.000 simulações</strong> diferentes do mercado de ações:</p>
                    
                    <div class="risk-scenarios">
                        <div class="scenario pessimistic">
                            <div class="scenario-icon">😰</div>
                            <span class="label">Cenário Ruim<br>(10% das vezes)</span>
                            <span class="value">${formatCurrency(mc.p10)}</span>
                            <small>Quando o mercado vai mal</small>
                        </div>
                        <div class="scenario median">
                            <div class="scenario-icon">😊</div>
                            <span class="label">Cenário Normal<br>(50% das vezes)</span>
                            <span class="value">${formatCurrency(mc.p50)}</span>
                            <small>O que mais acontece</small>
                        </div>
                        <div class="scenario optimistic">
                            <div class="scenario-icon">🤩</div>
                            <span class="label">Cenário Ótimo<br>(10% das vezes)</span>
                            <span class="value">${formatCurrency(mc.p90)}</span>
                            <small>Quando o mercado dispara!</small>
                        </div>
                    </div>
                    
                    <div class="warning">
                        ⚠️ <strong>Lição importante:</strong> Investimentos em ações podem tanto 
                        <span class="gain">ganhar muito</span> quanto <span class="loss">perder dinheiro</span>! 
                        Por isso é importante:
                        <ul>
                            <li>🕰️ Investir por <strong>longo prazo</strong> (mais de 5 anos)</li>
                            <li>🎯 <strong>Diversificar</strong> (não colocar tudo em ações)</li>
                            <li>📚 <strong>Estudar</strong> antes de investir</li>
                            <li>😌 Manter a <strong>calma</strong> nas oscilações</li>
                        </ul>
                    </div>
                </div>
            `;
            
            console.log('✅ Simulação Monte Carlo exibida!');
        }
        
    } catch (error) {
        console.error('❌ Erro na simulação Monte Carlo:', error);
        // Se der erro, não quebra a página, só não mostra a simulação
    }
}

/**
 * 📈 FUNÇÃO PARA DESENHAR GRÁFICO DE BARRAS
 * 
 * Usa Canvas API para criar um gráfico visual simples das projeções.
 * Ajuda os estudantes a visualizarem as diferenças entre os investimentos.
 */
function drawProjectionsChart(projections) {
    const canvas = qs('projectionsChart');
    if (!canvas) {
        console.log('⚠️ Canvas não encontrado, pulando gráfico');
        return;
    }
    
    const ctx = canvas.getContext('2d');
    
    console.log('🎨 Desenhando gráfico de projeções...');
    
    // 📊 Prepara os dados para o gráfico
    const types = Object.keys(projections);
    const values = types.map(type => projections[type].final);
    const maxValue = Math.max(...values);
    
    // 🎨 Configurações visuais
    const barWidth = (canvas.width - 100) / types.length - 20;
    const colors = ['#10b981', '#f59e0b', '#ef4444']; // Verde, Amarelo, Vermelho
    const maxHeight = canvas.height - 80;
    
    // 🧹 Limpa o canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 🎨 Desenha cada barra
    types.forEach((type, i) => {
        const value = values[i];
        const height = (value / maxValue) * maxHeight;
        const x = 50 + i * (barWidth + 20);
        const y = canvas.height - height - 40;
        
        // 🎨 Desenha a barra
        ctx.fillStyle = colors[i];
        ctx.fillRect(x, y, barWidth, height);
        
        // 🏷️ Rótulo do tipo de investimento
        ctx.fillStyle = '#374151';
        ctx.font = 'bold 12px Inter';
        ctx.textAlign = 'center';
        ctx.fillText(type.toUpperCase(), x + barWidth / 2, canvas.height - 20);
        
        // 💰 Valor em cima da barra  
        ctx.fillStyle = '#1f2937';
        ctx.font = 'bold 11px Inter';
        ctx.fillText(formatCurrency(value), x + barWidth / 2, y - 5);
    });
    
    // 📊 Título do gráfico
    ctx.fillStyle = '#1f2937';
    ctx.font = 'bold 14px Inter';
    ctx.textAlign = 'center';
    ctx.fillText('Comparação dos Investimentos', canvas.width / 2, 20);
    
    console.log('✅ Gráfico desenhado com sucesso!');
}

// 🎯 CALCULADORA DE METAS FINANCEIRAS
qs('goalForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    console.log('🎯 Calculando meta financeira...');
    
    // 📦 Captura dados da meta
    const payload = {
        goal_amount: Number(qs('goal_amount').value),
        monthly_saving: Number(qs('monthly_saving').value),
        annual_rate: Number(qs('annual_rate').value) / 100 || 0.05 // Converte % para decimal
    };
    
    console.log('📊 Dados da meta:', payload);
    
    // 🛡️ Validações básicas
    if (payload.goal_amount <= 0) {
        qs('goalResult').innerHTML = `
            <div class="error-message">
                ❌ O valor da meta deve ser maior que R$ 0!
            </div>
        `;
        return;
    }
    
    if (payload.monthly_saving <= 0) {
        qs('goalResult').innerHTML = `
            <div class="error-message">
                ❌ O valor mensal deve ser maior que R$ 0!
            </div>
        `;
        return;
    }
    
    try {
        // 🚀 Envia para cálculo no backend
        const res = await fetch(API + '/calculate_goal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const j = await res.json();
        
        console.log('📊 Resultado da meta:', j);
        
        // 🎨 Mostra resultado de forma motivadora
        qs('goalResult').innerHTML = `
            <div class="goal-result">
                <h4>🎯 Para atingir sua meta de ${formatCurrency(payload.goal_amount)}:</h4>
                
                <div class="goal-stats">
                    <div class="stat">
                        <span class="stat-icon">⏱️</span>
                        <div class="stat-content">
                            <span class="label">Tempo necessário:</span>
                            <span class="value">${j.years_needed} anos e ${j.months_needed % 12} meses</span>
                        </div>
                    </div>
                    
                    <div class="stat">
                        <span class="stat-icon">💰</span>
                        <div class="stat-content">
                            <span class="label">Total que você vai investir:</span>
                            <span class="value">${formatCurrency(j.total_invested)}</span>
                        </div>
                    </div>
                    
                    <div class="stat">
                        <span class="stat-icon">📈</span>
                        <div class="stat-content">
                            <span class="label">Dinheiro que os juros vão gerar:</span>
                            <span class="value gain">${formatCurrency(j.interest_earned)}</span>
                        </div>
                    </div>
                </div>
                
                <div class="motivation">
                    ✨ <strong>Os juros compostos vão trabalhar para você!</strong> 
                    Começar cedo faz toda a diferença. Mesmo pequenas quantias, 
                    quando investidas consistentemente, se transformam em grandes valores!
                    
                    <div class="progress-visual">
                        <div class="progress-bar">
                            <div class="progress-invested" style="width: ${(j.total_invested/j.final_amount)*100}%"></div>
                            <div class="progress-interest" style="width: ${(j.interest_earned/j.final_amount)*100}%"></div>
                        </div>
                        <div class="progress-labels">
                            <span>💰 Seu dinheiro: ${((j.total_invested/j.final_amount)*100).toFixed(1)}%</span>
                            <span>📈 Juros: ${((j.interest_earned/j.final_amount)*100).toFixed(1)}%</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        console.log('✅ Meta calculada e exibida!');
        
    } catch (error) {
        console.error('❌ Erro ao calcular meta:', error);
        qs('goalResult').innerHTML = `
            <div class="error-message">
                ❌ Erro: ${error.message}
                <p>💡 Verifique os dados e tente novamente!</p>
            </div>
        `;
    }
});

// 📚 CARREGAMENTO DE CONTEÚDO EDUCATIVO

/**
 * 📖 Carrega glossário de termos financeiros
 */
async function loadGlossary() {
    console.log('📚 Carregando glossário...');
    
    try {
        const res = await fetch(API + '/glossary');
        const glossary = await res.json();
        
        let html = '<h3>📚 Glossário Financeiro</h3><div class="glossary-grid">';
        
        Object.keys(glossary).forEach(term => {
            html += `
                <div class="glossary-item">
                    <h4>📖 ${term}</h4>
                    <p>${glossary[term]}</p>
                </div>
            `;
        });
        
        html += '</div>';
        qs('glossaryContent').innerHTML = html;
        
        console.log('✅ Glossário carregado!');
        
    } catch (error) {
        console.error('❌ Erro ao carregar glossário:', error);
        qs('glossaryContent').innerHTML = '<p>❌ Erro ao carregar glossário</p>';
    }
}

/**
 * 💡 Carrega dicas práticas de educação financeira
 */
async function loadTips() {
    console.log('💡 Carregando dicas...');
    
    try {
        const res = await fetch(API + '/tips');
        const data = await res.json();
        
        let html = '<h3>💡 Dicas Financeiras Para o Dia a Dia</h3><ul class="tips-list">';
        
        data.tips.forEach((tip, index) => {
            html += `<li class="tip-item">
                <span class="tip-number">${index + 1}</span>
                ${tip}
            </li>`;
        });
        
        html += '</ul>';
        qs('tipsContent').innerHTML = html;
        
        console.log('✅ Dicas carregadas!');
        
    } catch (error) {
        console.error('❌ Erro ao carregar dicas:', error);
        qs('tipsContent').innerHTML = '<p>❌ Erro ao carregar dicas</p>';
    }
}

/**
 * 💼 Carrega informações sobre profissões e salários
 */
async function loadProfessions() {
    console.log('💼 Carregando profissões...');
    
    try {
        const res = await fetch(API + '/professions');
        const professions = await res.json();
        
        let html = '<h3>💼 Profissões e Perspectivas Salariais</h3><div class="professions-grid">';
        
        Object.keys(professions).forEach(profession => {
            const info = professions[profession];
            html += `
                <div class="profession-item">
                    <h4>💼 ${profession}</h4>
                    <div class="profession-info">
                        <p><strong>💰 Faixa salarial:</strong> R$ ${info.salary_range}</p>
                        <p><strong>🎓 Formação necessária:</strong> ${info.education}</p>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        qs('professionsContent').innerHTML = html;
        
        console.log('✅ Profissões carregadas!');
        
    } catch (error) {
        console.error('❌ Erro ao carregar profissões:', error);
        qs('professionsContent').innerHTML = '<p>❌ Erro ao carregar informações de profissões</p>';
    }
}

// 🎯 FUNCIONALIDADES AUXILIARES PARA A INTERFACE

/**
 * 🎯 Define uma meta pré-definida (chamada pelos botões de exemplo)
 */
function setGoal(amount, description) {
    console.log(`🎯 Meta selecionada: ${description} - R$ ${amount}`);
    
    qs('goal_amount').value = amount;
    
    // 🎨 Feedback visual temporário
    const input = qs('goal_amount');
    input.style.backgroundColor = '#e8f5e8';
    input.style.transform = 'scale(1.02)';
    
    setTimeout(() => {
        input.style.backgroundColor = '';
        input.style.transform = '';
    }, 1000);
    
    // 💡 Dica baseada no valor da meta
    let tip = '';
    if (amount <= 5000) {
        tip = '💡 Meta de curto prazo! Com disciplina, você consegue rápido!';
    } else if (amount <= 20000) {
        tip = '💡 Meta de médio prazo! Planeje bem e seja consistente!';
    } else {
        tip = '💡 Meta de longo prazo! Comece cedo e use o poder dos juros compostos!';
    }
    
    // Mostra a dica temporariamente
    const tipDiv = document.createElement('div');
    tipDiv.className = 'goal-tip';
    tipDiv.innerHTML = tip;
    tipDiv.style.marginTop = '10px';
    tipDiv.style.padding = '10px';
    tipDiv.style.background = '#f0f9ff';
    tipDiv.style.borderRadius = '8px';
    tipDiv.style.border = '1px solid #bae6fd';
    
    const container = qs('goal_amount').parentNode;
    container.appendChild(tipDiv);
    
    // Remove a dica após 3 segundos
    setTimeout(() => {
        if (tipDiv.parentNode) {
            tipDiv.parentNode.removeChild(tipDiv);
        }
    }, 3000);
}

/**
 * 📊 Atualiza display da taxa de juros no range slider
 */
function updateRateDisplay() {
    const rate = qs('annual_rate').value;
    const display = qs('rateDisplay');
    
    display.textContent = rate + '%';
    
    // 🎨 Muda cor baseado na taxa
    if (rate < 3) {
        display.style.color = '#ef4444'; // Vermelho para taxas baixas
    } else if (rate < 7) {
        display.style.color = '#f59e0b'; // Amarelo para taxas médias  
    } else {
        display.style.color = '#10b981'; // Verde para taxas altas
    }
}

// 🚀 SISTEMA DE ABAS DA INTERFACE

/**
 * 🔄 Alterna entre as diferentes abas da plataforma
 */
function showTab(tabName) {
    console.log(`🔄 Alternando para aba: ${tabName}`);
    
    // 👁️ Esconde todas as abas
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 🎨 Remove classe ativa de todos os botões
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // ✅ Mostra a aba selecionada
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // 🎨 Marca o botão como ativo
    event.target.classList.add('active');
    
    console.log(`✅ Aba ${tabName} ativada!`);
}

// 🎉 MENSAGEM DE BOAS-VINDAS NO CONSOLE
console.log(`
🎓💰 PLATAFORMA DE EDUCAÇÃO FINANCEIRA 💰🎓

Bem-vindo ao sistema que vai transformar sua relação com o dinheiro!

🎯 O que você pode fazer aqui:
✅ Simular investimentos com diferentes perfis
✅ Calcular metas financeiras realistas  
✅ Aprender termos financeiros importantes
✅ Descobrir profissões e salários
✅ Entender o poder dos juros compostos

💡 Lembre-se: Educação financeira é o primeiro passo para a independência!

🚀 Comece preenchendo o formulário "Realidade Atual"!
`);

// 🔧 CONFIGURAÇÕES DE DEBUG (apenas para desenvolvimento)
if (window.location.hostname === 'localhost') {
    console.log('🔧 Modo de desenvolvimento ativado');
    
    // Expõe funções úteis no console para debug
    window.debugFinanceiro = {
        setGoal: setGoal,
        formatCurrency: formatCurrency,
        showTab: showTab,
        API: API
    };
    
    console.log('🛠️ Funções de debug disponíveis em window.debugFinanceiro');
}