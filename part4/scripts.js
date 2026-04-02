/* =========================
  HBnB - Client JS
  All UI and comments in English for Holberton
  - Handles authentication (JWT token)
  - Fetches data from the API (places, details, reviews)
  - Renders the interface: list of places, details, and review form
  - Documented for demo and explanation
========================= */

/* =======================
   Utilities: Cookies
======================= */
// API base URL (adjust if your API runs on another address/port)
const API_BASE = 'http://127.0.0.1:5002';

/**
 * Resolves an image reference from the API.
 * - If absolute URL (http/https), returns as is.
 * - If relative path (e.g. /uploads/1.jpg), prepends API_BASE.
 * - If object with { url: '...' }, extracts the property.
 * - If missing, returns a default local image.
 */
function resolveImageUrl(img) {
  if (!img) return 'images/img_place.png';
  if (typeof img === 'string') {
    if (img.startsWith('http://') || img.startsWith('https://')) return img;
    if (img.startsWith('/')) return API_BASE + img;
    // If relative path without slash, assume relative to API
    return API_BASE + '/' + img;
  }
  if (typeof img === 'object' && img.url) return resolveImageUrl(img.url);
  return 'images/sample1.svg';
}

function setCookie(name, value, days = 1) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  // Add SameSite to improve cross-site behavior; do not set Secure to allow localhost HTTP
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
}

function getCookie(name) {
  return document.cookie.split('; ').reduce((r, v) => {
    const parts = v.split('=');
    const key = parts.shift();
    const val = parts.join('=');
    return key === name ? decodeURIComponent(val) : r;
  }, '');
}

function deleteCookie(name) {
  setCookie(name, '', -1);
}

// Variable to prevent redirect loops
let __redirectLock = false;

// Debug logger for development
function debugLog(...args) {
  try { console.debug('[HBnB]', ...args); } catch (e) {}
}

/**
 * Redirects to a URL, but prevents infinite loops.
 * Used for login/logout navigation.
 */
function guardedRedirect(url) {
  if (__redirectLock) {
    debugLog('Redirect blocked (lock active):', url);
    return;
  }
  __redirectLock = true;
  debugLog('Redirecting to:', url);
  setTimeout(() => { window.location.href = url; }, 100);
}

/* =======================
  UI Helpers: Loading & Buttons
  - Spinner and button loading state
======================= */
function createSpinnerEl() {
  const s = document.createElement('span');
  s.className = 'hbnb-spinner';
  s.setAttribute('role', 'status');
  s.setAttribute('aria-hidden', 'true');
  return s;
}

function setButtonLoading(btn, loading = true) {
  if (!btn) return;
  if (loading) {
    btn.dataset.orig = btn.innerHTML;
    btn.classList.add('btn-disabled');
    btn.setAttribute('aria-busy', 'true');
    btn.innerHTML = '';
    btn.appendChild(createSpinnerEl());
    const text = document.createElement('span');
    text.textContent = ' Loading';
    btn.appendChild(text);
  } else {
    btn.classList.remove('btn-disabled');
    btn.removeAttribute('aria-busy');
    if (btn.dataset.orig) btn.innerHTML = btn.dataset.orig;
  }
}

/* ======================
  Token storage helpers
  - Use localStorage for JWT, fallback to cookie for compatibility
====================== */
function setToken(token) {
  try {
    localStorage.setItem('hbnb_token', token);
  } catch (e) { /* ignore */ }
}

function getToken() {
  try {
    const t = localStorage.getItem('hbnb_token');
    return t || '';
  } catch (e) { return ''; }
}

function deleteToken() {
  try { localStorage.removeItem('hbnb_token'); } catch (e) {}
  try { deleteCookie('token'); } catch (e) {}
}

/* =======================
  Navbar and Footer
  - Renders navigation and copyright
======================= */
function setupNavbarFooter() {
  const header = document.querySelector('header');
  if (header) {
    const token = getToken();
    // Renderiza el header acorde al estado de autenticación
    header.innerHTML = `
      <nav class="navbar">
        <img src="images/logo.png" alt="HBnB Logo" class="logo">
        <div class="nav-links">
          <a href="index.html">Home</a>
          <a href="place.html">Place</a>
          <a href="add_review.html">Add Review</a>
          ${token ? '<a href="#" id="logout-link">Logout</a>' : '<a href="login.html" id="login-link" class="login-button">Login</a>'}
        </div>
      </nav>
    `;

    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
      logoutLink.addEventListener('click', () => {
        deleteToken();
        guardedRedirect('login.html');
      });
    }

    // Ocultar login si ya está autenticado
    const loginLink = document.getElementById('login-link');
    if (loginLink) loginLink.style.display = token ? 'none' : 'inline-block';
  }

  const footer = document.querySelector('footer');
  if (footer) {
    footer.innerHTML = `<p>&copy; ${new Date().getFullYear()} HBnB. All rights reserved.</p>`;
  }
}

/* =======================
  Login Page
  - Handles login form and authentication
======================= */
function setupLogin() {
  const loginForm = document.getElementById('login-form');
  const loginMessage = document.getElementById('login-message');
  debugLog('setupLogin initialized');
  if (!loginForm) return;
  // If already authenticated, go to index
  const existing = getToken();
  if (existing) {
    debugLog('Login page: token present, redirecting to index');
    guardedRedirect('index.html');
    return;
  }

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const submitBtn = loginForm.querySelector('button[type="submit"]');
    setButtonLoading(submitBtn, true);
    if (loginMessage) { loginMessage.setAttribute('aria-live', 'polite'); }

    try {
      const response = await fetch(`${API_BASE}/api/v1/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        // Guardar token JWT en localStorage (con fallback a cookie)
        setToken(data.access_token);
        // Redirigir al índice (lista de lugares)
        guardedRedirect('index.html');
      } else {
        const data = await response.json();
        loginMessage.textContent = 'Login failed: ' + (data.error || response.statusText);
      }
    } catch (err) {
      console.error(err);
      loginMessage.textContent = 'Error connecting to server';
    } finally {
      setButtonLoading(submitBtn, false);
    }
  });
}

/* =======================
  Index Page - Fetch & Display Places
  - Loads places after login
======================= */
async function fetchPlaces() {
  const token = getToken();
  debugLog('fetchPlaces token present:', !!token);
  if (!token) {
    // Redirect to login if not authenticated (index requires auth)
    debugLog('No token found, redirecting to login');
    guardedRedirect('login.html');
    return;
  }

  try {
    const list = document.getElementById('places-list');
    if (list) {
      list.setAttribute('aria-busy', 'true');
      const s = createSpinnerEl();
      s.style.margin = '12px';
      list.innerHTML = '';
      list.appendChild(s);
    }

    const response = await fetch(`${API_BASE}/api/v1/places`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed fetching places');
    const data = await response.json();
    debugLog('fetchPlaces received items:', Array.isArray(data) ? data.length : typeof data);
    // Render places in the UI
    displayPlaces(data);
    if (list) list.removeAttribute('aria-busy');
  } catch (error) {
    console.error(error);
    // Show error message in UI
    let errorDiv = document.getElementById('fetch-error');
    if (!errorDiv) {
      errorDiv = document.createElement('div');
      errorDiv.id = 'fetch-error';
      errorDiv.style.color = 'red';
      errorDiv.style.background = '#fff0f0';
      errorDiv.style.padding = '10px';
      errorDiv.style.margin = '10px 0';
      errorDiv.style.border = '1px solid #f99';
      errorDiv.style.fontWeight = 'bold';
      errorDiv.setAttribute('role', 'alert');
      const container = document.getElementById('places-list')?.parentNode || document.body;
      container.insertBefore(errorDiv, container.firstChild);
    }
    errorDiv.textContent = `Error fetching places: ${error.message}`;
  }
}

function displayPlaces(places) {
  const list = document.getElementById('places-list');
  if (!list) return;
  list.innerHTML = '';
  debugLog('displayPlaces count:', places ? places.length : 0);

  places.forEach(place => {
    const div = document.createElement('div');
    div.className = 'place-card';
    div.dataset.price = place.price;
    // determinar imagen usando resolveImageUrl
    const imgSrc = resolveImageUrl(place.image || (place.images && place.images[0]));

    div.innerHTML = `
      <img src="${imgSrc}" alt="${place.name}" class="place-thumb">
      <h3>${place.name}</h3>
      <p class="place-description">${place.description || ''}</p>
      <p class="place-price">Price: $<span class="price-value">${place.price}</span></p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;
    list.appendChild(div);
  });
}

/* =======================
  Filter Places by Price
  - Dropdown to filter places by price
======================= */
function setupPriceFilter() {
  const filter = document.getElementById('price-filter');
  if (!filter) return;

  filter.addEventListener('change', (e) => {
    const value = e.target.value;
    document.querySelectorAll('.place-card').forEach(card => {
      const price = parseFloat(card.dataset.price || card.querySelector('.price-value')?.textContent || '0');
      card.style.display = (value === 'All' || price <= parseFloat(value)) ? 'block' : 'none';
    });
  });
}

/* =======================
  Place Details Page
  - Shows details and reviews for a place
======================= */
async function fetchPlaceDetails() {
  const params = new URLSearchParams(window.location.search);
  const placeId = params.get('id');
  if (!placeId) return;

  const token = getToken();
  debugLog('fetchPlaceDetails id:', placeId, 'hasToken:', !!token);
  try {
    const section = document.getElementById('place-details');
    if (section) {
      section.setAttribute('aria-busy', 'true');
      section.innerHTML = '';
      const spinner = createSpinnerEl();
      spinner.style.display = 'block';
      spinner.style.margin = '18px auto';
      section.appendChild(spinner);
    }

    const response = await fetch(`${API_BASE}/api/v1/places/${placeId}`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });
    if (!response.ok) throw new Error('Failed fetching place details');
    const place = await response.json();
    displayPlaceDetails(place);
    if (section) section.removeAttribute('aria-busy');
  } catch (err) {
    console.error(err);
  }
}

function displayPlaceDetails(place) {
  const section = document.getElementById('place-details');
  if (!section) return;
  debugLog('displayPlaceDetails for:', place && (place.id || place.name));

  // host info
  const host = place.host || place.host_name || place.user || place.owner || '';

  // image: resolver posibles rutas proporcionadas por el API
  const imgSrc = resolveImageUrl(place.image || (place.images && place.images[0]));

  section.innerHTML = `
    <img src="${imgSrc}" alt="${place.name}" class="place-thumb">
    <h2>${place.name}</h2>
    <p>${place.description || ''}</p>
    <p>Host: ${host}</p>
    <p>Price: $${place.price}</p>
    <p class="place-info">Amenities: ${Array.isArray(place.amenities) ? place.amenities.map(a => (typeof a === 'string' ? a : a.name || '')).filter(Boolean).join(', ') : ''}</p>
  `;

  const reviewsSection = document.createElement('div');
  reviewsSection.id = 'reviews';
  place.reviews.forEach(r => {
    const div = document.createElement('div');
    div.className = 'review-card';
    const user = r.user || r.user_name || r.username || '';
    const rating = r.rating ? ` <strong>(${r.rating}/5)</strong>` : '';
    div.innerHTML = `<p class="review-text">${r.comment || r.text}${rating}</p><p class="review-user">— ${user}</p>`;
    reviewsSection.appendChild(div);
  });
  section.appendChild(reviewsSection);

  const addReviewSection = document.getElementById('add-review');
  if (addReviewSection) addReviewSection.style.display = getToken() ? 'block' : 'none';
}

/* =======================
  Add Review
  - Handles review form submission
======================= */
function setupAddReview() {
  const reviewForm = document.getElementById('review-form');
  // Redirect unauthenticated users immediately to index (per assignment)
  const token = getToken();
  if (!token) {
    debugLog('Add-review: no token, redirecting to index');
    guardedRedirect('index.html');
    return;
  }
  if (!reviewForm) return;

  reviewForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // token already checked on load

    const params = new URLSearchParams(window.location.search);
    const placeId = params.get('id');
    const reviewText = document.getElementById('review-text').value;
    const submitBtn = reviewForm.querySelector('button[type="submit"]');
    setButtonLoading(submitBtn, true);

    try {
      const response = await fetch(`${API_BASE}/api/v1/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ text: reviewText, place_id: parseInt(placeId, 10) })
      });

      if (response.ok) {
        alert('Review submitted successfully!');
        reviewForm.reset();
        fetchPlaceDetails();
      } else {
        const data = await response.json();
        alert('Failed: ' + (data.error || response.statusText));
      }
    } catch (err) {
      console.error(err);
      alert('Error submitting review');
    }
      setButtonLoading(submitBtn, false);
  });
}

/* =======================
  Initialize Page
  - Detects which page is loaded and runs the right setup
======================= */
document.addEventListener('DOMContentLoaded', () => {
  // Trace at load start for debugging redirect loop
  try {
    const token = getToken();
    debugLog('DOM ready. token present:', !!token, 'token_len:', token ? token.length : 0);
    // also store a persistent trace to inspect after redirects
    const traces = JSON.parse(localStorage.getItem('hbnb_traces') || '[]');
    traces.push({ ts: Date.now(), href: window.location.href, token_len: token ? token.length : 0 });
    localStorage.setItem('hbnb_traces', JSON.stringify(traces.slice(-50)));
  } catch (e) { console.error(e); }
  setupNavbarFooter();
  // Solo ejecutar setupLogin si estamos en login.html
  if (document.getElementById('login-form')) {
    setupLogin();
    return;
  }
  // Solo ejecutar fetchPlaces y filtro en index.html
  if (document.getElementById('places-list')) {
    setupPriceFilter();
    fetchPlaces();
    return;
  }
  // Solo ejecutar detalles y review en place.html
  if (document.getElementById('place-details')) {
    const placeTitle = document.getElementById('place-title');
    if (placeTitle) {
      const params = new URLSearchParams(window.location.search);
      const name = params.get('name');
      if (name) {
        placeTitle.textContent = name;
        const addReviewLink = document.getElementById('add-review-link');
        if (addReviewLink) {
          addReviewLink.href = `add_review.html?name=${encodeURIComponent(name)}`;
        }
      }
    }
    fetchPlaceDetails();
    setupAddReview();
    return;
  }
  if (document.getElementById('review-title')) {
    const params = new URLSearchParams(window.location.search);
    const name = params.get('name');
    const reviewTitle = document.getElementById('review-title');
    const placeSelect = document.getElementById('place-select');
    if (name && reviewTitle) reviewTitle.textContent = `Reviewing: ${name}`;
    if (name && placeSelect) placeSelect.value = name;
    if (placeSelect && reviewTitle) {
      placeSelect.addEventListener('change', () => {
        reviewTitle.textContent = `Reviewing: ${placeSelect.value}`;
      });
    }
    return;
  }
});
