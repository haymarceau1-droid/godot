// Godot & Fils Chartres — bannière de consentement
// Le site n'utilise aucun cookie de suivi. Seul le plan Google Maps (page Contact) est soumis à consentement.
(function () {
  var KEY = 'godot_consent', TTL = 180 * 24 * 3600 * 1000; // 6 mois

  function read() {
    try {
      var v = JSON.parse(window.localStorage.getItem(KEY));
      if (v && v.v === 1 && Date.now() - v.ts < TTL) return v;
    } catch (e) { /* stockage indisponible */ }
    return null;
  }
  function save(maps) {
    var v = { v: 1, maps: !!maps, ts: Date.now() };
    try { window.localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) { /* ignoré */ }
    applyMaps(v.maps);
    return v;
  }

  // --- Plan d'accès : l'iframe n'est chargée qu'avec consentement
  function applyMaps(on) {
    document.querySelectorAll('[data-map-consent]').forEach(function (box) {
      var frame = box.querySelector('iframe'), ph = box.querySelector('.map-placeholder');
      if (!frame) return;
      if (on) {
        if (!frame.getAttribute('src')) frame.setAttribute('src', frame.getAttribute('data-src'));
        frame.hidden = false; if (ph) ph.hidden = true;
      } else {
        frame.removeAttribute('src'); frame.hidden = true; if (ph) ph.hidden = false;
      }
    });
  }

  // --- Bannière
  var banner = null, lastFocus = null;
  function build() {
    var el = document.createElement('div');
    el.className = 'cookie';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-modal', 'false');
    el.setAttribute('aria-labelledby', 'ck-title');
    el.setAttribute('aria-describedby', 'ck-text');
    el.innerHTML =
      '<div class="cookie-head">' +
        '<img src="assets/img/logo-blanc.png" width="650" height="133" alt="Godot &amp; Fils, depuis 1933">' +
      '</div>' +
      '<h2 id="ck-title">Votre vie privée compte</h2>' +
      '<p id="ck-text">Aucun cookie de suivi sur ce site. Seul le plan d’accès (Google Maps) peut en déposer, et uniquement avec votre accord. Modifiable à tout moment depuis le pied de page.</p>' +
      '<div class="cookie-custom" hidden>' +
        '<label class="ck-row"><span><strong>Nécessaires</strong><small>Mémorise votre choix. Toujours actifs.</small></span>' +
          '<input type="checkbox" role="switch" checked disabled></label>' +
        '<label class="ck-row"><span><strong>Plan d’accès (Google Maps)</strong><small>Peut déposer des cookies tiers.</small></span>' +
          '<input type="checkbox" role="switch" data-ck-maps></label>' +
      '</div>' +
      '<div class="cookie-actions">' +
        '<button type="button" class="btn btn-ghost" data-ck="refuse">Tout refuser</button>' +
        '<button type="button" class="btn btn-gold" data-ck="accept">Tout accepter</button>' +
      '</div>' +
      '<button type="button" class="cookie-more" data-ck="custom" aria-expanded="false">Personnaliser</button>';
    document.body.appendChild(el);

    var custom = el.querySelector('.cookie-custom');
    var moreBtn = el.querySelector('[data-ck="custom"]');
    var actions = el.querySelector('.cookie-actions');
    el.addEventListener('click', function (e) {
      var t = e.target.closest('[data-ck]');
      if (!t) return;
      var k = t.getAttribute('data-ck');
      if (k === 'accept') { save(true); hide(); }
      else if (k === 'refuse') { save(false); hide(); }
      else if (k === 'custom') {
        var open = custom.hidden;
        custom.hidden = !open;
        moreBtn.setAttribute('aria-expanded', String(open));
        if (open) {
          moreBtn.textContent = 'Masquer';
          actions.innerHTML = '<button type="button" class="btn btn-ghost" data-ck="refuse">Tout refuser</button>' +
                              '<button type="button" class="btn btn-gold" data-ck="save">Enregistrer</button>';
        } else {
          moreBtn.textContent = 'Personnaliser';
          actions.innerHTML = '<button type="button" class="btn btn-ghost" data-ck="refuse">Tout refuser</button>' +
                              '<button type="button" class="btn btn-gold" data-ck="accept">Tout accepter</button>';
        }
      } else if (k === 'save') {
        save(el.querySelector('[data-ck-maps]').checked); hide();
      }
    });
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && read()) hide();   // on ne ferme sans choix que pour une réouverture
    });
    return el;
  }
  function show() {
    lastFocus = document.activeElement;
    if (!banner) banner = build();
    var cur = read();
    var sw = banner.querySelector('[data-ck-maps]');
    if (sw) sw.checked = !!(cur && cur.maps);
    banner.hidden = false;
    document.body.classList.add('ck-open');
    window.requestAnimationFrame(function () { banner.classList.add('in'); });
    var first = banner.querySelector('.cookie-actions .btn');
    if (first && cur) first.focus();   // réouverture volontaire : on place le focus dans la bannière
  }
  function hide() {
    if (!banner) return;
    banner.classList.remove('in');
    document.body.classList.remove('ck-open');
    setTimeout(function () { banner.hidden = true; }, 350);
    if (lastFocus && lastFocus.focus && document.body.contains(lastFocus)) lastFocus.focus();
  }

  // --- Branchements
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-consent-open]')) { e.preventDefault(); show(); }
    var m = e.target.closest('[data-consent-maps]');
    if (m) { save(true); hide(); }
  });

  var current = read();
  applyMaps(!!(current && current.maps));
  if (!current) setTimeout(show, 700);

  window.GodotConsent = { get: read, open: show };
})();
