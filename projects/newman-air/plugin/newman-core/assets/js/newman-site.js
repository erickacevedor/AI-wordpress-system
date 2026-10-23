/* newman-site.js: front-end behaviour of the V2.1 prototype (design-source/v2-1/
   index.html, <script>), minus the prototype-only Tokens panel and version
   switcher. Every block checks that its markup is on the page. */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };

  /* ---------- Header state + parallax ---------- */
  var head = $('#siteHead');
  var layers = $$('[data-parallax]');
  function onScroll() {
    var y = window.scrollY;
    if (head) head.classList.toggle('scrolled', y > 40);
    if (!reduce && y < 1200) layers.forEach(function (l) { l.style.transform = 'translateY(' + (y * parseFloat(l.dataset.parallax)) + 'px)'; });
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var menuBtn = $('#menuBtn'), drawer = $('#drawer');
  if (head && menuBtn) {
    menuBtn.addEventListener('click', function () { var o = head.classList.toggle('menu-open'); menuBtn.setAttribute('aria-expanded', o); });
  }
  if (head && drawer) {
    drawer.addEventListener('click', function (e) { if (e.target.closest('a')) { head.classList.remove('menu-open'); if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false'); } });
  }

  /* ---------- Count-up ---------- */
  function countUp(el) {
    var target = parseFloat(el.dataset.count), dec = +(el.dataset.decimals || 0), suf = el.dataset.suffix || '';
    var fmt = function (n) { return (dec ? n.toFixed(dec) : Math.round(n).toLocaleString('en-US')) + suf; };
    if (reduce) { el.textContent = fmt(target); return; }
    var t0 = null, dur = 1400;
    function step(t) { if (!t0) t0 = t; var p = Math.min((t - t0) / dur, 1); el.textContent = fmt(target * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); }
    el.textContent = fmt(0); requestAnimationFrame(step);
  }

  /* ---------- Reveal + count triggers ---------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        en.target.querySelectorAll('[data-count]').forEach(countUp);
        if (en.target.hasAttribute('data-count')) countUp(en.target);
        io.unobserve(en.target);
      });
    }, { threshold: .15 });
    $$('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    $$('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- Difference slider: arrows, drag, progress ---------- */
  var track = $('#diffTrack'), bar = $('#diffProgress');
  if (track) {
    var gap = function () { return parseFloat(getComputedStyle(track).columnGap) || 22; };
    var prog = function () { if (!bar) return; var max = track.scrollWidth - track.clientWidth; bar.style.width = (max > 0 ? 18 + 82 * track.scrollLeft / max : 100) + '%'; };
    track.addEventListener('scroll', prog, { passive: true }); prog();
    $$('.slider-nav button').forEach(function (b) {
      b.addEventListener('click', function () { var c = track.querySelector('.diff-card'); track.scrollBy({ left: +b.dataset.dir * (c.offsetWidth + gap()), behavior: 'smooth' }); });
    });
    var down = false, sx = 0, sl = 0;
    track.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') return; down = true; sx = e.clientX; sl = track.scrollLeft; track.classList.add('dragging'); });
    window.addEventListener('pointerup', function () { if (down) { down = false; track.classList.remove('dragging'); } });
    window.addEventListener('pointermove', function (e) { if (down) track.scrollLeft = sl - (e.clientX - sx); });
  }

  /* ---------- Brand marquee (seamless) ---------- */
  var bt = $('#brandTrack');
  if (bt) {
    bt.innerHTML += bt.innerHTML;
    Array.prototype.slice.call(bt.children, bt.children.length / 2).forEach(function (n) { n.setAttribute('aria-hidden', 'true'); });
  }

  /* ---------- Map <-> city list ----------
     Matched by city name (pin label vs list text without ", TN"): the list is a native
     icon-list widget, which cannot carry data attributes on every item. */
  var key = function (t) { return (t || '').replace(/,\s*TN\s*$/i, '').trim().toLowerCase(); };
  var pins = {}, items = {};
  $$('.pin').forEach(function (p) { var t = p.querySelector('text'); pins[key(t ? t.textContent : p.dataset.city)] = p; });
  $$('#cityList li').forEach(function (li) { items[key(li.textContent)] = li; });
  Object.keys(pins).forEach(function (k) {
    var pin = pins[k], li = items[k];
    var on = function (v) { pin.classList.toggle('on', v); if (li) li.classList.toggle('on', v); };
    pin.addEventListener('mouseenter', function () { on(true); }); pin.addEventListener('mouseleave', function () { on(false); });
    if (li) { li.addEventListener('mouseenter', function () { on(true); }); li.addEventListener('mouseleave', function () { on(false); }); }
  });
})();
