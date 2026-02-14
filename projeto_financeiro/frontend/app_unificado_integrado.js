// app_unificado_integrado.js - Lógica integrada mantendo as abas existentes

const API_BASE = 'http://localhost:5000';
let chartInstance = null;

// Elementos DOM
function el(id) { return document.getElementById(id) }

// ============================================
// EVENTO DO FORMULÁRIO
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    if (el('mainForm')) {
        el('mainForm').addEventListener('submit', procesarTodoAgora);
    }
    
    // Formulário de metas
    if (el('goalForm')) {
        el('goalForm').addEventListener('submit', calcularMeta);
    }
});

async function procesarTodoAgora(event) {
    event.preventDefault();
    
    console.log('⚡ Iniciando processamento completo...');
    
    // Mostrar loading
    el('loading').style.display = 'block';
    el('resultsSection').style.display = 'none';
    
    try {
        // 1️⃣ Coletar dados
        const dados = coletarDados();
        console.log('✅ Dados coletados:', dados);
        
        // 2️⃣ Fazer cálculos
        const resultados = calcularTudo(dados);
        console.log('✅ Cálculos feitos:', resultados);
        
        // 3️⃣ Salvar no servidor
        await salvarNoServidor(dados, resultados);
        console.log('✅ Dados salvos no servidor');
        
        // 4️⃣ Gerar gráfico
        gerarGrafico(resultados);
        console.log('✅ Gráfico gerado');
        
        // 5️⃣ Exibir resultados
        exibirResultados(dados, resultados);
        console.log('✅ Resultados exibidos');
        
        // Mostrar sucesso
        el('successMessage').style.display = 'block';
        setTimeout(() => el('successMessage').style.display = 'none', 3000);
        
    } catch (error) {
        console.error('❌ Erro:', error);
        alert('❌ Erro: ' + error.message);
    } finally {
        el('loading').style.display = 'none';
    }
}

// ============================================
// 1️⃣ COLETAR DADOS
// ============================================
function coletarDados() {
    return {
        tipo: 'Completo',
        nome: el('nome').value,
        idade_atual: Number(el('idade').value),
        renda_atual: Number(el('rentaAtual').value),
        profissao_atual: el('profissaoAtual').value || 'Não informada',
        idade_futura: Number(el('idadeFutura').value),
        profissao_futura: el('profissaoFutura').value,
        salario_futuro: Number(el('salarioFuturo').value),
        poupanca_mensal: Number(el('poupancaMensal').value),
        tipo_investimento: el('tipoInvestimento').value,
        meta_sonho: Number(el('metaSonho').value) || 0,
        notas: el('notas').value,
        timestamp: new Date().toLocaleString('pt-BR')
    };
}

// ============================================
// 2️⃣ CALCULAR TUDO
// ============================================
function calcularTudo(dados) {
    const anos = dados.idade_futura - dados.idade_atual;
    const meses = Math.max(1, anos * 12);
    const aporteTotal = dados.poupanca_mensal * meses;
    
    // Taxas de investimento
    const taxas = {
        conservador: 0.04,
        moderado: 0.07,
        arriscado: 0.10
    };
    
    const taxa = taxas[dados.tipo_investimento] || 0.07;
    
    // Calcular Valor Futuro
    const resultados = {};
    
    for (const [tipo, taxaAnual] of Object.entries(taxas)) {
        const taxaMensal = taxaAnual / 12;
        let vf;
        
        if (taxaMensal === 0) {
            vf = dados.poupanca_mensal * meses;
        } else {
            vf = dados.poupanca_mensal * (
                ((Math.pow(1 + taxaMensal, meses) - 1) / taxaMensal)
            );
        }
        
        resultados[tipo] = {
            valor_final: Math.round(vf),
            rendimento: Math.round(vf - aporteTotal),
            taxa_anual: (taxaAnual * 100).toFixed(1),
            label: tipo.charAt(0).toUpperCase() + tipo.slice(1)
        };
    }
    
    // Calcular tempo para meta
    let tempoParaMeta = '-';
    let tempoParaMetaDesc = '-';
    
    if (dados.meta_sonho > 0 && dados.poupanca_mensal > 0) {
        const taxaMensal = taxa / 12;
        if (taxaMensal === 0) {
            const mesesNecessarios = dados.meta_sonho / dados.poupanca_mensal;
            tempoParaMeta = `${Math.ceil(mesesNecessarios / 12)} anos`;
            tempoParaMetaDesc = `${Math.ceil(mesesNecessarios)} meses de poupança`;
        } else {
            const n = Math.log(
                (dados.meta_sonho * taxaMensal) / dados.poupanca_mensal + 1
            ) / Math.log(1 + taxaMensal);
            
            const mesesNecessarios = Math.ceil(n);
            const anosNecessarios = (mesesNecessarios / 12).toFixed(1);
            tempoParaMeta = `${anosNecessarios} anos`;
            tempoParaMetaDesc = `${mesesNecessarios} meses até conseguir R$ ${dados.meta_sonho.toLocaleString('pt-BR', {minimumFractionDigits: 0})}`;
        }
    }
    
    return {
        anos,
        meses,
        aporte_total: aporteTotal,
        projecoes: resultados,
        tempo_meta: tempoParaMeta,
        tempo_meta_desc: tempoParaMetaDesc,
        projecao_selecionada: resultados[dados.tipo_investimento]
    };
}

// ============================================
// 3️⃣ SALVAR NO SERVIDOR
// ============================================
async function salvarNoServidor(dados, resultados) {
    try {
        const payload = {
            ...dados,
            projecao_conservador: resultados.projecoes.conservador.valor_final,
            projecao_moderado: resultados.projecoes.moderado.valor_final,
            projecao_arriscado: resultados.projecoes.arriscado.valor_final
        };
        
        const response = await fetch(`${API_BASE}/salvar_dados`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error('Servidor não respondeu');
        }
        
        const resultado = await response.json();
        console.log('✅ Servidor respondeu:', resultado);
        
    } catch (error) {
        console.warn('⚠️ Servidor offline - dados salvos localmente:', error.message);
        // Salvar em localStorage como fallback
        let historico = JSON.parse(localStorage.getItem('formulario_respostas') || '[]');
        historico.push(dados);
        localStorage.setItem('formulario_respostas', JSON.stringify(historico));
    }
}

// ============================================
// 4️⃣ GERAR GRÁFICO
// ============================================
function gerarGrafico(resultados) {
    const ctx = el('graficoProjeccao').getContext('2d');
    
    // Destruir gráfico anterior se existir
    if (chartInstance) {
        chartInstance.destroy();
    }
    
    const labels = ['Aporte Inicial', '🛡️ Conservador', '⚖️ Moderado', '🚀 Arriscado'];
    const data = [
        resultados.aporte_total,
        resultados.projecoes.conservador.valor_final,
        resultados.projecoes.moderado.valor_final,
        resultados.projecoes.arriscado.valor_final
    ];
    
    const cores = ['#9ca3af', '#10b981', '#667eea', '#f59e0b'];
    
    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Valores (R$)',
                data: data,
                backgroundColor: cores,
                borderColor: cores,
                borderWidth: 2,
                borderRadius: 8,
                hoverBackgroundColor: [
                    '#6b7280', '#059669', '#5568d3', '#d97706'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const valor = context.raw;
                            return 'R$ ' + valor.toLocaleString('pt-BR', {minimumFractionDigits: 0});
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value.toLocaleString('pt-BR', {maximumFractionDigits: 0});
                        }
                    }
                }
            }
        }
    });
}

// ============================================
// 5️⃣ EXIBIR RESULTADOS
// ============================================
function exibirResultados(dados, resultados) {
    // Resumo Cards
    el('resumoRendaAtual').textContent = 
        'R$ ' + dados.renda_atual.toLocaleString('pt-BR', {minimumFractionDigits: 0});
    el('resumoProfissaoAtual').textContent = 
        `${dados.profissao_atual} • ${dados.idade_atual} anos`;
    
    el('resumoRendaFutura').textContent = 
        'R$ ' + dados.salario_futuro.toLocaleString('pt-BR', {minimumFractionDigits: 0});
    el('resumoProfissaoFutura').textContent = 
        `${dados.profissao_futura} • ${dados.idade_futura} anos`;
    
    el('tempoMeta').textContent = resultados.tempo_meta;
    el('tempoMetaDesc').textContent = resultados.tempo_meta_desc;
    
    // Tabela de Projeções
    let htmlTabela = '';
    const tipos = ['conservador', 'moderado', 'arriscado'];
    
    for (const tipo of tipos) {
        const proj = resultados.projecoes[tipo];
        const rendimento = proj.valor_final - resultados.aporte_total;
        const pct = ((rendimento / resultados.aporte_total) * 100).toFixed(1);
        
        htmlTabela += `
            <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 15px; border-bottom: 1px solid #e5e7eb; font-size: 14px;">${proj.label === 'Conservador' ? '🛡️' : proj.label === 'Moderado' ? '⚖️' : '🚀'} ${proj.label}</td>
                <td style="padding: 15px; border-bottom: 1px solid #e5e7eb; font-size: 14px;">${proj.label === 'Conservador' ? 'Baixo risco' : proj.label === 'Moderado' ? 'Risco equilibrado' : 'Alto risco'}</td>
                <td style="padding: 15px; border-bottom: 1px solid #e5e7eb; font-size: 14px;">${proj.taxa_anual}%</td>
                <td style="padding: 15px; border-bottom: 1px solid #e5e7eb; font-size: 14px;">R$ ${resultados.aporte_total.toLocaleString('pt-BR', {minimumFractionDigits: 0})}</td>
                <td style="padding: 15px; border-bottom: 1px solid #e5e7eb; font-size: 14px;\"><strong>R$ ${proj.valor_final.toLocaleString('pt-BR', {minimumFractionDigits: 0})}</strong></td>
                <td style="padding: 15px; border-bottom: 1px solid #e5e7eb; font-size: 14px; color: #10b981; font-weight: 600;\">+R$ ${rendimento.toLocaleString('pt-BR', {minimumFractionDigits: 0})} (${pct}%)</td>
            </tr>
        `;
    }
    
    el('tabelaProjecoes').innerHTML = htmlTabela;
    
    // Mostrar seção de resultados
    el('resultsSection').style.display = 'block';
    
    // Scroll para resultados
    setTimeout(() => {
        el('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }, 300);
}

// ============================================
// BOTÕES SECUNDÁRIOS E METAS
// ============================================
function novoCalculo() {
    el('mainForm').reset();
    el('resultsSection').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function setGoal(amount, description) {
    el('goal_amount').value = amount;
    const input = el('goal_amount');
    input.style.backgroundColor = '#e8f5e8';
    setTimeout(() => input.style.backgroundColor = '', 1000);
}

function updateRateDisplay() {
    const rate = el('annual_rate').value;
    el('rateDisplay').textContent = rate + '%';
}

function calcularMeta(event) {
    event.preventDefault();
    
    const goal = Number(el('goal_amount').value);
    const monthly = Number(el('monthly_saving').value);
    const annualRate = Number(el('annual_rate').value) / 100;
    const monthlyRate = annualRate / 12;
    
    let months;
    if (monthlyRate === 0) {
        months = Math.ceil(goal / monthly);
    } else {
        months = Math.ceil(
            Math.log((goal * monthlyRate / monthly) + 1) / Math.log(1 + monthlyRate)
        );
    }
    
    const years = (months / 12).toFixed(1);
    const totalSaved = monthly * months;
    const interest = totalSaved - (monthly * months);
    
    const resultDiv = el('goalResult');
    resultDiv.innerHTML = `
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin-top: 20px;">
            <h3 style="font-size: 24px; margin-bottom: 20px; text-align: center;">📊 Resultado da Sua Meta</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 8px;">
                    <div style="font-size: 14px; opacity: 0.9; margin-bottom: 5px;">⏰ Tempo Necessário</div>
                    <div style="font-size: 32px; font-weight: 700;">${years} anos</div>
                    <div style="font-size: 12px; opacity: 0.8;">${months} meses</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 8px;">
                    <div style="font-size: 14px; opacity: 0.9; margin-bottom: 5px;">💰 Meta</div>
                    <div style="font-size: 32px; font-weight: 700;">R$ ${goal.toLocaleString('pt-BR')}</div>
                    <div style="font-size: 12px; opacity: 0.8;">Valor desejado</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 8px;">
                    <div style="font-size: 14px; opacity: 0.9; margin-bottom: 5px;">📈 Poupança Mensal</div>
                    <div style="font-size: 32px; font-weight: 700;">R$ ${monthly.toLocaleString('pt-BR')}</div>
                    <div style="font-size: 12px; opacity: 0.8;">Por mês</div>
                </div>
            </div>
            <div style="margin-top: 25px; padding-top: 25px; border-top: 2px solid rgba(255,255,255,0.3); text-align: center;">
                <p style="font-size: 16px; line-height: 1.6; opacity: 0.95;">
                    💡 <strong>Dica:</strong> Poupando R$ ${monthly.toLocaleString('pt-BR')} por mês durante ${years} anos, 
                    você alcançará sua meta de R$ ${goal.toLocaleString('pt-BR')}!
                </p>
            </div>
        </div>
    `;
    
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}

async function baixarDados() {
    try {
        const response = await fetch(`${API_BASE}/baixar_csv`);
        
        if (!response.ok) {
            alert('Nenhum dado para baixar ainda');
            return;
        }
        
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `dados_financeiros_${new Date().toLocaleDateString('pt-BR', {day:'2-digit', month:'2-digit', year:'numeric'}).replace(/\//g, '-')}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        console.log('✅ CSV baixado');
    } catch (error) {
        console.error('❌ Erro ao baixar:', error);
        
        // Fallback: Baixar do localStorage
        const historico = JSON.parse(localStorage.getItem('formulario_respostas') || '[]');
        if (historico.length === 0) {
            alert('Nenhum dado coletado');
            return;
        }
        
        const csv = gerarCSVLocal(historico);
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `dados_financeiros_${new Date().toLocaleDateString('pt-BR', {day:'2-digit', month:'2-digit', year:'numeric'}).replace(/\//g, '-')}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

function gerarCSVLocal(dados) {
    if (dados.length === 0) return '';
    
    const headers = Object.keys(dados[0]);
    let csv = headers.join(',') + '\n';
    
    for (const row of dados) {
        const values = headers.map(h => {
            const val = row[h];
            if (val === null || val === undefined) return '';
            if (typeof val === 'string' && val.includes(',')) {
                return `"${val.replace(/"/g, '""')}"`;
            }
            return val;
        });
        csv += values.join(',') + '\n';
    }
    
    return csv;
}

console.log('✅ app_unificado_integrado.js carregado');
