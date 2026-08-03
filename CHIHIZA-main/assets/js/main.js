// CHIHIZA — Main Script
// Handles: header scroll, mobile menu, fade-in, lazy loading, counters, toast, lightbox

(function () {
  'use strict';

  // ========================
  // HEADER SCROLL EFFECT
  // ========================
  var header = document.querySelector('.header');
  var lastScroll = 0;

  function handleScroll() {
    var currentScroll = window.scrollY;
    if (currentScroll > 80) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    lastScroll = currentScroll;
  }

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  // ========================
  // MOBILE MENU
  // ========================
  var menuToggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.nav');

  if (menuToggle && nav) {
    menuToggle.addEventListener('click', function () {
      menuToggle.classList.toggle('active');
      nav.classList.toggle('active');
      document.body.style.overflow = nav.classList.contains('active') ? 'hidden' : '';
    });

    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        menuToggle.classList.remove('active');
        nav.classList.remove('active');
        document.body.style.overflow = '';
      });
    });

    // Also close menu when clicking play button
    var teamToggle = document.getElementById('teamToolsToggle');
    if (teamToggle) {
      teamToggle.addEventListener('click', function () {
        menuToggle.classList.remove('active');
        nav.classList.remove('active');
        document.body.style.overflow = '';
      });
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('active')) {
        menuToggle.classList.remove('active');
        nav.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  }

  // ========================
  // FADE-IN ON SCROLL
  // ========================
  var fadeElements = document.querySelectorAll('.fade-in');

  if ('IntersectionObserver' in window) {
    var fadeObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            fadeObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -60px 0px' }
    );
    fadeElements.forEach(function (el) { fadeObserver.observe(el); });
  } else {
    fadeElements.forEach(function (el) { el.classList.add('visible'); });
  }

  // ========================
  // SMOOTH SCROLL FOR ANCHORS
  // ========================
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ========================
  // LAZY LOADING (native + fallback)
  // ========================
  if ('loading' in HTMLImageElement.prototype) {
    document.querySelectorAll('img[loading="lazy"]').forEach(function (img) {
      img.src = img.src;
    });
  } else if ('IntersectionObserver' in window) {
    var lazyImages = document.querySelectorAll('img[loading="lazy"]');
    var lazyObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var img = entry.target;
          img.src = img.src;
          lazyObserver.unobserve(img);
        }
      });
    }, { rootMargin: '200px' });
    lazyImages.forEach(function (img) { lazyObserver.observe(img); });
  }

  // ========================
  // ANIMATED COUNTERS
  // ========================
  function animateCounter(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    if (isNaN(target)) return;
    var duration = 1800;
    var start = 0;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      el.textContent = Math.floor(eased * target);
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target;
      }
    }
    requestAnimationFrame(step);
  }

  var counterEls = document.querySelectorAll('[data-count]');
  if (counterEls.length && 'IntersectionObserver' in window) {
    var counterObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    counterEls.forEach(function (el) { counterObserver.observe(el); });
  }

  // ========================
  // TOAST NOTIFICATION
  // ========================
  function showToast(message, duration) {
    duration = duration || 4000;
    var toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(function () {
      toast.classList.remove('show');
    }, duration);
  }

  // Expose globally for inline scripts
  window.CHIHIZA = window.CHIHIZA || {};
  window.CHIHIZA.toast = showToast;

  // ========================
  // LIGHTBOX (gallery images)
  // ========================
  var galleryImages = document.querySelectorAll('.project-gallery img, .catalog-image img');

  if (galleryImages.length) {
    // Create lightbox overlay
    var overlay = document.createElement('div');
    overlay.className = 'lightbox';
    overlay.innerHTML = '<button class="lightbox-close" aria-label="Close">&times;</button><img src="" alt="">';
    document.body.appendChild(overlay);

    var lbImg = overlay.querySelector('img');
    var lbClose = overlay.querySelector('.lightbox-close');

    function openLightbox(src, alt) {
      lbImg.src = src;
      lbImg.alt = alt || '';
      overlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
      overlay.classList.remove('active');
      document.body.style.overflow = '';
    }

    galleryImages.forEach(function (img) {
      img.style.cursor = 'pointer';
      img.addEventListener('click', function () {
        openLightbox(this.src, this.alt);
      });
    });

    lbClose.addEventListener('click', closeLightbox);
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeLightbox();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('active')) closeLightbox();
    });
  }

  // FAQ accordion
  var faqItems = document.querySelectorAll('.faq-item');
  if (faqItems.length) {
    faqItems.forEach(function (item) {
      var question = item.querySelector('.faq-question');
      question.addEventListener('click', function () {
        var isActive = item.classList.contains('active');
        faqItems.forEach(function (el) { el.classList.remove('active'); });
        if (!isActive) item.classList.add('active');
      });
    });
  }

})();
