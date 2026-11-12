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

// Mobile menu
const burger = document.querySelector('.burger');
const nav = document.getElementById('nav');
if (burger && nav) {
  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });
  nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
    nav.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
  }));
}

// Respect reduced-motion: keep the hero video on its poster frame
const heroVideo = document.querySelector('.hero-v__video');
if (heroVideo) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    heroVideo.removeAttribute('autoplay');
    heroVideo.pause();
  } else {
    // some browsers skip autoplay in background tabs; start it once visible
    const tryPlay = () => { if (!document.hidden && heroVideo.paused) heroVideo.play().catch(() => {}); };
    document.addEventListener('visibilitychange', tryPlay);
    heroVideo.addEventListener('canplay', tryPlay, { once: true });
    tryPlay();
  }
}

// Hero journey steps: highlight the stage that is playing, click to jump
(() => {
  const video = document.querySelector('.hero-v__video');
  const items = [...document.querySelectorAll('.hero-v__steps li')];
  if (!video || !items.length) return;
  const starts = items.map((li) => parseFloat(li.dataset.t));
  let current = -1;
  const update = () => {
    const t = video.currentTime;
    const dur = video.duration || 0;
    let i = 0;
    while (i + 1 < starts.length && t >= starts[i + 1]) i++;
    if (i !== current) {
      items.forEach((li, k) => li.classList.toggle('is-active', k === i));
      current = i;
    }
    const end = i + 1 < starts.length ? starts[i + 1] : dur;
    const p = end > starts[i] ? Math.min(1, (t - starts[i]) / (end - starts[i])) : 0;
    items[i].style.setProperty('--p', p.toFixed(3));
  };
  const loop = () => { update(); if (!video.paused) requestAnimationFrame(loop); };
  video.addEventListener('play', () => requestAnimationFrame(loop));
  video.addEventListener('timeupdate', update); // also fires when animation frames are paused
  video.addEventListener('seeked', update);
  video.addEventListener('loadedmetadata', update);
  items.forEach((li, k) => li.querySelector('button').addEventListener('click', () => {
    video.currentTime = starts[k] + 0.05;
    update();
  }));
  update();
})();
