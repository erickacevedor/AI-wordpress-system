/* ============================================================================
   lenz-site.js -- front-end behaviour for the v6-1 build (lenz-core).
   Copied from the prototype's js/lenz.js (design-source/v6-1/js/lenz.js),
   modules 2, 3, 4a, 4b, 4c and 8, unchanged except:
     - the marquee no longer reads lenz-config.js: logos ship as <img> markup;
     - modules 1 (offer bar season), 5 (form: Elementor Pro handles it) and
       6, 7, 9 to 12 (config swaps) are not needed: their final values are in
       the Elementor markup.
   ============================================================================ */
(function () {
  'use strict';

  /* --- 2. STICKY-NAV STUCK-STATE TRACKING ------------------------------- */
  (function stickyNav() {
    var nav = document.getElementById('nav');
    if (!nav) return;
    // sentinel sits at the very top; when it leaves the viewport nav is stuck.
    var sentinel = document.getElementById('nav-sentinel');
    if (sentinel && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        nav.classList.toggle('is-stuck', !entries[0].isIntersecting);
      }, { threshold: 0 });
      io.observe(sentinel);
    } else {
      var onScroll = function () { nav.classList.toggle('is-stuck', window.scrollY > 30); };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }
  })();

  /* --- 4a. SERVICES MEGA MENU (desktop) --------------------------------- */
  /* Labelled disclosure pattern. The trigger is a <button> with no href — the
     "Services" top-level item is a label and must never navigate. Opens on
     hover (pointer) and on click/Enter/Space (keyboard + touch). Escape closes
     and returns focus to the trigger. Arrow keys walk the panel's links. */
  (function megaMenu() {
    var trigger = document.getElementById('mega-trigger');
    var panel = document.getElementById('mega-services');
    if (!trigger || !panel) return;

    var host = trigger.closest('.nav__item') || trigger.parentNode;
    var hoverCapable = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    var closeTimer = null;

    function links() {
      return Array.prototype.slice.call(panel.querySelectorAll('a[href]'));
    }
    function isOpen() {
      return trigger.getAttribute('aria-expanded') === 'true';
    }
    function open() {
      window.clearTimeout(closeTimer);
      panel.hidden = false;
      // next frame so the transition runs from the hidden state
      window.requestAnimationFrame(function () { panel.setAttribute('data-open', 'true'); });
      trigger.setAttribute('aria-expanded', 'true');
    }
    function close(returnFocus) {
      window.clearTimeout(closeTimer);
      panel.removeAttribute('data-open');
      trigger.setAttribute('aria-expanded', 'false');
      // keep it out of the tab order once the transition has finished
      closeTimer = window.setTimeout(function () {
        if (!isOpen()) panel.hidden = true;
      }, 200);
      if (returnFocus) trigger.focus();
    }
    function toggle() { isOpen() ? close(false) : open(); }

    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      toggle();
    });

    if (hoverCapable) {
      host.addEventListener('mouseenter', open);
      panel.addEventListener('mouseenter', function () { window.clearTimeout(closeTimer); });
      [host, panel].forEach(function (el) {
        el.addEventListener('mouseleave', function () {
          closeTimer = window.setTimeout(function () { close(false); }, 160);
        });
      });
    }

    // Arrow keys from the trigger drop into the panel.
    trigger.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        open();
        var first = links()[0];
        if (first) first.focus();
      }
    });

    // Roving arrow navigation + Tab containment inside the panel.
    panel.addEventListener('keydown', function (e) {
      var all = links();
      var i = all.indexOf(document.activeElement);
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
        e.preventDefault();
        all[(i + 1) % all.length].focus();
      } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
        e.preventDefault();
        all[(i - 1 + all.length) % all.length].focus();
      } else if (e.key === 'Home') {
        e.preventDefault(); all[0].focus();
      } else if (e.key === 'End') {
        e.preventDefault(); all[all.length - 1].focus();
      } else if (e.key === 'Tab') {
        // cycle within the panel rather than escaping into the page behind it
        if (!e.shiftKey && i === all.length - 1) { e.preventDefault(); trigger.focus(); }
        else if (e.shiftKey && i === 0) { e.preventDefault(); trigger.focus(); }
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isOpen()) close(true);
    });
    document.addEventListener('click', function (e) {
      if (isOpen() && !panel.contains(e.target) && !host.contains(e.target)) close(false);
    });
    // Focus leaving the whole disclosure closes it.
    document.addEventListener('focusin', function (e) {
      if (isOpen() && !panel.contains(e.target) && !host.contains(e.target)) close(false);
    });
  })();

  /* --- 4c. MOBILE MEGA-MENU ACCORDION ----------------------------------- */
  (function mobileServiceAccordion() {
    var triggers = document.querySelectorAll('.m-acc__trigger');
    triggers.forEach(function (trigger) {
      trigger.addEventListener('click', function () {
        var expanded = trigger.getAttribute('aria-expanded') === 'true';
        var panel = document.getElementById(trigger.getAttribute('aria-controls'));
        trigger.setAttribute('aria-expanded', expanded ? 'false' : 'true');
        if (panel) panel.hidden = expanded;
      });
    });
  })();

  /* --- 4b. MOBILE MENU -------------------------------------------------- */
  (function mobileMenu() {
    var toggle = document.getElementById('nav-toggle');
    var menu = document.getElementById('mobile-menu');
    var closeBtn = document.getElementById('mobile-menu-close');
    if (!toggle || !menu) return;

    function open() {
      menu.classList.add('is-open');
      document.body.classList.add('menu-open');
      toggle.setAttribute('aria-expanded', 'true');
      var first = menu.querySelector('a, button');
      if (first) first.focus();
    }
    function close() {
      menu.classList.remove('is-open');
      document.body.classList.remove('menu-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
    toggle.addEventListener('click', function () {
      menu.classList.contains('is-open') ? close() : open();
    });
    if (closeBtn) closeBtn.addEventListener('click', close);
    // close on link click (anchor navigation)
    menu.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', close);
    });
    // Escape closes
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('is-open')) close();
    });
    // click-outside (on the menu backdrop itself is full-screen, so use links region)
    menu.addEventListener('click', function (e) {
      if (e.target === menu) close();
    });
  })();

  /* --- 3. FAQ ACCORDION ------------------------------------------------- */
  (function faqAccordion() {
    var triggers = document.querySelectorAll('.faq__trigger');
    triggers.forEach(function (trigger) {
      trigger.addEventListener('click', function () {
        var expanded = trigger.getAttribute('aria-expanded') === 'true';
        var panel = document.getElementById(trigger.getAttribute('aria-controls'));
        trigger.setAttribute('aria-expanded', expanded ? 'false' : 'true');
        if (panel) {
          if (expanded) panel.removeAttribute('data-open');
          else panel.setAttribute('data-open', 'true');
        }
      });
    });
  })();

  /* --- 8. BRAND LOGO MARQUEE -------------------------------------------- */
  /* The nine brands ship in the markup as linked wordmarks, so they survive
     with JS off. This module (a) upgrades each one to a real logo image as
     soon as BRAND_LOGOS supplies a src, and (b) clones the track to give the
     loop a seamless seam. The clone is aria-hidden and untabbable so the
     brands are announced once. Reduced motion is handled in CSS: the
     animation freezes and the clone is hidden, leaving a wrapped grid. */
  (function brandMarquee() {
    var root = document.querySelector('[data-marquee]');
    if (!root) return;
    var track = root.querySelector('.marquee__track');
    if (!track) return;

    var clone = track.cloneNode(true);
    clone.classList.add('marquee__track--dupe');
    clone.setAttribute('aria-hidden', 'true');
    clone.querySelectorAll('a').forEach(function (a) {
      a.tabIndex = -1;
      a.removeAttribute('aria-label');
      var img = a.querySelector('img');
      if (img) img.alt = '';
    });
    root.appendChild(clone);

    // Pause on hover (CSS) and whenever focus lands inside the strip.
    root.addEventListener('focusin', function () { root.setAttribute('data-paused', 'true'); });
    root.addEventListener('focusout', function (e) {
      if (!root.contains(e.relatedTarget)) root.removeAttribute('data-paused');
    });
  })();

})();
