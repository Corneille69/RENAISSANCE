// Utilitaires globaux et fonctions communes
class ZenLoan {
    constructor() {
        this.init();
    }

    init() {
        this.setupNavigation();
        this.checkAuthStatus();
    }

    // Configuration de la navigation mobile
    setupNavigation() {
        const hamburger = document.getElementById('hamburger');
        const navList = document.getElementById('navList');

        if (hamburger && navList) {
            hamburger.addEventListener('click', () => {
                hamburger.classList.toggle('active');
                navList.classList.toggle('active');
            });

            // Fermer le menu mobile lors du clic sur un lien
            navList.addEventListener('click', (e) => {
                if (e.target.tagName === 'A') {
                    hamburger.classList.remove('active');
                    navList.classList.remove('active');
                }
            });
        }
    }

    // Vérifier le statut d'authentification
    checkAuthStatus() {
        const currentUser = this.getCurrentUser();
        const authLink = document.getElementById('authLink');
        const logoutBtn = document.getElementById('logoutBtn');
        const dashboardLink = document.getElementById('dashboardLink');

        if (currentUser) {
            // Utilisateur connecté
            if (authLink) authLink.style.display = 'none';
            if (logoutBtn) {
                logoutBtn.style.display = 'block';
                logoutBtn.addEventListener('click', () => this.logout());
            }
            if (dashboardLink) dashboardLink.style.display = 'block';
        } else {
            // Utilisateur non connecté
            if (authLink) authLink.style.display = 'block';
            if (logoutBtn) logoutBtn.style.display = 'none';
            if (dashboardLink) dashboardLink.style.display = 'none';
        }
    }

    // Obtenir l'utilisateur actuel
    getCurrentUser() {
        const sessionData = sessionStorage.getItem('zenloan_session');
        if (sessionData) {
            try {
                return JSON.parse(sessionData);
            } catch (e) {
                console.error('Erreur lors de la lecture de la session:', e);
                sessionStorage.removeItem('zenloan_session');
            }
        }
        return null;
    }

    // Déconnexion
    logout() {
        sessionStorage.removeItem('zenloan_session');
        window.location.href = 'index.html';
    }

    // Hachage simple pour les mots de passe
    static async hashPassword(password) {
        const encoder = new TextEncoder();
        const data = encoder.encode(password);
        const hash = await crypto.subtle.digest('SHA-256', data);
        return Array.from(new Uint8Array(hash))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    // Validation d'email
    static isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Validation de mot de passe
    static isValidPassword(password) {
        return password.length >= 6;
    }

    // Sanitisation des entrées
    static sanitizeInput(input) {
        const div = document.createElement('div');
        div.textContent = input;
        return div.innerHTML;
    }

    // Formatage des nombres en euros
    static formatCurrency(amount) {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'EUR'
        }).format(amount);
    }

    // Formatage des nombres
    static formatNumber(number, decimals = 2) {
        return new Intl.NumberFormat('fr-FR', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(number);
    }

    // Génération d'ID unique
    static generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    // Debounce pour les événements
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Affichage de notifications
    static showNotification(message, type = 'info', duration = 3000) {
        // Créer l'élément de notification
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Styles inline pour la notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '1rem 1.5rem',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '500',
            zIndex: '9999',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease',
            maxWidth: '300px',
            wordWrap: 'break-word'
        });

        // Couleurs selon le type
        const colors = {
            success: '#28a745',
            error: '#dc3545',
            warning: '#ffc107',
            info: '#4a90e2'
        };
        notification.style.backgroundColor = colors[type] || colors.info;

        // Ajouter au DOM
        document.body.appendChild(notification);

        // Animation d'entrée
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Suppression automatique
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, duration);

        // Suppression au clic
        notification.addEventListener('click', () => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        });
    }

    // Gestion du stockage local sécurisé
    static setSecureData(key, data) {
        try {
            const jsonData = JSON.stringify(data);
            localStorage.setItem(`zenloan_${key}`, jsonData);
            return true;
        } catch (e) {
            console.error('Erreur lors de la sauvegarde:', e);
            return false;
        }
    }

    static getSecureData(key) {
        try {
            const data = localStorage.getItem(`zenloan_${key}`);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.error('Erreur lors de la lecture:', e);
            return null;
        }
    }

    static removeSecureData(key) {
        try {
            localStorage.removeItem(`zenloan_${key}`);
            return true;
        } catch (e) {
            console.error('Erreur lors de la suppression:', e);
            return false;
        }
    }

    // Export CSV
    static exportToCSV(data, filename) {
        if (!data || !data.length) {
            ZenLoan.showNotification('Aucune donnée à exporter', 'warning');
            return;
        }

        // Créer le contenu CSV
        const headers = Object.keys(data[0]);
        const csvContent = [
            headers.join(','),
            ...data.map(row => 
                headers.map(header => {
                    let value = row[header];
                    if (typeof value === 'string' && value.includes(',')) {
                        value = `"${value}"`;
                    }
                    return value;
                }).join(',')
            )
        ].join('\n');

        // Créer et télécharger le fichier
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        ZenLoan.showNotification('Fichier CSV exporté avec succès', 'success');
    }

    // Vérification de la compatibilité du navigateur
    static checkBrowserCompatibility() {
        const features = [
            'localStorage' in window,
            'sessionStorage' in window,
            'crypto' in window && 'subtle' in window.crypto,
            'fetch' in window
        ];

        if (!features.every(feature => feature)) {
            ZenLoan.showNotification(
                'Votre navigateur ne supporte pas toutes les fonctionnalités requises. Veuillez le mettre à jour.',
                'warning',
                5000
            );
            return false;
        }
        return true;
    }
}

// Initialisation globale
document.addEventListener('DOMContentLoaded', () => {
    // Vérifier la compatibilité du navigateur
    ZenLoan.checkBrowserCompatibility();
    
    // Initialiser l'application
    window.zenLoan = new ZenLoan();
    
    // Ajouter des animations aux éléments visibles
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observer les éléments animables
    document.querySelectorAll('.feature-card, .about-card, .stat-card').forEach(el => {
        observer.observe(el);
    });
});

// Gestion des erreurs globales
window.addEventListener('error', (e) => {
    console.error('Erreur JavaScript:', e.error);
    ZenLoan.showNotification('Une erreur inattendue s\'est produite', 'error');
});

// Gestion des erreurs de promesses non gérées
window.addEventListener('unhandledrejection', (e) => {
    console.error('Promesse rejetée:', e.reason);
    ZenLoan.showNotification('Une erreur inattendue s\'est produite', 'error');
    e.preventDefault();
});

// Export pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ZenLoan;
}

