/**
 * UI Module - Yakınımdaki Deprem
 * Handles user interface updates and interactions
 */

class UIModule {
  constructor(app) {
    this.app = app;
    this.debounceTimeout = null;
  }

  /**
   * Update earthquake list
   */
  updateEarthquakeList() {
    const container = document.getElementById('earthquake-items');
    const filterValue = document.getElementById('magnitude-filter')?.value || 'all';

    if (!container) return;

    const filteredData = this.app.modules.data.getFilteredData(filterValue);
    this.renderEarthquakeList(container, filteredData);
  }

  /**
   * Render earthquake list
   */
  renderEarthquakeList(container, earthquakes) {
    if (earthquakes.length === 0) {
      container.innerHTML = '<div class="loading">Belirtilen kritere uygun deprem bulunamadı.</div>';
      return;
    }

    container.innerHTML = earthquakes
      .map(eq => this.createEarthquakeItem(eq))
      .join('');

    this.attachEarthquakeItemEvents(container);
  }

  /**
   * Create earthquake list item HTML
   */
  createEarthquakeItem(earthquake) {
    return `
      <div class="earthquake-item" data-id="${earthquake.id}">
        <div class="earthquake-item__magnitude" style="background-color: ${this.getMagnitudeColor(earthquake.magnitude)}">
          ${earthquake.magnitude.toFixed(1)}
        </div>
        <div class="earthquake-item__details">
          <h3 class="earthquake-item__location">${earthquake.location}</h3>
          <p class="earthquake-item__time">${earthquake.time_ago || earthquake.time.toLocaleString('tr-TR')}</p>
          <p class="earthquake-item__depth">Derinlik: ${earthquake.depth.toFixed(1)} km</p>
        </div>
      </div>
    `;
  }

  /**
   * Attach event listeners to earthquake items
   */
  attachEarthquakeItemEvents(container) {
    container.querySelectorAll('.earthquake-item').forEach(item => {
      item.addEventListener('click', () => {
        const eqId = item.getAttribute('data-id');
        const earthquake = this.app.modules.data.getEarthquakeById(eqId);
        
        if (earthquake) {
          this.app.modules.map.centerOnEarthquake(earthquake);
          this.app.emit('earthquake:selected', earthquake);
        }
      });
    });
  }

  /**
   * Get color based on magnitude
   */
  getMagnitudeColor(magnitude) {
    if (magnitude >= 8.0) return '#7b1fa2'; // Mor - 8.0+ (çok büyük)
    if (magnitude >= 7.0) return '#d32f2f'; // Koyu kırmızı/bordo - 7.0-7.9 (büyük)
    if (magnitude >= 6.0) return '#f44336'; // Kırmızı - 6.0-6.9 (kuvvetli)
    if (magnitude >= 5.0) return '#ff5722'; // Koyu turuncu - 5.0-5.9 (orta)
    if (magnitude >= 4.0) return '#ff9800'; // Turuncu - 4.0-4.9 (hafif)
    if (magnitude >= 3.0) return '#ffc107'; // Sarı - 3.0-3.9 (küçük)
    return '#4caf50'; // Yeşil - 0-2.9 (çok küçük/hissedilmez)
  }

  /**
   * Show loading state
   */
  showLoading(selector, message = 'Yükleniyor...') {
    const element = document.querySelector(selector);
    if (element) {
      element.innerHTML = `
        <div class="loading">
          <div class="loading__spinner"></div>
          ${message}
        </div>
      `;
    }
  }

  /**
   * Hide loading state
   */
  hideLoading(selector) {
    const element = document.querySelector(selector);
    if (element) {
      const loading = element.querySelector('.loading');
      if (loading) {
        loading.remove();
      }
    }
  }

  /**
   * Show error message
   */
  showError(message, selector = '#earthquake-items') {
    const element = document.querySelector(selector);
    if (element) {
      element.innerHTML = `
        <div class="alert alert--error">
          <i class="fas fa-exclamation-triangle"></i>
          ${message}
        </div>
      `;
    }
  }

  /**
   * Show success message
   */
  showSuccess(message, selector = '#earthquake-items') {
    const element = document.querySelector(selector);
    if (element) {
      element.innerHTML = `
        <div class="alert alert--success">
          <i class="fas fa-check-circle"></i>
          ${message}
        </div>
      `;
    }
  }

  /**
   * Update filter options
   */
  updateFilterOptions() {
    const filter = document.getElementById('magnitude-filter');
    if (!filter) return;

    const magnitudes = this.app.state.earthquakeData.map(eq => eq.magnitude);
    const uniqueMagnitudes = [...new Set(magnitudes)].sort((a, b) => b - a);
    
    // Update existing options or add new ones
    const existingOptions = Array.from(filter.options).map(opt => opt.value);
    
    uniqueMagnitudes.forEach(mag => {
      const value = Math.floor(mag).toString();
      if (!existingOptions.includes(value)) {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = `${value}.0+`;
        filter.appendChild(option);
      }
    });
  }

  /**
   * Animate element
   */
  animateElement(element, animation, duration = 300) {
    if (!element) return;

    element.style.animation = `${animation} ${duration}ms ease-in-out`;
    
    setTimeout(() => {
      element.style.animation = '';
    }, duration);
  }

  /**
   * Scroll to element
   */
  scrollToElement(selector, offset = 0) {
    const element = document.querySelector(selector);
    if (element) {
      const elementPosition = element.offsetTop - offset;
      window.scrollTo({
        top: elementPosition,
        behavior: 'smooth'
      });
    }
  }

  /**
   * Toggle element visibility
   */
  toggleElement(selector, show = null) {
    const element = document.querySelector(selector);
    if (!element) return;

    if (show === null) {
      element.style.display = element.style.display === 'none' ? '' : 'none';
    } else {
      element.style.display = show ? '' : 'none';
    }
  }

  /**
   * Update element text content
   */
  updateText(selector, text) {
    const element = document.querySelector(selector);
    if (element) {
      element.textContent = text;
    }
  }

  /**
   * Update element HTML content
   */
  updateHTML(selector, html) {
    const element = document.querySelector(selector);
    if (element) {
      element.innerHTML = html;
    }
  }

  /**
   * Add CSS class to element
   */
  addClass(selector, className) {
    const element = document.querySelector(selector);
    if (element) {
      element.classList.add(className);
    }
  }

  /**
   * Remove CSS class from element
   */
  removeClass(selector, className) {
    const element = document.querySelector(selector);
    if (element) {
      element.classList.remove(className);
    }
  }

  /**
   * Toggle CSS class on element
   */
  toggleClass(selector, className) {
    const element = document.querySelector(selector);
    if (element) {
      element.classList.toggle(className);
    }
  }

  /**
   * Debounce function execution
   */
  debounce(func, wait) {
    return (...args) => {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => func.apply(this, args), wait);
    };
  }
}

// Export for module usage
window.UIModule = UIModule;
