/* ================================================
   KHATALYZE — Frontend Application
   ================================================ */

const API_BASE = 'http://localhost:8000';

// =============================================
// STATE
// =============================================

const state = {
    statementId: null,
    report: null,
    transactions: [],
    filteredTransactions: [],
    currentPage: 1,
    perPage: 15,
    charts: {},
};

// =============================================
// DOM ELEMENTS
// =============================================

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const views = {
    upload: $('#upload-view'),
    processing: $('#processing-view'),
    dashboard: $('#dashboard-view'),
};

// =============================================
// VIEW MANAGEMENT
// =============================================

function showView(name) {
    Object.values(views).forEach(v => v.classList.remove('active'));
    views[name].classList.add('active');
}

// =============================================
// TOAST NOTIFICATIONS
// =============================================

function showToast(message, type = 'info') {
    let toast = $('.toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.className = 'toast';
        document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.className = `toast ${type}`;
    requestAnimationFrame(() => toast.classList.add('show'));
    setTimeout(() => toast.classList.remove('show'), 4000);
}

// =============================================
// FORMAT HELPERS
// =============================================

function formatCurrency(amount) {
    if (amount == null || isNaN(amount)) return '—';
    const abs = Math.abs(amount);
    if (abs >= 10000000) return `₹${(amount / 10000000).toFixed(2)}Cr`;
    if (abs >= 100000) return `₹${(amount / 100000).toFixed(2)}L`;
    return `₹${amount.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
}

function formatDate(dateStr) {
    if (!dateStr) return '—';
    try {
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
    } catch {
        return dateStr;
    }
}

function truncate(str, maxLen = 30) {
    if (!str) return '—';
    return str.length > maxLen ? str.slice(0, maxLen) + '…' : str;
}

// =============================================
// UPLOAD LOGIC
// =============================================

(function initUpload() {
    const dropZone = $('#drop-zone');
    const fileInput = $('#file-input');
    const filePreview = $('#file-preview');
    const fileName = $('#file-name');
    const fileSize = $('#file-size');
    const fileRemove = $('#file-remove');
    const hasPassword = $('#has-password');
    const passwordField = $('#password-field');
    const uploadBtn = $('#upload-btn');

    let selectedFile = null;

    // Click to browse
    dropZone.addEventListener('click', () => fileInput.click());

    // Drag & drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length) handleFileSelect(files[0]);
    });

    // File input change
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length) handleFileSelect(fileInput.files[0]);
    });

    function handleFileSelect(file) {
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            showToast('Please select a PDF file', 'error');
            return;
        }
        selectedFile = file;
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        dropZone.classList.add('hidden');
        filePreview.classList.remove('hidden');
        uploadBtn.disabled = false;
    }

    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / 1048576).toFixed(1) + ' MB';
    }

    // Remove file
    fileRemove.addEventListener('click', () => {
        selectedFile = null;
        fileInput.value = '';
        dropZone.classList.remove('hidden');
        filePreview.classList.add('hidden');
        uploadBtn.disabled = true;
    });

    // Password toggle
    hasPassword.addEventListener('change', () => {
        passwordField.classList.toggle('hidden', !hasPassword.checked);
    });

    // Upload
    uploadBtn.addEventListener('click', async () => {
        if (!selectedFile) return;
        try {
            uploadBtn.disabled = true;
            uploadBtn.innerHTML = '<span class="btn-spinner"></span> Uploading...';

            showView('processing');
            activateStep('upload');

            // Step 1: Upload
            const formData = new FormData();
            formData.append('file', selectedFile);
            if (hasPassword.checked) {
                formData.append('password', $('#pdf-password').value);
            }

            const uploadRes = await fetch(`${API_BASE}/upload/`, {
                method: 'POST',
                body: formData,
            });

            if (!uploadRes.ok) {
                const err = await uploadRes.json();
                throw new Error(err.detail || 'Upload failed');
            }

            const uploadData = await uploadRes.json();
            state.statementId = uploadData.data.statement_id;

            completeStep('upload');
            activateStep('parse');
            updateProgress(20);

            // Step 2: Analyze (this runs the full pipeline)
            activateStep('analyze');
            updateProgress(40);

            const analyzeRes = await fetch(`${API_BASE}/analyze/${state.statementId}`, {
                method: 'POST',
            });

            if (!analyzeRes.ok) {
                const err = await analyzeRes.json();
                throw new Error(err.detail || 'Analysis failed');
            }

            completeStep('parse');
            completeStep('analyze');
            activateStep('insights');
            updateProgress(70);

            const analyzeData = await analyzeRes.json();
            state.report = analyzeData.report;

            completeStep('insights');
            activateStep('vector');
            updateProgress(90);

            // Small delay for visual effect
            await new Promise(r => setTimeout(r, 600));

            completeStep('vector');
            updateProgress(100);

            await new Promise(r => setTimeout(r, 500));

            // Render dashboard
            renderDashboard(state.report);
            showView('dashboard');
            showToast('Analysis complete!', 'success');

        } catch (err) {
            console.error(err);
            showToast(err.message || 'Something went wrong', 'error');
            showView('upload');
        } finally {
            uploadBtn.disabled = false;
            uploadBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                <span>Upload & Analyze</span>`;
        }
    });
})();

// =============================================
// PROCESSING STEPS
// =============================================

function activateStep(name) {
    const step = $(`.proc-step[data-step="${name}"]`);
    if (step) {
        step.classList.add('active');
        step.classList.remove('done');
    }
    $('#processing-status').textContent = step ? step.querySelector('span').textContent + '...' : '';
}

function completeStep(name) {
    const step = $(`.proc-step[data-step="${name}"]`);
    if (step) {
        step.classList.remove('active');
        step.classList.add('done');
    }
}

function updateProgress(pct) {
    $('#processing-percent').textContent = `${pct}%`;
}

// =============================================
// DASHBOARD RENDERING
// =============================================

function renderDashboard(report) {
    renderAccountInfo(report);
    renderHealthScore(report);
    renderKPIs(report);
    renderCategoryChart(report);
    renderMonthlyChart(report);
    renderInsights(report);
    renderRisks(report);
    renderRecommendations(report);
    renderTransactions(report);
}

// ---------- Account Info ----------
function renderAccountInfo(report) {
    const acc = report.account || {};
    const parts = [];
    if (acc.bank && acc.bank !== 'Unknown') parts.push(acc.bank);
    if (acc.account_holder) parts.push(acc.account_holder);
    if (acc.account_number) parts.push(`A/C: ****${acc.account_number.slice(-4)}`);

    const el = $('#account-info');
    el.innerHTML = parts.length
        ? parts.map((p, i) => `<span>${p}</span>${i < parts.length - 1 ? '<span class="separator">•</span>' : ''}`).join('')
        : '';
}

// ---------- Health Score ----------
function renderHealthScore(report) {
    const score = report.financial_health_score || 0;
    const status = report.financial_health_status || '—';

    // Animate number
    const scoreEl = $('#health-score');
    animateNumber(scoreEl, 0, Math.round(score), 1500);

    $('#health-status').textContent = status;

    // Animate ring (circumference = 2 * PI * 85 ≈ 534)
    const circumference = 534;
    const offset = circumference - (circumference * score / 100);
    setTimeout(() => {
        $('#health-ring-progress').style.strokeDashoffset = offset;
    }, 100);
}

function animateNumber(el, start, end, duration) {
    const startTime = performance.now();
    function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
        el.textContent = Math.round(start + (end - start) * eased);
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

// ---------- KPIs ----------
function renderKPIs(report) {
    const kpis = report.kpis || {};
    const txnCount = (report.transactions || []).length;

    $('#kpi-income-val').textContent = formatCurrency(kpis.income);
    $('#kpi-expense-val').textContent = formatCurrency(kpis.expense);
    $('#kpi-cashflow-val').textContent = formatCurrency(kpis.net_cash_flow);
    $('#kpi-txns-val').textContent = txnCount.toLocaleString();

    // Color the cashflow
    const cfEl = $('#kpi-cashflow-val');
    cfEl.style.color = kpis.net_cash_flow >= 0 ? 'var(--color-success)' : 'var(--color-danger)';
}

// ---------- Category Chart ----------
function renderCategoryChart(report) {
    const spending = (report.category_analysis || {}).spending || {};
    const labels = Object.keys(spending);
    const data = Object.values(spending);

    if (!labels.length) return;

    const colors = [
        '#818cf8', '#f472b6', '#34d399', '#fbbf24', '#60a5fa',
        '#fb923c', '#a78bfa', '#f87171', '#2dd4bf', '#e879f9',
        '#94a3b8', '#78716c',
    ];

    const ctx = $('#category-chart').getContext('2d');

    if (state.charts.category) state.charts.category.destroy();

    state.charts.category = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels,
            datasets: [{
                data,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 0,
                hoverOffset: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#94a3c0',
                        font: { size: 11, family: 'Inter' },
                        padding: 12,
                        usePointStyle: true,
                        pointStyleWidth: 10,
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 20, 45, 0.95)',
                    titleColor: '#f1f3f9',
                    bodyColor: '#94a3c0',
                    borderColor: 'rgba(255,255,255,0.08)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 12,
                    callbacks: {
                        label: (ctx) => ` ${ctx.label}: ₹${ctx.raw.toLocaleString('en-IN')}`
                    }
                }
            },
        }
    });
}

// ---------- Monthly Chart ----------
function renderMonthlyChart(report) {
    const monthly = report.monthly_summary || {};
    const months = Object.keys(monthly).sort();

    if (!months.length) return;

    const incomeData = months.map(m => monthly[m].income || 0);
    const expenseData = months.map(m => monthly[m].expense || 0);
    const savingsData = months.map(m => monthly[m].savings || 0);

    const ctx = $('#monthly-chart').getContext('2d');

    if (state.charts.monthly) state.charts.monthly.destroy();

    state.charts.monthly = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: months.map(m => {
                const parts = m.split('-');
                const monthNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
                return parts.length >= 2 ? `${monthNames[parseInt(parts[1]) - 1]} ${parts[0].slice(2)}` : m;
            }),
            datasets: [
                {
                    label: 'Income',
                    data: incomeData,
                    backgroundColor: 'rgba(52, 211, 153, 0.7)',
                    borderRadius: 6,
                    borderSkipped: false,
                },
                {
                    label: 'Expense',
                    data: expenseData,
                    backgroundColor: 'rgba(248, 113, 113, 0.7)',
                    borderRadius: 6,
                    borderSkipped: false,
                },
                {
                    label: 'Savings',
                    data: savingsData,
                    backgroundColor: 'rgba(96, 165, 250, 0.5)',
                    borderRadius: 6,
                    borderSkipped: false,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#94a3c0',
                        font: { size: 11, family: 'Inter' },
                        usePointStyle: true,
                        pointStyleWidth: 10,
                        padding: 16,
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 20, 45, 0.95)',
                    titleColor: '#f1f3f9',
                    bodyColor: '#94a3c0',
                    borderColor: 'rgba(255,255,255,0.08)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 12,
                    callbacks: {
                        label: (ctx) => ` ${ctx.dataset.label}: ₹${ctx.raw.toLocaleString('en-IN')}`
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.04)', drawBorder: false },
                    ticks: { color: '#5b6782', font: { size: 11 } },
                },
                y: {
                    grid: { color: 'rgba(255,255,255,0.04)', drawBorder: false },
                    ticks: {
                        color: '#5b6782',
                        font: { size: 11 },
                        callback: (val) => formatCurrency(val),
                    },
                    beginAtZero: true,
                }
            }
        }
    });
}

// ---------- Insights ----------
function renderInsights(report) {
    const container = $('#insights-list');
    const insights = report.insights || {};

    let items = [];

    if (Array.isArray(insights)) {
        items = insights;
    } else if (typeof insights === 'object') {
        // insights is a dict of categories → arrays
        for (const [category, insightList] of Object.entries(insights)) {
            if (Array.isArray(insightList)) {
                items.push(...insightList);
            }
        }
    }

    if (!items.length) {
        container.innerHTML = '<p style="color: var(--text-muted); font-size: 0.85rem;">No insights generated.</p>';
        return;
    }

    container.innerHTML = items.slice(0, 12).map(insight => `
        <div class="intel-item">
            <span>${escapeHtml(typeof insight === 'string' ? insight : JSON.stringify(insight))}</span>
        </div>
    `).join('');
}

// ---------- Risks ----------
function renderRisks(report) {
    const container = $('#risks-list');
    const risks = report.risks || [];

    if (!risks.length) {
        container.innerHTML = '<p style="color: var(--text-muted); font-size: 0.85rem;">No risks detected. Great job! 🎉</p>';
        return;
    }

    container.innerHTML = risks.map(risk => `
        <div class="intel-item severity-${(risk.severity || '').toLowerCase()}">
            <div class="intel-item-header">
                <span class="intel-item-title">${escapeHtml(risk.title || '')}</span>
                <span class="severity-badge ${(risk.severity || '').toLowerCase()}">${risk.severity || ''}</span>
            </div>
            <p class="intel-item-desc">${escapeHtml(risk.description || '')}</p>
            ${risk.recommendation ? `<p class="intel-item-action">💡 ${escapeHtml(risk.recommendation)}</p>` : ''}
        </div>
    `).join('');
}

// ---------- Recommendations ----------
function renderRecommendations(report) {
    const container = $('#recommendations-list');
    const recs = report.recommendations || [];

    if (!recs.length) {
        container.innerHTML = '<p style="color: var(--text-muted); font-size: 0.85rem;">No recommendations at this time.</p>';
        return;
    }

    container.innerHTML = recs.map(rec => `
        <div class="intel-item priority-${(rec.priority || '').toLowerCase()}">
            <div class="intel-item-header">
                <span class="intel-item-title">${escapeHtml(rec.title || '')}</span>
                <span class="priority-badge ${(rec.priority || '').toLowerCase()}">${rec.priority || ''}</span>
            </div>
            <p class="intel-item-desc">${escapeHtml(rec.reason || '')}</p>
            ${rec.recommended_action ? `<p class="intel-item-action">→ ${escapeHtml(rec.recommended_action)}</p>` : ''}
        </div>
    `).join('');
}

// ---------- Transactions ----------
function renderTransactions(report) {
    state.transactions = report.transactions || [];
    state.filteredTransactions = [...state.transactions];
    state.currentPage = 1;

    // Populate category filter
    const categories = [...new Set(state.transactions.map(t => t.category).filter(Boolean))].sort();
    const catFilter = $('#txn-category-filter');
    catFilter.innerHTML = '<option value="all">All Categories</option>' +
        categories.map(c => `<option value="${c}">${c}</option>`).join('');

    renderTransactionTable();

    // Search
    $('#txn-search').addEventListener('input', filterTransactions);
    $('#txn-type-filter').addEventListener('change', filterTransactions);
    $('#txn-category-filter').addEventListener('change', filterTransactions);
}

function filterTransactions() {
    const search = ($('#txn-search').value || '').toLowerCase();
    const typeFilter = $('#txn-type-filter').value;
    const catFilter = $('#txn-category-filter').value;

    state.filteredTransactions = state.transactions.filter(t => {
        const matchSearch = !search ||
            (t.description || '').toLowerCase().includes(search) ||
            (t.party || '').toLowerCase().includes(search) ||
            (t.category || '').toLowerCase().includes(search);

        const matchType = typeFilter === 'all' || t.transaction_type === typeFilter;
        const matchCat = catFilter === 'all' || t.category === catFilter;

        return matchSearch && matchType && matchCat;
    });

    state.currentPage = 1;
    renderTransactionTable();
}

function renderTransactionTable() {
    const tbody = $('#txn-tbody');
    const start = (state.currentPage - 1) * state.perPage;
    const end = start + state.perPage;
    const page = state.filteredTransactions.slice(start, end);

    tbody.innerHTML = page.map(txn => {
        const type = (txn.transaction_type || '').toUpperCase();
        const isCredit = type === 'CREDIT';
        return `
            <tr>
                <td>${formatDate(txn.date)}</td>
                <td title="${escapeHtml(txn.description || '')}">${truncate(txn.description, 35)}</td>
                <td>${truncate(txn.party, 20)}</td>
                <td><span class="txn-category-badge">${txn.category || '—'}</span></td>
                <td>${txn.payment_mode || '—'}</td>
                <td class="align-right">
                    <span class="txn-amount ${isCredit ? 'credit' : 'debit'}">
                        ${isCredit ? '+' : '-'}₹${(txn.amount || 0).toLocaleString('en-IN')}
                    </span>
                </td>
                <td class="align-right">
                    <span class="txn-balance">₹${(txn.balance || 0).toLocaleString('en-IN')}</span>
                </td>
            </tr>
        `;
    }).join('');

    renderPagination();
}

function renderPagination() {
    const container = $('#txn-pagination');
    const totalPages = Math.ceil(state.filteredTransactions.length / state.perPage);

    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }

    let html = '';

    // Prev
    if (state.currentPage > 1) {
        html += `<button onclick="goToPage(${state.currentPage - 1})">‹ Prev</button>`;
    }

    // Page numbers (show max 7)
    const maxVisible = 7;
    let startPage = Math.max(1, state.currentPage - 3);
    let endPage = Math.min(totalPages, startPage + maxVisible - 1);
    if (endPage - startPage < maxVisible - 1) {
        startPage = Math.max(1, endPage - maxVisible + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
        html += `<button class="${i === state.currentPage ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>`;
    }

    // Next
    if (state.currentPage < totalPages) {
        html += `<button onclick="goToPage(${state.currentPage + 1})">Next ›</button>`;
    }

    container.innerHTML = html;
}

// Make goToPage global for onclick
window.goToPage = function(page) {
    state.currentPage = page;
    renderTransactionTable();
    // Scroll to top of table
    $('.txn-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
};

// =============================================
// CHAT LOGIC
// =============================================

(function initChat() {
    const panel = $('#chat-panel');
    const overlay = $('#chat-overlay');
    const toggleBtn = $('#chat-toggle-btn');
    const closeBtn = $('#chat-close');
    const input = $('#chat-input');
    const sendBtn = $('#chat-send');
    const messagesEl = $('#chat-messages');

    function openChat() {
        panel.classList.add('open');
        overlay.classList.add('active');
        input.focus();
    }

    function closeChat() {
        panel.classList.remove('open');
        overlay.classList.remove('active');
    }

    toggleBtn.addEventListener('click', openChat);
    closeBtn.addEventListener('click', closeChat);
    overlay.addEventListener('click', closeChat);

    // Input enable/disable send
    input.addEventListener('input', () => {
        sendBtn.disabled = !input.value.trim();
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && input.value.trim()) {
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', () => {
        if (input.value.trim()) sendMessage();
    });

    // Suggestions
    $$('.chat-suggestion').forEach(btn => {
        btn.addEventListener('click', () => {
            input.value = btn.dataset.q;
            sendBtn.disabled = false;
            sendMessage();
        });
    });

    async function sendMessage() {
        const question = input.value.trim();
        if (!question || !state.statementId) return;

        // Clear welcome message on first send
        const welcome = messagesEl.querySelector('.chat-welcome');
        if (welcome) welcome.remove();

        // Add user message
        appendMessage('user', question);
        input.value = '';
        sendBtn.disabled = true;

        // Show typing indicator
        const typingEl = appendTyping();

        try {
            const res = await fetch(`${API_BASE}/chat/${state.statementId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question, top_k: 5 }),
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Chat failed');
            }

            const data = await res.json();
            typingEl.remove();

            const answer = data.answer || data.response || JSON.stringify(data);
            appendMessage('bot', answer);

        } catch (err) {
            typingEl.remove();
            appendMessage('bot', `Sorry, I encountered an error: ${err.message}`);
        }
    }

    function appendMessage(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-msg ${role}`;

        const avatarLabel = role === 'user' ? 'You' : 'AI';
        msgDiv.innerHTML = `
            <div class="chat-msg-avatar">${avatarLabel === 'You' ? '👤' : '🤖'}</div>
            <div class="chat-msg-bubble">${escapeHtml(text)}</div>
        `;

        messagesEl.appendChild(msgDiv);
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    function appendTyping() {
        const div = document.createElement('div');
        div.className = 'chat-msg bot';
        div.innerHTML = `
            <div class="chat-msg-avatar">🤖</div>
            <div class="chat-msg-bubble chat-typing">
                <div class="chat-typing-dot"></div>
                <div class="chat-typing-dot"></div>
                <div class="chat-typing-dot"></div>
            </div>
        `;
        messagesEl.appendChild(div);
        messagesEl.scrollTop = messagesEl.scrollHeight;
        return div;
    }
})();

// =============================================
// NEW STATEMENT BUTTON
// =============================================

$('#new-upload-btn').addEventListener('click', () => {
    // Reset state
    state.statementId = null;
    state.report = null;
    state.transactions = [];
    state.filteredTransactions = [];
    state.currentPage = 1;

    // Destroy charts
    Object.values(state.charts).forEach(c => { try { c.destroy(); } catch {} });
    state.charts = {};

    // Reset processing steps
    $$('.proc-step').forEach(s => { s.classList.remove('active', 'done'); });
    updateProgress(0);

    // Reset upload form
    $('#drop-zone').classList.remove('hidden');
    $('#file-preview').classList.add('hidden');
    $('#upload-btn').disabled = true;
    $('#has-password').checked = false;
    $('#password-field').classList.add('hidden');
    $('#pdf-password').value = '';

    showView('upload');
});

// =============================================
// ESCAPE HTML
// =============================================

function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// =============================================
// INIT
// =============================================

document.addEventListener('DOMContentLoaded', () => {
    showView('upload');
});
