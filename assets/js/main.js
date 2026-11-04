// Godot & Fils Chartres — interactions et animations légères
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce) document.documentElement.classList.add('motion');

  // ---------------------------------------------------------------- Menu mobile
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  function setMenu(open) {
    nav.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); toggle.focus(); } });
    window.addEventListener('resize', function () { if (window.innerWidth > 1220 && nav.classList.contains('open')) setMenu(false); });
  }


  // Méga menu « Nos services » (ordinateur) : survol avec court délai, clic, clavier
  var dd = document.querySelector('.menu-dd');
  if (dd) {
    var ddBtn = dd.querySelector('.menu-dd-btn'), timer = null;
    var wideMenu = function () { return window.innerWidth > 1220; };
    var setDD = function (o) {
      dd.classList.toggle('open', o);
      ddBtn.setAttribute('aria-expanded', String(o));
      document.body.classList.toggle('mega-open', o && wideMenu());
    };
    ddBtn.addEventListener('click', function () { setDD(!dd.classList.contains('open')); });
    dd.addEventListener('mouseenter', function () { if (!wideMenu()) return; clearTimeout(timer); setDD(true); });
    dd.addEventListener('mouseleave', function () { clearTimeout(timer); timer = setTimeout(function () { setDD(false); }, 220); });
    dd.addEventListener('focusout', function (e) { if (!dd.contains(e.relatedTarget)) setDD(false); });
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) setDD(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && dd.classList.contains('open')) { setDD(false); ddBtn.focus(); } });
    window.addEventListener('resize', function () { if (!wideMenu()) setDD(false); });
  }

  // Surlignage glissant dans la barre de menu (ordinateur)
  var linksBar = document.querySelector('.menu-links');
  var glide = linksBar && linksBar.querySelector('.menu-glide');
  if (glide) {
    var targets = linksBar.querySelectorAll(':scope > a, :scope > .menu-dd > .menu-dd-btn');
    var moveGlide = function (el) {
      if (window.innerWidth <= 1220) return;
      var hidden = getComputedStyle(glide).opacity === '0';
      if (hidden) glide.style.transition = 'none';
      glide.style.left = el.offsetLeft + 'px';
      glide.style.width = el.offsetWidth + 'px';
      if (hidden) { void glide.offsetWidth; glide.style.transition = ''; }
      glide.style.opacity = '1';
    };
    targets.forEach(function (el) {
      el.addEventListener('mouseenter', function () { moveGlide(el); });
      el.addEventListener('focus', function () { moveGlide(el); });
    });
    linksBar.addEventListener('mouseleave', function () { glide.style.opacity = '0'; });
    linksBar.addEventListener('focusout', function (e) { if (!linksBar.contains(e.relatedTarget)) glide.style.opacity = '0'; });
  }

  // Méga menu au clavier : flèche bas pour ouvrir, flèches pour naviguer, Début/Fin
  var ddRoot = document.querySelector('.menu-dd');
  if (ddRoot) {
    var ddButton = ddRoot.querySelector('.menu-dd-btn'), panelLinks = ddRoot.querySelectorAll('.menu-panel a');
    ddButton.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown' && window.innerWidth > 1220) {
        e.preventDefault(); ddRoot.classList.add('open'); ddButton.setAttribute('aria-expanded', 'true');
        document.body.classList.add('mega-open');
        window.requestAnimationFrame(function () { panelLinks[0].focus(); });
      }
    });
    ddRoot.querySelector('.menu-panel').addEventListener('keydown', function (e) {
      var list = Array.prototype.slice.call(panelLinks), i = list.indexOf(document.activeElement), n = list.length;
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); list[(i + 1) % n].focus(); }
      else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); list[(i - 1 + n) % n].focus(); }
      else if (e.key === 'Home') { e.preventDefault(); list[0].focus(); }
      else if (e.key === 'End') { e.preventDefault(); list[n - 1].focus(); }
    });
  }

  // ---------------------------------------------------------------- Statut ouvert / fermé (heure de Paris, lun–ven 9h30–18h00)
  var HOURS = { 1: [570, 1080], 2: [570, 1080], 3: [570, 1080], 4: [570, 1080], 5: [570, 1080] };
  function parisNow() {
    var parts = new Intl.DateTimeFormat('en-GB', {
      timeZone: 'Europe/Paris', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false
    }).formatToParts(new Date());
    var map = {};
    parts.forEach(function (p) { map[p.type] = p.value; });
    var days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    return { day: days[map.weekday], minutes: (parseInt(map.hour, 10) % 24) * 60 + parseInt(map.minute, 10) };
  }
  try {
    var now = parisNow();
    var slot = HOURS[now.day];
    var open = slot && now.minutes >= slot[0] && now.minutes < slot[1];
    var sat = now.day === 6;
    document.querySelectorAll('[data-open-status]').forEach(function (status) {
      var short = status.hasAttribute('data-short');
      status.classList.add(open ? 'is-open' : (sat ? 'is-rdv' : 'is-closed'));
      status.querySelector('.status-text').textContent = open
        ? (short ? "Ouvert · jusqu'à 18h" : "Ouvert en ce moment · jusqu'à 18h00")
        : (sat ? (short ? 'Sam. matin sur RDV' : 'Samedi matin : sur rendez-vous')
               : (short ? 'Fermé · lun–ven 9h30–18h' : 'Fermé actuellement · ouvert du lundi au vendredi'));
    });
    var row = document.querySelector('.hours tr[data-day="' + now.day + '"]');
    if (row) row.classList.add('today');
  } catch (e) { /* navigateur sans Intl : on garde le texte par défaut */ }

  // Année du pied de page
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();

  // ---------------------------------------------------------------- Apparition au défilement (décalée, directionnelle)
  var SEL = '.section-head, .card, .card-row, .other-card, .coin-card, .tips li, .steps li, .formula > *, ' +
            '.faq details, .contact-grid > *, .split > *, .network > *, .notice, .table-wrap, ' +
            '.cta-inner > *, .footer-grid > *, .checks li, .tl-card, .history-stats > div, .bento-card, .tsteps li';
  if (!reduce && 'IntersectionObserver' in window) {
    var wide = window.matchMedia('(min-width: 861px)').matches;
    var items = Array.prototype.slice.call(document.querySelectorAll(SEL));
    // On ignore les éléments imbriqués dans un autre élément animé du même bloc pour éviter les doubles effets
    items = items.filter(function (el) { return !el.closest('.panel') && !el.closest('.hero'); });
    var rank = new Map();
    items.forEach(function (el) {
      var n = rank.get(el.parentNode) || 0;
      rank.set(el.parentNode, n + 1);
      el._delay = Math.min(n, 6) * 80;
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        io.unobserve(el);
        el.style.transitionDelay = el._delay + 'ms';
        el.classList.add('visible');
        // Une fois l'animation jouée, on rend l'élément à son style normal (survols, etc.)
        setTimeout(function () {
          el.classList.remove('reveal', 'reveal-left', 'reveal-right', 'reveal-pop', 'visible');
          el.style.transitionDelay = '';
        }, el._delay + 900);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    items.forEach(function (el) {
      el.classList.add('reveal');
      if (wide && el.matches('.split > *')) el.classList.add(el === el.parentNode.firstElementChild ? 'reveal-left' : 'reveal-right');
      else if (el.matches('.coin-card, .f-box, .tips li, .steps li, .tsteps li, .bento-card')) el.classList.add('reveal-pop');
      io.observe(el);
    });
  }

  // ---------------------------------------------------------------- Défilement : barre de progression, en-tête, parallaxe
  var header = document.querySelector('.site-header');
  var hero = document.querySelector('.hero-photo');
  var timeline = document.querySelector('.timeline');
  var tlItems = timeline ? Array.prototype.slice.call(timeline.querySelectorAll('.tl-item')) : [];
  var bar = null;
  if (!reduce) {
    bar = document.createElement('div');
    bar.className = 'progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.appendChild(bar);
  }
  var ticking = false;
  function onScroll() {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if (header) header.classList.toggle('is-scrolled', y > 8);
    if (bar) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(y / max, 1) : 0) + ')';
    }
    if (hero && !reduce && y < window.innerHeight * 1.2) hero.style.setProperty('--py', (y * 0.14).toFixed(1) + 'px');
    if (timeline) {
      var r = timeline.getBoundingClientRect(), vh = window.innerHeight;
      var prog = Math.max(0, Math.min(1, (vh * 0.62 - r.top) / r.height));
      timeline.style.setProperty('--tl', reduce ? 1 : prog.toFixed(3));
      tlItems.forEach(function (it) { it.classList.toggle('reached', reduce || it.getBoundingClientRect().top < vh * 0.62); });
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  // Années d'expérience : calculées à partir de l'année de fondation
  document.querySelectorAll('[data-since]').forEach(function (el) {
    var n = new Date().getFullYear() - parseInt(el.getAttribute('data-since'), 10);
    if (n > 0) { el.textContent = String(n); el.setAttribute('data-count', String(n)); el.setAttribute('data-from', '0'); }
  });

  // ---------------------------------------------------------------- Compteurs (année de fondation)
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length && !reduce && 'IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        co.unobserve(en.target);
        var el = en.target, to = parseInt(el.getAttribute('data-count'), 10), from = parseInt(el.getAttribute('data-from'), 10) || 0;
        var t0 = null, dur = 1200;
        function step(t) {
          if (t0 === null) t0 = t;
          var p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
          el.textContent = String(Math.round(from + (to - from) * e));
          if (p < 1) window.requestAnimationFrame(step); else el.textContent = String(to);
        }
        window.requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { co.observe(el); });
  }
})();

// ---------------------------------------------------------------- Carte du réseau
(function () {
  var section = document.getElementById('reseau');
  if (!section) return;
  var triggers = section.querySelectorAll('[data-target]');
  var panels = section.querySelectorAll('.panel');
  function show(id) {
    panels.forEach(function (p) { p.classList.toggle('is-active', p.id === id); });
    triggers.forEach(function (t) {
      var on = t.getAttribute('data-target') === id;
      t.classList.toggle('is-active', on);
      if (t.tagName === 'BUTTON') t.setAttribute('aria-pressed', String(on));
    });
  }
  triggers.forEach(function (t) {
    t.addEventListener('click', function () { show(t.getAttribute('data-target')); });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(t.getAttribute('data-target')); }
    });
  });
  show(section.getAttribute('data-default'));

  // Les points apparaissent un à un quand la carte entre dans l'écran
  var map = section.querySelector('.map-france');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!map) return;
  if (reduce || !('IntersectionObserver' in window)) { map.classList.add('in'); return; }
  var pins = map.querySelectorAll('.pin');
  var mo = new IntersectionObserver(function (entries) {
    if (!entries[0].isIntersecting) return;
    mo.disconnect();
    pins.forEach(function (p, i) { p.style.setProperty('--d', (350 + i * 40) + 'ms'); });
    map.classList.add('in');
    setTimeout(function () { pins.forEach(function (p) { p.style.removeProperty('--d'); }); }, 350 + pins.length * 40 + 900);
  }, { threshold: 0.25 });
  mo.observe(map);
})();

// ---------------------------------------------------------------- Avis : carrousel
(function () {
  var root = document.querySelector('[data-reviews]');
  if (!root) return;
  var track = root.querySelector('.reviews-track');
  var prev = root.querySelector('[data-rev="prev"]'), next = root.querySelector('[data-rev="next"]');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function step() {
    var card = track.querySelector('.review');
    return card ? card.getBoundingClientRect().width + 20 : 300;
  }
  function update() {
    prev.disabled = track.scrollLeft <= 4;
    next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
  }
  prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: reduce ? 'auto' : 'smooth' }); });
  next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: reduce ? 'auto' : 'smooth' }); });
  track.addEventListener('scroll', function () { window.requestAnimationFrame(update); }, { passive: true });
  track.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') { e.preventDefault(); next.click(); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); prev.click(); }
  });
  window.addEventListener('resize', update);
  update();
})();

// ---------------------------------------------------------------- Graphique du prix de l'or + barres de comparaison
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var blocks = document.querySelectorAll('[data-chart], [data-compare]');
  if (!blocks.length) return;

  // Déclenche le tracé / la croissance des barres quand le bloc entre à l'écran
  if (reduce || !('IntersectionObserver' in window)) {
    blocks.forEach(function (b) { b.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.3 });
    blocks.forEach(function (b) { io.observe(b); });
  }

  // Infobulle : survol (souris/tactile) et focus clavier
  document.querySelectorAll('[data-chart]').forEach(function (card) {
    var wrap = card.querySelector('.chart-wrap'), tip = card.querySelector('.chart-tip');
    var pts = Array.prototype.slice.call(card.querySelectorAll('.ch-pt'));
    var current = null;
    function show(pt) {
      if (current && current !== pt) current.classList.remove('is-hot');
      current = pt; pt.classList.add('is-hot');
      var r = pt.getBoundingClientRect(), w = wrap.getBoundingClientRect();
      tip.textContent = pt.getAttribute('data-label');
      tip.hidden = false;
      var x = r.left + r.width / 2 - w.left;
      var half = tip.offsetWidth / 2;
      x = Math.max(half, Math.min(w.width - half, x));
      tip.style.left = x + 'px';
      tip.style.top = (r.top + r.height / 2 - w.top) + 'px';
    }
    function hide() { if (current) current.classList.remove('is-hot'); current = null; tip.hidden = true; }
    wrap.addEventListener('pointermove', function (e) {
      var best = null, bd = 1e9;
      pts.forEach(function (p) {
        var r = p.getBoundingClientRect(), d = Math.abs(e.clientX - (r.left + r.width / 2));
        if (d < bd) { bd = d; best = p; }
      });
      if (best) show(best);
    });
    wrap.addEventListener('pointerleave', hide);
    pts.forEach(function (p) {
      p.addEventListener('focus', function () { show(p); });
      p.addEventListener('blur', hide);
      p.addEventListener('keydown', function (e) {
        var i = pts.indexOf(p);
        if (e.key === 'ArrowRight' && pts[i + 1]) { e.preventDefault(); pts[i + 1].focus(); }
        if (e.key === 'ArrowLeft' && pts[i - 1]) { e.preventDefault(); pts[i - 1].focus(); }
      });
    });
  });
})();

// ---------------------------------------------------------------- Comparateur de placements : courbes + simulateur (inflation déduite)
(function () {
  var dataEl = document.getElementById('cmp-data');
  if (!dataEl) return;
  var D = JSON.parse(dataEl.textContent), ALL = D.series, YEARS = [2000].concat(D.years);
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var INF = ALL.filter(function (s) { return s.ref; })[0];
  var A = ALL.filter(function (s) { return !s.ref; });
  var state = { real: false, start: 2000, scale: 'log', hidden: {}, cursor: null };

  // Niveaux cumulés (indice 0 = fin 2000, base 100) pour chaque placement et pour les prix
  function levels(r) { var l = [100]; r.forEach(function (x) { l.push(l[l.length - 1] * (1 + x / 100)); }); return l; }
  A.forEach(function (s) { s.levels = levels(s.returns); });
  var P = levels(INF.returns);
  var byId = {}; A.forEach(function (s) { byId[s.id] = s; });

  var fr = function (n, d) { return n.toLocaleString('fr-FR', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); };
  var mult = function (v) { var m = v / 100; return '× ' + (m < 10 ? fr(m, 1) : fr(m, 0)); };
  var short = { or: 'Or', sp: 'S&P 500', cac: 'CAC 40', immo: 'Immobilier', livret: 'Livret A' };
  var cagr = function (r, n) { var p = 1; r.slice(-n).forEach(function (x) { p *= 1 + x / 100; }); return Math.pow(p, 1 / n) - 1; };
  var pct = new Intl.NumberFormat('fr-FR', { style: 'percent', minimumFractionDigits: 1, maximumFractionDigits: 1, signDisplay: 'always' });
  var pf = function (x) { return pct.format(x).replace('-', '−'); };
  var eur = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
  var realRet = function (r) { return r.map(function (x, i) { return ((1 + x / 100) / (1 + INF.returns[i] / 100) - 1) * 100; }); };

  var listeners = [];   // fonctions à rappeler quand on (dés)active la déduction de l'inflation

  // ================================================================ GRAPHIQUE
  var root = document.querySelector('[data-cmp]');
  if (root) {
    var host = root.querySelector('[data-cmp-chart]'), tip = root.querySelector('.cmp-tip');
    host.tabIndex = 0;
    var svgNS = 'http://www.w3.org/2000/svg';
    var LOG_TICKS = [20, 30, 50, 70, 100, 150, 200, 300, 500, 700, 1000, 1500, 2000, 3000, 5000];
    function niceStep(range) { var raw = range / 5, p = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / p; return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p; }

    function render() {
      var W = Math.max(280, host.clientWidth), narrow = W < 560;
      var H = narrow ? 340 : Math.round(Math.min(470, W * 0.48));
      var ml = narrow ? 44 : 54, mr = narrow ? 58 : 128, mt = 14, mb = 30;
      var i0 = YEARS.indexOf(state.start), n = YEARS.length - 1;
      var vis = A.filter(function (s) { return !state.hidden[s.id]; });
      var pts = {};
      vis.forEach(function (s) {
        pts[s.id] = YEARS.slice(i0).map(function (y, k) {
          var v = 100 * s.levels[i0 + k] / s.levels[i0];
          return state.real ? v / (P[i0 + k] / P[i0]) : v;          // inflation déduite : on divise par l'indice des prix
        });
      });
      var vmin = 100, vmax = 100;
      vis.forEach(function (s) { pts[s.id].forEach(function (v) { vmin = Math.min(vmin, v); vmax = Math.max(vmax, v); }); });
      var lo, hi, ticks = [];
      if (state.scale === 'log') {
        lo = LOG_TICKS.filter(function (t) { return t <= vmin * 0.97; }).pop() || LOG_TICKS[0];
        hi = LOG_TICKS.filter(function (t) { return t >= vmax * 1.03; })[0] || LOG_TICKS[LOG_TICKS.length - 1];
        ticks = LOG_TICKS.filter(function (t) { return t >= lo && t <= hi; });
      } else {
        var step = niceStep(vmax); lo = 0; hi = Math.ceil(vmax * 1.04 / step) * step;
        for (var t = 0; t <= hi + 1e-9; t += step) ticks.push(t);
      }
      var X = function (k) { return ml + (k / (n - i0)) * (W - ml - mr); };
      var Y = function (v) {
        var r = state.scale === 'log' ? (Math.log(v) - Math.log(lo)) / (Math.log(hi) - Math.log(lo)) : (v - lo) / (hi - lo);
        return mt + (1 - r) * (H - mt - mb);
      };
      var sp = n - i0, xs = sp > 16 ? 5 : sp > 8 ? 2 : 1;
      var out = '<svg class="cmp-svg" width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + ' ' + H + '" aria-hidden="true">';
      ticks.forEach(function (t) {
        out += '<line class="cmp-grid' + (t === 100 ? ' cmp-base' : '') + '" x1="' + ml + '" x2="' + (W - mr) + '" y1="' + Y(t).toFixed(1) + '" y2="' + Y(t).toFixed(1) + '"/>' +
               '<text class="cmp-tick" x="' + (ml - 8) + '" y="' + (Y(t) + 4).toFixed(1) + '" text-anchor="end">' + fr(t) + '</text>';
      });
      for (var k = 0; k <= sp; k++) if (k % xs === 0) out += '<text class="cmp-tick" x="' + X(k).toFixed(1) + '" y="' + (H - 8) + '" text-anchor="middle">' + YEARS[i0 + k] + '</text>';
      vis.forEach(function (s) {
        var d = pts[s.id].map(function (v, kk) { return (kk ? 'L' : 'M') + X(kk).toFixed(1) + ' ' + Y(v).toFixed(1); }).join(' ');
        out += '<path class="cmp-line" pathLength="1" d="' + d + '" stroke="' + s.color + '"/>';
      });
      var labs = vis.map(function (s) { var v = pts[s.id][sp]; return { s: s, y: Y(v), v: v }; }).sort(function (a, b) { return a.y - b.y; });
      for (var q = 1; q < labs.length; q++) if (labs[q].y - labs[q - 1].y < 15) labs[q].y = labs[q - 1].y + 15;
      labs.forEach(function (l) {
        out += '<circle cx="' + X(sp).toFixed(1) + '" cy="' + Y(l.v).toFixed(1) + '" r="3.6" fill="' + l.s.color + '"/>' +
               '<text class="cmp-end" x="' + (X(sp) + 9).toFixed(1) + '" y="' + (l.y + 4).toFixed(1) + '" fill="' + l.s.color + '">' + (narrow ? mult(l.v) : short[l.s.id] + ' ' + mult(l.v)) + '</text>';
      });
      out += '<g class="cmp-cursor" hidden><line y1="' + mt + '" y2="' + (H - mb) + '"/></g></svg>';
      host.innerHTML = out;
      host._geo = { X: X, Y: Y, pts: pts, vis: vis, i0: i0, sp: sp, W: W, H: H, ml: ml, mr: mr, mt: mt, mb: mb };
      host.setAttribute('aria-label', 'Courbes comparées depuis ' + state.start + ', base 100, ' + (state.real ? 'inflation déduite' : 'avant inflation') + '. ' + labs.map(function (l) { return short[l.s.id] + ' ' + mult(l.v); }).join(', ') + '.');
      if (state.cursor !== null) showCursor(Math.min(state.cursor, sp));
    }

    function showCursor(k) {
      var g = host._geo; if (!g) return;
      state.cursor = k;
      var svg = host.querySelector('.cmp-svg'), cur = svg.querySelector('.cmp-cursor');
      cur.removeAttribute('hidden');
      var x = g.X(k);
      cur.querySelector('line').setAttribute('x1', x); cur.querySelector('line').setAttribute('x2', x);
      Array.prototype.forEach.call(cur.querySelectorAll('circle'), function (c) { c.remove(); });
      var rows = '';
      g.vis.forEach(function (s) {
        var v = g.pts[s.id][k];
        var c = document.createElementNS(svgNS, 'circle');
        c.setAttribute('cx', x); c.setAttribute('cy', g.Y(v)); c.setAttribute('r', 4.6); c.setAttribute('fill', s.color); c.setAttribute('stroke', '#080808'); c.setAttribute('stroke-width', 1.5);
        cur.appendChild(c);
        rows += '<li><span class="sw" style="--c:' + s.color + '"></span><span>' + short[s.id] + '</span><b>' + mult(v) + '</b></li>';
      });
      tip.innerHTML = '<strong>' + YEARS[g.i0 + k] + '</strong><span class="tip-sub">base 100 en ' + state.start + ' · ' + (state.real ? 'inflation déduite' : 'avant inflation') + '</span><ul>' + rows + '</ul>';
      tip.hidden = false;
      var half = tip.offsetWidth / 2, left = Math.max(half + 4, Math.min(g.W - half - 4, x + 16));
      tip.style.left = left + 'px';
    }
    function hideCursor() { state.cursor = null; tip.hidden = true; var c = host.querySelector('.cmp-cursor'); if (c) c.setAttribute('hidden', ''); }

    host.addEventListener('pointermove', function (e) {
      var g = host._geo; if (!g) return;
      var r = host.getBoundingClientRect(), x = e.clientX - r.left;
      var k = Math.round(((x - g.ml) / (g.W - g.ml - g.mr)) * g.sp);
      if (x < g.ml - 10 || k < 0 || k > g.sp) { hideCursor(); return; }
      showCursor(Math.max(0, Math.min(g.sp, k)));
    });
    host.addEventListener('pointerleave', hideCursor);
    host.addEventListener('blur', hideCursor);
    host.addEventListener('keydown', function (e) {
      var g = host._geo; if (!g) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); showCursor(Math.min(g.sp, (state.cursor === null ? -1 : state.cursor) + 1)); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); showCursor(Math.max(0, (state.cursor === null ? g.sp + 1 : state.cursor) - 1)); }
      if (e.key === 'Escape') hideCursor();
    });
    function redraw(animate) {
      render();
      if (animate && !reduce) { root.classList.remove('in'); void root.offsetWidth; window.requestAnimationFrame(function () { root.classList.add('in'); }); }
    }
    root.querySelector('[data-cmp-start]').addEventListener('change', function (e) { state.start = parseInt(e.target.value, 10); hideCursor(); redraw(true); });
    Array.prototype.forEach.call(root.querySelectorAll('[data-cmp-scale]'), function (b) {
      b.addEventListener('click', function () {
        state.scale = b.getAttribute('data-cmp-scale');
        Array.prototype.forEach.call(root.querySelectorAll('[data-cmp-scale]'), function (o) { var on = o === b; o.classList.toggle('is-on', on); o.setAttribute('aria-pressed', String(on)); });
        redraw(true);
      });
    });
    Array.prototype.forEach.call(root.querySelectorAll('[data-series]'), function (b) {
      b.addEventListener('click', function () {
        var id = b.getAttribute('data-series'), hiddenCount = Object.keys(state.hidden).filter(function (k) { return state.hidden[k]; }).length;
        if (!state.hidden[id] && hiddenCount >= A.length - 1) return;
        state.hidden[id] = !state.hidden[id];
        b.setAttribute('aria-pressed', String(!state.hidden[id]));
        redraw(false);
      });
    });
    listeners.push(function () { redraw(true); });
    render();
    if (reduce || !('IntersectionObserver' in window)) root.classList.add('in');
    else new IntersectionObserver(function (en, io) { if (en[0].isIntersecting) { root.classList.add('in'); io.disconnect(); } }, { threshold: 0.25 }).observe(root);
    var raf = 0, lastW = host.clientWidth;
    if ('ResizeObserver' in window) new ResizeObserver(function () {
      if (Math.abs(host.clientWidth - lastW) < 2) return;
      lastW = host.clientWidth; cancelAnimationFrame(raf); raf = requestAnimationFrame(render);
    }).observe(host);
  }

  // ================================================================ SIMULATEUR
  var form = document.querySelector('[data-sim]');
  if (form) {
    var amountEl = form.querySelector('[data-sim-amount]'), yearsEl = form.querySelector('[data-sim-years]'), winEl = form.querySelector('[data-sim-window]');
    var body = document.querySelector('[data-sim-body]'), cap = document.querySelector('[data-sim-caption]'), note = document.querySelector('[data-sim-infl]');
    var thVal = document.querySelector('[data-sim-th-val]'), thWorst = document.querySelector('[data-sim-th-worst]');
    var clamp = function (v, a, b, d) { v = parseFloat(v); return isFinite(v) ? Math.max(a, Math.min(b, v)) : d; };
    function update() {
      var amount = clamp(amountEl.value, 100, 1e7, 10000), years = Math.round(clamp(yearsEl.value, 1, 50, 10)), win = parseInt(winEl.value, 10), real = state.real;
      var ig = cagr(INF.returns, win);
      var rows = A.map(function (s) {
        var nom = cagr(s.returns, win), rr = (1 + nom) / (1 + ig) - 1;
        var val = amount * Math.pow(1 + (real ? rr : nom), years);
        var rets = real ? realRet(s.returns) : s.returns;
        return { s: s, nom: nom, rr: rr, val: val, worst: Math.min.apply(null, rets.slice(-win)) / 100 };
      }).sort(function (a, b) { return b.val - a.val; });
      var top = rows[0].val;
      body.innerHTML = rows.map(function (r) {
        var gain = r.val - amount;
        return '<tr class="sim-row"><th scope="row"><span class="sw" style="--c:' + r.s.color + '"></span>' + r.s.label + (r.s.approx ? ' <abbr title="Estimation arrondie">≈</abbr>' : '') + '</th>' +
          '<td data-label="Avant inflation" class="' + (real ? '' : 'on') + '">' + pf(r.nom) + '<small>/an</small></td>' +
          '<td data-label="Après inflation" class="' + (real ? 'on' : '') + '">' + pf(r.rr) + '<small>/an</small></td>' +
          '<td data-label="Valeur finale"><strong>' + eur.format(r.val) + '</strong><span class="mini-bar"><i style="--w:' + (r.val / top * 100).toFixed(1) + '%;--c:' + r.s.color + '"></i></span></td>' +
          '<td data-label="Gain">' + (gain >= 0 ? '+' : '−') + eur.format(Math.abs(gain)) + '</td><td data-label="Pire année">' + pf(r.worst) + '</td></tr>';
      }).join('');
      cap.textContent = 'Avec ' + eur.format(amount) + ' placés pendant ' + years + (years > 1 ? ' ans' : ' an') + ', au rendement annuel moyen des ' + win + ' dernières années' + (real ? ', inflation déduite.' : ', avant inflation.');
      thVal.innerHTML = 'Valeur finale<br><small>' + (real ? 'en euros d’aujourd’hui' : 'en euros courants') + '</small>';
      thWorst.innerHTML = 'Pire année<br><small>' + (real ? 'après inflation' : 'avant inflation') + '</small>';
      note.innerHTML = real
        ? 'L’inflation moyenne sur cette période (<strong>' + pf(ig) + '/an</strong>, Insee) est <strong>déduite</strong> : les valeurs sont exprimées en euros d’aujourd’hui, c’est-à-dire en pouvoir d’achat.'
        : 'Valeurs en euros courants, <strong>sans déduire l’inflation</strong> (' + pf(ig) + '/an en moyenne sur cette période) : le pouvoir d’achat réel est plus faible.';
    }
    ['input', 'change'].forEach(function (ev) { form.addEventListener(ev, update); });
    listeners.push(update);
    update();
  }

  // ================================================================ MATRICE PAR PÉRIODE
  var mat = document.querySelector('[data-matrix]');
  if (mat) {
    var thead = mat.querySelector('thead'), tbody = mat.querySelector('tbody'), tfoot = mat.querySelector('tfoot');
    function drawMatrix() {
      var real = state.real, W = D.windows;
      var rate = function (s, n) { var g = cagr(s.returns, n); return real ? (1 + g) / (1 + cagr(INF.returns, n)) - 1 : g; };
      thead.innerHTML = '<tr><th scope="col" data-matrix-title>' + (real ? 'Rendement annuel moyen après inflation' : 'Rendement annuel moyen avant inflation') + '</th>' + W.map(function (w) { return '<th scope="col">' + w.label + '</th>'; }).join('') + '</tr>';
      var best = {};
      W.forEach(function (w) { best[w.n] = A.slice().sort(function (a, b) { return rate(b, w.n) - rate(a, w.n); })[0].id; });
      tbody.innerHTML = A.map(function (s) {
        return '<tr><th scope="row"><span class="sw" style="--c:' + s.color + '"></span>' + s.label + (s.approx ? ' ≈' : '') + '</th>' +
          W.map(function (w) { return '<td class="' + (best[w.n] === s.id ? 'best' : '') + '">' + pf(rate(s, w.n)) + '</td>'; }).join('') + '</tr>';
      }).join('');
      tfoot.innerHTML = '<tr class="ref"><th scope="row" data-matrix-foot>' + (real ? 'Inflation moyenne (déjà déduite)' : 'Pour mémoire : inflation moyenne') + '</th>' +
        W.map(function (w) { return '<td>' + pf(cagr(INF.returns, w.n)) + '</td>'; }).join('') + '</tr>';
    }
    listeners.push(drawMatrix);
  }

  // ================================================================ INTERRUPTEUR « APRÈS INFLATION » (synchronisé partout)
  var switches = Array.prototype.slice.call(document.querySelectorAll('[data-real]'));
  switches.forEach(function (sw) {
    sw.addEventListener('change', function () {
      state.real = sw.checked;
      switches.forEach(function (o) { o.checked = state.real; });
      listeners.forEach(function (f) { f(); });
    });
  });
})();

// ---------------------------------------------------------------- Galerie : visionneuse (dialogue natif)
(function () {
  var btns = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));
  if (!btns.length || typeof HTMLDialogElement === 'undefined') return;
  var dlg = document.createElement('dialog');
  dlg.className = 'lightbox';
  dlg.setAttribute('aria-label', 'Photo agrandie');
  dlg.innerHTML = '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button type="button" class="lb-btn lb-prev" aria-label="Photo précédente"><span aria-hidden="true">‹</span></button>' +
    '<button type="button" class="lb-btn lb-next" aria-label="Photo suivante"><span aria-hidden="true">›</span></button>' +
    '<button type="button" class="lb-btn lb-close" aria-label="Fermer"><span aria-hidden="true">×</span></button>';
  document.body.appendChild(dlg);
  var img = dlg.querySelector('img'), cap = dlg.querySelector('figcaption'), cur = 0, opener = null;
  function show(i) {
    cur = (i + btns.length) % btns.length;
    var b = btns[cur];
    img.src = b.getAttribute('data-lightbox'); img.alt = b.getAttribute('data-alt') || '';
    cap.textContent = b.getAttribute('data-caption') || '';
  }
  btns.forEach(function (b, i) { b.addEventListener('click', function () { opener = b; show(i); dlg.showModal(); }); });
  dlg.querySelector('.lb-prev').addEventListener('click', function () { show(cur - 1); });
  dlg.querySelector('.lb-next').addEventListener('click', function () { show(cur + 1); });
  dlg.querySelector('.lb-close').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });       // clic sur le fond
  dlg.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') show(cur - 1);
    if (e.key === 'ArrowRight') show(cur + 1);
  });
  dlg.addEventListener('close', function () { if (opener) opener.focus(); });
})();


// ---------------------------------------------------------------- Cours de l'or et de l'argent (accueil)
// Les données viennent de /api/cours (fonction serverless du site) : le navigateur n'appelle aucun service tiers.
(function () {
  var box = document.querySelector('[data-prices]');
  if (!box || !window.fetch) return;
  var timeEl = box.querySelector('[data-prices-time]');
  var nf2 = new Intl.NumberFormat('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var pf = new Intl.NumberFormat('fr-FR', { minimumFractionDigits: 1, maximumFractionDigits: 1, signDisplay: 'exceptZero' });
  var tf = new Intl.DateTimeFormat('fr-FR', { hour: '2-digit', minute: '2-digit' });
  var df = { '1d': { hour: '2-digit', minute: '2-digit' }, '7d': { weekday: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }, '1m': { day: 'numeric', month: 'short' }, '1y': { day: 'numeric', month: 'short', year: 'numeric' }, '5y': { month: 'short', year: 'numeric' } };
  var colors = { or: '#e2ab45', argent: '#cfd3d8' };
  var range = '5y', last = {}, data = null, svgNS = 'http://www.w3.org/2000/svg';

  function set(key, text) {
    var el = box.querySelector('[data-p="' + key + '"]');
    if (!el) return;
    if (last[key] !== undefined && last[key] !== text) {
      var card = el.closest('.price-card');
      if (card) { card.classList.remove('flash'); void card.offsetWidth; card.classList.add('flash'); }
    }
    last[key] = text; el.textContent = text;
  }

  function chart(metal) {
    var host = box.querySelector('[data-pchart="' + metal + '"]');
    var v = box.querySelector('[data-var="' + metal + '"]');
    var hist = data && data.history && data.history[metal];
    if (!hist || hist.length < 2) {
      host.innerHTML = '<div class="pc-empty">Courbe indisponible pour le moment</div>'; v.textContent = ''; v.className = 'price-var';
      host.setAttribute('aria-label', 'Courbe indisponible'); return;
    }
    var n = hist.length, W = 600, H = 150, pt = 10, pb = 8;
    var min = Infinity, max = -Infinity;
    hist.forEach(function (p) { if (p[1] < min) min = p[1]; if (p[1] > max) max = p[1]; });
    var pad = (max - min) * .12 || max * .01; min -= pad; max += pad;
    function X(i) { return (i / (n - 1)) * W; }
    function Y(val) { return pt + (1 - (val - min) / (max - min)) * (H - pt - pb); }
    var d = hist.map(function (p, i) { return (i ? 'L' : 'M') + X(i).toFixed(1) + ' ' + Y(p[1]).toFixed(1); }).join('');
    var gid = 'pcg-' + metal;
    var grid = [0, 1, 2].map(function (g) { var y = pt + g * (H - pt - pb) / 2; return '<line class="pc-grid" x1="0" x2="' + W + '" y1="' + y + '" y2="' + y + '"/>'; }).join('');
    host.style.setProperty('--c', colors[metal]);
    host.innerHTML = '<svg viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none" aria-hidden="true">' +
      '<defs><linearGradient id="' + gid + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + colors[metal] + '" stop-opacity=".28"/><stop offset="1" stop-color="' + colors[metal] + '" stop-opacity="0"/></linearGradient></defs>' +
      grid + '<path d="' + d + 'L' + W + ' ' + H + 'L0 ' + H + 'Z" fill="url(#' + gid + ')"/><path class="pc-line" d="' + d + '"/>' +
      '<line class="pc-cursor" y1="0" y2="' + H + '" hidden/></svg>' +
      '<span class="pc-dot" hidden></span><div class="pc-tip" hidden></div>' +
      '<div class="pc-axis"><span>' + new Date(hist[0][0] * 1000).toLocaleString('fr-FR', df[range]) + '</span><span>' + new Date(hist[n - 1][0] * 1000).toLocaleString('fr-FR', df[range]) + '</span></div>';
    var first = hist[0][1], lastv = hist[n - 1][1], pct = (lastv / first - 1) * 100;
    v.textContent = pf.format(pct) + ' %'; v.className = 'price-var ' + (pct > 0 ? 'up' : pct < 0 ? 'down' : '');
    host.setAttribute('aria-label', 'Évolution du cours sur la période : ' + pf.format(pct) + ' %, de ' + nf2.format(first) + ' à ' + nf2.format(lastv) + ' euros le gramme');

    var svg = host.querySelector('svg'), cur = svg.querySelector('.pc-cursor'), dot = host.querySelector('.pc-dot'), tip = host.querySelector('.pc-tip');
    function show(e) {
      var r = svg.getBoundingClientRect(), x = (e.clientX - r.left) / r.width;
      var i = Math.max(0, Math.min(n - 1, Math.round(x * (n - 1))));
      var px = (i / (n - 1)) * r.width, py = (Y(hist[i][1]) / H) * r.height;
      cur.setAttribute('x1', X(i)); cur.setAttribute('x2', X(i)); cur.removeAttribute('hidden');
      dot.style.left = px + 'px'; dot.style.top = py + 'px'; dot.hidden = false;
      tip.innerHTML = nf2.format(hist[i][1]) + ' € / g<small>' + new Date(hist[i][0] * 1000).toLocaleString('fr-FR', (range === '1d' || range === '7d') ? { weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' } : { day: 'numeric', month: 'long', year: 'numeric' }) + '</small>';
      tip.hidden = false;
      tip.style.left = Math.max(60, Math.min(r.width - 60, px)) + 'px';
    }
    function hide() { cur.setAttribute('hidden', ''); dot.hidden = true; tip.hidden = true; }
    host.onpointermove = show; host.onpointerdown = show; host.onpointerleave = hide; host.onpointercancel = hide;
  }

  function render() {
    if (!data) return;
    set('or-g', nf2.format(data.or.eur_g)); set('or-oz', nf2.format(data.or.eur_oz));
    set('argent-g', nf2.format(data.argent.eur_g)); set('argent-oz', nf2.format(data.argent.eur_oz));
    timeEl.textContent = 'Mis à jour à ' + tf.format(new Date(data.updatedAt)) + ' · actualisation automatique';
    chart('or'); chart('argent');
    var src = box.querySelector('[data-source]');
    if (src) src.textContent = 'Source : cours instantané gold-api.com · historique ' + ((range === '1d' || range === '7d') ? 'Yahoo Finance (contrats à terme, taux de change du moment)' : 'Stooq / Yahoo Finance') + ' · taux de change BCE (Frankfurter).';
    box.hidden = false;
  }

  function load() {
    var asked = range;
    fetch('/api/cours?range=' + asked, { headers: { accept: 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        if (!d || !d.or || !d.argent) throw new Error('format');
        if (asked !== range) return;
        data = d; render();
      })
      .catch(function (e) { if (window.console) console.debug('cours', e); });
  }

  Array.prototype.forEach.call(box.querySelectorAll('[data-range]'), function (btn) {
    btn.addEventListener('click', function () {
      range = btn.getAttribute('data-range');
      Array.prototype.forEach.call(box.querySelectorAll('[data-range]'), function (b2) {
        var on = b2 === btn; b2.classList.toggle('is-on', on); b2.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      load();
    });
  });
  load();
  setInterval(function () { if (!document.hidden) load(); }, 60000);
  document.addEventListener('visibilitychange', function () { if (!document.hidden) load(); });
})();


// Gélules des pages services : la page active est centrée dans la rangée défilante (mobile)
(function () {
  var ul = document.querySelector('.subnav ul');
  var cur = ul && ul.querySelector('[aria-current="page"]');
  if (!cur || ul.scrollWidth <= ul.clientWidth) return;
  ul.scrollLeft = cur.offsetLeft - (ul.clientWidth - cur.offsetWidth) / 2;
})();
