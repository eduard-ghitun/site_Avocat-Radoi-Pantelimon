const menuButton = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('#mobile-menu');
const siteHeader = document.querySelector('.site-header');

if (siteHeader) {
  const updateHeader = () => siteHeader.classList.toggle('is-scrolled', window.scrollY > 24);
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });
}

if (menuButton && mobileMenu) {
  const closeMenu = () => {
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Deschide meniul');
    mobileMenu.hidden = true;
    document.body.classList.remove('menu-open');
  };
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Închide meniul' : 'Deschide meniul');
    mobileMenu.hidden = !open;
    document.body.classList.toggle('menu-open', open);
  });
  mobileMenu.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeMenu();
  });
  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) closeMenu();
  });
}

const mailFallback = document.querySelector('#mail-fallback');
const showMailFallback = (subject = '', body = '') => {
  if (!mailFallback) return;
  const email = mailFallback.dataset.email;
  const gmail = new URL('https://mail.google.com/mail/');
  gmail.search = new URLSearchParams({ view: 'cm', fs: '1', to: email, ...(subject ? { su: subject } : {}), ...(body ? { body } : {}) });
  const outlook = new URL('https://outlook.live.com/mail/0/deeplink/compose');
  outlook.search = new URLSearchParams({ to: email, ...(subject ? { subject } : {}), ...(body ? { body } : {}) });
  mailFallback.querySelector('.mail-gmail').href = gmail.href;
  mailFallback.querySelector('.mail-outlook').href = outlook.href;
  const copyValue = mailFallback.querySelector('#mail-copy-value');
  copyValue.value = subject ? `Către: ${email}\nSubiect: ${subject}\n\n${body}` : email;
  copyValue.rows = subject ? 6 : 1;
  mailFallback.querySelector('.mail-copy-button').textContent = subject ? 'Copiază mesajul' : 'Copiază adresa';
  mailFallback.querySelector('.mail-copy-status').textContent = '';
  mailFallback.hidden = false;
};

if (mailFallback) {
  document.querySelectorAll('a[href^="mailto:"]').forEach(link => {
    link.addEventListener('click', () => showMailFallback());
  });
  mailFallback.querySelector('.mail-fallback-close').addEventListener('click', () => {
    mailFallback.hidden = true;
  });
  mailFallback.querySelector('.mail-copy-button').addEventListener('click', async () => {
    const value = mailFallback.querySelector('#mail-copy-value');
    const status = mailFallback.querySelector('.mail-copy-status');
    try {
      await navigator.clipboard.writeText(value.value);
      status.textContent = 'Copiat. Poți lipi textul în aplicația ta de email.';
    } catch {
      value.focus();
      value.select();
      status.textContent = 'Textul este selectat. Copiază-l și lipește-l în aplicația ta de email.';
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') mailFallback.hidden = true;
  });
}

const form = document.querySelector('#contact-form');
if (form) {
  const status = document.querySelector('#form-status');
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = Object.fromEntries(new FormData(form).entries());
    if (!data.consent) {
      status.textContent = 'Confirmă acordul pentru prelucrarea datelor.';
      return;
    }
    const message = `Nume: ${data.name}\nEmail: ${data.email}\nTelefon: ${data.phone || '—'}\n\nMesaj:\n${data.message}`;
    status.textContent = 'Se deschide WhatsApp. Apasă Trimite în WhatsApp pentru a expedia mesajul.';
    window.location.href = `https://wa.me/40785869247?text=${encodeURIComponent(message)}`;
  });
}
