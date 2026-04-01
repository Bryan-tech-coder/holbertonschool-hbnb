/* =========================
   HBnB Part 4 - Client JS
   Compatible con todas las páginas
   Puerto backend: 5002
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
   Check Auth & Toggle Login Link
======================= */
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (loginLink) loginLink.style.display = token ? 'none' : 'block';
  return token;
}

/* =======================
   Login Page
======================= */
function setupLogin() {
  const loginForm = document.getElementById('login-form');
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
        alert('Login failed: ' + (data.error || response.statusText));
      }
    } catch (err) {
      console.error(err);
      alert('Error connecting to server');
    }
  });
}

/* =======================
   Fetch & Display Places
======================= */
async function fetchPlaces() {
  const token = checkAuthentication();
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
    div.style.margin = '20px';
    div.style.padding = '10px';
    div.style.border = '1px solid #ddd';
    div.style.borderRadius = '10px';

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
    const cards = document.querySelectorAll('.place-card');
    cards.forEach(card => {
      const price = parseFloat(card.querySelector('p:nth-child(3)').textContent.replace('Price: $', ''));
      card.style.display = (value === 'All' || price <= parseFloat(value)) ? 'block' : 'none';
    });
  });
}

/* =======================
   Fetch & Display Place Details
======================= */
async function fetchPlaceDetails() {
  const params = new URLSearchParams(window.location.search);
  const placeId = params.get('id');
  if (!placeId) return;

  const token = checkAuthentication();

  try {
    const response = await fetch(`http://127.0.0.1:5002/api/v1/places/${placeId}`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });
    if (!response.ok) throw new Error('Failed fetching place');
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
    div.style.margin = '20px';
    div.style.padding = '10px';
    div.style.border = '1px solid #ddd';
    div.style.borderRadius = '10px';
    div.innerHTML = `<p>${r.comment} - ${r.user}</p>`;
    reviewsSection.appendChild(div);
  });
  section.appendChild(reviewsSection);

  // Show Add Review Form if Authenticated
  const addReview = document.getElementById('add-review');
  if (addReview) addReview.style.display = getCookie('token') ? 'block' : 'none';
}

/* =======================
   Add Review
======================= */
function setupAddReview() {
  const reviewForm = document.getElementById('review-form');
  if (!reviewForm) return;

  reviewForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const token = checkAuthentication();
    if (!token) return window.location.href = 'index.html';

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
        fetchPlaceDetails(); // refresh reviews
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
  setupLogin();
  setupPriceFilter();
  setupAddReview();
  checkAuthentication();

  if (document.getElementById('places-list')) fetchPlaces();
  if (document.getElementById('place-details')) fetchPlaceDetails();
});
