/**
 * Gujarat UCC Information Platform
 * Interactive UX & Client Helpers
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Language Switcher Helper
  const langButtons = document.querySelectorAll('.lang-btn');
  langButtons.forEach(btn => {
    btn.addEventListener('click', function (e) {
      const selectedLang = this.getAttribute('data-lang');
      if (selectedLang) {
        e.preventDefault();
        const url = new URL(window.location.href);
        url.searchParams.set('lang', selectedLang);
        window.location.href = url.toString();
      }
    });
  });

  // 2. FAQ Accordion Handler
  const faqButtons = document.querySelectorAll('.faq-question-btn');
  faqButtons.forEach(button => {
    button.addEventListener('click', function () {
      const pane = this.nextElementSibling;
      const isOpen = pane.style.display === 'block';

      // Toggle state
      pane.style.display = isOpen ? 'none' : 'block';
      const indicator = this.querySelector('.faq-indicator');
      if (indicator) {
        indicator.textContent = isOpen ? '+' : '−';
      }
    });
  });

  // 3. Smooth scroll for Table of Contents
  const tocLinks = document.querySelectorAll('.toc-list a');
  tocLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId && targetId.startsWith('#')) {
        const targetEl = document.querySelector(targetId);
        if (targetEl) {
          e.preventDefault();
          targetEl.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });

  // 4. Navigation Dropdown & Mobile Menu Handler
  const mobileToggle = document.getElementById('mobileMenuToggle');
  const mainNavLinks = document.getElementById('mainNavLinks');

  if (mobileToggle && mainNavLinks) {
    mobileToggle.addEventListener('click', function () {
      const isOpen = mainNavLinks.classList.toggle('mobile-open');
      mobileToggle.setAttribute('aria-expanded', isOpen);
      const iconHam = mobileToggle.querySelector('.icon-hamburger');
      const iconClose = mobileToggle.querySelector('.icon-close');
      if (iconHam && iconClose) {
        iconHam.style.display = isOpen ? 'none' : 'inline-block';
        iconClose.style.display = isOpen ? 'inline-block' : 'none';
      }
    });
  }

  // Handle dropdown triggers on click/touch
  const dropdownTriggers = document.querySelectorAll('.nav-dropdown > .dropdown-trigger');
  dropdownTriggers.forEach(trigger => {
    trigger.addEventListener('click', function (e) {
      const parent = this.parentElement;
      // On mobile or on clicking arrow or button, toggle dropdown
      if (window.innerWidth <= 860 || e.target.closest('.dropdown-arrow')) {
        e.preventDefault();
        const wasOpen = parent.classList.contains('is-open');
        document.querySelectorAll('.nav-dropdown.is-open').forEach(d => {
          if (d !== parent) d.classList.remove('is-open');
        });
        parent.classList.toggle('is-open', !wasOpen);
      }
    });
  });

  // Close dropdowns on click outside
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-dropdown')) {
      document.querySelectorAll('.nav-dropdown.is-open').forEach(d => {
        d.classList.remove('is-open');
      });
    }
  });

  // Close on Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.nav-dropdown.is-open').forEach(d => {
        d.classList.remove('is-open');
      });
      if (mainNavLinks && mainNavLinks.classList.contains('mobile-open')) {
        mainNavLinks.classList.remove('mobile-open');
        if (mobileToggle) {
          mobileToggle.setAttribute('aria-expanded', 'false');
          const iconHam = mobileToggle.querySelector('.icon-hamburger');
          const iconClose = mobileToggle.querySelector('.icon-close');
          if (iconHam && iconClose) {
            iconHam.style.display = 'inline-block';
            iconClose.style.display = 'none';
          }
        }
      }
    }
  });
});
