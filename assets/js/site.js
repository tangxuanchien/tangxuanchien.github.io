(function () {
  var root = document.documentElement;
  var buttons = document.querySelectorAll('.lang button');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- language switch ----
  function setLang(lang) {
    root.lang = lang;
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.set === lang)); });
    try { localStorage.setItem('lang', lang); } catch (e) {}
  }
  buttons.forEach(function (b) { b.addEventListener('click', function () { setLang(b.dataset.set); }); });
  setLang(root.lang === 'vi' ? 'vi' : 'en');

  // ---- nav border + progress bar fallback ----
  var nav = document.querySelector('.nav');
  var bar = document.querySelector('.nav .progress');
  var cssTimelines = window.CSS && CSS.supports && CSS.supports('animation-timeline: view()');
  function onScroll() {
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 8);
    if (bar && !cssTimelines && !reduce) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, window.scrollY / max) : 0) + ')';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (!('IntersectionObserver' in window)) return;

  // ---- reveal fallback for browsers without CSS scroll timelines ----
  // Only items that start below the fold are hidden, and only once JS is running,
  // so nothing on screen can ever be left blank.
  if (!cssTimelines && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var idx = Array.prototype.indexOf.call(e.target.parentNode.children, e.target);
          e.target.style.transitionDelay = (idx % 3) * 80 + 'ms';
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -6% 0px' });
    document.querySelectorAll('.rv').forEach(function (el) {
      if (el.getBoundingClientRect().top > window.innerHeight) {
        el.classList.add('pre');
        io.observe(el);
      }
    });
  }

  // ---- count-up numbers ----
  function fmt(n) {
    var units = [[1e9, 'B'], [1e6, 'M'], [1e3, 'K']];
    for (var i = 0; i < units.length; i++) {
      if (n >= units[i][0]) {
        var v = n / units[i][0];
        return (v < 100 ? (Math.round(v * 10) / 10).toString() : Math.round(v).toString()) + units[i][1];
      }
    }
    return Math.round(n).toString();
  }
  if (!reduce) {
    var counters = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target, target = parseInt(el.getAttribute('data-count'), 10) || 0;
        counters.unobserve(el);
        if (target < 2) return;
        var start = null, dur = 1400;
        function step(ts) {
          if (start === null) start = ts;
          var p = Math.min(1, (ts - start) / dur);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = fmt(target * eased);
          if (p < 1) requestAnimationFrame(step); else el.textContent = fmt(target);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    document.querySelectorAll('[data-count]').forEach(function (el) { counters.observe(el); });
  }
})();
