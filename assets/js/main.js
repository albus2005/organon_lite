// =============================
// NAVBAR — scroll effect
// =============================
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    navbar.style.boxShadow = '0 2px 12px rgba(0,0,0,0.08)';
  } else {
    navbar.style.boxShadow = 'none';
  }
});

// =============================
// SMOOTH REVEAL — sections
// =============================
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.section, .projet-card, .tarif-card, .valeur-card')
  .forEach(el => {
    el.classList.add('hidden');
    observer.observe(el);
  });

// =============================
// NAVBAR — menu mobile
// =============================
const navLinks = document.querySelector('.nav-links');

const burger = document.createElement('div');
burger.classList.add('burger');
burger.innerHTML = '&#9776;';
navbar.appendChild(burger);

burger.addEventListener('click', () => {
  navLinks.classList.toggle('nav-open');
});