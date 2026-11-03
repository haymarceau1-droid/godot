// Godot & Fils Chartres — interactions
(function () {
  // Menu mobile
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Statut ouvert / fermé (heure de Paris). Lun–Ven 9h30–18h00.
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
      status.classList.add(open ? 'is-open' : 'is-closed');
      status.querySelector('.status-text').textContent = open
        ? "Ouvert en ce moment · jusqu'à 18h00"
        : 'Fermé actuellement · ouvert du lundi au vendredi';
    }
    var row = document.querySelector('.hours tr[data-day="' + now.day + '"]');
    if (row) row.classList.add('today');
  } catch (e) { /* navigateur sans Intl : on garde le texte par défaut */ }

  // Année du pied de page
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();

  // Apparition au défilement
  var items = document.querySelectorAll('.card, .steps li, .split > *, .faq details, .contact-grid > *, .section-head');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('visible'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    items.forEach(function (el) { el.classList.add('reveal'); io.observe(el); });
  }
})();

// Carte du réseau : clic sur un pin ou une ville => affiche la fiche correspondante
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
})();
