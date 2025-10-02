// Gestionnaire du tableau de bord
class Dashboard {
    constructor() {
        this.currentUser = null;
        this.loans = [];
        this.filteredLoans = [];
        this.currentLoanModal = null;
        this.init();
    }

    init() {
        this.checkAuthentication();
        this.loadUserData();
        this.setupEventListeners();
        this.renderDashboard();
    }

    // Vérification de l'authentification
    checkAuthentication() {
        this.currentUser = window.zenLoan?.getCurrentUser();
        if (!this.currentUser) {
            ZenLoan.showNotification('Vous devez être connecté pour accéder à cette page', 'warning');
            setTimeout(() => {
                window.location.href = 'auth.html';
            }, 2000);
            return;
        }

        // Afficher le nom de l'utilisateur
        const userNameElement = document.getElementById('userName');
        if (userNameElement) {
            userNameElement.textContent = this.currentUser.name;
        }
    }

    // Chargement des données utilisateur
    loadUserData() {
        if (!this.currentUser) return;

        const users = ZenLoan.getSecureData('users') || {};
        const userData = users[this.currentUser.email];

        if (userData && userData.loans) {
            this.loans = userData.loans;
            this.filteredLoans = [...this.loans];
        } else {
            this.loans = [];
            this.filteredLoans = [];
        }
    }

    // Configuration des écouteurs d'événements
    setupEventListeners() {
        // Recherche
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', ZenLoan.debounce((e) => {
                this.filterLoans(e.target.value, document.getElementById('typeFilter').value);
            }, 300));
        }

        // Filtre par type
        const typeFilter = document.getElementById('typeFilter');
        if (typeFilter) {
            typeFilter.addEventListener('change', (e) => {
                this.filterLoans(document.getElementById('searchInput').value, e.target.value);
            });
        }

        // Bouton nouveau prêt
        const addLoanBtn = document.getElementById('addLoanBtn');
        if (addLoanBtn) {
            addLoanBtn.addEventListener('click', () => {
                window.location.href = 'calculator.html';
            });
        }

        // Modal
        this.setupModalListeners();

        // Déconnexion
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                window.zenLoan.logout();
            });
        }
    }

    // Configuration des écouteurs de la modal
    setupModalListeners() {
        const modal = document.getElementById('loanModal');
        const modalClose = document.getElementById('modalClose');
        const editLoanBtn = document.getElementById('editLoanBtn');
        const deleteLoanBtn = document.getElementById('deleteLoanBtn');
        const exportModalBtn = document.getElementById('exportModalBtn');

        if (modalClose) {
            modalClose.addEventListener('click', () => this.closeModal());
        }

        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal();
                }
            });
        }

        if (editLoanBtn) {
            editLoanBtn.addEventListener('click', () => this.editLoan());
        }

        if (deleteLoanBtn) {
            deleteLoanBtn.addEventListener('click', () => this.deleteLoan());
        }

        if (exportModalBtn) {
            exportModalBtn.addEventListener('click', () => this.exportLoanData());
        }

        // Fermer avec Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
                this.closeModal();
            }
        });
    }

    // Rendu du tableau de bord
    renderDashboard() {
        this.updateStatistics();
        this.renderLoansGrid();
    }

    // Mise à jour des statistiques
    updateStatistics() {
        const totalBorrowed = this.loans.reduce((sum, loan) => sum + loan.amount, 0);
        const totalInterest = this.loans.reduce((sum, loan) => sum + loan.totalInterest, 0);
        const totalLoans = this.loans.length;

        document.getElementById('totalBorrowed').textContent = ZenLoan.formatCurrency(totalBorrowed);
        document.getElementById('totalInterestStats').textContent = ZenLoan.formatCurrency(totalInterest);
        document.getElementById('totalLoans').textContent = totalLoans;
    }

    // Rendu de la grille des prêts
    renderLoansGrid() {
        const loansGrid = document.getElementById('loansGrid');
        const emptyState = document.getElementById('emptyState');

        if (!loansGrid) return;

        if (this.filteredLoans.length === 0) {
            loansGrid.style.display = 'none';
            if (emptyState) emptyState.style.display = 'block';
            return;
        }

        loansGrid.style.display = 'grid';
        if (emptyState) emptyState.style.display = 'none';

        loansGrid.innerHTML = this.filteredLoans.map(loan => this.createLoanCard(loan)).join('');

        // Ajouter les écouteurs d'événements aux cartes
        this.filteredLoans.forEach(loan => {
            const card = document.querySelector(`[data-loan-id="${loan.id}"]`);
            if (card) {
                card.addEventListener('click', (e) => {
                    if (!e.target.closest('button')) {
                        this.openLoanModal(loan);
                    }
                });

                // Boutons d'action
                const editBtn = card.querySelector('.edit-btn');
                const duplicateBtn = card.querySelector('.duplicate-btn');
                const deleteBtn = card.querySelector('.delete-btn');

                if (editBtn) {
                    editBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.editLoan(loan);
                    });
                }

                if (duplicateBtn) {
                    duplicateBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.duplicateLoan(loan);
                    });
                }

                if (deleteBtn) {
                    deleteBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.deleteLoan(loan);
                    });
                }
            }
        });
    }

    // Création d'une carte de prêt
    createLoanCard(loan) {
        const typeLabels = {
            immobilier: 'Immobilier',
            auto: 'Automobile',
            personnel: 'Personnel',
            travaux: 'Travaux'
        };

        return `
            <div class="loan-card" data-loan-id="${loan.id}">
                <div class="loan-card-header">
                    <h3 class="loan-card-title">${ZenLoan.sanitizeInput(loan.name)}</h3>
                    <span class="loan-card-type">${typeLabels[loan.type] || loan.type}</span>
                </div>
                <div class="loan-card-details">
                    <div class="loan-detail">
                        <div class="loan-detail-label">Montant</div>
                        <div class="loan-detail-value">${ZenLoan.formatCurrency(loan.amount)}</div>
                    </div>
                    <div class="loan-detail">
                        <div class="loan-detail-label">Mensualité</div>
                        <div class="loan-detail-value">${ZenLoan.formatCurrency(loan.monthlyPayment)}</div>
                    </div>
                    <div class="loan-detail">
                        <div class="loan-detail-label">Taux</div>
                        <div class="loan-detail-value">${ZenLoan.formatNumber(loan.rate, 2)}%</div>
                    </div>
                    <div class="loan-detail">
                        <div class="loan-detail-label">Durée</div>
                        <div class="loan-detail-value">${loan.duration} ans</div>
                    </div>
                </div>
                <div class="loan-card-actions">
                    <button class="btn-secondary edit-btn">Modifier</button>
                    <button class="btn-secondary duplicate-btn">Dupliquer</button>
                    <button class="btn-danger delete-btn">Supprimer</button>
                </div>
            </div>
        `;
    }

    // Filtrage des prêts
    filterLoans(searchTerm, typeFilter) {
        this.filteredLoans = this.loans.filter(loan => {
            const matchesSearch = !searchTerm || 
                loan.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                loan.type.toLowerCase().includes(searchTerm.toLowerCase());
            
            const matchesType = !typeFilter || loan.type === typeFilter;
            
            return matchesSearch && matchesType;
        });

        this.renderLoansGrid();
    }

    // Ouverture de la modal de détails
    openLoanModal(loan) {
        this.currentLoanModal = loan;
        const modal = document.getElementById('loanModal');
        const modalTitle = document.getElementById('modalTitle');
        const loanDetails = document.getElementById('loanDetails');

        if (!modal || !modalTitle || !loanDetails) return;

        modalTitle.textContent = `Détails - ${loan.name}`;

        // Détails du prêt
        loanDetails.innerHTML = `
            <div class="loan-details-grid">
                <div class="detail-item">
                    <strong>Type de prêt:</strong> ${this.getTypeLabel(loan.type)}
                </div>
                <div class="detail-item">
                    <strong>Montant emprunté:</strong> ${ZenLoan.formatCurrency(loan.amount)}
                </div>
                <div class="detail-item">
                    <strong>Taux d'intérêt:</strong> ${ZenLoan.formatNumber(loan.rate, 2)}%
                </div>
                <div class="detail-item">
                    <strong>Durée:</strong> ${loan.duration} années
                </div>
                <div class="detail-item">
                    <strong>Mensualité:</strong> ${ZenLoan.formatCurrency(loan.monthlyPayment)}
                </div>
                <div class="detail-item">
                    <strong>Coût total:</strong> ${ZenLoan.formatCurrency(loan.totalCost)}
                </div>
                <div class="detail-item">
                    <strong>Intérêts totaux:</strong> ${ZenLoan.formatCurrency(loan.totalInterest)}
                </div>
                <div class="detail-item">
                    <strong>Créé le:</strong> ${new Date(loan.createdAt).toLocaleDateString('fr-FR')}
                </div>
            </div>
        `;

        // Graphique dans la modal
        this.drawModalChart(loan);

        // Tableau d'amortissement complet
        this.renderModalAmortizationTable(loan);

        modal.classList.add('active');
    }

    // Fermeture de la modal
    closeModal() {
        const modal = document.getElementById('loanModal');
        if (modal) {
            modal.classList.remove('active');
        }
        this.currentLoanModal = null;
    }

    // Dessin du graphique dans la modal
    drawModalChart(loan) {
        const canvas = document.getElementById('modalChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 30;

        // Calculer les angles
        const total = loan.amount + loan.totalInterest;
        const principalAngle = (loan.amount / total) * 2 * Math.PI;
        const interestAngle = (loan.totalInterest / total) * 2 * Math.PI;

        // Effacer le canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Dessiner le graphique
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

        // Labels
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 16px Arial';
        ctx.textAlign = 'center';

        const principalLabelAngle = principalAngle / 2;
        const principalLabelX = centerX + Math.cos(principalLabelAngle) * (radius * 0.7);
        const principalLabelY = centerY + Math.sin(principalLabelAngle) * (radius * 0.7);
        ctx.fillText('Capital', principalLabelX, principalLabelY - 10);
        ctx.font = '14px Arial';
        ctx.fillText(ZenLoan.formatCurrency(loan.amount), principalLabelX, principalLabelY + 10);

        const interestLabelAngle = principalAngle + (interestAngle / 2);
        const interestLabelX = centerX + Math.cos(interestLabelAngle) * (radius * 0.7);
        const interestLabelY = centerY + Math.sin(interestLabelAngle) * (radius * 0.7);
        ctx.font = 'bold 16px Arial';
        ctx.fillText('Intérêts', interestLabelX, interestLabelY - 10);
        ctx.font = '14px Arial';
        ctx.fillText(ZenLoan.formatCurrency(loan.totalInterest), interestLabelX, interestLabelY + 10);
    }

    // Rendu du tableau d'amortissement complet dans la modal
    renderModalAmortizationTable(loan) {
        const tbody = document.getElementById('modalAmortizationBody');
        if (!tbody || !loan.amortizationTable) return;

        tbody.innerHTML = '';

        loan.amortizationTable.forEach(row => {
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

    // Obtenir le libellé du type de prêt
    getTypeLabel(type) {
        const labels = {
            immobilier: 'Prêt immobilier',
            auto: 'Prêt automobile',
            personnel: 'Prêt personnel',
            travaux: 'Prêt travaux'
        };
        return labels[type] || type;
    }

    // Modification d'un prêt
    editLoan(loan = null) {
        const loanToEdit = loan || this.currentLoanModal;
        if (!loanToEdit) return;

        // Stocker les données du prêt à modifier
        sessionStorage.setItem('zenloan_edit_loan', JSON.stringify(loanToEdit));
        window.location.href = 'calculator.html';
    }

    // Duplication d'un prêt
    duplicateLoan(loan) {
        if (!loan) return;

        const duplicatedLoan = {
            ...loan,
            id: ZenLoan.generateId(),
            name: `${loan.name} (Copie)`,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };

        this.saveLoanToUser(duplicatedLoan);
        ZenLoan.showNotification('Prêt dupliqué avec succès', 'success');
    }

    // Suppression d'un prêt
    deleteLoan(loan = null) {
        const loanToDelete = loan || this.currentLoanModal;
        if (!loanToDelete) return;

        if (!confirm(`Êtes-vous sûr de vouloir supprimer le prêt "${loanToDelete.name}" ?`)) {
            return;
        }

        try {
            const users = ZenLoan.getSecureData('users') || {};
            const userData = users[this.currentUser.email];

            if (userData && userData.loans) {
                userData.loans = userData.loans.filter(l => l.id !== loanToDelete.id);
                users[this.currentUser.email] = userData;

                if (ZenLoan.setSecureData('users', users)) {
                    this.loadUserData();
                    this.renderDashboard();
                    this.closeModal();
                    ZenLoan.showNotification('Prêt supprimé avec succès', 'success');
                } else {
                    ZenLoan.showNotification('Erreur lors de la suppression', 'error');
                }
            }
        } catch (error) {
            console.error('Erreur lors de la suppression:', error);
            ZenLoan.showNotification('Erreur lors de la suppression', 'error');
        }
    }

    // Export des données du prêt
    exportLoanData() {
        if (!this.currentLoanModal || !this.currentLoanModal.amortizationTable) {
            ZenLoan.showNotification('Aucune donnée à exporter', 'warning');
            return;
        }

        const data = this.currentLoanModal.amortizationTable.map(row => ({
            'Mois': row.month,
            'Mensualité': ZenLoan.formatNumber(row.payment),
            'Capital': ZenLoan.formatNumber(row.principalPayment),
            'Intérêts': ZenLoan.formatNumber(row.interestPayment),
            'Capital restant': ZenLoan.formatNumber(row.balance)
        }));

        const filename = `tableau_amortissement_${this.currentLoanModal.name.replace(/[^a-z0-9]/gi, '_')}_${new Date().toISOString().split('T')[0]}.csv`;
        ZenLoan.exportToCSV(data, filename);
    }

    // Sauvegarde d'un prêt pour l'utilisateur
    saveLoanToUser(loan) {
        try {
            const users = ZenLoan.getSecureData('users') || {};
            const userData = users[this.currentUser.email];

            if (userData) {
                if (!userData.loans) {
                    userData.loans = [];
                }
                userData.loans.push(loan);
                users[this.currentUser.email] = userData;

                if (ZenLoan.setSecureData('users', users)) {
                    this.loadUserData();
                    this.renderDashboard();
                    return true;
                }
            }
        } catch (error) {
            console.error('Erreur lors de la sauvegarde:', error);
        }
        return false;
    }

    // Actualisation des données
    refreshData() {
        this.loadUserData();
        this.renderDashboard();
        ZenLoan.showNotification('Données actualisées', 'info');
    }
}

// Initialisation lors du chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
});

// Export pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Dashboard;
}

