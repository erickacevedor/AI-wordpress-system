/* ============================================================================
   lenz.js — shared behavior for index.html, v2.html and v3.html.
   No framework, no CDN.
    1. Offer bar season switcher   2. Sticky-nav stuck tracking
    3. FAQ accordion               4. Services mega menu + mobile menu
    5. Form validation             6. Hero copy/image  7. Logo
    8. Brand marquee               9. Service area map 10. Google reviews
   Modules 6-10 read js/lenz-config.js, which must load first.
   Progressive enhancement: page is fully readable/callable with JS disabled —
   the mega menu links, hero copy, brand names and review quotes are all in the
   markup, and JS only enhances or swaps them.
   ============================================================================ */
(function () {
  'use strict';

  /* --- 1. OFFER BAR SEASON SWITCHER ------------------------------------- */
  (function offerBar() {
    var bar = document.getElementById('offer-bar');
    if (!bar) return;
    var COPY = {
      summer: { msg: "AC out? We're on it — 24/7, 365.", cta: 'Call now' },
      winter: { msg: 'No heat? Certified techs on call 24/7.', cta: 'Call now' },
      spring: { msg: 'Book your AC tune-up before summer hits.', cta: 'Book now' },
      fall:   { msg: 'Furnace check before the first freeze.', cta: 'Book now' }
    };
    // An explicit data-season-lock opts the bar out of the seasonal rotation
    // and pins it to the message authored in the markup.
    //
    // Deliberately NOT gated on data-season="financing": v6.html carries that
    // same attribute (verified across all seven variants — v1-v5 are
    // "summer", v6 and v6.1 are "financing"), so keying on the value would
    // silently change the frozen v6 reference too. Opting in per page keeps
    // every other variant byte-for-byte in its reviewed behaviour.
    var isFinancingVariant = bar.hasAttribute('data-season-lock');
    var m = new Date().getMonth() + 1; // 1..12
    var season = (m >= 6 && m <= 8) ? 'summer'
               : (m >= 9 && m <= 11) ? 'fall'
               : (m === 12 || m === 1 || m === 2) ? 'winter'
               : 'spring';
    var c = isFinancingVariant
      ? { msg: 'Own your comfort with flexible financing options.', cta: 'Explore financing' }
      : COPY[season];
    if (!isFinancingVariant) bar.setAttribute('data-season', season);
    var msgEl = bar.querySelector('.offer-bar__msg');
    var ctaEl = bar.querySelector('.offer-bar__cta-label');
    if (msgEl) msgEl.textContent = c.msg;
    if (ctaEl) ctaEl.textContent = c.cta;
  })();

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

  /* --- 5. FORM VALIDATION + SUCCESS STATE ------------------------------- */
  (function contactForm() {
    var form = document.getElementById('estimate-form');
    if (!form) return;
    var status = document.getElementById('form-status');
    var success = document.getElementById('form-success');

    function fieldError(field) {
      var group = field.closest('.form-field');
      return group ? group.querySelector('.form-error') : null;
    }
    function setError(field, msg) {
      field.setAttribute('aria-invalid', 'true');
      var err = fieldError(field);
      if (err) { err.textContent = msg; err.classList.add('is-visible'); }
    }
    function clearError(field) {
      field.removeAttribute('aria-invalid');
      var err = fieldError(field);
      if (err) { err.textContent = ''; err.classList.remove('is-visible'); }
    }
    function validate() {
      var ok = true, firstBad = null;
      var name = form.elements['name'];
      var phone = form.elements['phone'];
      var service = form.elements['service'];

      if (!name.value.trim()) { setError(name, 'Please enter your name.'); ok = false; firstBad = firstBad || name; }
      else clearError(name);

      var digits = (phone.value.match(/\d/g) || []).length;
      if (!phone.value.trim()) { setError(phone, 'Please enter a phone number.'); ok = false; firstBad = firstBad || phone; }
      else if (digits < 10) { setError(phone, 'Please enter a valid 10-digit phone number.'); ok = false; firstBad = firstBad || phone; }
      else clearError(phone);

      if (!service.value) { setError(service, 'Please choose a service.'); ok = false; firstBad = firstBad || service; }
      else clearError(service);

      return { ok: ok, firstBad: firstBad };
    }

    // clear a field's error as the user fixes it
    ['name', 'phone', 'service'].forEach(function (n) {
      var el = form.elements[n];
      if (el) el.addEventListener('input', function () { if (el.getAttribute('aria-invalid') === 'true') clearError(el); });
      if (el && el.tagName === 'SELECT') el.addEventListener('change', function () { clearError(el); });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var res = validate();
      if (!res.ok) {
        if (status) status.textContent = 'Please fix the highlighted fields and try again.';
        if (res.firstBad) res.firstBad.focus();
        return;
      }
      // The form posts nowhere (action unset). Show the success state.
      form.setAttribute('hidden', 'hidden');
      if (success) {
        success.classList.add('is-visible');
        success.setAttribute('tabindex', '-1');
        success.focus();
      }
      if (status) status.textContent = 'Thanks — your request was received.';
    });
  })();

  /* ==========================================================================
     Config-driven modules. Everything below reads js/lenz-config.js, so the
     pending assets swap in from one place. Each module no-ops when its markup
     hook is absent, which keeps the three variants independent.
     ========================================================================== */
  var CFG = window.LENZ_CONFIG || {};

  /* --- 6. HERO COPY + HERO IMAGE ---------------------------------------- */
  (function heroContent() {
    var copy = CFG.HERO_COPY || {};
    var h1 = document.getElementById('hero-title');
    var sub = document.querySelector('.hero__sub');

    // The approved copy is server-rendered in the markup, where the H1 also
    // carries a <span class="accent"> for the highlighted phrase. Only rewrite
    // when the config text actually DIFFERS — otherwise setting textContent
    // would flatten that span and drop the accent styling for no reason.
    function sync(el, text) {
      if (!el || !text) return;
      var norm = function (s) { return s.replace(/[‘’]/g, "'").replace(/\s+/g, ' ').trim(); };
      if (norm(el.textContent) !== norm(text)) el.textContent = text;
    }
    sync(h1, copy.h1);
    sync(sub, copy.subhead);

    var img = document.querySelector('.hero__media img[data-hero-image]');
    var hero = CFG.LENZ_HERO_IMAGE;
    if (img && hero && hero.src) {
      img.src = hero.src;
      img.alt = hero.alt || '';
      if (hero.width) img.width = hero.width;
      if (hero.height) img.height = hero.height;
    }
  })();

  /* --- 7. LOGO ----------------------------------------------------------- */
  (function logos() {
    var logo = CFG.LENZ_LOGO;
    if (!logo) return;
    document.querySelectorAll('img[data-logo]').forEach(function (img) {
      var surface = img.getAttribute('data-logo'); // "light" | "dark"
      var src = surface === 'dark' ? logo.reversed : logo.standard;
      if (src) img.src = src;
      // Decorative footer marks keep alt="" — only label the linked ones.
      if (img.alt !== '') img.alt = logo.alt || 'Lenz Heating & Cooling';
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

    var brands = CFG.BRAND_LOGOS || [];
    var byName = {};
    brands.forEach(function (b) { byName[b.name] = b; });

    // Upgrade wordmarks to logo images where a file exists.
    track.querySelectorAll('.brand-logo').forEach(function (a) {
      var b = byName[a.getAttribute('data-brand')];
      if (!b) return;
      if (b.url) a.href = b.url;
      if (!b.src) return;
      var img = document.createElement('img');
      img.src = b.src;
      img.alt = b.name + ' HVAC equipment serviced by Lenz';
      img.loading = 'lazy';
      img.decoding = 'async';
      a.innerHTML = '';
      a.removeAttribute('aria-label');
      a.appendChild(img);
    });

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

  /* --- 12. WHO 13 NEWS SEGMENT ------------------------------------------ */
  /* The section ships with a labelled placeholder. As soon as WHO13.videoUrl
     is set, the placeholder is swapped for a lazy-loaded player. */
  (function who13() {
    var cfg = CFG.WHO13 || {};
    var cta = document.querySelector('[data-who13-cta]');
    if (cta && cfg.segmentsUrl) {
      cta.href = cfg.segmentsUrl;
      cta.target = '_blank';
      cta.rel = 'noopener noreferrer';
    }

    var media = document.querySelector('[data-who13-media]');
    if (!media || !cfg.videoUrl) return;
    var frame = document.createElement('iframe');
    frame.src = cfg.videoUrl;
    frame.title = 'Lenz Heating & Cooling on WHO 13 News Hello Iowa!';
    frame.loading = 'lazy';
    frame.allow = 'accelerometer; clipboard-write; encrypted-media; picture-in-picture';
    frame.allowFullscreen = true;
    media.innerHTML = '';
    media.appendChild(frame);
  })();

  /* --- 11. FINANCING CTA ------------------------------------------------- */
  (function financingCta() {
    var cta = document.querySelector('[data-financing-cta]');
    var fin = CFG.FINANCING;
    if (cta && fin && fin.applyUrl) cta.href = fin.applyUrl;
  })();

  /* --- 9. SERVICE AREA MAP ---------------------------------------------- */
  (function serviceAreaMap() {
    var frame = document.querySelector('iframe[data-gbp-map]');
    if (frame && CFG.GBP_EMBED_URL) frame.src = CFG.GBP_EMBED_URL;

    var dir = document.querySelector('[data-directions]');
    if (dir && CFG.GBP_DIRECTIONS_URL) dir.href = CFG.GBP_DIRECTIONS_URL;

    var reviewsLink = document.querySelector('[data-gbp-reviews-link]');
    var gbp = CFG.GOOGLE_REVIEWS;
    if (reviewsLink && gbp && gbp.profileUrl) reviewsLink.href = gbp.profileUrl;
  })();

  /* --- 10. GOOGLE REVIEWS ------------------------------------------------ */
  /* Renders live Google reviews when a proxy endpoint is configured, and the
     hardcoded quotes already in the markup otherwise. The Places API key must
     stay server-side, so `endpoint` is expected to be our own proxy, never
     Google directly. */
  (function googleReviews() {
    var root = document.getElementById('google-reviews');
    if (!root) return;

    var cfg = CFG.GOOGLE_REVIEWS || {};
    var skeleton = root.querySelector('[data-reviews-skeleton]');
    var live = root.querySelector('[data-reviews-live]');
    var fallback = root.querySelector('[data-reviews-fallback]');

    function showFallback() {
      if (skeleton) skeleton.hidden = true;
      if (live) live.hidden = true;
      if (fallback) fallback.hidden = false;
    }

    // Not wired up yet — go straight to the fallback, no skeleton flash.
    if (!cfg.PLACE_ID || !cfg.endpoint) { showFallback(); return; }

    if (skeleton) skeleton.hidden = false;
    if (fallback) fallback.hidden = true;

    var url = cfg.endpoint +
      (cfg.endpoint.indexOf('?') === -1 ? '?' : '&') +
      'place_id=' + encodeURIComponent(cfg.PLACE_ID);

    fetch(url, { headers: { Accept: 'application/json' } })
      .then(function (r) {
        if (!r.ok) throw new Error('Reviews request failed: ' + r.status);
        return r.json();
      })
      .then(function (data) {
        var reviews = (data && data.reviews) || [];
        if (!reviews.length) throw new Error('No reviews returned');
        render(data, reviews);
      })
      .catch(function (err) {
        if (window.console) console.warn('[lenz] Google reviews unavailable, using fallback.', err);
        showFallback();
      });

    function starsMarkup(rating) {
      var n = Math.round(rating) || 5;
      var out = '<span class="stars" role="img" aria-label="' + n + ' out of 5 stars">';
      for (var i = 0; i < n; i++) {
        out += '<svg viewBox="0 0 24 24" aria-hidden="true" ' +
               'style="fill:var(--color-star);stroke:var(--color-star-edge);stroke-width:1">' +
               '<use href="#i-star"/></svg>';
      }
      return out + '</span>';
    }
    function esc(s) {
      return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
      });
    }
    function card(r, featured) {
      return '<figure class="' + (featured ? 'review-feature' : 'review-card') + '">' +
        starsMarkup(r.rating) +
        '<blockquote>' + esc(r.text) + '</blockquote>' +
        '<figcaption class="review-name">— ' + esc(r.author_name) +
        (r.relative_time_description
          ? ' <span class="review-date">' + esc(r.relative_time_description) + '</span>'
          : '') +
        '</figcaption></figure>';
    }

    function render(data, reviews) {
      // Featured = the longest recent 5-star review.
      var fives = reviews.filter(function (r) { return Math.round(r.rating) === 5; });
      var pool = fives.length ? fives : reviews;
      var featured = pool.slice().sort(function (a, b) {
        return (b.text || '').length - (a.text || '').length;
      })[0];
      var rest = reviews.filter(function (r) { return r !== featured; }).slice(0, 2);

      var summary =
        '<div class="reviews__summary">' +
          starsMarkup(data.rating) +
          '<span class="reviews__rating">' + esc((data.rating || 5).toFixed(1)) + '</span>' +
          '<span class="reviews__count">' + esc(data.user_ratings_total || reviews.length) +
            ' Google reviews</span>' +
          '<a class="reviews__link" href="' + esc(data.url || cfg.profileUrl) + '" ' +
            'target="_blank" rel="noopener noreferrer">Read all reviews on Google</a>' +
        '</div>';

      live.innerHTML = summary +
        '<div class="reviews__grid">' + card(featured, true) +
        '<div class="review-side">' + rest.map(function (r) { return card(r, false); }).join('') +
        '</div></div>';

      if (skeleton) skeleton.hidden = true;
      if (fallback) fallback.hidden = true;
      live.hidden = false;

      // Rating is now verified, so the AggregateRating schema can be emitted.
      var ld = document.createElement('script');
      ld.type = 'application/ld+json';
      ld.textContent = JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'HVACBusiness',
        name: 'Lenz Heating & Cooling',
        aggregateRating: {
          '@type': 'AggregateRating',
          ratingValue: data.rating,
          reviewCount: data.user_ratings_total || reviews.length
        },
        review: reviews.slice(0, 5).map(function (r) {
          return {
            '@type': 'Review',
            author: { '@type': 'Person', name: r.author_name },
            reviewRating: { '@type': 'Rating', ratingValue: r.rating, bestRating: 5 },
            reviewBody: r.text
          };
        })
      });
      document.head.appendChild(ld);
    }
  })();
})();
