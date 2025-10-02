// === script.js ===

// ====== MENU BURGER (responsive) ======
const menuToggle = document.querySelector(".menu-toggle");
const navbar = document.querySelector(".navbar");

menuToggle.addEventListener("click", () => {
  navbar.classList.toggle("active");
  menuToggle.classList.toggle("active");
});

// ====== MODE SOMBRE / CLAIR ======
const themeToggle = document.getElementById("theme-toggle");
const body = document.body;

// Vérifier le thème sauvegardé dans le navigateur
if (localStorage.getItem("theme") === "dark") {
  body.classList.add("dark-mode");
  themeToggle.textContent = "☀️";
}

themeToggle.addEventListener("click", () => {
  body.classList.toggle("dark-mode");

  if (body.classList.contains("dark-mode")) {
    themeToggle.textContent = "☀️";
    localStorage.setItem("theme", "dark");
  } else {
    themeToggle.textContent = "🌙";
    localStorage.setItem("theme", "light");
  }
});

// ====== GALERIE : agrandir une image au clic ======
const images = document.querySelectorAll("#galerie img");

images.forEach(img => {
  img.addEventListener("click", () => {
    // Créer une boîte modale
    const modal = document.createElement("div");
    modal.classList.add("modal");

    const modalImg = document.createElement("img");
    modalImg.src = img.src;
    modalImg.alt = img.alt;

    // Fermer au clic
    modal.addEventListener("click", () => {
      modal.remove();
    });

    modal.appendChild(modalImg);
    document.body.appendChild(modal);
  });
});
// Sélectionne le bouton et le menu
const toggle = document.querySelector('.menu-toggle');
const menu = document.querySelector('nav ul');

// Quand on clique sur le bouton ☰
toggle.addEventListener('click', () => {
  menu.classList.toggle('active'); // active/désactive l'affichage du menu
});
