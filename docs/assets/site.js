(() => {
  const d = document;
  d.documentElement.classList.add('js');

  // Mobilmeny
  const burger = d.querySelector('.burger');
  const drawer = d.getElementById('drawer');
  if (burger && drawer) {
    const set = (open) => {
      burger.setAttribute('aria-expanded', String(open));
      drawer.hidden = !open;
      d.body.classList.toggle('menu-open', open);
    };
    burger.addEventListener('click', () => set(burger.getAttribute('aria-expanded') !== 'true'));
    drawer.addEventListener('click', (e) => { if (e.target.closest('a')) set(false); });
    d.addEventListener('keydown', (e) => { if (e.key === 'Escape') set(false); });
    matchMedia('(min-width: 1101px)').addEventListener('change', (e) => { if (e.matches) set(false); });
  }

  // Linje under headern när man scrollat
  const hdr = d.querySelector('.site-h');
  const onScroll = () => hdr && hdr.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Tjänstelistan: bilden bredvid följer raden man pekar på
  const fig = d.querySelector('.svc-fig');
  if (fig) {
    const rows = d.querySelectorAll('[data-svc]');
    const show = (v) => {
      fig.querySelectorAll('img').forEach((img) => img.classList.toggle('on', img.dataset.for === v));
      rows.forEach((r) => r.classList.toggle('on', r.dataset.svc === v));
    };
    rows.forEach((r) => {
      r.addEventListener('mouseenter', () => show(r.dataset.svc));
      r.addEventListener('focus', () => show(r.dataset.svc));
    });
  }

  // Bildgallerier
  d.querySelectorAll('[data-car]').forEach((root) => {
    const track = root.querySelector('[data-track]');
    if (!track) return;
    const prev = root.querySelector('[data-prev]');
    const next = root.querySelector('[data-next]');
    const count = root.querySelector('[data-count]');
    const items = [...track.children];
    const step = () => (items[1] ? items[1].offsetLeft - items[0].offsetLeft : track.clientWidth);
    const sync = () => {
      const max = track.scrollWidth - track.clientWidth - 2;
      if (prev) prev.disabled = track.scrollLeft <= 2;
      if (next) next.disabled = track.scrollLeft >= max;
      if (count) count.textContent = `${Math.min(items.length, Math.round(track.scrollLeft / step()) + 1)} / ${items.length}`;
    };
    if (prev) prev.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
    if (next) next.addEventListener('click', () => track.scrollBy({ left: step(), behavior: 'smooth' }));
    track.addEventListener('scroll', () => requestAnimationFrame(sync), { passive: true });
    addEventListener('resize', sync);
    sync();
  });

  const form = d.getElementById('booking');
  if (form) booking(form);

  function booking(form) {
    const MAIL = form.dataset.mail;
    const DAYS = ['Sön', 'Mån', 'Tis', 'Ons', 'Tors', 'Fre', 'Lör'];
    const DAYS_LONG = ['söndag', 'måndag', 'tisdag', 'onsdag', 'torsdag', 'fredag', 'lördag'];
    const MONTHS = ['januari', 'februari', 'mars', 'april', 'maj', 'juni', 'juli', 'augusti', 'september', 'oktober', 'november', 'december'];
    const MON_S = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec'];
    // Vardagar 15–19, helger 9–19 (samma som öppettiderna på sajten)
    const WEEKDAY = [{ id: 'em', label: 'Eftermiddag', short: 'em', time: '15–19', start: 15 }];
    const WEEKEND = [{ id: 'fm', label: 'Förmiddag', short: 'fm', time: '9–13', start: 9 }, { id: 'em', label: 'Eftermiddag', short: 'em', time: '13–19', start: 13 }];
    const WEEKS_AHEAD = 4;

    const kr = (n) => n.toLocaleString('sv-SE') + ' kr';
    const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const steps = [...form.querySelectorAll('.bk-step')];
    const marks = [...form.querySelectorAll('.bk-steps li')];
    const err = form.querySelector('.bk-err');
    const back = form.querySelector('[data-go="-1"]');
    const fwd = form.querySelector('[data-go="1"]');
    const submit = form.querySelector('[type=submit]');
    const done = form.querySelector('.bk-done');
    const f = form.elements;
    let cur = 0;
    let slot = null; // { date: Date, id, label, time }
    let week = 0;

    // Förval från länkar, t.ex. boka.html?tjanst=punktering eller ?paket=paket_cykelcheck
    const q = new URLSearchParams(location.search);
    ['tjanst', 'paket'].forEach((k) => {
      const v = (q.get(k) || '').replace(/^paket_/, '').replace(/_/g, '-');
      const el = v && form.querySelector(`input[name="svc"][value="${CSS.escape(v)}"]`);
      if (el) el.checked = true;
    });

    const selected = () => [...form.querySelectorAll('input[name=svc]:checked')].map((i) => ({ name: i.dataset.name, price: +i.dataset.price }));
    const bikeType = () => {
      const r = form.querySelector('input[name=typ]:checked');
      return { name: r.dataset.name, add: +r.dataset.add };
    };
    const slotText = () => {
      if (f.foreslag.checked) return 'Föreslå en tid åt mig';
      if (!slot) return '';
      const dt = slot.date;
      return `${DAYS_LONG[dt.getDay()]} ${dt.getDate()} ${MONTHS[dt.getMonth()]}, ${slot.label.toLowerCase()} (${slot.time})`;
    };
    const totals = () => {
      const items = selected();
      const t = bikeType();
      const sum = items.reduce((a, b) => a + b.price, 0) + (items.length ? t.add : 0);
      return { items, t, sum, quote: items.some((i) => !i.price) };
    };

    // Sammanfattning
    const sumList = d.getElementById('sum-list');
    const sumMeta = d.getElementById('sum-meta');
    const sumTotal = d.getElementById('sum-total');
    function update() {
      const { items, t, sum, quote } = totals();
      sumList.innerHTML = items.length
        ? items.map((i) => `<li><span>${esc(i.name)}</span><b>${i.price ? kr(i.price) : 'Prisförslag'}</b></li>`).join('')
          + (t.add ? `<li class="add"><span>Tillägg: ${esc(t.name.toLowerCase())}</span><b>+${kr(t.add)}</b></li>` : '')
        : '<li class="empty">Inget valt ännu</li>';
      const meta = [];
      if (slotText()) meta.push(`<p>${icon('calendar')}<span>${esc(slotText())}</span></p>`);
      if (f.adress.value.trim()) meta.push(`<p>${icon('pin')}<span>${esc(f.adress.value.trim())}</span></p>`);
      sumMeta.innerHTML = meta.join('');
      sumTotal.textContent = items.length ? (sum ? kr(sum) + (quote ? ' +' : '') : 'Prisförslag') : '–';
    }
    function icon(name) {
      const paths = {
        calendar: '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
        pin: '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
      };
      return `<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths[name]}</svg>`;
    }
    form.addEventListener('change', () => { err.textContent = ''; update(); });
    form.addEventListener('input', update);

    // Veckokalender
    const weekEl = d.getElementById('week');
    const monday = (() => {
      const t = new Date();
      t.setHours(0, 0, 0, 0);
      t.setDate(t.getDate() - ((t.getDay() + 6) % 7));
      return t;
    })();
    const sameDay = (a, b) => a && b && a.toDateString() === b.toDateString();
    function renderWeek() {
      const now = new Date();
      const start = new Date(monday);
      start.setDate(start.getDate() + week * 7);
      const end = new Date(start);
      end.setDate(end.getDate() + 6);
      const label = week === 0 ? 'Denna vecka' : week === 1 ? 'Nästa vecka' : `Om ${week} veckor`;
      let days = '';
      for (let i = 0; i < 7; i++) {
        const dt = new Date(start);
        dt.setDate(dt.getDate() + i);
        const wknd = dt.getDay() === 0 || dt.getDay() === 6;
        const past = dt < new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const slots = (wknd ? WEEKEND : WEEKDAY).map((s) => {
          const st = new Date(dt);
          st.setHours(s.start, 0, 0, 0);
          const off = st <= now;
          const on = slot && sameDay(slot.date, dt) && slot.id === s.id;
          return `<button type="button" class="slot" data-date="${dt.toISOString()}" data-id="${s.id}" aria-pressed="${on}"${off ? ' disabled' : ''} aria-label="${DAYS_LONG[dt.getDay()]} ${dt.getDate()} ${MONTHS[dt.getMonth()]}, ${s.label.toLowerCase()} ${s.time}"><b>${s.time}</b><small><span class="lg">${s.label}</span><span class="sh">${s.short}</span></small></button>`;
        }).join('');
        days += `<div class="day${past ? ' past' : ''}"><span class="day-n">${DAYS[dt.getDay()]}<small>${dt.getDate()} ${MON_S[dt.getMonth()]}</small></span>${slots}</div>`;
      }
      weekEl.innerHTML = `<div class="wk-head"><div><b>${label}</b><small>${start.getDate()} ${MON_S[start.getMonth()]} – ${end.getDate()} ${MON_S[end.getMonth()]}</small></div>
        <div class="wk-tabs"><button type="button" data-wk="-1" aria-label="Föregående vecka"${week === 0 ? ' disabled' : ''}>‹ Föregående</button><button type="button" data-wk="1" aria-label="Nästa vecka"${week >= WEEKS_AHEAD - 1 ? ' disabled' : ''}>Nästa ›</button></div></div>
        <div class="days">${days}</div>
        <p class="picked">${slot ? `Vald tid: <b>${esc(slotText())}</b>` : 'Ingen tid vald ännu.'}</p>`;
    }
    weekEl.addEventListener('click', (e) => {
      const wk = e.target.closest('[data-wk]');
      if (wk && !wk.disabled) { week += +wk.dataset.wk; renderWeek(); return; }
      const b = e.target.closest('.slot');
      if (!b || b.disabled) return;
      const dt = new Date(b.dataset.date);
      const s = (dt.getDay() === 0 || dt.getDay() === 6 ? WEEKEND : WEEKDAY).find((x) => x.id === b.dataset.id);
      slot = { date: dt, ...s };
      f.foreslag.checked = false;
      err.textContent = '';
      renderWeek();
      update();
    });
    f.foreslag.addEventListener('change', () => { if (f.foreslag.checked) { slot = null; renderWeek(); } });
    renderWeek();

    // Steg
    function show(i) {
      cur = i;
      steps.forEach((s, j) => { s.hidden = j !== i; });
      marks.forEach((m, j) => { m.classList.toggle('on', j === i); m.classList.toggle('done', j < i); });
      back.hidden = i === 0;
      fwd.hidden = i === steps.length - 1;
      submit.hidden = i !== steps.length - 1;
      err.textContent = '';
      const top = form.getBoundingClientRect().top;
      if (top < 0) form.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      steps[i].setAttribute('tabindex', '-1');
      steps[i].focus({ preventScroll: true });
    }
    function fail(msg, el) {
      err.textContent = msg;
      if (el) { el.setAttribute('aria-invalid', 'true'); el.focus(); }
      return false;
    }
    function valid(i) {
      form.querySelectorAll('[aria-invalid]').forEach((el) => el.removeAttribute('aria-invalid'));
      err.textContent = '';
      if (i === 0 && !selected().length) return fail('Välj minst en tjänst eller ett servicepaket.');
      if (i === 1) {
        if (!slot && !f.foreslag.checked) return fail('Välj en tid, eller kryssa i att vi ska föreslå en tid åt dig.');
        if (!f.adress.value.trim()) return fail('Fyll i var cykeln står.', f.adress);
      }
      if (i === 2) {
        if (!f.namn.value.trim()) return fail('Fyll i ditt namn.', f.namn);
        if (f.telefon.value.replace(/\D/g, '').length < 7) return fail('Fyll i ett telefonnummer vi kan nå dig på.', f.telefon);
        if (!f.epost.value.trim() || !f.epost.checkValidity()) return fail('Fyll i en giltig e-postadress.', f.epost);
        if (!f.villkor.checked) return fail('Du behöver godkänna användarvillkoren och integritetspolicyn.', f.villkor);
      }
      return true;
    }
    form.addEventListener('click', (e) => {
      const b = e.target.closest('[data-go]');
      if (!b) return;
      const dir = +b.dataset.go;
      if (dir > 0 && !valid(cur)) return;
      show(cur + dir);
    });
    form.addEventListener('keydown', (e) => {
      // Enter i ett textfält ska ta en till nästa steg, inte skicka formuläret
      if (e.key === 'Enter' && e.target.matches('input:not([type=checkbox]):not([type=radio])') && cur < steps.length - 1) {
        e.preventDefault();
        fwd.click();
      }
    });

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!valid(2)) return;
      const { items, t, sum, quote } = totals();
      const lines = [
        'Bokningsförfrågan via hemmacykel.se',
        '',
        'TJÄNSTER',
        ...items.map((i) => `- ${i.name}: ${i.price ? kr(i.price) : 'prisförslag'}`),
        `Cykeltyp: ${t.name}${t.add ? ` (+${kr(t.add)})` : ''}`,
        `Uppskattat pris: ${sum ? kr(sum) : '–'}${quote ? ' + prisförslag för övrigt' : ''} (reseavgift kan tillkomma)`,
        '',
        'TID OCH PLATS',
        `Önskad tid: ${slotText()}`,
        `Adress: ${f.adress.value.trim()}`,
        f.beskrivning.value.trim() ? `\nBESKRIVNING\n${f.beskrivning.value.trim()}` : null,
        '',
        'KONTAKT',
        `Namn: ${f.namn.value.trim()}`,
        `Telefon: ${f.telefon.value.trim()}`,
        `E-post: ${f.epost.value.trim()}`,
        f.kod.value.trim() ? `Rabattkod: ${f.kod.value.trim()}` : null,
        `Erbjudanden via e-post: ${f.inga_erbjudanden.checked ? 'Nej tack' : 'Ja'}`,
      ].filter((l) => l !== null);
      const body = lines.join('\n');
      const subject = `Bokning: ${items.map((i) => i.name).join(', ')} – ${f.namn.value.trim()}`;
      form.querySelector('.bk-copy').textContent = body;
      steps.forEach((s) => { s.hidden = true; });
      form.querySelector('.bk-steps').hidden = true;
      form.querySelector('.bk-nav').hidden = true;
      err.textContent = '';
      done.hidden = false;
      done.focus();
      location.href = `mailto:${MAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    });

    update();
  }
})();
