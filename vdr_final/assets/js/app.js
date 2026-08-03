(function () {
  var gate = document.getElementById('gate');
  var app = document.getElementById('app');
  var form = document.getElementById('gateForm');
  var input = document.getElementById('gateInput');
  var error = document.getElementById('gateError');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (input.value === '8888') {
      gate.classList.add('unlocked');
      app.style.display = 'block';
      input.value = '';
      error.style.display = 'none';
    } else {
      error.textContent = 'Incorrect access code.';
      error.style.display = 'block';
      input.value = '';
      input.focus();
    }
  });

  var mobileMenu = document.getElementById('mobileMenu');
  var nav = document.getElementById('mainNav');

  mobileMenu.addEventListener('click', function () {
    nav.classList.toggle('open');
  });

  document.querySelectorAll('.nav-link').forEach(function (link) {
    link.addEventListener('click', function () {
      nav.classList.remove('open');
    });
  });

  var langBtns = document.querySelectorAll('.lang-btn');
  var currentLang = 'en';

  function applyTranslations(lang) {
    if (typeof TRANSLATIONS === 'undefined') return;
    document.querySelectorAll('[data-lang-key]').forEach(function (el) {
      var key = el.getAttribute('data-lang-key');
      if (TRANSLATIONS[key] && TRANSLATIONS[key][lang]) {
        el.textContent = TRANSLATIONS[key][lang];
      }
    });
    document.documentElement.lang = lang === 'es' ? 'es' : 'en';
  }

  langBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var lang = btn.getAttribute('data-lang');
      if (lang === currentLang) return;
      currentLang = lang;

      langBtns.forEach(function (b) {
        b.classList.toggle('active', b.getAttribute('data-lang') === lang);
      });

      applyTranslations(lang);
    });
  });

  if (typeof Chart !== 'undefined') {
    var chartDefaults = {
      color: '#6b7280',
      borderColor: '#e5e7eb',
      font: { family: 'Inter' }
    };
    Chart.defaults.color = chartDefaults.color;
    Chart.defaults.borderColor = chartDefaults.borderColor;
    Chart.defaults.font.family = chartDefaults.font.family;

    var chartOpts = {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          ticks: {
            callback: function (v) {
              return 'USD ' + (v / 1000).toFixed(0) + 'k';
            }
          },
          grid: { color: '#f3f4f6' }
        },
        x: {
          grid: { display: false }
        }
      },
      elements: {
        point: { radius: 3 },
        line: { tension: 0.3, borderWidth: 2 }
      }
    };

    new Chart(document.getElementById('chartRevenue'), {
      type: 'line',
      data: {
        labels: TRANSLATIONS.chart_years || ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'],
        datasets: [{
          data: TRANSLATIONS.chart_revenue_data || [180000, 245000, 290000, 320000, 340000],
          borderColor: '#1a1a1a',
          backgroundColor: 'rgba(26,26,26,0.04)',
          fill: true
        }]
      },
      options: chartOpts
    });

    new Chart(document.getElementById('chartEBITDA'), {
      type: 'line',
      data: {
        labels: TRANSLATIONS.chart_years || ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'],
        datasets: [{
          data: TRANSLATIONS.chart_ebitda_data || [-45000, 62000, 116000, 148000, 170000],
          borderColor: '#059669',
          backgroundColor: 'rgba(5,150,105,0.04)',
          fill: true
        }]
      },
      options: chartOpts
    });

    new Chart(document.getElementById('chartCashFlow'), {
      type: 'line',
      data: {
        labels: TRANSLATIONS.chart_years || ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'],
        datasets: [{
          data: TRANSLATIONS.chart_cash_data || [-120000, -28000, 42000, 78000, 95000],
          borderColor: '#2563eb',
          backgroundColor: 'rgba(37,99,235,0.04)',
          fill: true
        }]
      },
      options: chartOpts
    });

    new Chart(document.getElementById('chartDividends'), {
      type: 'bar',
      data: {
        labels: TRANSLATIONS.chart_years || ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'],
        datasets: [{
          data: TRANSLATIONS.chart_div_data || [0, 0, 32000, 48000, 58000],
          backgroundColor: '#d97706',
          borderRadius: 4
        }]
      },
      options: chartOpts
    });
  }
})();