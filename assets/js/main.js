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
    var status = document.querySelector('[data-open-status]');
    if (status) {
      var sat = now.day === 6;
      status.classList.add(open ? 'is-open' : (sat ? 'is-rdv' : 'is-closed'));
      status.querySelector('.status-text').textContent = open
        ? "Ouvert en ce moment · jusqu'à 18h00"
        : (sat ? 'Samedi matin : sur rendez-vous' : 'Fermé actuellement · ouvert du lundi au vendredi');
    }
    var row = document.querySelector('.hours tr[data-day="' + now.day + '"]');
    if (row) row.classList.add('today');
  } catch (e) { /* navigateur sans Intl : on garde le texte par défaut */ }

  // Année du pied de page
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();

  // ---------------------------------------------------------------- Apparition au défilement (décalée, directionnelle)
  var SEL = '.section-head, .card, .card-row, .other-card, .coin-card, .tips li, .steps li, .formula > *, ' +
            '.faq details, .contact-grid > *, .split > *, .network > *, .notice, .table-wrap, ' +
            '.cta-inner > *, .footer-grid > *, .checks li';
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
      else if (el.matches('.coin-card, .f-box, .tips li, .steps li')) el.classList.add('reveal-pop');
      io.observe(el);
    });
  }

  // ---------------------------------------------------------------- Défilement : barre de progression, en-tête, parallaxe
  var header = document.querySelector('.site-header');
  var hero = document.querySelector('.hero-photo');
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
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

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
