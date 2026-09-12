document.addEventListener('DOMContentLoaded', () => {
  const burger = document.getElementById('burger');
  const navLinks = document.getElementById('navLinks');
  if (burger && navLinks) {
    burger.addEventListener('click', () => {
      burger.classList.toggle('open');
      navLinks.classList.toggle('open');
    });
    navLinks.querySelectorAll('a').forEach(a =>
      a.addEventListener('click', () => {
        burger.classList.remove('open');
        navLinks.classList.remove('open');
      })
    );
  }

  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(el => observer.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('visible'));
  }

  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      const success = document.getElementById('formSuccess');
      if (success) success.classList.remove('show');
      btn.disabled = true;
      btn.textContent = 'Sending...';

      const data = {
        name: form.querySelector('[name="name"]').value,
        email: form.querySelector('[name="email"]').value,
        service: form.querySelector('[name="service"]').value,
        message: form.querySelector('[name="message"]').value,
      };

      try {
        const resp = await fetch('/api/contact/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });
        const result = await resp.json();
        if (result.success) {
          if (success) success.classList.add('show');
          form.reset();
          setTimeout(() => success && success.classList.remove('show'), 5000);
        } else {
          alert('Xabar yuborishda xatolik. Qaytadan urinib ko\'ring.');
        }
      } catch (err) {
        alert('Xabar yuborishda xatolik. Qaytadan urinib ko\'ring.');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Send Message';
      }
    });
  }
});
