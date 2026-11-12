(function () {
  var t = document.getElementById('navToggle');
  var nav = document.getElementById('nav');
  if (t && nav) {
    t.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // FAQ accordion
  document.querySelectorAll('.faq-q').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.parentElement;
      var open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  // Reveal on scroll
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { threshold: 0.08 }) : null;
  document.querySelectorAll('.car-card, .cat-tile, .trust-card, .cta-band').forEach(function (el) {
    el.classList.add('reveal');
    if (io) { io.observe(el); } else { el.classList.add('in'); }
  });
})();
