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

  document.querySelectorAll('[data-copy]').forEach((button) => {
    button.addEventListener('click', async () => {
      const value = button.dataset.copy || '';
      const region = button.closest('[data-copy-region]');
      const status = region?.querySelector('[data-copy-status]') || document.querySelector('[data-copy-status]');
      try {
        await navigator.clipboard.writeText(value);
        button.textContent = 'Copied';
        if (status) status.textContent = 'Checksum copied to clipboard.';
        window.setTimeout(() => { button.textContent = 'Copy'; }, 1600);
      } catch {
        if (status) status.textContent = 'Copy failed. Select the checksum manually.';
      }
    });
  });

  const lightbox = document.querySelector('[data-lightbox-dialog]');
  const lightboxImage = lightbox?.querySelector('[data-lightbox-image]');
  const lightboxCaption = lightbox?.querySelector('[data-lightbox-caption]');
  const lightboxClose = lightbox?.querySelector('[data-lightbox-close]');
  let lightboxReturnFocus = null;

  const closeLightbox = () => {
    if (!lightbox) return;
    if (typeof lightbox.close === 'function' && lightbox.open) lightbox.close();
    document.body.classList.remove('lightbox-open');
    if (lightboxReturnFocus) lightboxReturnFocus.focus();
  };

  document.addEventListener('click', (event) => {
    const trigger = event.target.closest('[data-lightbox]');
    if (!trigger || !lightbox || !lightboxImage) return;
    event.preventDefault();
    lightboxReturnFocus = trigger;
    lightboxImage.src = trigger.getAttribute('href');
    const sourceImage = trigger.querySelector('img');
    lightboxImage.alt = sourceImage?.alt || '';
    if (lightboxCaption) {
      lightboxCaption.textContent = trigger.dataset.lightboxCaption || '';
      lightboxCaption.hidden = !lightboxCaption.textContent;
    }
    document.body.classList.add('lightbox-open');
    if (typeof lightbox.showModal === 'function') lightbox.showModal();
    else lightbox.setAttribute('open', '');
    lightboxClose?.focus();
  });

  lightboxClose?.addEventListener('click', closeLightbox);
  lightbox?.addEventListener('click', (event) => {
    if (event.target === lightbox) closeLightbox();
  });
  lightbox?.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeLightbox();
  });

  const searchDataElement = document.getElementById('search-data');
  const searchInput = document.querySelector('[data-search-input]');
  const searchForm = document.querySelector('[data-search-form]');
  const searchResults = document.querySelector('[data-search-results]');
  const searchStatus = document.querySelector('[data-search-status]');
  const searchClear = document.querySelector('[data-search-clear]');

  if (searchDataElement && searchInput && searchResults && searchStatus) {
    let searchItems = [];
    try {
      searchItems = JSON.parse(searchDataElement.textContent || '[]');
    } catch {
      searchStatus.textContent = 'The search index could not be loaded.';
    }

    const disciplineNames = {
      'examiner-bench': 'Digital Forensics',
      'evidence-room': 'Property & Evidence',
      'watch': 'Law Enforcement & Support',
      'signal': 'Cybersecurity'
    };

    const normalize = (value) => String(value || '')
      .toLowerCase()
      .normalize('NFKD')
      .replace(/[\u0300-\u036f]/g, '');

    const createResult = (item) => {
      const article = document.createElement('article');
      article.className = 'search-result';

      const link = document.createElement('a');
      link.href = item.url;

      const meta = document.createElement('div');
      meta.className = 'search-result-meta';
      const kind = document.createElement('span');
      kind.textContent = item.kind;
      meta.appendChild(kind);
      if (item.discipline && disciplineNames[item.discipline]) {
        const discipline = document.createElement('span');
        discipline.textContent = disciplineNames[item.discipline];
        meta.appendChild(discipline);
      }

      const title = document.createElement('h2');
      title.textContent = item.title;
      const summary = document.createElement('p');
      summary.textContent = item.summary || '';
      const action = document.createElement('strong');
      action.textContent = 'Open';

      link.append(meta, title, summary, action);
      article.appendChild(link);
      return article;
    };

    const scoreItem = (item, terms) => {
      const title = normalize(item.title);
      const summary = normalize(item.summary);
      const body = normalize(item.body);
      const kind = normalize(item.kind);
      const discipline = normalize(disciplineNames[item.discipline] || item.discipline);
      const journalKind = normalize(item.journalKind);
      const tags = normalize((item.tags || []).join(' '));
      let score = 0;
      for (const term of terms) {
        if (title.includes(term)) score += 12;
        if (title.startsWith(term)) score += 5;
        if (summary.includes(term)) score += 6;
        if (discipline.includes(term)) score += 5;
        if (kind.includes(term)) score += 3;
        if (journalKind.includes(term)) score += 4;
        if (tags.includes(term)) score += 5;
        if (body.includes(term)) score += 2;
        if (![title, summary, body, kind, discipline, journalKind, tags].some((field) => field.includes(term))) return -1;
      }
      return score;
    };

    const renderSearch = (query, updateUrl = true) => {
      const cleanQuery = query.trim();
      const terms = normalize(cleanQuery).split(/\s+/).filter(Boolean);
      let results;

      if (!terms.length) {
        results = searchItems.slice(0, 16);
        searchStatus.textContent = `Showing ${results.length} entries from the studio index.`;
      } else {
        results = searchItems
          .map((item) => ({ item, score: scoreItem(item, terms) }))
          .filter((entry) => entry.score >= 0)
          .sort((a, b) => b.score - a.score || a.item.title.localeCompare(b.item.title))
          .map((entry) => entry.item);
        searchStatus.textContent = results.length
          ? `${results.length} result${results.length === 1 ? '' : 's'} for “${cleanQuery}.”`
          : `No results for “${cleanQuery}.”`;
      }

      searchResults.replaceChildren(...results.map(createResult));
      searchResults.classList.toggle('is-empty', results.length === 0);
      if (!results.length) {
        const empty = document.createElement('p');
        empty.className = 'search-empty';
        empty.textContent = 'Try a profession, working moment, object, or phrase from the piece.';
        searchResults.appendChild(empty);
      }

      if (searchClear) searchClear.hidden = !cleanQuery;

      if (updateUrl) {
        const url = new URL(window.location.href);
        if (cleanQuery) url.searchParams.set('q', cleanQuery);
        else url.searchParams.delete('q');
        window.history.replaceState({}, '', url);
      }
    };

    let searchTimer;
    searchInput.addEventListener('input', () => {
      window.clearTimeout(searchTimer);
      searchTimer = window.setTimeout(() => renderSearch(searchInput.value), 120);
    });

    searchForm?.addEventListener('submit', (event) => {
      event.preventDefault();
      renderSearch(searchInput.value);
    });

    searchClear?.addEventListener('click', () => {
      searchInput.value = '';
      renderSearch('');
      searchInput.focus();
    });

    const initialQuery = new URL(window.location.href).searchParams.get('q') || '';
    searchInput.value = initialQuery;
    renderSearch(initialQuery, false);

    document.addEventListener('keydown', (event) => {
      const target = event.target;
      const isTyping = target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement || target?.isContentEditable;
      if (event.key === '/' && !isTyping) {
        event.preventDefault();
        searchInput.focus();
      }
    });
  }
})();
