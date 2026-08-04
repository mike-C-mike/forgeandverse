(() => {
  const toggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');

  const setNav = (open) => {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', String(open));
    nav.dataset.open = String(open);
    document.body.classList.toggle('nav-open', open);
    const label = toggle.querySelector('.nav-toggle-label');
    if (label) label.textContent = open ? 'Close' : 'Menu';
  };

  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });

    nav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => setNav(false));
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') setNav(false);
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 900) setNav(false);
    });
  }

  const toolbar = document.querySelector('[data-filter-toolbar]');
  const cards = Array.from(document.querySelectorAll('[data-work-card]'));

  if (toolbar && cards.length) {
    const buttons = Array.from(toolbar.querySelectorAll('[data-filter]'));
    const count = document.querySelector('[data-visible-count]');
    const empty = document.querySelector('[data-filter-empty]');

    const applyFilter = (filter, updateUrl = true) => {
      const valid = filter === 'all' || buttons.some((button) => button.dataset.filter === filter);
      const activeFilter = valid ? filter : 'all';
      let visible = 0;

      cards.forEach((card) => {
        const show = activeFilter === 'all' || card.dataset.discipline === activeFilter;
        card.hidden = !show;
        if (show) visible += 1;
      });

      buttons.forEach((button) => {
        const active = button.dataset.filter === activeFilter;
        button.classList.toggle('is-active', active);
        button.setAttribute('aria-pressed', String(active));
      });

      if (count) count.textContent = String(visible);
      if (empty) empty.hidden = visible !== 0;

      if (updateUrl) {
        const url = new URL(window.location.href);
        if (activeFilter === 'all') url.searchParams.delete('discipline');
        else url.searchParams.set('discipline', activeFilter);
        window.history.replaceState({}, '', url);
      }
    };

    buttons.forEach((button) => {
      button.addEventListener('click', () => applyFilter(button.dataset.filter));
    });

    const initial = new URL(window.location.href).searchParams.get('discipline') || 'all';
    applyFilter(initial, false);
  }
})();
