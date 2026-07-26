// three-collapses.js — Evidence-driven. Zero hardcoded metrics. Uses shared EvidenceLoader.
(function() {
  function showProv(metric) {
    if (!metric) return;
    const popup = document.getElementById('provenance-popup');
    const content = document.getElementById('provenance-content');
    const overlay = document.getElementById('collapses-overlay');
    if (!popup || !content) return;
    
    const status = metric.status || 'unknown';
    const cls = status.includes('invalid') ? 'status-invalid' : 'status-valid';
    content.innerHTML = `
      <h3>Evidence Record</h3>
      <div class="pv-row"><span class="pv-key">Experiment</span><span class="pv-val">${metric.experiment_id || 'N/A'}</span></div>
      <div class="pv-row"><span class="pv-key">Period</span><span class="pv-val">${metric.period || 'N/A'}</span></div>
      <div class="pv-row"><span class="pv-key">Universe</span><span class="pv-val">${metric.universe || 'N/A'}</span></div>
      <div class="pv-row"><span class="pv-key">Protocol</span><span class="pv-val">${metric.protocol || 'N/A'}</span></div>
      <div class="pv-row"><span class="pv-key">Artifact</span><span class="pv-val">${metric.artifact || 'N/A'}</span></div>
      <div class="pv-row"><span class="pv-key">Status</span><span class="pv-val ${cls}">${status.toUpperCase()}</span></div>
    `;
    if (overlay) overlay.classList.add('show');
    popup.classList.add('show');
  }

  function hideProv() {
    const popup = document.getElementById('provenance-popup');
    const overlay = document.getElementById('collapses-overlay');
    if (popup) popup.classList.remove('show');
    if (overlay) overlay.classList.remove('show');
  }

  function computeDecline(before, after) {
    if (!before || !after || before.value === 0) return null;
    const abs = before.value - after.value;
    const rel = (abs / Math.abs(before.value)) * 100;
    return { abs, rel };
  }

  function formatVal(m) {
    if (!m) return { val:'—', cls:'neutral' };
    const v = m.value; const u = m.unit || '';
    let cls = 'neutral';
    if (m.status && m.status.includes('invalid')) cls = 'invalid';
    else if (v > 0) cls = 'positive';
    else if (v < 0) cls = 'negative';
    let display;
    if (u.includes('return') || u.includes('drawdown') || u.includes('excess') || u.includes('fraction') || u.includes('share')) display = (v*100).toFixed(1)+'%';
    else if (u.includes('correlation') || u.includes('IC') || u.includes('t-statistic') || u.includes('value')) display = v.toFixed(2);
    else display = v.toFixed(2);
    return { val:display, cls, metric:m };
  }

  window.renderCollapses = function(evidence) {
    const container = document.getElementById('collapses-container');
    const hero = document.getElementById('collapse-hero');
    if (!container) return;
    
    const metrics = evidence.metrics || {};
    const collapses = evidence.collapses || [];
    if (!collapses.length) { container.innerHTML = '<p style="color:var(--amber);">No collapse records in evidence.</p>'; return; }

    container.innerHTML = '';
    for (const c of collapses) {
      const bm = c.before?.metric ? metrics[c.before.metric] : null;
      const am = c.after?.metric ? metrics[c.after.metric] : null;
      const bf = formatVal(bm); const af = formatVal(am);
      const decline = bm && am ? computeDecline(bm, am) : null;
      const prov = am || bm;

      const panel = document.createElement('div');
      panel.className = 'collapse-panel';
      panel.innerHTML = `
        <h2>${c.title||''}</h2>
        <div class="label">Initial Belief</div><div class="belief">${c.belief||''}</div>
        <div class="label">Intervention</div><div class="intervention">${c.intervention||''}</div>
        <div class="label">Before</div>
        <div class="metric-row"><span class="metric-label">${bm?.unit||''}</span><span class="metric-value ${bf.cls}">${bf.val}</span></div>
        ${decline?`<div class="arrow-section"><span class="arrow">↓</span><span class="decline">−${decline.rel.toFixed(0)}%</span></div>`:''}
        <div class="label">After</div>
        <div class="metric-row"><span class="metric-label">${am?.unit||''}</span><span class="metric-value ${af.cls}">${af.val}</span></div>
        <div class="interpretation">${c.interpretation||''}</div>
        <div class="evidence-link">
          <div style="font-family:'SF Mono',monospace;font-size:0.7rem;">${prov?.experiment_id||'N/A'}</div>
          <button onclick="window._showProv('${c.after?.metric||c.before?.metric||''}')">View Evidence →</button>
        </div>`;
      container.appendChild(panel);
    }

    // Hero percentage
    const c1 = collapses[0];
    if (c1) {
      const bm1 = c1.before?.metric ? metrics[c1.before.metric] : null;
      const am1 = c1.after?.metric ? metrics[c1.after.metric] : null;
      if (bm1 && am1) { const d = computeDecline(bm1, am1); if (d && hero) hero.textContent = `${d.rel.toFixed(0)}% collapse`; }
    }

    console.log('✅ Three Collapses rendered from evidence.json');
  };

  window._showProv = function(key) {
    const m = EvidenceLoader.getMetric(key);
    if (m) showProv(m);
  };

  // Wire up provenance close
  document.addEventListener('DOMContentLoaded', () => {
    const close = document.getElementById('pv-close');
    const overlay = document.getElementById('collapses-overlay');
    if (close) close.addEventListener('click', hideProv);
    if (overlay) overlay.addEventListener('click', e => { if (e.target===overlay) hideProv(); });
    document.addEventListener('keydown', e => { if (e.key==='Escape') hideProv(); });
  });

  // Auto-render when evidence loads
  EvidenceLoader.onLoad((evidence, err) => {
    if (evidence) window.renderCollapses(evidence);
  });
})();
