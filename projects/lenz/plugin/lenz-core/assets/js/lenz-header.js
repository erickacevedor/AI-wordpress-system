/* ============================================================================
   lenz-header.js — offer bar seasonality, sticky-nav state, and the mega-menu
   accessibility shim.

   No framework, no dependencies. Every module no-ops when its markup is absent,
   so the header template can change without this throwing.
   ============================================================================ */
(function () {
  'use strict';

  /* --- 1. OFFER BAR SEASON SWITCHER ------------------------------------- */
  /* The summer copy ships in the markup so the bar is never empty with JS off;
     this swaps it for the current season. */
  (function offerBar() {
    var bar = document.querySelector('.lenz-offer-bar');
    if (!bar) return;

    var COPY = {
      summer: { msg: "AC out? We're on it — 24/7, 365.", cta: 'Call now' },
      winter: { msg: 'No heat? Certified techs on call 24/7.', cta: 'Call now' },
      spring: { msg: 'Book your AC tune-up before summer hits.', cta: 'Book now' },
      fall:   { msg: 'Furnace check before the first freeze.', cta: 'Book now' }
    };

    var m = new Date().getMonth() + 1; // 1..12
    var season = (m >= 6 && m <= 8) ? 'summer'
               : (m >= 9 && m <= 11) ? 'fall'
               : (m === 12 || m === 1 || m === 2) ? 'winter'
               : 'spring';

    bar.setAttribute('data-season', season);

    var msgEl = bar.querySelector('.lenz-offer-bar__msg');
    var ctaEl = bar.querySelector('.lenz-offer-bar__cta-label');
    if (msgEl) msgEl.textContent = COPY[season].msg;
    if (ctaEl) ctaEl.textContent = COPY[season].cta;
  })();

  /* --- 2. STICKY-NAV STUCK STATE ---------------------------------------- */
  (function stickyNav() {
    var nav = document.querySelector('.lenz-nav');
    if (!nav) return;

    // A zero-height sentinel above the bar: once it leaves the viewport the nav
    // is stuck. Cheaper and less jittery than listening to every scroll event.
    var sentinel = document.createElement('span');
    sentinel.setAttribute('aria-hidden', 'true');
    sentinel.style.cssText = 'position:absolute;top:0;height:1px;width:1px;';
    nav.parentNode.insertBefore(sentinel, nav);

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        nav.classList.toggle('is-stuck', !entries[0].isIntersecting);
      }, { threshold: 0 }).observe(sentinel);
    } else {
      var onScroll = function () { nav.classList.toggle('is-stuck', window.scrollY > 30); };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }
  })();

  /* --- 3. MEGA MENU ACCESSIBILITY SHIM ----------------------------------- */
  /* Pro's Mega Menu handles opening, closing and its own responsive collapse. What
     it does not provide is the keyboard behaviour the source design implemented by
     hand: arrow keys walking the panel's links, Tab staying inside the open panel,
     and Escape returning focus to the trigger that opened it.

     This layers those on WITHOUT taking over the widget: we never open or close
     anything ourselves, we only move focus and let the widget's own click handling
     do the rest. If Elementor changes its markup, every query below simply misses
     and the widget keeps working unshimmed. */
  (function megaMenuA11y() {
    var roots = document.querySelectorAll('.lenz-nav__menu');
    if (!roots.length) return;

    Array.prototype.forEach.call(roots, function (root) {
      function panels() {
        return Array.prototype.slice.call(root.querySelectorAll('.e-n-menu-content > *'));
      }
      function openPanel() {
        /* MARKUP NOTE (verified against the render): aria-expanded does NOT sit on
           `.e-n-menu-title` — that is a plain div wrapper. It sits on the nested
           `.e-n-menu-dropdown-icon` <button>, whose aria-controls points at the
           `e-n-menu-content-*` panel. That button is also the right thing to return
           focus to on Escape, since it is what opened the panel. */
        var trigger = root.querySelector('.e-n-menu-dropdown-icon[aria-expanded="true"]')
                   || root.querySelector('[aria-expanded="true"]');
        if (!trigger) return null;

        var id = trigger.getAttribute('aria-controls');
        var panel = id ? document.getElementById(id) : null;
        if (!panel) {
          panel = panels().filter(function (p) { return p.offsetParent !== null; })[0] || null;
        }
        return panel ? { title: trigger, panel: panel } : null;
      }
      function linksIn(panel) {
        return Array.prototype.slice.call(panel.querySelectorAll('a[href]'))
          .filter(function (a) { return a.offsetParent !== null; });
      }

      root.addEventListener('keydown', function (e) {
        var state = openPanel();

        // ArrowDown on a closed trigger drops into its panel once the widget opens it.
        // Match anything focusable inside the title block (the dropdown-icon button,
        // or the title container) rather than the wrapper div, which is never focused.
        if (!state) {
          var inTitle = e.target.closest && e.target.closest('.e-n-menu-title');
          if (e.key === 'ArrowDown' && inTitle) {
            var opener = inTitle.querySelector('.e-n-menu-dropdown-icon') || e.target;
            opener.click();
            window.setTimeout(function () {
              var s = openPanel();
              if (s) { var l = linksIn(s.panel); if (l.length) l[0].focus(); }
            }, 60);
            e.preventDefault();
          }
          return;
        }

        var all = linksIn(state.panel);
        var i = all.indexOf(document.activeElement);

        if (e.key === 'Escape') {
          e.preventDefault();
          state.title.click();          // let the widget close it
          state.title.focus();          // ...and return focus where it came from
        } else if (!all.length) {
          return;
        } else if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
          e.preventDefault();
          all[i < 0 ? 0 : (i + 1) % all.length].focus();
        } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
          e.preventDefault();
          all[i < 0 ? all.length - 1 : (i - 1 + all.length) % all.length].focus();
        } else if (e.key === 'Home') {
          e.preventDefault(); all[0].focus();
        } else if (e.key === 'End') {
          e.preventDefault(); all[all.length - 1].focus();
        } else if (e.key === 'Tab' && i >= 0) {
          // Cycle within the open panel rather than escaping into the page behind it.
          if (!e.shiftKey && i === all.length - 1) { e.preventDefault(); state.title.focus(); }
          else if (e.shiftKey && i === 0) { e.preventDefault(); state.title.focus(); }
        }
      });
    });
  })();
})();
