/* Telo.Sabe — интерактив: меню, услуги, сертификаты, отзывы, вопросы, лайтбокс */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* мобильное меню */
  var burger = $('.burger'), mmenu = $('#mmenu');
  if (burger && mmenu) {
    var setMenu = function (open) {
      mmenu.hidden = !open;
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? burger.dataset.close : burger.dataset.open);
    };
    burger.addEventListener('click', function () { setMenu(mmenu.hidden); });
    $$('a', mmenu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  }

  /* услуги: вкладки (десктоп) и аккордеон (мобильный) */
  var tabs = $$('#services .tab');
  var panels = $$('#services .svc-panel');
  var svcWa = $('#services .svc-wa');
  function pick(i) {
    tabs.forEach(function (t, k) {
      var on = k === i;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.parentNode.classList.toggle('on', on);
    });
    panels.forEach(function (p, k) { p.hidden = k !== i; });
    if (svcWa && panels[i]) svcWa.href = panels[i].dataset.wa;
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { pick(i); });
    t.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? 1 : e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      var n = (i + d + tabs.length) % tabs.length;
      tabs[n].focus(); pick(n);
    });
  });

  /* лайтбокс */
  var lb = $('#lb'), lbImg = lb && $('img', lb), lbCap = lb && $('figcaption', lb);
  var lbItems = [], lbIdx = 0, lbReturn = null;
  function lbShow() {
    var it = lbItems[lbIdx];
    lbImg.src = it.src; lbImg.alt = it.alt; lbCap.textContent = it.cap || '';
    lb.setAttribute('aria-label', it.alt);
  }
  function lbOpen(items, idx) {
    lbItems = items; lbIdx = idx; lbReturn = document.activeElement;
    lb.classList.toggle('single', items.length < 2);
    lbShow(); lb.hidden = false; document.body.style.overflow = 'hidden';
    $('.lb-x', lb).focus();
  }
  function lbClose() {
    lb.hidden = true; document.body.style.overflow = '';
    if (lbReturn) lbReturn.focus();
  }
  function lbGo(d) { lbIdx = (lbIdx + d + lbItems.length) % lbItems.length; lbShow(); }
  if (lb) {
    $$('[data-close]', lb).forEach(function (b) { b.addEventListener('click', lbClose); });
    $('.lb-prev', lb).addEventListener('click', function () { lbGo(-1); });
    $('.lb-next', lb).addEventListener('click', function () { lbGo(1); });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') lbClose();
      if (e.key === 'ArrowLeft' && lbItems.length > 1) lbGo(-1);
      if (e.key === 'ArrowRight' && lbItems.length > 1) lbGo(1);
    });
  }

  /* сертификаты */
  var certs = $$('#experience .cert');
  var certItems = certs.map(function (c) { return { src: c.dataset.full, alt: c.dataset.alt, cap: c.dataset.alt }; });
  certs.forEach(function (c, i) { c.addEventListener('click', function () { lbOpen(certItems, i); }); });
  var track = $('#experience .track');
  $$('#experience .arr').forEach(function (b) {
    b.addEventListener('click', function () {
      if (track) track.scrollBy({ left: Number(b.dataset.dir) * track.clientWidth * 0.8, behavior: 'smooth' });
    });
  });

  /* отзывы */
  var rc = $('#reviews .rev-card');
  if (rc) {
    var revs = JSON.parse(rc.dataset.reviews), ri = 0;
    var txt = $('.rev-text', rc), from = $('.rev-from', rc), note = $('.rev-note', rc), pos = $('.pos', rc);
    var renderRev = function () {
      var r = revs[ri];
      txt.textContent = rc.dataset.prefix + r.t + rc.dataset.suffix;
      from.textContent = r.from;
      note.textContent = r.note ? '· ' + r.note : '';
      pos.textContent = (ri + 1) + ' / ' + revs.length;
    };
    var goRev = function (d) { ri = (ri + d + revs.length) % revs.length; renderRev(); };
    $$('.nav-b', rc).forEach(function (b) { b.addEventListener('click', function () { goRev(Number(b.dataset.dir)); }); });
    $('.orig', rc).addEventListener('click', function () {
      lbOpen([{ src: revs[ri].shot, alt: rc.dataset.shotAlt, cap: revs[ri].from }], 0);
    });
    var x0 = null;
    rc.addEventListener('touchstart', function (e) { x0 = e.changedTouches[0].clientX; }, { passive: true });
    rc.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) goRev(dx < 0 ? 1 : -1);
    });
    renderRev();
  }

  /* вопросы */
  var fqs = $$('#faq .fq');
  fqs.forEach(function (f) {
    $('.qrow', f).addEventListener('click', function () {
      var open = !f.classList.contains('open');
      fqs.forEach(function (o) {
        var on = o === f && open;
        o.classList.toggle('open', on);
        $('.qrow', o).setAttribute('aria-expanded', on ? 'true' : 'false');
        $('.ans', o).hidden = !on;
      });
    });
  });

  /* e-mail для сотрудничества (собирается в браузере, чтобы не попадать к спам-ботам) */
  $$('.b2b').forEach(function (a) {
    a.href = 'mailto:' + a.dataset.u + '@' + a.dataset.d + '?subject=' + encodeURIComponent(a.dataset.s);
  });
})();
