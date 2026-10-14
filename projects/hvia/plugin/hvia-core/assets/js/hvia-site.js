/* HVIA front-end behaviour, ported from the prototype's js/main.js (option 2; main.js is shared by all three options):
   sticky-header state, mobile nav, active-link spy, scroll reveals, footer year.
   Dropped: the option switcher, the Review panel and the bio dialogs (prototype only). */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Sticky header state */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 12); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* Mobile nav */
  var nav = document.querySelector('.main-nav');
  var navToggle = document.querySelector('.nav-toggle');
  if (nav && navToggle) {
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
  }

  /* Active nav link while scrolling */
  if (nav && 'IntersectionObserver' in window) {
    var links = {};
    nav.querySelectorAll('a[href^="#"]').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
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

  /* Footer year */
  var y = document.getElementById('year');
  if (y) y.textContent = String(new Date().getFullYear());
})();
