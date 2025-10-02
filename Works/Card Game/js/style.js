document.addEventListener("DOMContentLoaded", () => {
  /* -----------------------  Sélection des éléments  ----------------------- */
  const allCards = Array.from(document.querySelectorAll(".card"));
  const cardsContainer = document.querySelector(".cards");

  /* -----------------------  Création des UI dynamiques  ------------------- */
  // > Sélecteur de difficulté
  const difficultySelect = document.createElement("select");
  ["facile", "moyen", "difficile"].forEach(level => {
    const opt = document.createElement("option");
    opt.value = level;
    opt.textContent = level.charAt(0).toUpperCase() + level.slice(1);
    difficultySelect.appendChild(opt);
  });
  difficultySelect.style.cssText =
    " color=black; font-size:16px;margin-bottom:10px;padding:4px;";
  cardsContainer.parentElement.insertBefore(difficultySelect, cardsContainer);

  // > Zone d’infos (messages gagnés/échoués)
  const infoDiv = document.createElement("div");
  infoDiv.style.cssText =
    " color=black ;font-size:18px;color:white;margin:10px 0;text-align:center;";
  cardsContainer.parentElement.insertBefore(infoDiv, cardsContainer);

  // > Bouton Rejouer
  const replayBtn = document.createElement("button");
  replayBtn.textContent = "Rejouer";
  replayBtn.style.cssText =
    "  background: green;padding:6px 18px;font-size:16px;margin-top:10px;cursor:pointer;";
  cardsContainer.parentElement.appendChild(replayBtn);


  
  

  // > Chrono en arrière‑plan
  const bgTimer = document.createElement("div");
  bgTimer.id = "bg-timer";
  bgTimer.textContent = " 0";
  document.body.appendChild(bgTimer);
  
  
  /* -----------------------  Variables de jeu  ----------------------------- */
  let difficulty = "moyen";
  let activeCards = [];
  let flippedCards = [];
  let matchedCount = 0;

  // Chrono
  let timeLimit = 0;     // secondes max selon le niveau
  let timeLeft = 0;      // temps restant
  let timerInterval;     // setInterval handle
  let gameEnded = false; // gagné ou non
  

  /* -----------------------  Événements UI  -------------------------------- */
  difficultySelect.addEventListener("change", () => {
    difficulty = difficultySelect.value;
    init();
  });

  replayBtn.addEventListener("click", () => {
    if (!gameEnded && matchedCount > 0) {
      clearInterval(timerInterval);
      infoDiv.textContent =
        `❌ Tu as échoué... Tu avais trouvé ${matchedCount} paires.`;
    }
    init();
  });

  /* -----------------------  Logique principale  --------------------------- */
  function shuffleCards() {
    activeCards.forEach(card => {
      card.style.order = Math.floor(Math.random() * activeCards.length);
    });

  }

  function flipCard(card) {
    card.classList.add("flipped");
    card.querySelector(".front-view").style.transform = "rotateY(180deg)";
    card.querySelector(".back-view").style.transform = "rotateY(0deg)";
  }

  function unflipCard(card) {
    card.classList.remove("flipped");
    card.querySelector(".front-view").style.transform = "rotateY(0deg)";
    card.querySelector(".back-view").style.transform = "rotateY(180deg)";
  }

  function onCardClick(e) {
    const card = e.currentTarget;
    if (
      flippedCards.length === 2 ||
      flippedCards.includes(card) ||
      card.classList.contains("matched")
    ) return;

    flipCard(card);
    flippedCards.push(card);
    if (flippedCards.length === 2) checkMatch();
  }

  function checkMatch() {
    const [c1, c2] = flippedCards;
    const same =
      c1.querySelector(".back-view img").src ===
      c2.querySelector(".back-view img").src;

    if (same) {
      c1.classList.add("matched");
      c2.classList.add("matched");
      matchedCount++;
      flippedCards = [];

      if (matchedCount === activeCards.length / 2) {
        winGame();
      }
    } else {
      setTimeout(() => {
        unflipCard(c1);
        unflipCard(c2);
        flippedCards = [];
      }, 900);
    }
  }

  function winGame() {
    clearInterval(timerInterval);
    gameEnded = true;
    infoDiv.textContent =
      `🎉 Tu as gagné ! ${matchedCount} paires en ${timeLimit - timeLeft}s.`;
  }

  function loseGame() {
    clearInterval(timerInterval);
    gameEnded = true;
    infoDiv.textContent =
      `⏰Temps écoulé ! Tu as échoué… ${matchedCount} paires trouvées.`;
    
  }

  /* -----------------------  Gestion du chronomètre  ----------------------- */
  function startTimer() {
    clearInterval(timerInterval);
    timeLeft = timeLimit;
    updateBgTimer(); // premier affichage
    timerInterval = setInterval(() => {
      timeLeft--;
      updateBgTimer();
      if (timeLeft <= 0) loseGame();
    }, 1000);
  }

  function updateBgTimer() {
    bgTimer.textContent = timeLeft; // gros chiffre en arrière‑plan
  }

  /* -----------------------  Initialisation complète  ---------------------- */
  function init() {
    /* Nombre de paires + limite de temps selon la difficulté */
    let numPairs;
    if (difficulty === "facile") {
      numPairs = 4;    // 10 cartes
      timeLimit = 20;  // 40 s
    } else if (difficulty === "moyen") {
      numPairs = 6;    // 14 cartes
      timeLimit = 25;  // 1 min
    } else { // difficile
      numPairs = 8;    // 16 cartes
      timeLimit = 30;  // 1 min 30
    }

    /* Prépare les cartes */
    allCards.forEach(card => {
      card.style.display = "none";
      card.removeEventListener("click", onCardClick);
    });

    activeCards = allCards.slice(0, numPairs * 2);
    activeCards.forEach(card => {
      card.style.display = "block";
      card.addEventListener("click", onCardClick);
      unflipCard(card);
      card.classList.remove("matched");
    });

    /* Réinit variables */
    shuffled = [];
    flippedCards = [];
    matchedCount = 0;
    gameEnded = false;
    infoDiv.textContent = ""; // message effacé
    shuffleCards();
    startTimer();
  }

  /* Lancement initial */
  init();
});
