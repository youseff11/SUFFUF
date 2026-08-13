/* Editorial Engineering interaction layer — theme, language, mobile nav, reveal motion, gallery. */
(function () {
  const body = document.body;
  const root = document.documentElement;
  const savedTheme = localStorage.getItem('suffuf-theme');
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  body.classList.toggle('theme-dark', savedTheme ? savedTheme === 'dark' : prefersDark);
  body.dataset.theme = body.classList.contains('theme-dark') ? 'dark' : 'light';

  const language = localStorage.getItem('suffuf-language') === 'ar' ? 'ar' : 'en';
  function applyLanguage(next) {
    const isArabic = next === 'ar';
    root.lang = next;
    root.dir = isArabic ? 'rtl' : 'ltr';
    body.dir = root.dir;
    body.dataset.language = next;
    document.querySelectorAll('[data-en][data-ar]').forEach(function (element) {
      element.textContent = isArabic ? element.dataset.ar : element.dataset.en;
    });
    document.querySelectorAll('[data-en-placeholder][data-ar-placeholder]').forEach(function (element) {
      element.placeholder = isArabic ? element.dataset.arPlaceholder : element.dataset.enPlaceholder;
    });
    document.querySelectorAll('[data-lang-label]').forEach(function (element) { element.textContent = isArabic ? 'EN' : 'ع'; });
    localStorage.setItem('suffuf-language', next);
  }
  applyLanguage(language);
  document.querySelectorAll('[data-language-toggle]').forEach(function (button) {
    button.addEventListener('click', function () { applyLanguage(root.lang === 'ar' ? 'en' : 'ar'); });
  });
  document.querySelectorAll('[data-theme-toggle]').forEach(function (button) {
    button.addEventListener('click', function () {
      const dark = !body.classList.contains('theme-dark');
      body.classList.toggle('theme-dark', dark); body.dataset.theme = dark ? 'dark' : 'light';
      localStorage.setItem('suffuf-theme', dark ? 'dark' : 'light');
      button.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
    });
  });

  const menu = document.querySelector('[data-menu]');
  const menuToggle = document.querySelector('[data-menu-toggle]');
  if (menu && menuToggle) menuToggle.addEventListener('click', function () { menu.classList.toggle('open'); menuToggle.setAttribute('aria-expanded', menu.classList.contains('open') ? 'true' : 'false'); });
  document.querySelectorAll('.main-nav a').forEach(function (link) { link.addEventListener('click', function () { if (menu) menu.classList.remove('open'); }); });

  const observer = new IntersectionObserver(function (entries) { entries.forEach(function (entry) { if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); } }); }, { threshold: .1 });
  document.querySelectorAll('.reveal').forEach(function (element) { observer.observe(element); });

  const lightbox = document.querySelector('[data-lightbox-modal]');
  const lightboxImage = lightbox && lightbox.querySelector('img');
  if (lightbox && lightboxImage) {
    document.querySelectorAll('[data-lightbox]').forEach(function (trigger) { trigger.addEventListener('click', function () { lightboxImage.src = trigger.dataset.lightbox; lightbox.classList.add('open'); }); });
    lightbox.addEventListener('click', function (event) { if (event.target === lightbox || event.target.closest('[data-lightbox-close]')) lightbox.classList.remove('open'); });
    document.addEventListener('keydown', function (event) { if (event.key === 'Escape') lightbox.classList.remove('open'); });
  }
}());
