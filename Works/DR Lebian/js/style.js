let chartInstance = null;

function calculateLoan() {
  const amount = parseFloat(document.getElementById("loanAmount").value);
  const interest = parseFloat(document.getElementById("interestRate").value) / 100 / 12;
  const years = parseFloat(document.getElementById("loanTerm").value);
  const months = years * 12;

  if (!amount || !interest || !years) {
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
  const ctx = document.getElementById('loanChart').getContext('2d');

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Principal', 'Intérêts'],
      datasets: [{
        data: [principal, interest],
        backgroundColor: ['#0099ff', '#ff6666']
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom'
        },
        title: {
          display: true,
          text: 'Répartition du remboursement'
        }
      }
    }
  });
}

function resetCalculator() {
  document.getElementById("loanAmount").value = "";
  document.getElementById("interestRate").value = "";
  document.getElementById("loanTerm").value = "";

  document.getElementById("monthlyPayment").textContent = "0.00";
  document.getElementById("totalPayment").textContent = "0.00";
  document.getElementById("totalInterest").textContent = "0.00";

  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }
}
