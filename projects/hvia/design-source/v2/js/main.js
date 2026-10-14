/* HVIA one-page homepage, prototype behavior (vanilla JS, no dependencies). */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.remove('no-js');
  var body = document.body;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var page = body.getAttribute('data-page') || 'v1';
  function store(key, val) {
    try {
      if (val === undefined) return localStorage.getItem('hvia-proto-' + key);
      localStorage.setItem('hvia-proto-' + key, val);
    } catch (e) { return null; }
  }

  /* Sticky header state */
  var header = document.querySelector('.site-header');
  function onScroll() { header.classList.toggle('is-scrolled', window.scrollY > 12); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Mobile nav */
  var nav = document.querySelector('.main-nav');
  var navToggle = document.querySelector('.nav-toggle');
  navToggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', String(open));
  });
  nav.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () {
      nav.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });

  /* Active nav link while scrolling */
  var links = {};
  nav.querySelectorAll('a[href^="#"]').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
  if ('IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var link = links[en.target.id];
        if (link && en.isIntersecting) {
          Object.keys(links).forEach(function (k) { links[k].classList.remove('is-active'); });
          link.classList.add('is-active');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(links).forEach(function (id) { var s = document.getElementById(id); if (s) spy.observe(s); });
  }

  /* Scroll reveals */
  var reveals = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || reduce) {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* Bio dialogs */
  var lastTrigger = null;
  document.querySelectorAll('.doc-open').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var dlg = document.getElementById(btn.getAttribute('data-bio'));
      if (!dlg) return;
      lastTrigger = btn;
      if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
    });
  });
  document.querySelectorAll('dialog.bio').forEach(function (dlg) {
    dlg.querySelector('.bio-close').addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('close', function () { if (lastTrigger) lastTrigger.focus(); });
  });

  /* Option switcher: mark the current page, keep the reader's section, keys 1/2/3 */
  var opts = document.querySelectorAll('.opt-switch a[data-opt]');
  function currentSection() {
    var mid = window.innerHeight / 2, found = '';
    ['about', 'physicians', 'locations'].forEach(function (id) {
      var s = document.getElementById(id);
      if (s && s.getBoundingClientRect().top <= mid) found = id;
    });
    return found;
  }
  function go(a) {
    var sec = currentSection();
    window.location.href = a.getAttribute('href') + (sec ? '#' + sec : '');
  }
  opts.forEach(function (a) {
    if (a.getAttribute('data-opt') === page) a.setAttribute('aria-current', 'page');
    a.addEventListener('click', function (e) {
      if (a.getAttribute('aria-current') === 'page') { e.preventDefault(); return; }
      if (e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault();
      go(a);
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'select' || tag === 'textarea' || document.querySelector('dialog[open]')) return;
    var a = document.querySelector('.opt-switch a[data-opt="v' + e.key + '"]');
    if (a && a.getAttribute('aria-current') !== 'page') go(a);
  });

  /* Footer year */
  var y = document.getElementById('year');
  if (y) y.textContent = String(new Date().getFullYear());

  /* Review panel (prototype only) */
  var panel = document.getElementById('review');
  if (!panel) return;
  var panelToggle = panel.querySelector('.review-toggle');
  var panelBody = document.getElementById('review-body');
  var list = document.getElementById('reviewList');
  var notesBox = document.getElementById('toggleNotes');
  var fontSel = document.getElementById('headingFont');

  var pending = Array.prototype.slice.call(document.querySelectorAll('[data-label]'));
  document.getElementById('reviewCount').textContent = String(pending.length);
  pending.forEach(function (el) {
    var li = document.createElement('li');
    var b = document.createElement('button');
    var text = el.classList.contains('pending-block')
      ? el.querySelector('.pending-title').textContent.trim()
      : el.textContent.trim();
    b.innerHTML = '<strong></strong> ';
    b.querySelector('strong').textContent = el.getAttribute('data-label') + ':';
    b.appendChild(document.createTextNode(text));
    b.addEventListener('click', function () {
      var dlg = el.closest('dialog');
      var det = el.closest('details');
      if (det) { det.open = true; }
      if (dlg) {
        var trigger = document.querySelector('[data-bio="' + dlg.id + '"]');
        if (trigger) trigger.click();
      } else {
        el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
      }
      el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash');
    });
    li.appendChild(b);
    list.appendChild(li);
  });

  panelToggle.addEventListener('click', function () {
    var open = panelBody.hasAttribute('hidden');
    if (open) panelBody.removeAttribute('hidden'); else panelBody.setAttribute('hidden', '');
    panelToggle.setAttribute('aria-expanded', String(open));
  });

  function applyNotes(on) { body.classList.toggle('hide-notes', !on); notesBox.checked = on; }
  function applyFont(f) {
    Array.prototype.forEach.call(fontSel.options, function (o) { body.classList.remove('font-' + o.value); });
    if (!f || !fontSel.querySelector('option[value="' + f + '"]')) f = fontSel.options[0].value;
    body.classList.add('font-' + f);
    fontSel.value = f;
  }
  applyNotes(store('notes') !== 'off');
  applyFont(store('font-' + page));
  notesBox.addEventListener('change', function () { applyNotes(notesBox.checked); store('notes', notesBox.checked ? 'on' : 'off'); });
  fontSel.addEventListener('change', function () { applyFont(fontSel.value); store('font-' + page, fontSel.value); });
})();
