// frontend/app.js
const API = 'http://localhost:8000/api'

// Helpers
function qs(id) { return document.getElementById(id) }
function formatCurrency(value) { 
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value) 
}

// Load educational content on page load
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀🚀🚀 DOMContentLoaded INICIADO 🚀🚀🚀');
    
    // Adicionar event listeners para formulários
    const formReality = qs('formReality');
    if (formReality) {
        formReality.addEventListener('submit', handleRealitySubmit);
        console.log('✅ formReality event listener adicionado');
    }
    
    const formFuture = qs('formFuture');
    if (formFuture) {
        formFuture.addEventListener('submit', handleFutureSubmit);
        console.log('✅ formFuture event listener adicionado');
    }
    
    const goalForm = qs('goalForm');
    if (goalForm) {
        goalForm.addEventListener('submit', handleGoalSubmit);
        console.log('✅ goalForm event listener adicionado');
    }
    
    console.log('📚 Iniciando carregamento de conteúdo educacional...');
    console.log('API URL:', API);
    
    // Carregar conteúdo educacional
    loadGlossary();
    loadTips();
    loadProfessions();
    
    console.log('🚀🚀🚀 DOMContentLoaded COMPLETO 🚀🚀🚀');
});

// Submit reality
async function handleRealitySubmit(e) {
    e.preventDefault();
    const payload = {
        nome: qs('r_nome').value,
        idade: Number(qs('r_idade').value),
        renda_atual: Number(qs('r_renda').value),
        renda_futura_possivel: Number(qs('r_renda_futura').value) || 0,
        profissao_interesse: qs('r_profissao').value || ""
    }
    
    try {
        const res = await fetch(API + '/submit_reality', {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' }, 
            body: JSON.stringify(payload)
        });
        const j = await res.json();
        qs('realityResult').innerHTML = `
            <div class="success-message">
                ✅ ${j.message}
                <p>Agora preencha o formulário "Futuro Profissional" para ver suas projeções!</p>
            </div>
        `;
    } catch (error) {
        qs('realityResult').innerHTML = `<div class="error-message">❌ Erro ao enviar: ${error.message}</div>`;
    }
}

// Submit future and show projections
async function handleFutureSubmit(e) {
    e.preventDefault();
    const payload = {
        nome: qs('f_nome').value,
        idade: Number(qs('f_idade').value),
        profissao_dos_sonhos: qs('f_profissao').value,
        faixa_salarial: Number(qs('f_faixa').value),
        poupanca_mensal: Number(qs('f_poupanca').value),
        investimento_tipo: qs('f_tipo').value,
        tempo_anos: Number(qs('f_tempo').value)
    }
    
    try {
        const res = await fetch(API + '/submit_future', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const j = await res.json();
        
        if (j.status === 'ok') {
            displayProjections(j.projections, payload);
            // Also get Monte Carlo simulation for arriscado
            await displayMonteCarloSimulation(payload);
        }
    } catch (error) {
        qs('futureResult').innerHTML = `<div class="error-message">❌ Erro ao calcular: ${error.message}</div>`;
    }
}

function displayProjections(projections, payload) {
    const resultDiv = qs('futureResult');
    
    let html = `
        <div class="projections-container">
            <h3>📊 Suas Projeções de Investimento</h3>
            <p><strong>Poupando ${formatCurrency(payload.poupanca_mensal)} por mês durante ${payload.tempo_anos} anos:</strong></p>
            
            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>Tipo de Investimento</th>
                            <th>Valor Final</th>
                            <th>Rendimento</th>
                            <th>Total Investido</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    
    const totalInvestido = payload.poupanca_mensal * payload.tempo_anos * 12;
    const tipos = {
        'conservador': '🛡️ Conservador (Poupança/CDI)',
        'moderado': '⚖️ Moderado (Fundos)',
        'arriscado': '🚀 Arriscado (Ações)'
    };
    
    Object.keys(projections).forEach(tipo => {
        const proj = projections[tipo];
        const valorFinal = proj.final;
        const rendimento = valorFinal - totalInvestido;
        
        html += `
            <tr>
                <td>${tipos[tipo]}</td>
                <td class="highlight">${formatCurrency(valorFinal)}</td>
                <td class="gain">${formatCurrency(rendimento)}</td>
                <td>${formatCurrency(totalInvestido)}</td>
            </tr>
        `;
    });
    
    html += `
                    </tbody>
                </table>
            </div>
            
            <div class="insights">
                <h4>💡 O que isso significa?</h4>
                <ul>
                    <li><strong>Conservador:</strong> Menor risco, menor retorno. Ideal para reserva de emergência.</li>
                    <li><strong>Moderado:</strong> Equilibrio entre risco e retorno. Boa opção para metas de médio prazo.</li>
                    <li><strong>Arriscado:</strong> Maior risco, maior potencial de retorno. Para objetivos de longo prazo.</li>
                </ul>
                <p class="tip">🎯 <strong>Dica:</strong> Uma boa estratégia é diversificar, colocando parte do dinheiro em cada tipo!</p>
            </div>
            
            <div class="chart-container">
                <canvas id="projectionsChart" width="400" height="200"></canvas>
            </div>
        </div>
    `;
    
    resultDiv.innerHTML = html;
    
    // Draw simple chart
    drawProjectionsChart(projections);
}

async function displayMonteCarloSimulation(payload) {
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
            
            resultDiv.innerHTML += `
                <div class="monte-carlo-section">
                    <h4>🎲 Simulação de Risco (Investimento Arriscado)</h4>
                    <p>Baseado em 1.000 simulações diferentes:</p>
                    <div class="risk-scenarios">
                        <div class="scenario pessimistic">
                            <span class="label">Cenário Pessimista (10% das vezes)</span>
                            <span class="value">${formatCurrency(mc.p10)}</span>
                        </div>
                        <div class="scenario median">
                            <span class="label">Cenário Provável (50% das vezes)</span>
                            <span class="value">${formatCurrency(mc.p50)}</span>
                        </div>
                        <div class="scenario optimistic">
                            <span class="label">Cenário Otimista (90% das vezes)</span>
                            <span class="value">${formatCurrency(mc.p90)}</span>
                        </div>
                    </div>
                    <p class="warning">⚠️ Lembre-se: investimentos arriscados podem tanto ganhar muito quanto perder!</p>
                </div>
            `;
        }
    } catch (error) {
        console.log('Erro na simulação Monte Carlo:', error);
    }
}

function drawProjectionsChart(projections) {
    const canvas = qs('projectionsChart');
    if (!canvas) {
        console.log('Canvas não encontrado');
        return;
    }
    
    const ctx = canvas.getContext('2d');
    
    // Redimensionar canvas para tela de toque
    canvas.width = canvas.offsetWidth;
    canvas.height = 300;
    
    // Simple bar chart
    const types = Object.keys(projections);
    const values = types.map(type => projections[type].final);
    const maxValue = Math.max(...values);
    
    const barWidth = (canvas.width / types.length) - 30;
    const colors = ['#65a30d', '#84cc16', '#1e3a8a'];
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    types.forEach((type, i) => {
        const value = values[i];
        const height = (value / maxValue) * (canvas.height - 80);
        const x = i * (barWidth + 30) + 20;
        const y = canvas.height - height - 40;
        
        // Desenhar barra
        ctx.fillStyle = colors[i];
        ctx.fillRect(x, y, barWidth, height);
        
        // Desenhar borda
        ctx.strokeStyle = '#1f2937';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, barWidth, height);
        
        // Labels - tipo
        ctx.fillStyle = '#1f2937';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(type.charAt(0).toUpperCase() + type.slice(1), x + barWidth / 2, canvas.height - 10);
        
        // Values - valor em reais
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 13px Arial';
        ctx.fillText(formatCurrency(value).substring(0, 12), x + barWidth / 2, y + height / 2 + 5);
    });
    
    // Título
    ctx.fillStyle = '#1f2937';
    ctx.font = 'bold 18px Arial';
    ctx.textAlign = 'left';
    ctx.fillText('Projeção de Investimentos', 20, 30);
}

// Goal Calculator
async function handleGoalSubmit(e) {
    e.preventDefault();
    const payload = {
        goal_amount: Number(qs('goal_amount').value),
        monthly_saving: Number(qs('monthly_saving').value),
        annual_rate: Number(qs('annual_rate').value) / 100 || 0.05
    };
    
    try {
        const res = await fetch(API + '/calculate_goal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const j = await res.json();
        
        qs('goalResult').innerHTML = `
            <div class="goal-result">
                <h4>🎯 Para atingir sua meta de ${formatCurrency(payload.goal_amount)}:</h4>
                <div class="goal-stats">
                    <div class="stat">
                        <span class="label">⏱️ Tempo necessário:</span>
                        <span class="value">${j.years_needed} anos (${j.months_needed} meses)</span>
                    </div>
                    <div class="stat">
                        <span class="label">💰 Total que você vai investir:</span>
                        <span class="value">${formatCurrency(j.total_invested)}</span>
                    </div>
                    <div class="stat">
                        <span class="label">📈 Dinheiro que os juros vão gerar:</span>
                        <span class="value gain">${formatCurrency(j.interest_earned)}</span>
                    </div>
                </div>
                <p class="motivation">✨ Os juros compostos vão trabalhar para você! Começar cedo faz toda a diferença.</p>
            </div>
        `;
    } catch (error) {
        qs('goalResult').innerHTML = `<div class="error-message">❌ Erro: ${error.message}</div>`;
    }
}

// Load educational content
async function loadGlossary() {
    console.log('▶️ loadGlossary() iniciada');
    try {
        console.log('📚 Fetching glossário...');
        const res = await fetch(API + '/glossary');
        console.log('📡 Response status:', res.status);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        
        const glossary = await res.json();
        console.log('✅ Glossário recebido:', glossary);
        
        let html = '<h3>📚 Glossário Financeiro</h3><div class="glossary-grid">';
        Object.keys(glossary).forEach(term => {
            html += `
                <div class="glossary-item">
                    <h4>${term}</h4>
                    <p>${glossary[term]}</p>
                </div>
            `;
        });
        html += '</div>';
        
        const glossaryContent = qs('glossaryContent');
        console.log('📍 Elemento glossaryContent encontrado?', !!glossaryContent);
        if (glossaryContent) {
            glossaryContent.innerHTML = html;
            console.log('✅ Glossário renderizado com sucesso');
        } else {
            console.error('❌ glossaryContent não encontrado!');
        }
    } catch (error) {
        console.error('❌ Erro em loadGlossary:', error);
        const elem = qs('glossaryContent');
        if (elem) elem.innerHTML = `<div style="color: red; padding: 20px;"><strong>ERRO:</strong> ${error.message}<br>Verifique o console (F12)</div>`;
    }
}

async function loadTips() {
    console.log('▶️ loadTips() iniciada');
    try {
        console.log('💡 Fetching dicas...');
        const res = await fetch(API + '/tips');
        console.log('📡 Response status:', res.status);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        
        const data = await res.json();
        console.log('✅ Dicas recebidas:', data);
        
        let html = '<h3>💡 Dicas Financeiras Práticas</h3><ul class="tips-list">';
        data.tips.forEach(tip => {
            html += `<li>${tip}</li>`;
        });
        html += '</ul>';
        
        const tipsContent = qs('tipsContent');
        console.log('📍 Elemento tipsContent encontrado?', !!tipsContent);
        if (tipsContent) {
            tipsContent.innerHTML = html;
            console.log('✅ Dicas renderizadas com sucesso');
        } else {
            console.error('❌ tipsContent não encontrado!');
        }
    } catch (error) {
        console.error('❌ Erro em loadTips:', error);
        const elem = qs('tipsContent');
        if (elem) elem.innerHTML = `<div style="color: red; padding: 20px;"><strong>ERRO:</strong> ${error.message}</div>`;
    }
}

async function loadProfessions() {
    console.log('▶️ loadProfessions() iniciada');
    try {
        console.log('💼 Fetching profissões...');
        const res = await fetch(API + '/professions');
        console.log('📡 Response status:', res.status);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        
        const professions = await res.json();
        console.log('✅ Profissões recebidas:', professions);
        
        let html = '<h3>💼 Guia de Profissões e Salários</h3><div class="professions-grid">';
        Object.keys(professions).forEach(profession => {
            const info = professions[profession];
            html += `
                <div class="profession-item">
                    <h4>${profession}</h4>
                    <p><strong>💰 Faixa salarial:</strong> R$ ${info.salary_range}</p>
                    <p><strong>🎓 Formação:</strong> ${info.education}</p>
                </div>
            `;
        });
        html += '</div>';
        
        const professionsContent = qs('professionsContent');
        console.log('📍 Elemento professionsContent encontrado?', !!professionsContent);
        if (professionsContent) {
            professionsContent.innerHTML = html;
            console.log('✅ Profissões renderizadas com sucesso');
        } else {
            console.error('❌ professionsContent não encontrado!');
        }
    } catch (error) {
        console.error('❌ Erro em loadProfessions:', error);
        const elem = qs('professionsContent');
        if (elem) elem.innerHTML = `<div style="color: red; padding: 20px;"><strong>ERRO:</strong> ${error.message}</div>`;
    }
}