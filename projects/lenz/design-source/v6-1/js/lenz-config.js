/* ============================================================================
   lenz-config.js — SINGLE SWAP POINT for every asset, URL and copy string that
   is still pending from the team. Loaded before lenz.js on all three variants.

   Everything marked TODO is a placeholder. Replace the value here and it
   updates across index.html, v2.html and v3.html at once — do not hardcode
   these anywhere else.
   ============================================================================ */
(function (global) {
  'use strict';

  /* --- Hero ------------------------------------------------------------- */

  /* TODO(asset): approved in-home Lenz photography. Must read as "comfortable
     home" — natural light, living space, visible Lenz branding on the tech or
     vehicle. NOT a mechanical room or a basement repair shot.
     lenz-comfort.webp is the closest existing in-home frame and is a STAND-IN:
     it has the right emotional register but shows no technician and no Lenz
     branding, so the alt below describes what is actually in the frame. When
     the approved photography lands, update the alt with it — the brief's
     suggested "Lenz technician in a Des Moines family home" only becomes
     accurate once a technician is actually in the shot. */
  var LENZ_HERO_IMAGE = {
    src: 'assets/img/lenz-comfort.webp',
    alt: 'A family relaxing together in a bright, comfortable Des Moines living room',
    width: 1024,
    height: 1024
  };

  /* RESOLVED: the content team's prepared H1 and body copy, from the approved
     home page document. Both now ship in the markup (server-rendered for SEO);
     these values mirror them so a copy change can be made in one place.

     Note for anyone reading the revision brief: that brief quoted
     "Des Moines HVAC Repair & Install" as the interim H1, but that string is
     the SEO <title>, not the headline. The approved H1 is below. */
  var HERO_COPY = {
    h1: "Des Moines' Trusted Heating, Cooling & Air Quality Experts",
    subhead: "Since 2009, Lenz Heating & Cooling has been Central Iowa's go-to team for honest, hassle-free home comfort. We're a local, veteran-owned, and family-run business based right here in Urbandale, dedicated to keeping your home comfortable in every season. Whether you need 24/7 emergency HVAC repair, a new furnace, or a high-efficiency AC installation, we proudly serve homeowners across Des Moines, West Des Moines, Ankeny, Waukee, and surrounding Central Iowa communities."
  };

  /* --- WHO 13 News / Hello Iowa! ---------------------------------------- */

  /* TODO(asset): the Hello Iowa! segment to embed, plus the destination for
     "Watch Our Latest News Segments". While videoUrl is null the section
     renders a labelled placeholder instead of a player. Use the youtube-nocookie
     embed form, e.g. https://www.youtube-nocookie.com/embed/<id> */
  var WHO13 = {
    videoUrl: 'https://www.youtube-nocookie.com/embed/8jsNz6yxry0',
    segmentsUrl: null
  };

  /* --- Logo -------------------------------------------------------------- */

  /* TODO(asset): both lockups as SVG. Today they are transparent PNGs, picked
     per surface by the `data-logo` attribute on each <img>:
       standard -> dark ink, purple sub-line. For LIGHT surfaces.
       reversed -> white keyline + white sub-line. For DARK surfaces.
     What matters is the surface the mark actually lands on, not the section
     around it: V3's footer keeps a white plate, so it takes `standard` even
     though that footer is navy. V1 and V2 run plateless, so their dark
     surfaces take `reversed`. */
  var LENZ_LOGO = {
    standard: 'assets/img/lenz-logo-new-dark.png',
    reversed: 'assets/img/lenz-logo-new.png',
    alt: 'Lenz Heating & Cooling'
  };

  /* --- Brand logo marquee ------------------------------------------------ */

  /* TODO(asset): manufacturer logo files for all nine brands. `src: null`
     renders an accessible text wordmark in place of the image, so the marquee
     works today and upgrades cleanly once the SVGs land. */
  var BRAND_LOGOS = [
    { name: 'Carrier',        src: null, url: 'https://www.carrier.com/' },
    { name: 'Goodman',        src: null, url: 'https://www.goodmanmfg.com/' },
    { name: 'Lennox',         src: null, url: 'https://www.lennox.com/' },
    { name: 'Rheem',          src: null, url: 'https://www.rheem.com/' },
    { name: 'Trane',          src: null, url: 'https://www.trane.com/' },
    { name: 'Ruud',           src: null, url: 'https://www.ruud.com/' },
    { name: 'American Pride', src: null, url: 'https://www.americanpridehvac.com/' },
    { name: 'Amana',          src: null, url: 'https://www.amana-hac.com/' },
    { name: 'Optimus',        src: null, url: 'https://www.optimushvac.com/' },
    { name: 'Bryant',         src: null, url: 'https://www.bryant.com/' }
  ];

  /* --- Service area map -------------------------------------------------- */

  /* TODO(asset): Google Business Profile embed URL for the Urbandale shop.
     This is a plain address query embed, which needs no API key — swap it for
     the GBP place embed once the Place ID is confirmed. */
  var GBP_EMBED_URL =
    'https://www.google.com/maps?q=7641+Douglas+Avenue,+Urbandale,+IA+50322&output=embed';

  var GBP_DIRECTIONS_URL =
    'https://www.google.com/maps/dir/?api=1&destination=7641+Douglas+Avenue,+Urbandale,+IA+50322';

  /* --- Google reviews ---------------------------------------------------- */

  /* TODO(integration): Google Business Profile Place ID.
     While PLACE_ID is null the widget renders the hardcoded fallback quotes.
     `endpoint` must point at a server-side proxy that returns the reviews
     payload — the Places API key must never ship in the browser bundle. */
  var GOOGLE_REVIEWS = {
    PLACE_ID: null,
    endpoint: null,
    profileUrl: 'https://www.google.com/maps/search/?api=1&query=Lenz+Heating+and+Cooling+Urbandale+IA'
  };

  /* --- Financing --------------------------------------------------------- */

  /* TODO(input): financing partner terms and the real destination URL.
     The FAQ copy already names Synchrony Bank; `applyUrl` stays an on-page
     anchor until the approved application link is supplied. */
  var FINANCING = {
    applyUrl: '#contact',
    partner: 'Synchrony Bank'
  };

  /* --- Services ---------------------------------------------------------- */

  /* The four sitemap categories and their eighteen sub-services. This array is
     the single source for the mega menu, the services grid and the footer.

     TODO(input): real service page URLs. The slugs below are placeholders that
     mirror the sitemap structure — they are NOT live pages yet. */
  var SERVICES = [
    {
      category: 'Air Conditioning',
      icon: 'i-snow',
      blurb: 'Repairs, tune-ups and right-sized replacements for hot Iowa summers.',
      url: '/services/air-conditioning/',
      items: [
        { name: 'AC Installation', url: '/services/air-conditioning/ac-installation/', icon: 'i-snow', blurb: 'Right-sized systems, installed properly.' },
        { name: 'AC Repair',       url: '/services/air-conditioning/ac-repair/',       icon: 'i-wrench', blurb: 'Fast diagnosis, day or night.' },
        { name: 'AC Maintenance',  url: '/services/air-conditioning/ac-maintenance/',  icon: 'i-calendar', blurb: 'Seasonal tune-ups that prevent breakdowns.' },
        { name: 'AC Replacement',  url: '/services/air-conditioning/ac-replacement/',  icon: 'i-snow', blurb: 'Efficient upgrades sized to your home.' }
      ]
    },
    {
      category: 'Heating',
      icon: 'i-flame',
      blurb: 'Dependable heat for Central Iowa winters, from repairs to full replacements.',
      url: '/services/heating/',
      items: [
        { name: 'Heating Installation', url: '/services/heating/heating-installation/', icon: 'i-flame', blurb: 'High-efficiency gas and electric furnaces.' },
        { name: 'Heating Repair',       url: '/services/heating/heating-repair/',       icon: 'i-wrench', blurb: 'No heat? We diagnose it fast.' },
        { name: 'Heating Maintenance',  url: '/services/heating/heating-maintenance/',  icon: 'i-calendar', blurb: 'Safety inspections before the first freeze.' },
        { name: 'Heating Replacement',  url: '/services/heating/heating-replacement/',  icon: 'i-heat', blurb: 'Upgrade an aging or failing furnace.' }
      ]
    },
    {
      category: 'Indoor Air Quality',
      icon: 'i-air',
      blurb: 'Cleaner, better-balanced air in every room of the house.',
      url: '/services/indoor-air-quality/',
      items: [
        { name: 'Humidity Control',      url: '/services/indoor-air-quality/humidity-control/',      icon: 'i-droplet', blurb: 'Whole-home humidifiers and dehumidifiers.' },
        { name: 'UV Light Purification', url: '/services/indoor-air-quality/uv-light-purification/', icon: 'i-shield', blurb: 'Treat air as it moves through the system.' },
        { name: 'Indoor Purification',   url: '/services/indoor-air-quality/indoor-purification/',   icon: 'i-air', blurb: 'Filtration for dust, dander and allergens.' },
        { name: 'Duct Cleaning',         url: '/services/indoor-air-quality/duct-cleaning/',         icon: 'i-wind', blurb: 'Clear out built-up dust and debris.' }
      ]
    },
    {
      category: 'Additional Services',
      icon: 'i-wrench',
      blurb: 'The rest of the home comfort work our licensed techs handle.',
      url: '/services/additional-services/',
      items: [
        { name: 'Thermostat Services',  url: '/services/additional-services/thermostat-services/',  icon: 'i-calendar', blurb: 'Smart thermostat install and setup.' },
        { name: 'Water Heater Services', url: '/services/additional-services/water-heater-services/', icon: 'i-droplet', blurb: 'Tank and tankless, professionally installed.' },
        { name: 'Ductwork',             url: '/services/additional-services/ductwork/',             icon: 'i-wind', blurb: 'Repairs, modifications and airflow balancing.' },
        { name: 'Gas Lines',            url: '/services/additional-services/gas-lines/',            icon: 'i-flame', blurb: 'Safe runs for appliances and outdoor setups.' },
        { name: 'Heat Pumps',           url: '/services/additional-services/heat-pumps/',           icon: 'i-heat', blurb: 'Heating and cooling from one efficient system.' }
      ]
    }
  ];

  /* --- Top-level navigation, in sitemap order ---------------------------- */
  /* "Services" is a label, not a link: it has no href and must not navigate. */
  var NAV_ITEMS = [
    { label: 'Services',          megaMenu: true },
    { label: 'Maintenance Plans', href: '#plans' },
    /* TODO(input): Specials is a standalone page on the sitemap with no
       on-page equivalent yet. Placeholder slug, same as the service URLs. */
    { label: 'Specials',          href: '/specials/' },
    { label: 'Financing',         href: '#financing' },
    { label: 'Service Areas',     href: '#area' },
    { label: 'About Us',          href: '#about' },
    { label: 'Contact Us',        href: '#contact' }
  ];

  global.LENZ_CONFIG = {
    LENZ_HERO_IMAGE: LENZ_HERO_IMAGE,
    HERO_COPY: HERO_COPY,
    WHO13: WHO13,
    LENZ_LOGO: LENZ_LOGO,
    BRAND_LOGOS: BRAND_LOGOS,
    GBP_EMBED_URL: GBP_EMBED_URL,
    GBP_DIRECTIONS_URL: GBP_DIRECTIONS_URL,
    GOOGLE_REVIEWS: GOOGLE_REVIEWS,
    FINANCING: FINANCING,
    SERVICES: SERVICES,
    NAV_ITEMS: NAV_ITEMS
  };
})(window);
