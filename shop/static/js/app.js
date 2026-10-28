(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const menu = $('.menu'), nav = $('#nav');
  menu?.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menu.setAttribute('aria-expanded', open);
  });

  const toast = (msg) => {
    const t = $('#toast');
    t.textContent = msg; t.classList.add('show');
    clearTimeout(toast.id); toast.id = setTimeout(() => t.classList.remove('show'), 2200);
  };

  $('form.add')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = e.currentTarget;
    try {
      const r = await fetch(f.action, { method: 'POST', body: new FormData(f), headers: { 'X-Requested-With': 'fetch' } });
      const d = await r.json();
      if (d.ok) { $('#count').textContent = d.count; toast('Added to your bag'); }
      else toast(d.error);
    } catch { f.submit(); }
  });

  document.querySelectorAll('[data-autosubmit]').forEach((el) =>
    el.addEventListener('change', () => el.form.submit()));
})();
