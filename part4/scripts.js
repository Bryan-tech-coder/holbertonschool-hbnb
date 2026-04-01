/* =========================
   HBnB - Client JS
========================= */

/* =======================
   Utilities: Cookies
======================= */
function setCookie(name, value, days = 1) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

function getCookie(name) {
  return document.cookie.split('; ').reduce((r, v) => {
    const parts = v.split('=');
    return parts[0] === name ? decodeURIComponent(parts[1]) : r;
  }, '');
}

function deleteCookie(name) {
  setCookie(name, '', -1);
}

/* =======================
   Navbar y Footer
======================= */
function setupNavbarFooter() {
  const header = document.querySelector('header');
  if (header) {
    const token = getCookie('token');
    header.innerHTML = `
      <img src="images/logo.png" alt="HBnB Logo" class="logo">
      <nav>
        <a href="index.html">Home</a>
        <a href="login.html" id="login-link">Login</a>
        ${token ? '<a href="#" id="logout-link">Logout</a>' : ''}
      </nav>
    `;

    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
      logoutLink.addEventListener('click', () => {
        deleteCookie('token');
        window.location.href = 'login.html';
      });
    }

    // Ocultar login si ya está autenticado
    const loginLink = document.getElementById('login-link');
    if (loginLink) loginLink.style.display = token ? 'none' : 'block';
  }

  const footer = document.querySelector('footer');
  if (footer) {
    footer.innerHTML = `<p>&copy; ${new Date().getFullYear()} HBnB. All rights reserved.</p>`;
  }
}

/* =======================
   Login Page
======================= */
function setupLogin() {
  const loginForm = document.getElementById('login-form');
  const loginMessage = document.getElementById('login-message');
  if (!loginForm) return;

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
      const response = await fetch('http://127.0.0.1:5002/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        setCookie('token', data.access_token);
        window.location.href = 'index.html';
      } else {
        const data = await response.json();
        loginMessage.textContent = 'Login failed: ' + (data.error || response.statusText);
      }
    } catch (err) {
      console.error(err);
      loginMessage.textContent = 'Error connecting to server';
    }
  });
}

/* =======================
   Index Page - Fetch & Display Places
======================= */
async function fetchPlaces() {
  const token = getCookie('token');
  try {
    const response = await fetch('http://127.0.0.1:5002/api/v1/places', {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });
    if (!response.ok) throw new Error('Failed fetching places');
    const data = await response.json();
    displayPlaces(data);
  } catch (err) {
    console.error(err);
  }
}

function displayPlaces(places) {
  const list = document.getElementById('places-list');
  if (!list) return;
  list.innerHTML = '';

  places.forEach(place => {
    const div = document.createElement('div');
    div.className = 'place-card';
    div.innerHTML = `
      <h3>${place.name}</h3>
      <p>${place.description}</p>
      <p>Price: $${place.price}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;
    list.appendChild(div);
  });
}

/* =======================
   Filter Places by Price
======================= */
function setupPriceFilter() {
  const filter = document.getElementById('price-filter');
  if (!filter) return;

  filter.addEventListener('change', (e) => {
    const value = e.target.value;
    document.querySelectorAll('.place-card').forEach(card => {
      const price = parseFloat(card.querySelector('p:nth-child(3)').textContent.replace('Price: $', ''));
      card.style.display = (value === 'All' || price <= parseFloat(value)) ? 'block' : 'none';
    });
  });
}

/* =======================
   Place Details Page
======================= */
async function fetchPlaceDetails() {
  const params = new URLSearchParams(window.location.search);
  const placeId = params.get('id');
  if (!placeId) return;

  const token = getCookie('token');
  try {
    const response = await fetch(`http://127.0.0.1:5002/api/v1/places/${placeId}`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });
    if (!response.ok) throw new Error('Failed fetching place details');
    const place = await response.json();
    displayPlaceDetails(place);
  } catch (err) {
    console.error(err);
  }
}

function displayPlaceDetails(place) {
  const section = document.getElementById('place-details');
  if (!section) return;

  section.innerHTML = `
    <h2>${place.name}</h2>
    <p>${place.description}</p>
    <p>Price: $${place.price}</p>
    <p>Amenities: ${place.amenities.join(', ')}</p>
  `;

  const reviewsSection = document.createElement('div');
  reviewsSection.id = 'reviews';
  place.reviews.forEach(r => {
    const div = document.createElement('div');
    div.className = 'review-card';
    div.innerHTML = `<p>${r.comment} - ${r.user}</p>`;
    reviewsSection.appendChild(div);
  });
  section.appendChild(reviewsSection);

  const addReviewSection = document.getElementById('add-review');
  if (addReviewSection) addReviewSection.style.display = getCookie('token') ? 'block' : 'none';
}

/* =======================
   Add Review
======================= */
function setupAddReview() {
  const reviewForm = document.getElementById('review-form');
  if (!reviewForm) return;

  reviewForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const token = getCookie('token');
    if (!token) return window.location.href = 'login.html';

    const params = new URLSearchParams(window.location.search);
    const placeId = params.get('id');
    const reviewText = document.getElementById('review-text').value;

    try {
      const response = await fetch(`http://127.0.0.1:5002/api/v1/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ comment: reviewText })
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
  });
}

/* =======================
   Initialize Page
======================= */
document.addEventListener('DOMContentLoaded', () => {
  setupNavbarFooter();
  setupLogin();
  setupPriceFilter();
  setupAddReview();

  if (document.getElementById('places-list')) fetchPlaces();
  if (document.getElementById('place-details')) fetchPlaceDetails();
});
