// evidence-loader.js — Single authoritative fetch shared by all page sections
const EvidenceLoader = (function() {
  let evidence = null;
  let loadPromise = null;
  let listeners = [];

  function load() {
    if (loadPromise) return loadPromise;
    loadPromise = fetch('data/evidence.json')
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(data => { evidence = data; notify(); return data; })
      .catch(err => { console.error('Evidence load failed:', err); notify(err); throw err; });
    return loadPromise;
  }

  function onLoad(fn) {
    if (evidence) { fn(evidence); return; }
    listeners.push(fn);
  }

  function notify(err) {
    const pending = listeners;
    listeners = [];
    for (const fn of pending) {
      try { fn(evidence, err); } catch(e) { console.error('Evidence listener error:', e); }
    }
  }

  function get() { return evidence; }
  function getMetric(key) { return evidence?.metrics?.[key] || null; }

  return { load, onLoad, get, getMetric };
})();
