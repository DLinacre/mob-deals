const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

function updateSavings() {
  const current = Number($('#current-bill')?.value || 0);
  const next = Number($('#new-price')?.value || 0);
  const monthly = Math.max(0, current - next);
  $('#monthly-save').textContent = `£${monthly}`;
  $('#yearly-save').textContent = `£${monthly * 12}`;
  $('#two-year-save').textContent = `£${monthly * 24}`;
}

function setFilter(filter) {
  $$('.chip[data-filter]').forEach(btn => btn.setAttribute('aria-pressed', String(btn.dataset.filter === filter)));
  let visible = 0;
  $$('.deal-card').forEach(card => {
    const show = filter === 'all' || card.dataset.category === filter || card.dataset.network === filter;
    card.classList.toggle('hidden', !show);
    if (show) visible += 1;
  });
  const count = $('#result-count');
  if (count) count.textContent = `${visible} plan${visible === 1 ? '' : 's'} shown`;
}

function sortTable(mode) {
  const tbody = $('#comparison-body');
  if (!tbody) return;
  const rows = $$('tr', tbody);
  rows.sort((a,b) => {
    if (mode === 'price') return Number(a.dataset.price) - Number(b.dataset.price);
    if (mode === 'data') return a.dataset.data.localeCompare(b.dataset.data, undefined, {numeric:true});
    if (mode === 'reviewed') return b.dataset.reviewed.localeCompare(a.dataset.reviewed);
    return a.dataset.provider.localeCompare(b.dataset.provider);
  });
  rows.forEach(row => tbody.append(row));
}

async function loadLiveSourceChecks() {
  const summary = $('#live-source-summary');
  if (!summary) return;
  try {
    const response = await fetch('data/live-sources.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    const checked = new Date(data.generatedAt).toLocaleString('en-GB', { dateStyle: 'medium', timeStyle: 'short' });
    summary.textContent = `${data.reachableCount}/${data.sourceCount} public provider sources reachable. Last automated check: ${checked}. Prices still require provider confirmation.`;
    for (const source of data.sources || []) {
      const badge = document.querySelector(`[data-source-status="${source.id}"]`);
      if (!badge) continue;
      badge.textContent = source.ok ? 'Reachable' : `Check manually${source.status ? ` (${source.status})` : ''}`;
      badge.classList.toggle('status-ok', Boolean(source.ok));
      badge.classList.toggle('status-warn', !source.ok);
      badge.title = source.error || source.finalUrl || source.sourceUrl;
    }
  } catch (error) {
    summary.textContent = 'Live source status is temporarily unavailable. Use provider links to confirm current prices.';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateSavings();
  ['#current-bill', '#new-price'].forEach(sel => $(sel)?.addEventListener('input', updateSavings));
  $$('.chip[data-filter]').forEach(btn => btn.addEventListener('click', () => setFilter(btn.dataset.filter)));
  $('#sort-deals')?.addEventListener('change', event => sortTable(event.target.value));
  loadLiveSourceChecks();
});
