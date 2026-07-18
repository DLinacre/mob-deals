
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
  $('#result-count').textContent = `${visible} plan${visible === 1 ? '' : 's'} shown`;
}

function sortTable(mode) {
  const tbody = $('#comparison-body');
  if (!tbody) return;
  const rows = $$('tr', tbody);
  rows.sort((a,b) => {
    if (mode === 'price') return Number(a.dataset.price) - Number(b.dataset.price);
    if (mode === 'data') return a.dataset.data.localeCompare(b.dataset.data, undefined, {numeric:true});
    return a.dataset.provider.localeCompare(b.dataset.provider);
  });
  rows.forEach(row => tbody.append(row));
}

document.addEventListener('DOMContentLoaded', () => {
  updateSavings();
  ['#current-bill', '#new-price'].forEach(sel => $(sel)?.addEventListener('input', updateSavings));
  $$('.chip[data-filter]').forEach(btn => btn.addEventListener('click', () => setFilter(btn.dataset.filter)));
  $('#sort-deals')?.addEventListener('change', event => sortTable(event.target.value));
});
