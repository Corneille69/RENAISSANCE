// Gestionnaire du calculateur de prêts
class LoanCalculator {
    constructor() {
        this.currentLoan = null;
        this.chart = null;
        this.init();
    }

    init() {
        this.setupFormElements();
        this.setupEventListeners();
        this.calculateLoan(); // Calcul initial
        this.checkAuthForSave();
    }

    // Configuration des éléments du formulaire
    setupFormElements() {
        this.elements = {
            // Inputs
            loanAmount: document.getElementById('loanAmount'),
            loanRate: document.getElementById('loanRate'),
            loanDuration: document.getElementById('loanDuration'),
            loanType: document.getElementById('loanType'),
            loanName: document.getElementById('loanName'),
            
            // Sliders
            amountSlider: document.getElementById('amountSlider'),
            rateSlider: document.getElementById('rateSlider'),
            durationSlider: document.getElementById('durationSlider'),
            
            // Résultats
            monthlyPayment: document.getElementById('monthlyPayment'),
            totalCost: document.getElementById('totalCost'),
            totalInterest: document.getElementById('totalInterest'),
            
            // Boutons
            saveBtn: document.getElementById('saveBtn'),
            exportBtn: document.getElementById('exportBtn'),
            
            // Tableau
            amortizationBody: document.getElementById('amortizationBody'),
            
            // Graphique
            loanChart: document.getElementById('loanChart')
        };
    }

    // Configuration des écouteurs d'événements
    setupEventListeners() {
        // Synchronisation inputs/sliders
        this.elements.loanAmount.addEventListener('input', (e) => {
            this.elements.amountSlider.value = e.target.value;
            this.debouncedCalculate();
        });

        this.elements.amountSlider.addEventListener('input', (e) => {
            this.elements.loanAmount.value = e.target.value;
            this.debouncedCalculate();
        });

        this.elements.loanRate.addEventListener('input', (e) => {
            this.elements.rateSlider.value = e.target.value;
            this.debouncedCalculate();
        });

        this.elements.rateSlider.addEventListener('input', (e) => {
            this.elements.loanRate.value = e.target.value;
            this.debouncedCalculate();
        });

        this.elements.loanDuration.addEventListener('input', (e) => {
            this.elements.durationSlider.value = e.target.value;
            this.debouncedCalculate();
        });

        this.elements.durationSlider.addEventListener('input', (e) => {
            this.elements.loanDuration.value = e.target.value;
            this.debouncedCalculate();
        });

        // Autres changements
        this.elements.loanType.addEventListener('change', () => this.debouncedCalculate());

        // Boutons
        if (this.elements.saveBtn) {
            this.elements.saveBtn.addEventListener('click', () => this.saveLoan());
        }

        if (this.elements.exportBtn) {
            this.elements.exportBtn.addEventListener('click', () => this.exportToCSV());
        }

        // Debounce pour éviter trop de calculs
        this.debouncedCalculate = ZenLoan.debounce(() => this.calculateLoan(), 300);
    }

    // Vérifier l'authentification pour la sauvegarde
    checkAuthForSave() {
        const currentUser = window.zenLoan?.getCurrentUser();
        if (currentUser && this.elements.saveBtn) {
            this.elements.saveBtn.style.display = 'block';
        }
    }

    // Calcul principal du prêt
    calculateLoan() {
        try {
            const amount = parseFloat(this.elements.loanAmount.value) || 0;
            const rate = parseFloat(this.elements.loanRate.value) || 0;
            const duration = parseInt(this.elements.loanDuration.value) || 0;

            if (amount <= 0 || rate < 0 || duration <= 0) {
                this.clearResults();
                return;
            }

            // Calcul de la mensualité
            const monthlyPayment = this.calculateMonthlyPayment(amount, rate, duration * 12);
            const totalCost = monthlyPayment * duration * 12;
            const totalInterest = totalCost - amount;

            // Génération du tableau d'amortissement
            const amortizationTable = this.generateAmortizationTable(amount, rate, duration * 12);

            // Stockage des données actuelles
            this.currentLoan = {
                amount,
                rate,
                duration,
                type: this.elements.loanType.value,
                name: this.elements.loanName.value || `Prêt ${this.elements.loanType.options[this.elements.loanType.selectedIndex].text}`,
                monthlyPayment,
                totalCost,
                totalInterest,
                amortizationTable
            };

            // Mise à jour de l'affichage
            this.updateResults(monthlyPayment, totalCost, totalInterest);
            this.updateAmortizationTable(amortizationTable);
            this.updateChart(amount, totalInterest);

        } catch (error) {
            console.error('Erreur lors du calcul:', error);
            ZenLoan.showNotification('Erreur lors du calcul du prêt', 'error');
            this.clearResults();
        }
    }

    // Calcul de la mensualité
    calculateMonthlyPayment(principal, annualRate, totalMonths) {
        if (annualRate === 0) {
            return principal / totalMonths;
        }

        const monthlyRate = annualRate / 100 / 12;
        const numerator = monthlyRate * Math.pow(1 + monthlyRate, totalMonths);
        const denominator = Math.pow(1 + monthlyRate, totalMonths) - 1;
        
        return principal * (numerator / denominator);
    }

    // Génération du tableau d'amortissement
    generateAmortizationTable(principal, annualRate, totalMonths) {
        const monthlyPayment = this.calculateMonthlyPayment(principal, annualRate, totalMonths);
        const monthlyRate = annualRate / 100 / 12;
        const table = [];
        let balance = principal;

        for (let month = 1; month <= totalMonths; month++) {
            const interestPayment = balance * monthlyRate;
            const principalPayment = monthlyPayment - interestPayment;
            balance = Math.max(balance - principalPayment, 0);

            table.push({
                month,
                payment: monthlyPayment,
                principalPayment,
                interestPayment,
                balance
            });
        }

        return table;
    }

    // Mise à jour des résultats
    updateResults(monthlyPayment, totalCost, totalInterest) {
        this.elements.monthlyPayment.textContent = ZenLoan.formatCurrency(monthlyPayment);
        this.elements.totalCost.textContent = ZenLoan.formatCurrency(totalCost);
        this.elements.totalInterest.textContent = ZenLoan.formatCurrency(totalInterest);
    }

    // Mise à jour du tableau d'amortissement (version résumée)
    updateAmortizationTable(table) {
        const tbody = this.elements.amortizationBody;
        tbody.innerHTML = '';

        // Afficher seulement les 12 premiers mois et quelques points clés
        const displayRows = [];
        
        // 12 premiers mois
        for (let i = 0; i < Math.min(12, table.length); i++) {
            displayRows.push(table[i]);
        }

        // Ajouter des points clés (années complètes)
        for (let year = 2; year <= Math.floor(table.length / 12); year++) {
            const index = (year * 12) - 1;
            if (index < table.length) {
                displayRows.push(table[index]);
            }
        }

        // Dernier mois si pas déjà inclus
        if (table.length > 12 && !displayRows.includes(table[table.length - 1])) {
            displayRows.push(table[table.length - 1]);
        }

        displayRows.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.month}</td>
                <td>${ZenLoan.formatCurrency(row.payment)}</td>
                <td>${ZenLoan.formatCurrency(row.principalPayment)}</td>
                <td>${ZenLoan.formatCurrency(row.interestPayment)}</td>
                <td>${ZenLoan.formatCurrency(row.balance)}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    // Mise à jour du graphique
    updateChart(principal, totalInterest) {
        const canvas = this.elements.loanChart;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 20;

        // Calculer les angles
        const total = principal + totalInterest;
        const principalAngle = (principal / total) * 2 * Math.PI;
        const interestAngle = (totalInterest / total) * 2 * Math.PI;

        // Effacer le canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Dessiner le graphique en secteurs
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, 0, principalAngle);
        ctx.closePath();
        ctx.fillStyle = '#4a90e2';
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, principalAngle, principalAngle + interestAngle);
        ctx.closePath();
        ctx.fillStyle = '#64b5f6';
        ctx.fill();

        // Ajouter les labels
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'center';

        // Label capital
        const principalLabelAngle = principalAngle / 2;
        const principalLabelX = centerX + Math.cos(principalLabelAngle) * (radius * 0.7);
        const principalLabelY = centerY + Math.sin(principalLabelAngle) * (radius * 0.7);
        ctx.fillText('Capital', principalLabelX, principalLabelY - 10);
        ctx.font = '12px Arial';
        ctx.fillText(ZenLoan.formatCurrency(principal), principalLabelX, principalLabelY + 5);

        // Label intérêts
        const interestLabelAngle = principalAngle + (interestAngle / 2);
        const interestLabelX = centerX + Math.cos(interestLabelAngle) * (radius * 0.7);
        const interestLabelY = centerY + Math.sin(interestLabelAngle) * (radius * 0.7);
        ctx.font = 'bold 14px Arial';
        ctx.fillText('Intérêts', interestLabelX, interestLabelY - 10);
        ctx.font = '12px Arial';
        ctx.fillText(ZenLoan.formatCurrency(totalInterest), interestLabelX, interestLabelY + 5);

        // Légende
        ctx.textAlign = 'left';
        ctx.font = '12px Arial';
        ctx.fillStyle = '#4a90e2';
        ctx.fillRect(20, canvas.height - 60, 15, 15);
        ctx.fillStyle = '#ffffff';
        ctx.fillText('Capital emprunté', 40, canvas.height - 48);

        ctx.fillStyle = '#64b5f6';
        ctx.fillRect(20, canvas.height - 35, 15, 15);
        ctx.fillStyle = '#ffffff';
        ctx.fillText('Intérêts totaux', 40, canvas.height - 23);
    }

    // Effacer les résultats
    clearResults() {
        this.elements.monthlyPayment.textContent = '0 €';
        this.elements.totalCost.textContent = '0 €';
        this.elements.totalInterest.textContent = '0 €';
        this.elements.amortizationBody.innerHTML = '';
        
        if (this.elements.loanChart) {
            const ctx = this.elements.loanChart.getContext('2d');
            ctx.clearRect(0, 0, this.elements.loanChart.width, this.elements.loanChart.height);
        }
    }

    // Sauvegarde du prêt
    saveLoan() {
        const currentUser = window.zenLoan?.getCurrentUser();
        if (!currentUser) {
            ZenLoan.showNotification('Vous devez être connecté pour sauvegarder', 'warning');
            return;
        }

        if (!this.currentLoan) {
            ZenLoan.showNotification('Aucun prêt à sauvegarder', 'warning');
            return;
        }

        try {
            // Récupérer les utilisateurs
            const users = ZenLoan.getSecureData('users') || {};
            const user = users[currentUser.email];

            if (!user) {
                ZenLoan.showNotification('Erreur: utilisateur non trouvé', 'error');
                return;
            }

            // Créer l'objet prêt à sauvegarder
            const loanToSave = {
                id: ZenLoan.generateId(),
                ...this.currentLoan,
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString()
            };

            // Ajouter le prêt à l'utilisateur
            if (!user.loans) {
                user.loans = [];
            }
            user.loans.push(loanToSave);

            // Sauvegarder
            users[currentUser.email] = user;
            if (ZenLoan.setSecureData('users', users)) {
                ZenLoan.showNotification('Prêt sauvegardé avec succès', 'success');
                
                // Proposer d'aller au dashboard
                setTimeout(() => {
                    if (confirm('Voulez-vous voir vos prêts sauvegardés ?')) {
                        window.location.href = 'dashboard.html';
                    }
                }, 1500);
            } else {
                ZenLoan.showNotification('Erreur lors de la sauvegarde', 'error');
            }

        } catch (error) {
            console.error('Erreur lors de la sauvegarde:', error);
            ZenLoan.showNotification('Erreur lors de la sauvegarde', 'error');
        }
    }

    // Export CSV
    exportToCSV() {
        if (!this.currentLoan || !this.currentLoan.amortizationTable) {
            ZenLoan.showNotification('Aucune donnée à exporter', 'warning');
            return;
        }

        const data = this.currentLoan.amortizationTable.map(row => ({
            'Mois': row.month,
            'Mensualité': ZenLoan.formatNumber(row.payment),
            'Capital': ZenLoan.formatNumber(row.principalPayment),
            'Intérêts': ZenLoan.formatNumber(row.interestPayment),
            'Capital restant': ZenLoan.formatNumber(row.balance)
        }));

        const filename = `tableau_amortissement_${this.currentLoan.name.replace(/[^a-z0-9]/gi, '_')}_${new Date().toISOString().split('T')[0]}.csv`;
        ZenLoan.exportToCSV(data, filename);
    }

    // Charger un prêt existant (pour modification)
    loadLoan(loanData) {
        this.elements.loanAmount.value = loanData.amount;
        this.elements.amountSlider.value = loanData.amount;
        this.elements.loanRate.value = loanData.rate;
        this.elements.rateSlider.value = loanData.rate;
        this.elements.loanDuration.value = loanData.duration;
        this.elements.durationSlider.value = loanData.duration;
        this.elements.loanType.value = loanData.type;
        this.elements.loanName.value = loanData.name;

        this.calculateLoan();
    }

    // Réinitialiser le formulaire
    resetForm() {
        this.elements.loanAmount.value = 200000;
        this.elements.amountSlider.value = 200000;
        this.elements.loanRate.value = 3.5;
        this.elements.rateSlider.value = 3.5;
        this.elements.loanDuration.value = 20;
        this.elements.durationSlider.value = 20;
        this.elements.loanType.value = 'immobilier';
        this.elements.loanName.value = '';

        this.calculateLoan();
    }
}

// Initialisation lors du chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.loanCalculator = new LoanCalculator();
});

// Export pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LoanCalculator;
}

