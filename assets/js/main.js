// =============================
// ORGANON DATA SOLUTIONS - MAIN.JS
// Version corrigée - Popups fonctionnels + menu mobile + accordéon
// =============================

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
// NAVBAR — menu mobile (CORRIGÉ)
// Plus de doublon : on utilise le burger existant dans le HTML
// =============================
const burger = document.querySelector('.burger');
const navLinks = document.querySelector('.nav-links');

if (burger && navLinks) {
  burger.addEventListener('click', () => {
    navLinks.classList.toggle('nav-open');
  });
}

// Fermer le menu après clic sur un lien (meilleure UX)
const navLinksItems = document.querySelectorAll('.nav-links a');
navLinksItems.forEach(link => {
  link.addEventListener('click', () => {
    if (navLinks.classList.contains('nav-open')) {
      navLinks.classList.remove('nav-open');
    }
  });
});

// =============================
// PROCESS SECTION — accordéon discret
// =============================
const processToggle = document.getElementById('processToggle');
const processContent = document.getElementById('processContent');

if (processToggle && processContent) {
  processToggle.addEventListener('click', () => {
    const isHidden = processContent.classList.contains('hidden-process');
    if (isHidden) {
      processContent.classList.remove('hidden-process');
      processToggle.classList.add('open');
    } else {
      processContent.classList.add('hidden-process');
      processToggle.classList.remove('open');
    }
  });
}

// =============================
// MODALS (POPUPS) pour les tarifs — VERSION CORRIGÉE
// Gère l'ouverture/fermeture de chaque popup
// =============================

// Récupérer tous les boutons "En savoir plus"
const detailsButtons = document.querySelectorAll('.btn-details');

// Récupérer tous les modals
const modals = document.querySelectorAll('.modal');

// Récupérer tous les boutons de fermeture (les "×")
const closeButtons = document.querySelectorAll('.modal-close');

// Fonction pour ouvrir un modal spécifique
function openModal(modal) {
  if (modal) {
    modal.style.display = 'flex';
    // Empêcher le scroll de la page quand le modal est ouvert
    document.body.style.overflow = 'hidden';
    // Petit log pour confirmer l'ouverture (debug)
    console.log('Modal ouvert:', modal.id);
  }
}

// Fonction pour fermer un modal
function closeModal(modal) {
  if (modal) {
    modal.style.display = 'none';
    // Réactiver le scroll
    document.body.style.overflow = '';
    console.log('Modal fermé:', modal.id);
  }
}

// Ajouter un événement de clic à chaque bouton "En savoir plus"
detailsButtons.forEach(button => {
  button.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    const modalId = button.getAttribute('data-modal');
    if (modalId) {
      const modal = document.getElementById(modalId);
      if (modal) {
        openModal(modal);
      } else {
        console.error('Modal non trouvé:', modalId);
      }
    }
  });
  
  // Ajout d'une indication discrète (tooltip)
  button.setAttribute('title', 'Cliquez pour voir le détail de l\'offre');
});

// Ajouter un événement de clic à chaque bouton de fermeture (×)
closeButtons.forEach(closeBtn => {
  closeBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    const modal = closeBtn.closest('.modal');
    if (modal) {
      closeModal(modal);
    }
  });
});

// Fermer le modal si on clique à l'extérieur du contenu (sur le fond gris)
modals.forEach(modal => {
  modal.addEventListener('click', (e) => {
    // Si on clique sur le fond gris (le modal lui-même) et pas sur son contenu
    if (e.target === modal) {
      closeModal(modal);
    }
  });
});

// =============================
// FERMER LE MODAL AVEC LA TOUCHE ÉCHAP (ESC)
// =============================
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    modals.forEach(modal => {
      if (modal.style.display === 'flex') {
        closeModal(modal);
      }
    });
  }
});

// =============================
// SMOOTH SCROLL POUR LES ANCRES
// Améliore la navigation
// =============================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const targetId = this.getAttribute('href');
    if (targetId === '#' || targetId === '') return;
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      e.preventDefault();
      targetElement.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
      // Mettre à jour l'URL sans recharger (optionnel mais propre)
      history.pushState(null, null, targetId);
    }
  });
});

// =============================
// VÉRIFICATION QUE LES MODALS SONT BIEN PRÉSENTS
// (debug - à supprimer en production si souhaité)
// =============================
console.log('✅ Organon Data Solutions — Site prêt');
console.log('👉 Nombre de boutons "En savoir plus":', detailsButtons.length);
console.log('👉 Nombre de modals:', modals.length);
console.log('👉 Burger menu:', burger ? 'trouvé' : 'non trouvé');
console.log('👉 Process section:', processToggle ? 'trouvée' : 'non trouvée');

// =============================
// PETIT BONUS : EMPÊCHER LE CLIC SUR LIEN VIDE DE RECHARGER-
// =============================
document.querySelectorAll('a[href="#"]').forEach(emptyLink => {
  emptyLink.addEventListener('click', (e) => {
    e.preventDefault();
  });
});