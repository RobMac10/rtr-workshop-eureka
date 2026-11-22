/* Reopen the Record · Workshop case files. Answers stay in this browser only. */
(function () {
  'use strict';
  var KEY = 'rtr-workshop:';
  var store = {
    get: function (k) { try { return localStorage.getItem(KEY + k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(KEY + k, v); } catch (e) {} },
    clear: function () { try { Object.keys(localStorage).forEach(function (k) { if (k.indexOf(KEY) === 0) localStorage.removeItem(k); }); } catch (e) {} }
  };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---- open one case at a time ---- */
  function openCase(id, scroll) {
    var sec = document.getElementById('case-' + id);
    if (!sec) return;
    $$('.case').forEach(function (c) { c.classList.toggle('open', c === sec); });
    document.body.classList.add('has-case');
    $$('.case-switch a').forEach(function (a) { a.setAttribute('aria-current', a.getAttribute('href') === '#case-' + id ? 'true' : 'false'); });
    if (scroll !== false) { var bar = document.querySelector('.topbar'); var off = (bar && getComputedStyle(bar).position === 'sticky') ? bar.offsetHeight + 8 : 8;
      window.scrollTo({ top: sec.getBoundingClientRect().top + window.pageYOffset - off, behavior: 'smooth' }); }
  }
  function route() {
    var m = /^#case-([a-z-]+)$/.exec(location.hash);
    if (m) openCase(m[1]);
  }
  window.addEventListener('hashchange', route);
  route();

  /* ---- save answers on this device ---- */
  $$('textarea[data-key]').forEach(function (t) {
    var v = store.get(t.dataset.key); if (v) t.value = v;
    t.addEventListener('input', function () { store.set(t.dataset.key, t.value); });
  });
  $$('input[type=radio][data-key]').forEach(function (r) {
    if (store.get(r.dataset.key) === r.value) r.checked = true;
    r.addEventListener('change', function () { if (r.checked) store.set(r.dataset.key, r.value); });
  });
  var clr = $('#clear-all');
  if (clr) clr.addEventListener('click', function () {
    if (!confirm('Clear all your answers on this device?')) return;
    store.clear();
    $$('textarea[data-key]').forEach(function (t) { t.value = ''; });
    $$('input[type=radio][data-key]').forEach(function (r) { r.checked = false; });
  });

  /* ---- print / save as PDF: one case, as a take-away pack ---- */
  var opened = [];
  function preparePrint(id) {
    var sec = document.getElementById('case-' + id);
    if (!sec) return;
    document.body.setAttribute('data-print', id);
    $$('.case').forEach(function (c) { c.classList.toggle('print-me', c === sec); });
    $('.pc-title').textContent = $('h2', sec).textContent;
    $('.pc-q').textContent = $('.key-q', sec).textContent;
    var qr = $('.app-card img', sec); var pq = $('.pc-qr-case');
    if (qr && pq) { pq.src = qr.getAttribute('src'); pq.alt = qr.alt; }
    $$('textarea[data-key]').forEach(function (t) {
      var pl = t.parentNode.querySelector('.print-lines'); if (pl) pl.textContent = t.value;
    });
    opened = [];
    $$('details').forEach(function (d) { if (!d.open) { d.open = true; opened.push(d); } });
    /* print the Bias Button questions on an evidence card only if something was written there */
    $$('.ev-card .bias', sec).forEach(function (d) {
      var used = $$('textarea', d).some(function (t) { return t.value.trim() !== ''; });
      d.classList.toggle('print-skip', !used);
    });
  }
  function cleanPrint() {
    opened.forEach(function (d) { d.open = false; }); opened = [];
  }
  $$('.print-case').forEach(function (b) {
    b.addEventListener('click', function () {
      var id = b.dataset.case;
      openCase(id, false);
      preparePrint(id);
      window.print();
    });
  });
  window.addEventListener('beforeprint', function () {
    if (!document.body.getAttribute('data-print')) {
      var open = $('.case.open');
      if (open) preparePrint(open.dataset.case);
      else { $$('details').forEach(function (d) { if (!d.open) { d.open = true; opened.push(d); } });
             $$('textarea[data-key]').forEach(function (t) { var pl = t.parentNode.querySelector('.print-lines'); if (pl) pl.textContent = t.value; }); }
    }
  });
  window.addEventListener('afterprint', function () { cleanPrint(); document.body.removeAttribute('data-print'); });
  window.rtrPreparePrint = preparePrint; // used to export a sample PDF

  /* ---- tap to enlarge ---- */
  var lb = $('#lightbox'), lbImg = $('#lightbox img'), lbCap = $('#lightbox .lb-cap'), lastFocus = null;
  function closeLb() { lb.hidden = true; lbImg.src = ''; if (lastFocus) lastFocus.focus(); }
  $$('.zoom-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var img = $('img', b); if (!img) return;
      lastFocus = b; lbImg.src = img.currentSrc || img.src; lbImg.alt = img.alt;
      var fig = b.closest('figure'); var cap = fig && $('figcaption', fig);
      lbCap.textContent = cap ? cap.textContent : img.alt;
      lb.hidden = false; $('.lb-close', lb).focus();
    });
  });
  lb.addEventListener('click', function (ev) { if (ev.target !== lbImg) closeLb(); });
  document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && !lb.hidden) closeLb(); });
})();
