// Reveal-on-scroll
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

// Accordion: keep only one item open per list
document.querySelectorAll('[data-accordion]').forEach((acc) => {
  acc.querySelectorAll('details').forEach((d) => {
    d.addEventListener('toggle', () => {
      if (!d.open) return;
      acc.querySelectorAll('details[open]').forEach((o) => { if (o !== d) o.open = false; });
    });
  });
});

// Site header: solid on scroll, mobile slide-in menu with accordion dropdowns
(() => {
  const header = document.querySelector('.site-header');
  const nav = document.querySelector('.main-nav');
  const toggle = document.querySelector('.nav-toggle');
  if (!header) return;

  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 40);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  if (!nav || !toggle) return;
  const mq = window.matchMedia('(max-width: 980px)');
  const setMenu = (open) => {
    nav.classList.toggle('open', open);
    header.classList.toggle('menu-open', open);
    document.body.classList.toggle('nav-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (!open) nav.querySelectorAll('.sub-open').forEach((el) => {
      el.classList.remove('sub-open');
      el.firstElementChild.setAttribute('aria-expanded', 'false');
    });
  };
  toggle.addEventListener('click', () => setMenu(!nav.classList.contains('open')));

  // On phones, dropdown parents expand their sub-links instead of navigating
  nav.querySelectorAll('.nav-item.has-sub > .nav-link').forEach((link) => {
    link.addEventListener('click', (e) => {
      if (!mq.matches) return;
      e.preventDefault();
      const item = link.parentElement;
      const open = !item.classList.contains('sub-open');
      nav.querySelectorAll('.nav-item.sub-open').forEach((el) => {
        if (el !== item) { el.classList.remove('sub-open'); el.firstElementChild.setAttribute('aria-expanded', 'false'); }
      });
      item.classList.toggle('sub-open', open);
      link.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  // Close after choosing a destination, on Escape, or when widening to desktop
  nav.addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (a && !a.matches('.nav-item.has-sub > .nav-link')) setMenu(false);
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); toggle.focus(); }
  });
  mq.addEventListener('change', (e) => { if (!e.matches) setMenu(false); });
})();
