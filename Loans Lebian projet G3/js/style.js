 let chartInstance = null;

    function calculateLoan() {
      const amount = parseFloat(document.getElementById("loanAmount").value);
      const interest = parseFloat(document.getElementById("interestRate").value) / 100 / 12;
      const years = parseFloat(document.getElementById("loanTerm").value);
      const months = years * 12;

      if (isNaN(amount) || isNaN(interest) || isNaN(months) || months === 0) {
        alert("Veuillez remplir tous les champs avec des valeurs valides.");
        return;
      }

      const x = Math.pow(1 + interest, months);
      const monthly = (amount * x * interest) / (x - 1);
      const total = monthly * months;
      const totalInterest = total - amount;

      document.getElementById("monthlyPayment").textContent = monthly.toFixed(2);
      document.getElementById("totalPayment").textContent = total.toFixed(2);
      document.getElementById("totalInterest").textContent = totalInterest.toFixed(2);

      drawChart(amount, totalInterest);
    }

    function drawChart(principal, interest) {
      const ctx = document.getElementById("loanChart").getContext("2d");

      if (chartInstance) {
        chartInstance.destroy();
      }

      chartInstance = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: ["Capital", "Intérêts"],
          datasets: [{
            label: "Répartition du remboursement",
            data: [principal, interest],
            backgroundColor: ["#2ecc71", "#e74c3c"],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom'
            }
          }
        }
      });
    }

    function resetCalculator() {
      // Réinitialiser les champs
      document.getElementById("loanAmount").value = "";
      document.getElementById("interestRate").value = "";
      document.getElementById("loanTerm").value = "";

      // Réinitialiser les résultats
      document.getElementById("monthlyPayment").textContent = "0.00";
      document.getElementById("totalPayment").textContent = "0.00";
      document.getElementById("totalInterest").textContent = "0.00";

      // Supprimer le graphique
      if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
      }
    }