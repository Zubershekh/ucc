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
});
