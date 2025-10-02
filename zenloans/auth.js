// Gestion de l'authentification
class AuthManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupTabs();
        this.setupForms();
        this.checkURLParams();
    }

    // Configuration des onglets
    setupTabs() {
        const tabs = document.querySelectorAll('.auth-tab');
        const forms = document.querySelectorAll('.auth-form');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetTab = tab.dataset.tab;
                
                // Mettre à jour les onglets actifs
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                // Mettre à jour les formulaires actifs
                forms.forEach(form => {
                    form.classList.remove('active');
                    if (form.id === `${targetTab}Form`) {
                        form.classList.add('active');
                    }
                });
            });
        });
    }

    // Configuration des formulaires
    setupForms() {
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');

        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
            this.setupRealTimeValidation(loginForm);
        }

        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
            this.setupRealTimeValidation(registerForm);
        }
    }

    // Vérifier les paramètres URL
    checkURLParams() {
        const urlParams = new URLSearchParams(window.location.search);
        const mode = urlParams.get('mode');

        if (mode === 'register') {
            const registerTab = document.querySelector('[data-tab="register"]');
            if (registerTab) {
                registerTab.click();
            }
        }
    }

    // Configuration de la validation en temps réel
    setupRealTimeValidation(form) {
        const inputs = form.querySelectorAll('input');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', ZenLoan.debounce(() => this.validateField(input), 500));
        });
    }

    // Validation d'un champ
    validateField(input) {
        const fieldName = input.name;
        const value = input.value.trim();
        const errorElement = document.getElementById(`${input.id}Error`);

        let isValid = true;
        let errorMessage = '';

        switch (fieldName) {
            case 'name':
                if (value.length < 2) {
                    isValid = false;
                    errorMessage = 'Le nom doit contenir au moins 2 caractères';
                }
                break;

            case 'email':
                if (!ZenLoan.isValidEmail(value)) {
                    isValid = false;
                    errorMessage = 'Veuillez saisir une adresse email valide';
                }
                break;

            case 'password':
                if (!ZenLoan.isValidPassword(value)) {
                    isValid = false;
                    errorMessage = 'Le mot de passe doit contenir au moins 6 caractères';
                }
                break;

            case 'confirmPassword':
                const passwordField = document.getElementById('registerPassword');
                if (passwordField && value !== passwordField.value) {
                    isValid = false;
                    errorMessage = 'Les mots de passe ne correspondent pas';
                }
                break;
        }

        // Afficher/masquer l'erreur
        if (errorElement) {
            errorElement.textContent = errorMessage;
            errorElement.style.display = isValid ? 'none' : 'block';
        }

        // Styling du champ
        input.style.borderColor = isValid ? '' : 'var(--danger-color)';

        return isValid;
    }

    // Validation complète du formulaire
    validateForm(form) {
        const inputs = form.querySelectorAll('input[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    // Gestion de la connexion
    async handleLogin(e) {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        const email = formData.get('email').trim();
        const password = formData.get('password');

        // Validation
        if (!this.validateForm(form)) {
            return;
        }

        try {
            // Afficher le chargement
            const submitBtn = form.querySelector('.auth-submit');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Connexion...';
            submitBtn.disabled = true;

            // Vérifier les identifiants
            const users = ZenLoan.getSecureData('users') || {};
            const user = users[email];

            if (!user) {
                this.showMessage('loginMessage', 'Aucun compte trouvé avec cette adresse email', 'error');
                return;
            }

            const hashedPassword = await ZenLoan.hashPassword(password);
            if (user.password !== hashedPassword) {
                this.showMessage('loginMessage', 'Mot de passe incorrect', 'error');
                return;
            }

            // Créer la session
            const sessionData = {
                email: user.email,
                name: user.name,
                loginTime: new Date().toISOString()
            };

            sessionStorage.setItem('zenloan_session', JSON.stringify(sessionData));

            // Succès
            this.showMessage('loginMessage', 'Connexion réussie ! Redirection...', 'success');
            
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1500);

        } catch (error) {
            console.error('Erreur lors de la connexion:', error);
            this.showMessage('loginMessage', 'Une erreur est survenue lors de la connexion', 'error');
        } finally {
            // Restaurer le bouton
            const submitBtn = form.querySelector('.auth-submit');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    }

    // Gestion de l'inscription
    async handleRegister(e) {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        const name = formData.get('name').trim();
        const email = formData.get('email').trim();
        const password = formData.get('password');
        const confirmPassword = formData.get('confirmPassword');

        // Validation
        if (!this.validateForm(form)) {
            return;
        }

        if (password !== confirmPassword) {
            this.showMessage('registerMessage', 'Les mots de passe ne correspondent pas', 'error');
            return;
        }

        try {
            // Afficher le chargement
            const submitBtn = form.querySelector('.auth-submit');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Inscription...';
            submitBtn.disabled = true;

            // Vérifier si l'utilisateur existe déjà
            const users = ZenLoan.getSecureData('users') || {};
            
            if (users[email]) {
                this.showMessage('registerMessage', 'Un compte existe déjà avec cette adresse email', 'error');
                return;
            }

            // Créer le nouvel utilisateur
            const hashedPassword = await ZenLoan.hashPassword(password);
            const newUser = {
                name: ZenLoan.sanitizeInput(name),
                email: email,
                password: hashedPassword,
                createdAt: new Date().toISOString(),
                loans: []
            };

            users[email] = newUser;
            
            if (!ZenLoan.setSecureData('users', users)) {
                this.showMessage('registerMessage', 'Erreur lors de la sauvegarde du compte', 'error');
                return;
            }

            // Créer la session automatiquement
            const sessionData = {
                email: newUser.email,
                name: newUser.name,
                loginTime: new Date().toISOString()
            };

            sessionStorage.setItem('zenloan_session', JSON.stringify(sessionData));

            // Succès
            this.showMessage('registerMessage', 'Compte créé avec succès ! Redirection...', 'success');
            
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1500);

        } catch (error) {
            console.error('Erreur lors de l\'inscription:', error);
            this.showMessage('registerMessage', 'Une erreur est survenue lors de l\'inscription', 'error');
        } finally {
            // Restaurer le bouton
            const submitBtn = form.querySelector('.auth-submit');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    }

    // Affichage des messages
    showMessage(elementId, message, type) {
        const messageElement = document.getElementById(elementId);
        if (messageElement) {
            messageElement.textContent = message;
            messageElement.className = `auth-message ${type}`;
            messageElement.style.display = 'block';

            // Masquer le message après 5 secondes
            setTimeout(() => {
                messageElement.style.display = 'none';
            }, 5000);
        }
    }

    // Vérification si l'utilisateur est déjà connecté
    static checkIfLoggedIn() {
        const currentUser = window.zenLoan?.getCurrentUser();
        if (currentUser) {
            // Rediriger vers le dashboard si déjà connecté
            window.location.href = 'dashboard.html';
            return true;
        }
        return false;
    }

    // Déconnexion
    static logout() {
        sessionStorage.removeItem('zenloan_session');
        ZenLoan.showNotification('Vous avez été déconnecté', 'info');
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1000);
    }

    // Réinitialisation du mot de passe (simulation)
    static resetPassword(email) {
        const users = ZenLoan.getSecureData('users') || {};
        
        if (!users[email]) {
            ZenLoan.showNotification('Aucun compte trouvé avec cette adresse email', 'error');
            return false;
        }

        // Dans une vraie application, on enverrait un email
        ZenLoan.showNotification(
            'Un email de réinitialisation a été envoyé (fonctionnalité simulée)', 
            'info',
            5000
        );
        return true;
    }
}

// Initialisation lors du chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    // Vérifier si l'utilisateur est déjà connecté
    if (!AuthManager.checkIfLoggedIn()) {
        // Initialiser le gestionnaire d'authentification
        window.authManager = new AuthManager();
    }
});

// Gestion des erreurs spécifiques à l'authentification
window.addEventListener('storage', (e) => {
    if (e.key === 'zenloan_users' && e.newValue === null) {
        // Les données utilisateur ont été supprimées
        ZenLoan.showNotification('Données utilisateur corrompues, veuillez vous reconnecter', 'warning');
        AuthManager.logout();
    }
});

// Export pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AuthManager;
}

